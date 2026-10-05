---
name: lenses-and-levels
description: Author, decompose, structure, and audit architecture documentation using the Lenses & Levels framework. Use when given unstructured text to split into architectural lenses and detail levels, or when given a documentation path to assess whether content is in the correct lens and level, eliminate cross-lens duplication, verify downward self-containment, and enforce overview discipline.
---

# Lenses & Levels Architecture Documentation Skill

This skill guides the authoring, decomposition, and auditing of software architecture documentation using the **Lenses & Levels** framework.

The framework organizes architecture documentation along two orthogonal dimensions:
1. **Lenses (Concerns)**: 15 distinct architectural perspectives (System, Capability, Domain, Data, Integration, Runtime, Deployment, Security, Quality Attributes, Governance & Decision, Evolution, UX & Interaction, Organization, Cost, Compliance).
2. **Levels (Detail & Audience)**: 3 consistent zoom levels for every lens:
   - **Level 1 — Overview**: Mental model, executive narrative, visual-first, strictly central aspects.
   - **Level 2 — Map**: Navigation, structural orientation, catalog, answers *"Where does X live?"*.
   - **Level 3 — Detail**: Deep technical specification, contracts, edge cases, trade-offs, living artifacts, answers *"How does X work?"*.

---

## The 4 Golden Principles of Lenses & Levels

Whenever splitting text or auditing existing documentation, you **MUST** uphold these four principles:

1. **Non-Duplication Between Lenses (Single Source of Truth)**
   - Information belongs canonically to exactly **one** primary lens.
   - Never duplicate conceptual descriptions or diagrams across lenses.
   - If another lens relies on that information, provide a direct **cross-lens reference** (e.g., `> See [Data Lens > Level 2: Data Landscape](...) for persistence stores`).

2. **Downward Self-Containment (Zero Upward Dependencies)**
   - **Lower levels must be completely self-contained.**
   - A reader jumping directly into Level 2 (Map) or Level 3 (Detail) must **never** be forced to jump upward to Level 1 or Level 2 to understand what is being detailed.
   - Include necessary local context, define key local identifiers, or state prerequisites inline. Never write upward trap phrases like *"as defined in the overview above"* or assume prior reading of upper levels.

3. **Overview Discipline (Strict Centrality Filter)**
   - **Level 1 (Overview) covers ONLY core, central aspects.**
   - It is designed for newcomers and executives to build a high-level mental model in minutes.
   - **Demote non-central content**: Edge cases, configuration options, secondary workflows, and implementation details do not belong in Level 1; push them down to Level 2 (Map) or Level 3 (Detail).

4. **Living Artifact Anchoring (Level 3 Reality)**
   - Level 3 (Detail) should prioritize links and embeddings to living artifacts (e.g., OpenAPI specs, Terraform code, database migrations, ADRs, source code symbols, Grafana dashboards) rather than retyping static prose.

---

## Operating Modes

Determine which mode to execute based on user input:

- **Mode A: Text Ingestion & Splitting** — Triggered when the user provides raw text, notes, an RFC, PRD, or unstructured architectural draft.
- **Mode B: Documentation Assessment & Audit** — Triggered when the user provides a file path or directory location of existing documentation, or asks to review/audit documentation.

If the user provides neither, ask whether they would like to author new documentation from raw text or audit existing documentation at a specific path.

---

## Mode A: Text Ingestion & Splitting Workflow

Follow this procedure when decomposing raw text into Lenses & Levels:

### Step 1: Lens Mapping
Analyze the input text and extract topics into the appropriate Lenses. Consult [references/lenses_catalog.md](references/lenses_catalog.md) for precise boundaries:
- **Core Lenses**: `System`, `Capability`, `Domain`, `Data`, `Integration`, `Runtime`, `Deployment`.
- **Contextual / Quality Lenses**: `Security`, `Quality Attributes`, `Governance & Decision`, `Evolution`, `UX & Interaction`, `Organization`, `Cost`, `Compliance`.

*Disambiguation Rule*: If a concept overlaps multiple lenses (e.g., database storage touches System, Data, and Deployment):
- Assign canonical ownership to the primary concern (e.g., table schemas & storage models -> **Data Lens**; hosting instance topology -> **Deployment Lens**; service boundary -> **System Lens**).

### Step 2: Level Assignment & Overview Filtering
For each extracted piece within a lens, assign it to Level 1, Level 2, or Level 3:
- **Level 1 (Overview)**:
  - Ask: *"Is this concept strictly essential for a newcomer or executive to understand why this lens matters and its core posture?"*
  - If YES: Retain in Level 1.
  - If NO (e.g., non-central details, specific parameters, edge cases): Demote to Level 2 or Level 3.
