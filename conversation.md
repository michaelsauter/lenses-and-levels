
You said:
I am a software architect. I am not happy with the popular templates / structures for architecture documentation. I have my own idea. here it is: "lenses & levels". basically, the documentation is divided into lenses - e.h. system lens, capability lens, data lens, security lens, and so on. for each lens there are 3 levels - introduction (for people who have no clue yet about the lens), orientation (for people who need to find information about the lens) and elaboration (when you really need to know). sometimes a level can also be a link to an artefact, e.g. a swagger doc. also, the system lens could be c4 model the first 3 levels. now: does something like this already exist?

ChatGPT said:
Short answer: your idea is original in its combination of concerns and the “three levels per lens” concept — but there are existing approaches and standards that are conceptually adjacent. Let’s unpack that with concrete references.
📌 What already exists that is similar
✅ View-centric / multi-perspective documentation frameworks
ISO/IEC/IEEE 42010 (Architecture Description Standard)
• This international standard defines views and viewpoints for architecture descriptions — the idea is that different stakeholders care about different aspects (views) of architecture. Your lenses are conceptually similar to viewpoints in this standard. 
Viewpoints and Perspectives (SEI / Carnegie Mellon)
• A classic structured way to describe architecture by viewpoints (logical view, process view, physical view) and scenarios — similar philosophy to “look through different lenses.” (this stems from ISO 42010 and the predecessor “4+1” model). 
✅ C4 Model — similar in levels
The C4 Model decomposes a system into four hierarchical views (context → containers → components → code).
This multi-level abstraction is quite close to your concept of “levels,” even though the C4 focus is structural views of a system, not a set of lenses across different concerns. 
So:

C4 = “three-four levels of zoom for the system lens.”
You = “*three levels of detail for each lens.””
They intersect in the idea of levels of detail, but your structure spans multiple concerns (lenses).
✅ Arc42 Template — a modular documentation structure
arc42 is a widely-used software architecture documentation template. It defines chapters like:
Introduction and goals
Constraints
Context and scope
Building block view
Runtime view
Deployment view
… and more. 
This is conceptually similar to lenses but arranged as document sections rather than a matrix of lenses × levels. It also provides guidance on:
What should be documented
Why
How
That’s close to your intent, but not expressed as lenses with three levels.
✅ AWS Well-Architected Lenses
Interestingly, AWS uses the term “Lens” in a different domain:
AWS Well-Architected Framework has lenses like security lens, data analytics lens, hybrid networking lens, etc. These overlay best practices for specific concerns. 
This shows the lens metaphor exists in architecture frameworks — though not as part of a documentation template per se.
🚀 Where your idea fits / what’s new
Your proposal is essentially a two-dimensional documentation structure:
Axis 1 — Lenses
• different architectural concerns (system, capability, data, security, etc.)

Axis 2 — Levels
• introduction (for novices)
• orientation (for people navigating the lens)
• elaboration (deep knowledge)

This has two key innovations:
✔ explicit separation of concerns (like ISO 42010’s view types but in a uniform grid),
✔ consistent levels of detail for each concern (so documentation scales with audience need).

I haven’t seen a widely-adopted published template that uses exactly this “lens × level matrix” pattern. Most existing approaches either:

define views per stakeholder in a fixed set of sections (ISO 42010 / arc42),
or define levels of abstraction for a single concern (like structural views in C4).
But nobody bundles multiple concern lenses with three distinct levels per lens in a formalized template.
So your idea isn’t something already packaged in the mainstream, at least not under a commonly known name.
✨ How your idea relates to established patterns
Concept	Existing Equivalent	Difference
Multiple lenses	ISO 42010 views/viewpoints; AWS Well-Architected lenses	You formalize them into documentation structure rather than review/best practice context
Levels of abstraction	C4’s zoom levels	Existing levels are structural; yours are about audience understanding
Template with guidance	arc42	arc42 has fixed sections; yours is a matrix of lenses × levels
💡 Final summary
✅ Your idea combines two established concepts — viewpoints and levels of detail — in a novel documentation pattern.
❌ There isn’t a well-known standard or template that explicitly formalizes this “lens & level” approach as you described.
💡 But you are standing on the shoulders of architecture documentation frameworks like ISO 42010, the C4 model, arc42, and lens-based frameworks like AWS Well-Architected. 
If you want, I can help you formalize your approach into a reusable template (e.g., a Markdown framework or a documentation generator scaffold). Just let me know what output format you’d prefer!

