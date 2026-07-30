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

## 1. Impact assessment

Classify the change as **small**, **medium**, or **large**. Complete only the
rows that materially affect this initiative; do not restate standard platform
capabilities that are already provided by the target deployment pattern.

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

## 2. Problem and outcome

State the problem, intended outcome, and measurable success signal in a few
sentences.

## 3. Scope and boundaries

## 4. Context basis and gap register

Keep one canonical context-gap register in this section. Other sections must
reference gap IDs only; do not repeat gap descriptions in impact, risks, or
review sections. Separate confirmed facts from proposed changes and do not
fill gaps with guesses.

## 5. Current-state and target approach

## 6. Options and trade-offs

For a small change, show one recommended option and alternatives only when a
material trade-off exists. Medium and large changes may include a short option
comparison and link to supporting detail.

## 7. Recommendation and decision points

**Applicable standards and approved patterns:**

| Standard / pattern | How it applies | Evidence |
|---|---|---|
| | | |

**Recommended option:** one concise statement explaining why this is the
smallest compliant design.

**Alternatives considered:** include only alternatives with a material trade-off,
pattern mismatch, or meaningful constraint.

## 8. Security, NFRs, and operations

Cover only the NFRs and operational concerns changed or specifically relevant
to this initiative.

## 9. Delivery, rollout, and rollback

## 10. Diagrams

<!-- Embed only useful, renderable Mermaid diagrams. Small changes normally need
     one context/flow diagram and at most one deployment or component view. -->

## 11. Risks and decision points

Keep one canonical risk register in this section. Add ADRs or open questions
only when they represent a distinct decision that is not already captured.

## 12. Traceability

Link the requirement, selected context, affected systems, related repositories,
and follow-on LLD. Keep evidence in YAML; keep the human decision here.

## Architecture approval

Solution Architect / ARB: pending
