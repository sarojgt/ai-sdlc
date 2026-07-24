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

## 3. Scope and boundaries

## 4. Confirmed context and context gaps

## 5. Current-state and target approach

## 6. Options and trade-offs

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

## 9. Delivery, rollout, and rollback

## 10. Diagrams

<!-- Embed only the diagrams useful for this change as Mermaid fenced blocks. -->

## 11. Risks, ADRs, and open questions

## 12. Traceability

## Architecture approval

Solution Architect / ARB: pending
