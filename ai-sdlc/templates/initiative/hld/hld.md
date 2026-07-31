---
das_version: "0.1"
artifact:
  id: "HLD-{{ initiative.id }}"
  type: hld
  version: 1
  status: draft
  title: "{{ initiative.title }}"
  initiative: "{{ initiative.id }}"
  owner: "{{ roles.solution_architect }}"
  profile: "{{ hld.profile }}"
  change_size: ""
traceability:
  parents: ["REQ-{{ initiative.id }}"]
  satisfies: []
  impacts: []
design_baseline: "../evidence/design-baseline.yaml"
approvals:
  required: [architecture]
  records: []
policy:
  implementation_locked_until: architecture.approved
---

# HLD: {{ initiative.title }}

<!-- Adapted from the Paymentology Architecture SDD template. Keep the main
     document concise and decision-oriented; move substantial detail to linked
     supporting artifacts. -->

## 1. Change assessment

Classify the change as **small**, **medium**, or **large**. Record only impacts
that are material to this initiative; do not restate standard platform
capabilities already supplied by the target deployment pattern.

| Dimension | Assessment | Evidence or context gap |
|---|---|---|
| Change size | small / medium / large / program-level | |
| Complexity / risk | low / moderate / high / critical | |
| Services or repositories | count and names | |
| Internal integrations | count and names | |
| External integrations | count and names | |
| Data and security impact | low / medium / high | |
| Runtime or deployment impact | low / medium / high | |
| Migration or compatibility impact | low / medium / high | |
| Recommended governance path | standard / enhanced / ARB | |

**Assessment summary:** one short paragraph explaining why this classification was chosen.

## 2. Motivation and outcome

State the business problem, intended outcome, and measurable success signal.

## 3. Authors and approvals

| Role | Person or team | Status |
|---|---|---|
| Business owner | | |
| Solution Architect / ARB | | Pending |
| Infrastructure / Platform | | |
| Engineering lead | | |
| Security | | |

## 4. Solution overview

Summarize the recommended solution in one short paragraph.

## 5. Context gaps

Keep one canonical context-gap register in this section. Other sections must
reference gap IDs only. Separate confirmed facts from proposed changes and do
not fill gaps with guesses.

| Gap ID | Missing fact | Owner | Retrieval action | Blocks decision? |
|---|---|---|---|---|
| GAP-001 | | | | |

## 6. Risks

| Risk ID | Risk | Impact | Mitigation or owner |
|---|---|---|---|
| RISK-001 | | | |

## 7. Solution design

Add only the relevant SDD views below. Use subsections freely, and omit views
that do not affect the decision. Keep diagrams beside the view they explain.

<!-- Optional SDD sections to add when material:

## High-level business requirements
Link the requirements, epic, or business case satisfied by this design.

## Architecture principles applied
Reference only the approved principles and patterns that constrain this design.

## Non-functional requirements
Cover relevant performance, availability, security, scalability, cost,
operability, and compliance constraints without inventing target values.

## Assumptions and scope boundaries
Record confirmed assumptions and explicit exclusions.

### Context view
C4 Level 1: actors, system boundary, and major external interactions.

### Logical view
C4 Level 2/container view of affected or relevant existing components.

### Information and data view
ERD or data flow only when data ownership, storage, or movement is material.

### Process and interaction view
Sequence or activity view for material runtime, asynchronous, retry, or
failure behavior.

### Physical and deployment view
Relevant workload zone, regional deployment, platform boundary, and operations.
Reference approved platform topology instead of duplicating it.

## Security considerations
Cover only initiative-specific trust, identity, data protection, PCI/CHD,
audit, and security review needs.

## Testing considerations
Cover only design-specific functional, integration, performance, resilience,
migration, security, or disaster-recovery testing needs.

## Operations and delivery
Cover only changed monitoring, alerting, runbooks, rollout, rollback,
migration, and operational ownership.

## Options and trade-offs
Include alternatives only when they represent a material trade-off.
-->

## 8. Recommendation and decision points

**Applicable standards and approved patterns:**

| Standard / pattern | How it applies | Evidence |
|---|---|---|
| | | |

**Recommended option:** one concise statement explaining why this is the
smallest compliant design.

**Alternatives considered:** include only alternatives with a material trade-off,
pattern mismatch, or meaningful constraint.

<!-- Embed only useful, renderable Mermaid diagrams in the relevant design-view
     sections. Small changes normally need one context/flow diagram and at most
     one deployment or component view. -->

## 9. Traceability and ADRs

Link the requirement, selected context, affected systems, related repositories,
and follow-on LLD. Record only decisions that need an ADR; keep evidence in
YAML and human decisions in this document.

## Architecture approval

Solution Architect / ARB: pending
