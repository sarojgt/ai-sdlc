# High-Level Design

The AI creates a proposal here after the requirement is approved.

Expected proposal content:

- Impact assessment before solution design: change size, affected services and
  repositories, integration points, data/security impact, deployment impact, and
  required governance path.
- Concise problem, outcome, scope, current state, and confirmed context.
- Only the architecture-level options and trade-offs needed for a decision.
- Recommended direction, decision points, risks, NFRs, rollout, and rollback.
- Mermaid diagrams embedded directly in `hld.md`; use context, C4, deployment,
  sequence, or ERD views only when they clarify the decision.
- Context gaps with an owner and retrieval action. Do not invent missing facts.
- Traceability to requirements and proposed ADRs.

The HLD is a human-readable decision document. Detailed SQL, class structure,
package layout, endpoint implementation, test cases, and migration scripts belong
in the LLD after architecture approval.

Architecture approval is recorded only after human Solution Architect or ARB
review. An HLD approval unlocks engineering design; the AI cannot grant it.