You said:
cool. continuing on this standing on the shoulders of giants, which lenses should there be? give a name and short description for each

ChatGPT said:
Great question. Since you’re explicitly building on view-based architecture traditions like ISO/IEC 42010 and structural zoom approaches like C4 model, a good set of lenses should:
Cover the core architectural concerns
Map cleanly to stakeholder interests
Avoid overlap as much as possible
Be stable across domains (enterprise, SaaS, embedded, etc.)
Below is a pragmatic, minimal-but-complete set of lenses that works well as a foundation. You can expand or specialize later.
Core Lenses for “Lenses & Levels”
1️⃣ System Lens
What the system is and how it is structured.
Covers boundaries, context, containers, components, and their relationships.
(Your C4-style zoom levels fit naturally here.)
2️⃣ Capability Lens
What the system enables the business to do.
Describes business capabilities, value streams, feature groupings, and ownership domains.
Bridges strategy and implementation.
3️⃣ Domain Lens
The conceptual model of the problem space.
Core domain concepts, aggregates, bounded contexts, ubiquitous language, invariants.
This is where domain-driven design thinking lives.
4️⃣ Data Lens
How information is structured, stored, and flows.
Data models, ownership, lifecycle, integration flows, persistence choices, APIs, schemas.
5️⃣ Integration Lens
How the system interacts with other systems.
APIs, contracts, events, external dependencies, messaging, protocols, versioning strategy.
6️⃣ Runtime Lens
How the system behaves when it runs.
Execution flows, concurrency, scaling, state management, failure handling, resilience patterns.
7️⃣ Deployment Lens
How the system is built, deployed, and operated.
Environments, infrastructure topology, CI/CD, containerization, cloud setup, networking.
8️⃣ Security Lens
How risk is mitigated and trust is established.
Threat model, identity, authorization, data protection, compliance, auditability.
9️⃣ Quality Attributes Lens
How non-functional requirements are realized.
Performance, availability, scalability, maintainability, observability, operability.
(This is where trade-offs become explicit.)
🔟 Governance & Decision Lens
Why the architecture is the way it is.
Architecture Decision Records (ADRs), constraints, principles, standards, trade-offs.
1️⃣1️⃣ Evolution Lens
How the system changes over time.
Roadmap, technical debt, migration paths, deprecation strategy, architectural runway.
Optional Context-Dependent Lenses
Depending on organization maturity or scale:
Organization Lens – team topology, ownership, Conway’s Law implications
Cost Lens – FinOps, cost drivers, scaling economics
UX Lens – user journeys, interaction patterns
Compliance Lens – regulatory mapping
What Makes This Cohesive
These lenses cluster naturally into four meta-domains:
Meta-domain	Lenses
Structure	System, Domain, Data
Interaction	Integration, Runtime
Operation	Deployment, Security, Quality
Intent & Change	Capability, Governance, Evolution
That gives your framework internal logic instead of being just a list.
If you’d like, next we can:
Refine this into a minimal canonical set (7 lenses instead of 11)
Or design a Lens Selection Guide (which lenses are mandatory vs optional)
Or define what “Introduction / Orientation / Elaboration” means consistently across all lenses
This is shaping into something publishable, by the way.

You said:
I think we can keep the 7 lenses with 4 optional ones. that's helpful. lets define the levels and what they mean for each lense

ChatGPT said:
Excellent. This is where your idea becomes structurally powerful.
We’ll define:

