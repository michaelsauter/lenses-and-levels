# Documentation Audit Rubric & Checklist

Use this rubric when evaluating existing documentation against the Lenses & Levels framework.

---

## The 5 Audit Criteria

### 1. Lens Fit & Boundary Compliance
*Does content reside in its true architectural home?*

- **Pass**: Content strictly reflects the focus of its containing lens (e.g., data entities in Domain/Data Lens, network subnets in Deployment Lens, failure recovery in Runtime Lens).
- **Warning**: Content touches multiple lenses but includes light contextual crossover without cross-references.
- **Fail / Misplacement**: Deep content is housed in the wrong lens (e.g. database table definitions placed inside System Lens; CI/CD pipeline steps placed in Runtime Lens; business capability OKRs placed in Domain Lens).

---

### 2. Level Fit & Audience Granularity
*Does content match the target cognitive zoom level?*

- **Pass**:
  - Level 1 is concise, narrative, and visual.
  - Level 2 acts as a roadmap/catalog answering *"Where does X live?"*.
  - Level 3 provides deep technical contracts, trade-offs, and living artifact links answering *"How does X work?"*.
- **Warning**: Level 2 contains slight over-elaboration or Level 3 lacks living artifact references.
- **Fail / Misplacement**:
  - Level 1 contains code snippets, parameter lists, or schema declarations.
  - Level 2 is an empty placeholder or just repeats Level 1.
  - Level 3 is a superficial summary that doesn't enable actual implementation.

---

### 3. Cross-Lens Duplication
*Is information documented in exactly one canonical lens with references elsewhere?*

- **Pass**: Zero duplicate blocks. All cross-cutting concerns are unified in their primary canonical lens and referenced with links from other lenses.
- **Warning**: Concepts are re-summarized in multiple lenses without differing perspectives or links.
- **Fail / Duplication**: Identical paragraphs, architecture diagrams, or schema tables are copy-pasted across multiple lenses, creating synchronization hazards.

---

### 4. Downward Self-Containment (Upward Trap Check)
*Can lower levels be understood in isolation without jumping upward?*

- **Pass**: A reader starting directly at Level 2 or Level 3 can fully understand the technical specification and carry out implementation without opening Level 1.
- **Warning**: Level 3 introduces unfamiliar acronyms without brief inline expansion, requiring the reader to search.
- **Fail / Upward Trap**:
  - Explicit upward dependency phrases (*"as described in Level 1"*, *"refer to the overview for context"*).
  - Level 3 omits necessary local identifiers, system context, or preconditions, forcing the reader to toggle back to Level 1 or Level 2.

---

### 5. Overview Discipline (Centrality Filter)
*Is Level 1 strictly confined to central, high-impact aspects?*

- **Pass**: Level 1 focuses purely on the mental model, business/system mission, and core boundaries. It can be read in under 5 minutes.
- **Warning**: Level 1 includes auxiliary features or mild configuration details that could be moved down.
- **Fail / Overview Bloat**:
  - Level 1 includes edge-case handling, retry loop parameters, database indexing choices, or non-central features.
  - Level 1 is significantly longer in word count than Level 2 or Level 3.

---

## Audit Report Markdown Format

When executing **Mode B (Documentation Assessment & Audit)**, deliver the findings using this structured markdown report:

```markdown
# Lenses & Levels Documentation Audit Report

**Target Path**: `<inspected_path>`
**Audit Date**: `<date>`
**Overall Health Score**: `<Pass | Needs Attention | Significant Drift>`

---

## 1. Executive Summary
<Brief 2-3 paragraph summary highlighting the primary architectural strengths and main areas of concern in the audited documentation.>

---

## 2. Invariants Evaluation Matrix

| Invariant | Status | Primary Findings |
| :--- | :--- | :--- |
| **1. Lens Fit** | ✅ / ⚠️ / ❌ | <Summary of placement accuracy> |
| **2. Level Fit** | ✅ / ⚠️ / ❌ | <Summary of zoom-level appropriateness> |
| **3. Non-Duplication** | ✅ / ⚠️ / ❌ | <Summary of cross-lens duplication & references> |
| **4. Downward Self-Containment** | ✅ / ⚠️ / ❌ | <Summary of upward dependency traps> |
| **5. Overview Discipline** | ✅ / ⚠️ / ❌ | <Summary of overview bloat vs centrality> |

---

## 3. Detailed Findings & Recommended Actions

### Finding 1: [Issue Title]
- **Location**: `[file_path#L...]` (Lens: `<LensName>`, Level: `<LevelNumber>`)
- **Category**: `[Wrong Lens | Wrong Level | Duplication | Upward Dependency | Overview Bloat]`
- **Severity**: `[Critical | Major | Minor]`
- **Observation**:
  <Detailed explanation of what was found in the text.>
- **Remediation**:
  <Actionable instruction on how to fix it: where to move the content, what reference to insert, or how to reframe.>

---

## 4. Proposed Refactoring Plan
<Concrete step-by-step instructions or markdown code diffs illustrating the restructured documentation.>
```
