# Solution Design / High-Level Design

The AI creates a proposal here after the requirement is approved.

The template follows the section names used by the company’s existing solution
design documents. It is a section menu, not a checklist. The generated HLD must
be concise and decision-oriented: retain only sections that affect this
initiative, remove empty sections and placeholder tables, and use short tables
or bullets instead of long narrative.

The mandatory core is:

- Motivation
- Solution Overview
- Risks
- Solution Design
- One Context gaps register

The AI must always generate this core, even when a section contains a concise
statement such as “None identified.”

The AI selects optional sections and design views from
[`section-catalog.md`](section-catalog.md) using the preflight impact
assessment. The catalog contains inclusion questions, not mandatory headings.

Small changes normally use one HLD. Medium and large changes may use a short
parent HLD with focused linked supporting HLD or LLD documents. Do not move
detail out merely to reduce a line count; move it when it would make the main
architecture decision harder for a human to review.

The authoritative suitability, document strategy, option-analysis, design-view,
timeout, and loop limits for each size are defined in
`ai-sdlc/config/hld-profiles.yaml`. `auto` is assessment-only and must resolve
to a concrete profile before final generation.

Diagrams are optional. Use Mermaid only when it clarifies a material decision;
consider an ERD when changed data ownership or persistence is part of that
decision.

Architecture approval is recorded only after human Solution Architect or ARB
review. An HLD approval unlocks engineering design; the AI cannot grant it.
