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

## 5. High-level business requirements

List the requirements this design satisfies and link the approved requirement
or business epic where available.

## 6. Architecture principles applied

| Principle or approved pattern | Application to this design | Context evidence |
|---|---|---|
| | | |

## 7. Non-functional requirements

Cover only relevant performance, availability, security, scalability, cost,
operability, and compliance constraints. Do not invent target values.

## 8. Assumptions and scope boundaries

State confirmed assumptions and what is explicitly out of scope.

## 9. Context gaps

Keep one canonical context-gap register in this section. Other sections must
reference gap IDs only. Separate confirmed facts from proposed changes and do
not fill gaps with guesses.

| Gap ID | Missing fact | Owner | Retrieval action | Blocks decision? |
|---|---|---|---|---|
| GAP-001 | | | | |

## 10. Risks

| Risk ID | Risk | Impact | Mitigation or owner |
|---|---|---|---|
| RISK-001 | | | |

## 11. Solution design

### Context view

Use a C4 Level 1 diagram showing actors, system boundaries, and major external
interactions.

### Logical view

Use a C4 Level 2/container view, showing only the affected or relevant
existing components.

### Information and data view

Include an ERD or data-flow diagram only when data ownership, storage, or
movement is material to the decision.

### Process and interaction view

Include a sequence or activity diagram for material runtime behavior,
including asynchronous, retry, concurrency, or failure paths where relevant.

### Physical and deployment view

Show the relevant workload zone, regional deployment, platform boundary, and
operational dependencies. Reference the approved platform design instead of
duplicating standard topology.

## 12. Options and trade-offs

For a small change, show one recommended option and alternatives only when a
material trade-off exists. Medium and large changes may include a short option
comparison and link to supporting detail.

## 13. Recommendation and decision points

**Applicable standards and approved patterns:**

| Standard / pattern | How it applies | Evidence |
|---|---|---|
| | | |

**Recommended option:** one concise statement explaining why this is the
smallest compliant design.

**Alternatives considered:** include only alternatives with a material trade-off,
pattern mismatch, or meaningful constraint.

## 14. Security considerations

Describe authentication, authorization, trust boundaries, data protection,
PCI/CHD implications, audit, and security review needs that are specific to
this initiative.

## 15. Testing considerations

Describe only design-specific functional, integration, performance, resilience,
migration, security, or disaster-recovery testing needs.

## 16. Operations and delivery

Cover monitoring, alerting, runbooks, deployment, rollout, rollback, migration,
and operational ownership. Include only what changes or is material.

<!-- Embed only useful, renderable Mermaid diagrams in the relevant design-view
     sections. Small changes normally need one context/flow diagram and at most
     one deployment or component view. -->

## 17. Traceability and ADRs

Link the requirement, selected context, affected systems, related repositories,
and follow-on LLD. Record only decisions that need an ADR; keep evidence in
YAML and human decisions in this document.

## Architecture approval

Solution Architect / ARB: pending
