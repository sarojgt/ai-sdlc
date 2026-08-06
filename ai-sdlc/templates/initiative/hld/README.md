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

The following sections are selected by the AI only when relevant:

- Authors & Approvals
- High Level Business Requirements
- Architecture Principles Applied
- Non-Functional Requirements
- Assumptions
- Context, Logical, Information/Data, and Physical/Deployment Views
- API and Integration Design
- Event and Message Flow
- Security, Networking, Testing, and Operations Considerations
- Migration and Rollout
- Commercial View
- Open Items & Decisions Required
- Pending Items from ARB, when applicable
- Traceability, when cross-artifact links need to be recorded in the human document

Key Design Decisions is also optional and should be included only when the
initiative has decisions that need an explicit decision record.

Small changes normally use one HLD. Medium and large changes may use a short
parent HLD with focused linked supporting HLD or LLD documents. Do not move
detail out merely to reduce a line count; move it when it would make the main
architecture decision harder for a human to review.

Use Mermaid diagrams only when they clarify a material decision; include an
ERD when data ownership or persistence is part of the HLD.

Architecture approval is recorded only after human Solution Architect or ARB
review. An HLD approval unlocks engineering design; the AI cannot grant it.
