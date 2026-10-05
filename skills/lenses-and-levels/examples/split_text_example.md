# Example: Splitting Unstructured Text by Lenses & Levels

This example demonstrates how the **Lenses & Levels Skill** takes raw, unstructured architectural notes and decomposes them into a clean, modular structure complying with all 4 golden principles.

---

## 1. Raw Input Text (Unstructured Architecture Notes)

> "We are building an Order & Payment Processing system for an international e-commerce platform. The system needs to support high availability and handle flash sales of 10,000 orders/second.
> The core goal is to enable seamless 1-click checkout for shoppers and support multiple currencies (USD, EUR, JPY) while providing instant fraud screening.
> Architects decided to use a microservices approach deployed on AWS EKS with Terraform. The primary services are Checkout Web App (React), Order API (Go), Payment Gateway Service (Go), and Notification Service (Node.js).
> The Order API writes order events into Apache Kafka. The Kafka cluster has 12 partitions per topic and 3 replicas across availability zones.
> Orders are stored in PostgreSQL with a table schema: `orders(id UUID PRIMARY KEY, user_id UUID, amount DECIMAL(10,2), currency VARCHAR(3), status VARCHAR(20), created_at TIMESTAMP)`. We shard the orders database by user_id hash.
> For integration, external third-party payment processors (Stripe, Adyen, PayPal) are invoked using synchronous HTTPS webhooks with HMAC-SHA256 signatures. If Stripe returns 5xx, the Payment Gateway retries with exponential backoff (initial delay 500ms, max 3 attempts) and then falls back to Adyen.
> All customer payment details are tokenized; PCI-DSS compliance mandates that raw credit card numbers never touch our servers.
> When things go wrong, we use OpenTelemetry for distributed tracing and Prometheus for alerting if latency exceeds 250ms at p99."

---

## 2. Decomposition Strategy & Analysis

The skill analyzes the input text against the **Lenses & Levels Principles**:

1. **Lens Identification**:
   - High availability, p99 latency targets, OpenTelemetry -> **Quality Attributes Lens**
   - 1-click checkout, multiple currencies, fraud screening -> **Capability Lens**
   - Services breakdown (Checkout Web App, Order API, Payment Gateway) -> **System Lens**
   - PostgreSQL schema, user_id sharding -> **Data Lens**
   - Third-party payment gateways (Stripe, Adyen, PayPal), webhook signatures, fallback -> **Integration Lens**
   - Kafka event streaming, concurrency, retry loop, fallback logic -> **Runtime Lens**
   - AWS EKS, Terraform, multi-AZ deployment -> **Deployment Lens**
   - PCI-DSS tokenization, HMAC-SHA256 authentication -> **Security Lens**

2. **Overview Filtering (Centrality Check)**:
   - *PostgreSQL column definitions and Kafka partition counts* are non-central implementation details -> demoted from Level 1 to Level 3.
   - *Stripe 500ms exponential backoff retry parameters* -> demoted from Level 1 to Level 3.
   - *Only North Star value propositions, high-level context, and core postures remain in Level 1.*

3. **Non-Duplication (Single Source of Truth)**:
   - Do not repeat the PostgreSQL schema in the System Lens. Place it in the **Data Lens** and cross-reference from the System Lens.
   - Place Stripe webhook HMAC signatures in the **Integration Lens** and cross-reference from the Security Lens.

4. **Downward Self-Containment (Zero Upward Dependencies)**:
   - Level 3 sections include local context (e.g. defining `Order API (Go)` responsibilities directly in the section) so implementers don't need to jump back up to Level 1.

---

## 3. Resulting Output: Structured Lenses & Levels Documentation

### System Lens

#### Level 1 — Overview
The Order & Payment Platform provides a resilient, event-driven backbone for processing international e-commerce checkouts across mobile and web interfaces. It isolates critical transactional boundaries between consumer checkout, payment settlement, and asynchronous fulfillment notifications.

```
[ Shopper ] ──> [ Checkout Web App ] ──> [ Order API ] ──> [ Kafka ] ──> [ Notification Svc ]
                                                │
                                                └──> [ Payment Gateway ] ──> [ Third-Party PSPs ]
```

#### Level 2 — Map
The architecture decomposes into four deployable container units:

| Container | Technology | Responsibility | Primary Boundaries |
| :--- | :--- | :--- | :--- |
| **Checkout Web App** | React / SPA | User checkout interface, cart review | Communicates with Order API |
| **Order API** | Go (Gin) | Order orchestration, validation, persistence | Upstream to Kafka & Payment Gateway |
| **Payment Gateway Service**| Go | PSP routing, tokenization, transaction capture | Integrates with Stripe/Adyen/PayPal |
| **Notification Service** | Node.js | Asynchronous order confirmation emails/SMS | Subscribes to Kafka order events |

