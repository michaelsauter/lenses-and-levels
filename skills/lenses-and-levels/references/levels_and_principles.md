# Levels & Core Principles Reference Guide

This document defines the three standard levels of the Lenses & Levels framework and the foundational principles governing documentation quality, scoping, and referencing.

---

## The Three Universal Levels

The core premise of the framework is that every architectural concern (lens) can and should be presented across three consistent cognitive levels. This ensures predictable information discovery across the entire architecture.

```
┌────────────────────────────────────────────────────────┐
│ Level 1 — Overview                                     │
│ Audience: Newcomers, Executives, Adjacent Teams        │
│ Purpose: Build mental model (Visual-first, Narrative)  │
├────────────────────────────────────────────────────────┤
│ Level 2 — Map                                          │
│ Audience: Engineers, Architects, Reviewers             │
│ Purpose: Enable navigation & lookup ("Where is X?")    │
├────────────────────────────────────────────────────────┤
│ Level 3 — Detail                                       │
│ Audience: Implementers, Maintainers, Auditors          │
│ Purpose: Enable action & analysis ("How does it work?")│
└────────────────────────────────────────────────────────┘
```

---

### Level 1 — Overview

- **Audience**: Newcomers to the project, engineering leadership, product managers, adjacent teams.
- **Cognitive Purpose**: Establish an intuitive mental model in under 5 minutes without cognitive overload.
- **Guiding Questions**:
  - Why does this lens matter for our system?
  - What is the high-level posture or vision?
  - What are the 3-5 primary concepts or boundaries?
- **Tone & Format**:
  - Narrative over exhaustive detail.
  - Diagram or visual representation first.
  - Zero prerequisite jargon assumed.

#### The Centrality Filter (Overview Discipline)
Level 1 is vulnerable to "Overview Bloat", where authors dump every detail into the introduction. Apply the **Centrality Filter** to keep Level 1 lean:

| Keep in Level 1 (Central) | Demote to Level 2 (Map) | Demote to Level 3 (Detail) |
| :--- | :--- | :--- |
| High-level system context diagram | Component / service catalog | Class diagrams, function signatures |
| Core business mission & value | Capability-to-service matrix | Feature Jira links & backlog specs |
| Primary security posture | Identity provider & RBAC roles | Cryptographic algorithm & salt specs |
| Target cloud provider & region | Network topology & VPC zoning | Terraform resource declarations |
| Primary storage paradigm | Storage landscape by entity type | Table DDL, column types, indexes |

---

### Level 2 — Map

- **Audience**: Software engineers, architects, security engineers, code reviewers.
- **Cognitive Purpose**: Provide a reliable roadmap of the lens so that readers can quickly find where any component, schema, or rule lives.
- **Guiding Questions**:
  - Where does capability or component $X$ reside?
  - What are the relationships and boundaries between these entities?
  - What living artifacts or documentation contain the deeper details?
- **Tone & Format**:
  - Tabular catalogs, matrices, structured maps, and relational diagrams.
  - Definitions of ubiquitous domain terminology.
  - Direct pointers to repositories, services, or Level 3 sections.

---

### Level 3 — Detail

- **Audience**: Implementers, maintainers, auditors, deep technical reviewers.
- **Cognitive Purpose**: Provide all technical specifications, invariants, and edge cases necessary to build, modify, or audit the system without ambiguity.
- **Guiding Questions**:
  - How exactly does this protocol, schema, or algorithm execute?
  - What are the edge cases, failure semantics, and retry budgets?
  - What are the explicit architectural trade-offs made?
- **Tone & Format**:
  - Formal contracts (OpenAPI, AsyncAPI, protobuf, SQL DDL).
  - Code references, configuration blocks, state machine tables.
  - Exhaustive documentation of edge cases and recovery procedures.

---

## The 4 Core Principles in Depth

### Principle 1: Single Source of Truth (No Duplication Between Lenses)

**Rule**: An architectural fact belongs to exactly **one canonical lens**. Never copy-paste or restate detailed descriptions across multiple lenses.

- **The Problem**: When the same architecture detail is documented in multiple places (e.g. data schema repeated in System Lens and Data Lens), documentation drifts and falls out of sync.
- **The Solution**: Cross-lens references.
- **Implementation Pattern**:
  ```markdown
  <!-- System Lens Level 2 (Container Map) -->
  The Order Service persists state into an isolated PostgreSQL cluster.
  
  > 🔗 **Storage Specification**: For table schemas, indexing strategies, and data retention policies, see [Data Lens > Level 3: Order Persistence Schema](#data-lens-level-3).
  ```

---

### Principle 2: Downward Self-Containment (Zero Upward Dependencies)

**Rule**: Lower levels (Level 2 and Level 3) must be fully self-contained. Readers jumping directly to Level 2 or Level 3 must not be required to read Level 1 to understand the content.

- **The Problem**: Developers looking for implementation instructions in Level 3 are forced to jump upwards to Level 1 to decode undefined acronyms, learn the system's role, or understand the architecture.
- **The Anti-Pattern (Upward Trap)**:
  - ❌ *"As discussed in Level 1 above, we use the aforementioned proxy architecture..."*
  - ❌ *"Refer to Level 1 for the definition of the OMS module before configuring these endpoints."*
- **The Correct Pattern**:
  - Provide a concise 1-sentence local context sentence:
    ```markdown
    <!-- Level 3 Detail -->
    ### Order Management Service (OMS) API Specification
    The Order Management Service (OMS) handles checkout transactions and cart transitions.
    Below is the OpenAPI specification and failure handling contract:
    ```
  - Lower levels may reference laterally (to other lenses at the same or deeper level) or link out to external living artifacts, but should never force upward cognitive back-tracking.

---

### Principle 3: Overview Discipline (Strict Scoping)

**Rule**: Level 1 (Overview) covers strictly central aspects. Peripheral, edge-case, and technical implementation details must be pushed down to lower levels.

- **The Anti-Pattern (Overview Bloat)**:
  - ❌ Listing every environment variable in the System Overview.
  - ❌ Explaining fallback retry exponential backoff formulas in the Integration Overview.
  - ❌ Embedding raw JSON payloads into the Domain Overview.
- **The Correct Pattern**:
  - Keep Level 1 focused on the **Why**, the **Primary Boundary**, and the **Mental Model**.
  - Move configuration tables to Level 2.
  - Move algorithms, payloads, and edge cases to Level 3.

---

### Principle 4: Living Artifact Anchoring (Level 3 Reality)

**Rule**: For Level 3 (Detail), prefer linking to or embedding **living artifacts** over writing long, static markdown prose that rots as code changes.

- **Living Artifact Types**:
  - **OpenAPI / Swagger Specs**: `specs/order-service-api.yaml`
  - **Infrastructure as Code (IaC)**: Terraform modules, Helm charts, Kubernetes YAMLs.
  - **Database Migrations & Schemas**: Prisma schema, Flyway migrations, SQL DDL files.
  - **Architecture Decision Records (ADRs)**: `docs/adr/0004-postgresql-sharding.md`.
  - **Observability Dashboards**: Grafana dashboard links, Datadog monitors.
- **Pattern**:
  ```markdown
  ### Level 3 — Detail
  
  #### Contract Definition
  - **Living Contract**: [`order-api-v2.yaml`](file:///workspace/contracts/order-api-v2.yaml)
  - **Interactive Swagger UI**: [https://api.internal/docs/orders](https://api.internal/docs/orders)
  - **ADR Reference**: [ADR-0012: Event-Driven Order Processing](file:///workspace/docs/adr/0012.md)
  ```