- **Level 2 (Map)**:
  - Group into catalogs, relationship matrices, component listings, bounded contexts, or topology maps that orient the reader.
- **Level 3 (Detail)**:
  - Place precise specifications, schemas, contracts, failure semantics, trade-offs, and pointers to source code or config files.

### Step 3: Eliminate Duplication & Add References
- Identify any redundant explanations across different lenses.
- Consolidate the explanation into the single canonical lens.
- Replace duplicate instances in other lenses with markdown cross-references:
  ```markdown
  > **Related Architecture**: For data storage schemas and classification, see [Data Lens > Level 2: Data Landscape](#data-lens-level-2-map).
  ```

### Step 4: Verify Downward Self-Containment
- Review Level 2 and Level 3 sections independently.
- Check: Can a developer read Level 3 directly and execute their task without opening Level 1?
- If Level 3 relies on an acronym, system role, or business term, ensure it is clearly contextualized locally. Remove any *"as explained in Level 1"* phrasing.

### Step 5: Format and Present
Output the structured documentation using standard Markdown. Follow the template provided in [references/levels_and_principles.md](references/levels_and_principles.md) and inspect [examples/split_text_example.md](examples/split_text_example.md) for a reference implementation.

---

## Mode B: Documentation Assessment & Audit Workflow

Follow this procedure when reviewing or auditing existing documentation at a given path:

### Step 1: Scan and Discover
1. Inspect the provided path using directory listing and file view tools.
2. Locate all documentation files (Markdown, HTML, AsciiDoc, etc.).
3. Optional: Run the automated audit helper script to gather structural metrics:
   ```bash
   python3 skills/lenses-and-levels/scripts/audit_docs.py --path <docs_location>
   ```

### Step 2: Evaluate Against Framework Invariants
Perform a systematic audit against the 5 key criteria (see [references/audit_rubric.md](references/audit_rubric.md)):

1. **Lens Appropriateness**:
   - Is content located in the right lens?
   - Common violations: Database schemas inside System Lens (should be Data Lens); CI/CD pipelines inside Runtime Lens (should be Deployment Lens); business KPIs inside Domain Lens (should be Capability Lens).
2. **Level Appropriateness**:
   - Is Level 1 overloaded with details?
   - Is Level 2 actually serving as a map/navigation guide?
   - Is Level 3 providing deep specs or linking to living artifacts?
3. **Cross-Lens Duplication**:
   - Search for identical or near-identical explanations copied across multiple files/lenses.
   - Flag duplicate sections and identify which lens should be the Single Source of Truth.
4. **Downward Self-Containment**:
   - Scan Level 2 and Level 3 for upward dependencies:
     - Explicit upward phrases (*"as mentioned in overview"*, *"refer to level 1"*, *"as stated previously"*).
     - Missing local context (e.g. Level 3 assumes knowledge of terms only defined in Level 1).
5. **Overview Discipline (Bloat Check)**:
   - Identify peripheral, non-central information cluttering Level 1.
   - Mark specific items that must be demoted to Level 2 or 3.

### Step 3: Produce the Audit Report
Deliver a clear, actionable audit report formatted as:
1. **Executive Summary & Health Score** (Pass / Needs Attention / Significant Drift).
2. **Findings Table**:
   - `Location` (File, Lens, Level)
   - `Violation Type` (Wrong Lens, Level Misplacement, Cross-Lens Duplication, Upward Dependency, Overview Bloat)
   - `Details & Evidence`
   - `Recommended Action`
3. **Targeted Refactoring / Diffs**:
   - Concrete before-and-after restructuring proposals for the affected sections.

See [examples/audit_report_example.md](examples/audit_report_example.md) for an example audit output.

---

## Detailed References & Tools

- **All 15 Lenses Guide**: [references/lenses_catalog.md](references/lenses_catalog.md) — Boundary definitions, canonical owners, and level prompts.
- **Levels & Core Principles**: [references/levels_and_principles.md](references/levels_and_principles.md) — Universal definitions, centrality filter rules, and self-containment guidelines.
- **Audit Rubric**: [references/audit_rubric.md](references/audit_rubric.md) — Checklists, scoring criteria, and violation remediation patterns.
- **Text Splitting Example**: [examples/split_text_example.md](examples/split_text_example.md) — Full before-and-after demonstration of text decomposition.
- **Audit Report Example**: [examples/audit_report_example.md](examples/audit_report_example.md) — Real-world example of auditing documentation.
- **Automated Audit Script**: [scripts/audit_docs.py](scripts/audit_docs.py) — CLI tool for fast structural and text analysis.
