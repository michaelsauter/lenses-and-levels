# Example: Documentation Assessment & Audit Report

This example illustrates the output produced when the **Lenses & Levels Skill** is invoked in **Mode B** to assess existing documentation against the framework.

---

# Lenses & Levels Documentation Audit Report

**Target Path**: `/docs/architecture/`
**Audit Date**: 2026-10-05
**Overall Health Score**: ⚠️ **Needs Attention** (Moderate Architectural Drift)

---

## 1. Executive Summary

An audit of the documentation repository at `/docs/architecture/` reveals a solid foundational structure that adopts the Lenses & Levels naming conventions. However, several critical architectural invariants are compromised:
1. **Overview Bloat in System Lens**: Level 1 contains complete database column listings and SQL scripts that overwhelm newcomers.
2. **Cross-Lens Duplication**: Authentication token handling is copy-pasted identically across both the System Lens and the Security Lens.
3. **Upward Dependency Traps**: Multiple Level 3 sections explicitly demand that the reader "review Level 1 first" before configuring APIs, breaking downward self-containment.
4. **Static Prose in Level 3**: Level 3 contains manually typed JSON payloads that have drifted from the actual OpenAPI specifications in the codebase.

Remediating these issues will significantly improve readability, prevent documentation rot, and ensure each level serves its intended audience.

---

## 2. Invariants Evaluation Matrix

| Invariant | Status | Primary Findings |
| :--- | :---: | :--- |
| **1. Lens Fit** | ⚠️ Warning | Database schemas and table definitions are housed in the System Lens rather than the Data Lens. |
| **2. Level Fit** | ❌ Fail | SQL table definitions and environment configs are embedded in Level 1 (Overview). |
| **3. Non-Duplication** | ❌ Fail | JWT token lifecycle and validation logic is duplicated across `system.md` and `security.md`. |
| **4. Downward Self-Containment** | ❌ Fail | `api-detail.md#L45` contains explicit upward phrases ("as defined in Level 1"). |
| **5. Overview Discipline** | ❌ Fail | Level 1 word count exceeds Level 2 and Level 3 combined due to low-level implementation details. |

---

## 3. Detailed Findings & Recommended Actions

### Finding 1: Database Table DDL in System Overview
- **Location**: `docs/architecture/system.md#L32-L68` (Lens: `System`, Level: `Level 1`)
- **Category**: `Wrong Lens` & `Overview Bloat`
- **Severity**: `Critical`
- **Observation**:
  `system.md` contains a 35-line SQL `CREATE TABLE accounts (...)` block directly under the "Level 1: System Overview" heading. This violates Overview Discipline (mental model only) and Lens Boundaries (belongs in Data Lens).
- **Remediation**:
  1. Remove the SQL DDL block from `system.md`.
  2. Move the SQL DDL block to `docs/architecture/data.md` under `Level 3 — Detail`.
  3. In `system.md` (Level 2), insert a reference link: `> See [Data Lens > Level 3: Account Persistence](data.md#level-3)`.

---

### Finding 2: Duplicated Authentication Workflow
- **Location**: `docs/architecture/system.md#L90-L115` & `docs/architecture/security.md#L20-L45`
- **Category**: `Cross-Lens Duplication`
- **Severity**: `Major`
- **Observation**:
  An identical 25-line paragraph and sequence diagram describing OAuth2 JWT bearer token verification is present in both the System Lens (Level 2) and Security Lens (Level 2).
- **Remediation**:
  1. Designate **Security Lens** as the Single Source of Truth for identity and authentication.
  2. Remove the duplicated text from `system.md`.
  3. In `system.md`, reference the Security Lens:
     ```markdown
     Authentication is enforced at the API gateway via JWT bearer verification.
     > 🔗 For authentication token issuance, validation rules, and claims, see [Security Lens > Level 2: Identity & Auth](security.md#level-2).
     ```

---

### Finding 3: Upward Reading Dependency in Level 3
- **Location**: `docs/architecture/integration.md#L88`
- **Category**: `Downward Self-Containment Violation`
- **Severity**: `Major`
- **Observation**:
  Level 3 states: *"Before implementing these webhook handlers, refer to the high-level architecture in Level 1 above to understand who the upstream caller is."*
  This breaks downward self-containment for implementers.
- **Remediation**:
  Provide the single sentence of local context directly in Level 3:
  ```markdown
  ### Webhook Ingestion Handler
  The Payment Ingestion Service processes asynchronous payment confirmation webhooks dispatched by Stripe and Adyen.
  ```

---

## 4. Proposed Refactoring Plan (Diffs)

### System Lens (`system.md`) Refactoring Diff:

```diff
 ## Level 1 — Overview
 The Core Banking Platform manages customer ledgers and payment settlements.
-
-### Storage Schema
-CREATE TABLE accounts (
-    account_id UUID PRIMARY KEY,
-    balance NUMERIC(12, 2) NOT NULL,
-    currency VARCHAR(3) NOT NULL
-);

 ## Level 2 — Map
 ...
 ### Services & Persistence
 The Account Service maintains transaction ledgers in PostgreSQL.
+
+> 🔗 **Data Specifications**: For table schemas, indexing, and isolation levels, see [Data Lens > Level 3: Ledger Schema](data.md#level-3).
```

### Integration Lens (`integration.md`) Refactoring Diff:

```diff
 ## Level 3 — Detail
-Before implementing these webhook handlers, refer to the high-level architecture in Level 1 above to understand who the upstream caller is.
+### Webhook Ingestion Handler
+The Payment Ingestion Service processes asynchronous payment confirmation webhooks dispatched by Stripe and Adyen.
```
