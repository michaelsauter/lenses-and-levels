# Lenses Catalog & Boundary Reference Guide

The Lenses & Levels framework classifies architectural concerns across 15 distinct lenses divided into 5 meta-domains.

---

## Meta-Domains & Lenses Overview

| Meta-Domain | Lens | Status | Primary Focus |
| :--- | :--- | :--- | :--- |
| **Structure** | [1. System Lens](#1-system-lens) | Core | Structural decomposition (C4 model: context, containers, components) |
| | [2. Domain Lens](#2-domain-lens) | Core | Conceptual business model (DDD, bounded contexts, ubiquitous language) |
| | [3. Data Lens](#3-data-lens) | Core | Data classification, persistence models, lifecycles, and storage schemas |
| **Interaction** | [4. Integration Lens](#4-integration-lens) | Core | External interfaces, API contracts, protocols, async events, versioning |
| | [5. Runtime Lens](#5-runtime-lens) | Core | Execution flows, concurrency, state, failure modes, resilience patterns |
| **Operation** | [6. Deployment Lens](#6-deployment-lens) | Core | Infrastructure topology, cloud environments, CI/CD, IaC, networking |
| | [7. Security Lens](#7-security-lens) | Contextual | Threat models, identity, authentication, authorization, cryptography |
| | [8. Quality Attributes Lens](#8-quality-attributes-lens) | Contextual | Non-functional requirements, SLOs, latency, scalability, observability |
| **Intent & Change** | [9. Capability Lens](#9-capability-lens) | Core | Business capabilities, value streams, feature sets, strategic intent |
| | [10. Governance & Decision Lens](#10-governance--decision-lens) | Contextual | Architecture Decision Records (ADRs), constraints, principles |
| | [11. Evolution Lens](#11-evolution-lens) | Contextual | Migration roadmaps, technical debt, lifecycle states, deprecation plans |
| **Organization & Business** | [12. UX & Interaction Lens](#12-ux--interaction-lens) | Contextual | User journeys, design systems, frontend architecture, accessibility |
| | [13. Organization Lens](#13-organization-lens) | Contextual | Team topologies, Conway's law alignment, cognitive load, ownership |
| | [14. Cost Lens](#14-cost-lens) | Contextual | FinOps, unit economics, infrastructure spend, operational efficiency |
| | [15. Compliance Lens](#15-compliance-lens) | Contextual | Regulatory mandates (GDPR, SOC2, HIPAA), audit requirements, privacy |

---

## Detailed Lens Guidance & Boundaries

### 1. System Lens
- **What Belongs**: Structural decomposition of software units and their structural dependencies. Aligns directly with C4 (Context, Containers, Components).
- **What Does NOT Belong**:
  - Business capability narratives (belongs in **Capability Lens**).
  - Business entity definitions / aggregates (belongs in **Domain Lens**).
  - Storage schemas or DDL (belongs in **Data Lens**).
  - Cloud server instances / Kubernetes pod scheduling (belongs in **Deployment Lens**).
- **Level Guidance**:
  - **Level 1 (Overview)**: C4 Context diagram; system boundary; external actors and neighboring software systems; concise mission narrative.
  - **Level 2 (Map)**: C4 Container diagram; deployable services/applications; responsibilities of each container; high-level interaction protocols.
  - **Level 3 (Detail)**: C4 Component diagrams for complex containers; internal component responsibilities; source code package mapping.

### 2. Capability Lens
- **What Belongs**: The strategic and functional abilities the software provides to its business and users.
- **What Does NOT Belong**:
  - Technical component lists or server architectures (belongs in **System Lens**).
  - API endpoints or payload definitions (belongs in **Integration Lens**).
- **Level Guidance**:
  - **Level 1 (Overview)**: North Star capabilities; high-level capability canvas; user value proposition.
  - **Level 2 (Map)**: Capability-to-System mapping matrix; value streams; capability grouping by domain.
  - **Level 3 (Detail)**: Feature breakdowns; business KPIs; functional dependency chains; links to product backlogs/roadmaps.

### 3. Domain Lens
- **What Belongs**: Conceptual model of the problem space using Domain-Driven Design (DDD) concepts.
- **What Does NOT Belong**:
  - Relational database tables, SQL DDL, or cache keys (belongs in **Data Lens**).
  - HTTP endpoints or JSON serialization (belongs in **Integration Lens**).
- **Level Guidance**:
  - **Level 1 (Overview)**: Core domain vision statement; subdomain classification (Core, Supporting, Generic).
  - **Level 2 (Map)**: DDD Context Map; Ubiquitous Language glossary; upstream/downstream domain relationships.
  - **Level 3 (Detail)**: Entities, Value Objects, Aggregates, domain invariants, domain lifecycle state machines.

### 4. Data Lens
- **What Belongs**: Information structure, storage technologies, data governance, schemas, and data pipelines.
- **What Does NOT Belong**:
  - Pure conceptual business definitions without storage representation (belongs in **Domain Lens**).
  - API transport payloads (belongs in **Integration Lens**).
- **Level Guidance**:
  - **Level 1 (Overview)**: High-level information map; source of truth for critical entities; data privacy posture.
  - **Level 2 (Map)**: Data landscape map (which persistence store handles what data); data classification matrix (PII, Restricted, Public); ETL/CDC movement flows.
  - **Level 3 (Detail)**: Database schemas (SQL DDL, NoSQL models), partitioning/indexing schemes, field-level encryption, data retention/deletion scripts.

### 5. Integration Lens
- **What Belongs**: Boundaries and interactions with outside systems and third-party services.
- **What Does NOT Belong**:
  - Internal function calls or module imports within a container (belongs in **System Lens**).
  - Execution thread concurrency (belongs in **Runtime Lens**).
- **Level Guidance**:
  - **Level 1 (Overview)**: External systems ecosystem map; integration rationale.
  - **Level 2 (Map)**: API & Event catalog; communication styles (REST, gRPC, GraphQL, Async Event); versioning policy.
  - **Level 3 (Detail)**: OpenAPI/AsyncAPI specifications; error semantics; retry/backoff policies; webhook contracts.

### 6. Runtime Lens
- **What Belongs**: Dynamic behavioral patterns when the system is operating.
- **What Does NOT Belong**:
  - Static software component hierarchy (belongs in **System Lens**).
  - Physical cloud networking / subnets (belongs in **Deployment Lens**).
- **Level Guidance**:
  - **Level 1 (Overview)**: Operational execution paradigm (stateless request-response vs event-driven streaming); high-level transaction model.
  - **Level 2 (Map)**: Primary end-to-end execution flows; scaling model; concurrency approach.
  - **Level 3 (Detail)**: Thread pools; circuit breakers; timeout budgets; fallback sequences; distributed locking mechanisms.

### 7. Deployment Lens
- **What Belongs**: Physical and virtual environments, hosting infrastructure, CI/CD pipelines, and network topology.
- **What Does NOT Belong**:
  - Software application components (belongs in **System Lens**).
  - Run-time execution thread management (belongs in **Runtime Lens**).
- **Level Guidance**:
  - **Level 1 (Overview)**: Environment strategy (dev/stage/prod); cloud provider & hosting model.
  - **Level 2 (Map)**: Infrastructure topology diagram; VPC/network zoning; CI/CD pipeline flow.
  - **Level 3 (Detail)**: Terraform/IaC modules, Kubernetes manifests, autoscaling parameters, DNS configurations.

### 8. Security Lens
- **What Belongs**: Risk mitigation, authentication, authorization, data protection, and trust boundaries.
- **What Does NOT Belong**:
  - General software bugs (belongs in **Quality Attributes Lens**).
  - Pure legal regulatory articles (belongs in **Compliance Lens**).
- **Level Guidance**:
  - **Level 1 (Overview)**: Security posture statement; primary threat categories; trust boundaries.
  - **Level 2 (Map)**: Identity provider model (OAuth2/OIDC, IAM); authorization model (RBAC/ABAC); data classification boundaries.
  - **Level 3 (Detail)**: Threat models (STRIDE); cryptographic key rotation specifications; token validation logic; penetration test remediations.

### 9. Quality Attributes Lens
- **What Belongs**: Non-functional requirements (NFRs) and cross-cutting system characteristics (performance, reliability, observability).
- **What Does NOT Belong**:
  - Financial costs (belongs in **Cost Lens**).
  - Strategic product roadmap (belongs in **Evolution Lens**).
- **Level Guidance**:
  - **Level 1 (Overview)**: Quality goals & architectural trade-offs (e.g. latency vs consistency).
  - **Level 2 (Map)**: Quality attribute scenarios; observability architecture (telemetry, metrics, logs, traces).
  - **Level 3 (Detail)**: SLO/SLA specifications; benchmark results; load test thresholds; alerting policies.

### 10. Governance & Decision Lens
- **What Belongs**: The rationale behind architectural choices, architectural principles, standards, and records.
- **What Does NOT Belong**:
  - Technical component specifications (belongs in **System Lens**).
- **Level Guidance**:
  - **Level 1 (Overview)**: Core architectural principles and hard constraints.
  - **Level 2 (Map)**: ADR index (sorted by status: Proposed, Accepted, Deprecated); technology radar / standards index.
  - **Level 3 (Detail)**: Full ADR texts, evaluation matrices, rejected alternatives, decision consequences.

### 11. Evolution Lens
- **What Belongs**: How the architecture adapts over time, technical debt, migrations, and lifecycle stages.
- **What Does NOT Belong**:
  - Product feature wishlists (belongs in **Capability Lens**).
- **Level Guidance**:
  - **Level 1 (Overview)**: Strategic architectural runway and major multi-year milestones.
  - **Level 2 (Map)**: Technical debt register; architecture roadmap; component lifecycle state map (Active, Maintenance, Deprecated).
  - **Level 3 (Detail)**: Step-by-step migration plans; data dual-write / strangler fig procedures; sunset timelines.

### 12. UX & Interaction Lens
- **What Belongs**: Human interaction patterns, frontend design systems, client-side state architecture, and accessibility.
- **Level Guidance**:
  - **Level 1 (Overview)**: Core user personas and key user journeys.
  - **Level 2 (Map)**: Information architecture map; design system component hierarchy; client-side state model.
  - **Level 3 (Detail)**: Wireframe/Figma references; accessibility (WCAG) audit matrices; client routing and caching rules.

### 13. Organization Lens
- **What Belongs**: Alignment of teams with software architecture (Team Topologies, Conway's Law, cognitive load).
- **Level Guidance**:
  - **Level 1 (Overview)**: Operating model & organizational principles (e.g. stream-aligned teams).
  - **Level 2 (Map)**: Team-to-Component ownership matrix; communication modes between teams.
  - **Level 3 (Detail)**: Escalation paths; RACI matrices; on-call rotation boundaries.

### 14. Cost Lens
- **What Belongs**: Economic aspects, cloud bills, infrastructure sizing economics, and FinOps practices.
- **Level Guidance**:
  - **Level 1 (Overview)**: Target cost model (e.g. cost-per-active-user target); major cost drivers.
  - **Level 2 (Map)**: Monthly cost breakdown by service/environment; unit economic metrics.
  - **Level 3 (Detail)**: Cloud billing allocation tags; reservation/savings plan schedules; scale-down automation scripts.

### 15. Compliance Lens
- **What Belongs**: Legal, regulatory, and audit mandates (SOC2, HIPAA, ISO27001, GDPR).
- **Level Guidance**:
  - **Level 1 (Overview)**: Compliance commitments and regulatory frameworks applicable to the system.
  - **Level 2 (Map)**: Compliance matrix mapping regulatory controls to technical controls and lenses.
  - **Level 3 (Detail)**: Evidence collection procedures; audit log retention configurations; PIA/DPIA documents.

---

## Canonical Disambiguation Matrix

When content seems to fit multiple lenses, resolve using this canonical guide:

| Content Topic | Primary Canonical Lens | Where It Does NOT Belong (Reference Instead) |
| :--- | :--- | :--- |
| **Database table schemas & SQL** | **Data Lens** (L3) | System Lens or Runtime Lens |
| **API endpoints & request/response** | **Integration Lens** (L2/L3) | System Lens |
| **Kubernetes pods, nodes, clusters** | **Deployment Lens** (L2/L3) | System Lens or Runtime Lens |
| **Business goals & feature sets** | **Capability Lens** (L1/L2) | Domain Lens or System Lens |
| **Domain entities & invariants** | **Domain Lens** (L3) | Data Lens or System Lens |
| **ADRs & Technology selections** | **Governance Lens** (L2/L3) | System Lens |
| **Auth tokens & identity provider** | **Security Lens** (L2/L3) | Integration Lens or System Lens |
| **SLOs, latency targets, load tests** | **Quality Attributes Lens** (L2/L3) | Runtime Lens |
| **Migration plans & strangler fig** | **Evolution Lens** (L2/L3) | System Lens |