3 universal levels
Then concretize what each level means per lens
Keep it consistent enough to be learnable
But specific enough to be useful
The Three Levels (Universal Definition)
🟢 Level 1 — Introduction
Purpose: Build basic mental model.
Audience: Newcomers, executives, adjacent teams.
Characteristics:
Narrative over detail
Visual first
No prerequisite knowledge assumed
Explains why this lens matters
🟡 Level 2 — Orientation
Purpose: Enable navigation and targeted lookup.
Audience: Engineers, architects, reviewers.
Characteristics:
Structured overview
Key artefact references
Terminology defined
Shows “where to find more”
This level answers: “Where does X live?”
🔴 Level 3 — Elaboration
Purpose: Enable implementation, analysis, or change.
Audience: Implementers, auditors, deep reviewers.
Characteristics:
Detailed diagrams, specs, contracts
Links to living artefacts (e.g., OpenAPI, Terraform, ADRs)
Trade-offs documented
Edge cases covered
This level answers: “How exactly does this work?”
Now let’s apply this to the 7 core lenses + 4 optional.
Core Lenses × Levels
1️⃣ System Lens
Intro:
System context diagram + short narrative.
What is in scope? What is not?
Orientation:
Container/component overview. Responsibility boundaries.
Mapping to teams or repos.

Elaboration:
Detailed component diagrams, sequence flows, code structure references.

2️⃣ Capability Lens
Intro:
High-level capability map. What business value areas exist?
Orientation:
Capabilities mapped to systems, services, or bounded contexts. Ownership defined.

Elaboration:
Capability decomposition, KPIs, supporting features, dependency map.

3️⃣ Domain Lens
Intro:
Core domain concepts and glossary. Ubiquitous language.
Orientation:
Bounded contexts and their relationships. Context map.

Elaboration:
Aggregates, invariants, domain rules, lifecycle state machines.

4️⃣ Data Lens
Intro:
Major data entities and flows. Where does critical data live?
Orientation:
Data ownership map. Storage technologies. Integration flows.

Elaboration:
Schemas, data contracts, retention rules, migration strategies.

5️⃣ Integration Lens
Intro:
External systems overview. Why integrations exist.
Orientation:
API/event catalog. Protocols. Versioning strategy.

Elaboration:
OpenAPI specs, async schemas, retry policies, error semantics.

6️⃣ Runtime Lens
Intro:
How the system behaves at runtime (sync/async, stateless/stateful).
Orientation:
Execution flows, scaling model, concurrency approach.

Elaboration:
Thread models, resilience patterns, timeouts, circuit breakers.

7️⃣ Deployment Lens
Intro:
Environment overview (dev/test/prod). Cloud/on-prem context.
Orientation:
Infrastructure topology. CI/CD flow. Network zones.

Elaboration:
IaC definitions, pipeline configs, autoscaling rules.

Optional Lenses × Levels
8️⃣ Security Lens (Optional)
Intro:
Security posture overview. Threat categories.
Orientation:
Identity model, trust boundaries, data classification.

Elaboration:
Threat model, encryption details, access matrices, audit controls.

9️⃣ Quality Attributes Lens (Optional)
Intro:
Key quality goals (performance, availability, etc.).
Orientation:
Quality attribute scenarios. Measurement strategy.

Elaboration:
Benchmarks, SLOs, load tests, trade-off analysis.

🔟 Governance & Decision Lens (Optional)
Intro:
Architecture principles and constraints.
Orientation:
ADR index. Technology standards.

Elaboration:
Detailed ADRs, rejected alternatives, compliance mapping.

1️⃣1️⃣ Evolution Lens (Optional)
Intro:
Strategic direction and major upcoming changes.
Orientation:
Roadmap, technical debt register, lifecycle states.

Elaboration:
Migration plans, deprecation timelines, refactoring strategy.

What Makes This Powerful
Your model now has:
Horizontal coherence → same 3 cognitive levels everywhere
Vertical completeness → each concern fully covered
Audience-based clarity → readers know what level they need
Artefact linking built-in → level 3 naturally connects to living docs
If you'd like, next we can:
Formalize this into a repeatable template format (Markdown skeleton)
Define how to keep it lightweight (avoid documentation explosion)
Or design a navigation structure (how lenses are discovered and linked)
You're very close to having a genuinely distinct documentation methodology.