> 🔗 **Related Specifications**:
> - For data persistence and sharding, see [Data Lens > Level 2: Data Landscape](#data-lens-level-2).
> - For container hosting and Kubernetes topology, see [Deployment Lens > Level 2: Topology](#deployment-lens-level-2).

#### Level 3 — Detail
*Living Code Repositories*:
- Order API Service: [`services/order-api`](file:///workspace/services/order-api)
- Payment Gateway Service: [`services/payment-gateway`](file:///workspace/services/payment-gateway)

---

### Capability Lens

#### Level 1 — Overview
The platform enables global commerce through frictionless, localized checkout experiences with automated risk mitigation.

**North Star Capabilities**:
1. **1-Click International Checkout**: Seamless purchase flow supporting localized currencies (USD, EUR, JPY).
2. **Instant Fraud Screening**: Real-time risk evaluation prior to payment capture.
3. **Guaranteed Order Fulfillment**: Decoupled, zero-loss order processing during traffic spikes.

#### Level 2 — Map
| Capability Area | Realizing System Container | Business Outcome |
| :--- | :--- | :--- |
| **Multi-Currency Checkout** | Checkout Web App + Order API | Conversion rate optimization in global markets |
| **PSP Multi-Provider Routing** | Payment Gateway Service | Redundancy and fee optimization |
| **Customer Notifications** | Notification Service | Real-time shopper updates |

#### Level 3 — Detail
- **Success KPIs**: Checkout completion rate > 98.5%; checkout abandonment due to latency < 0.2%.
- **Backlog Tracking**: Epics tracked under Jira board `COMMERCE-CORE`.

---

### Data Lens

#### Level 1 — Overview
All transactional order records and payment receipts are treated as critical business records requiring strict ACID guarantees and auditability. PII is minimized and isolated to dedicated encrypted records.

#### Level 2 — Map
- **Primary Transactional Store**: Relational PostgreSQL cluster (Orders & Line Items).
- **Event Bus / Log**: Apache Kafka (Order state change stream).
- **Data Classification**: Order metadata (Confidential); Payment tokens (Restricted/PCI-DSS).

#### Level 3 — Detail
The `Order API` manages transactional records in PostgreSQL. Orders are horizontally partitioned by hashing `user_id` to distribute load evenly across database shards.

```sql
-- Living Migration: migrations/0001_create_orders.sql
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_orders_user_id ON orders (user_id);
```

---

### Integration Lens

#### Level 1 — Overview
The platform interacts with third-party Payment Service Providers (PSPs) via secure, redundant external APIs, ensuring payment processing continues even during third-party provider outages.

#### Level 2 — Map
| Integration Partner | Protocol | Authentication | Failure Strategy |
| :--- | :--- | :--- | :--- |
| **Stripe** | HTTPS / REST | Bearer API Key + HMAC Webhook | Active primary with Adyen fallback |
| **Adyen** | HTTPS / REST | HMAC Signature | Secondary fallback PSP |
| **PayPal** | HTTPS / REST | OAuth2 | Alternate checkout option |

#### Level 3 — Detail
The Payment Gateway Service manages external PSP calls.

- **Living Contract**: [`specs/psp-webhook-contract.yaml`](file:///workspace/specs/psp-webhook-contract.yaml)

**Retry & Failover Policy**:
- Initial HTTP timeout: `1500ms`.
- On Stripe `5xx` error response: Exponential backoff retry (initial delay: `500ms`, multiplier: `2.0`, max attempts: `3`).
- On exhaustion of Stripe retries: Automatic failover invocation to Adyen payment endpoint.
- Webhook Signature Verification: Incoming webhooks from PSPs require validation using HMAC-SHA256 with the shared secret stored in AWS Secrets Manager.

---

### Deployment Lens

#### Level 1 — Overview
The architecture is deployed entirely in AWS across multiple Availability Zones to ensure uninterrupted operation during infrastructure failures.

#### Level 2 — Map
- **Runtime Compute**: AWS Elastic Kubernetes Service (EKS) multi-AZ cluster.
- **Infrastructure as Code (IaC)**: Managed via Terraform modules.
- **Message Broker**: Managed Kafka across 3 Availability Zones.

#### Level 3 — Detail
- **IaC Repository**: Terraform manifests located in [`infra/terraform/eks`](file:///workspace/infra/terraform/eks).
- **Kafka Topology**: 12 partitions per order topic, replication factor of 3 with `min.insync.replicas=2`.

---

### Quality Attributes Lens

#### Level 1 — Overview
The system is engineered for flash-sale peak scalability and sub-second checkout responsiveness while maintaining zero order loss.

#### Level 2 — Map
| Quality Dimension | Target Scenario | Observability Tool |
| :--- | :--- | :--- |
| **Throughput** | 10,000 orders/sec during flash sales | Prometheus + Grafana |
| **Latency** | Order API response < 250ms at p99 | OpenTelemetry traces |
| **Reliability** | Zero order loss during single AZ failure | AWS Multi-AZ Health Dashboard |

#### Level 3 — Detail
- **Tracing Configuration**: OpenTelemetry SDK embedded into Go and Node.js containers exporting OTLP traces to Jaeger.
- **Alerting Threshold**: PagerDuty alert triggers when `order_api_p99_latency_seconds > 0.25` for 3 consecutive evaluation cycles.
