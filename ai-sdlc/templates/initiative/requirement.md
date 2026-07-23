---
das_version: "0.1"
artifact:
  id: "REQ-{{ initiative.id }}"
  type: requirement
  version: 1
  status: draft
  title: "{{ initiative.title }}"
  initiative: "{{ initiative.id }}"
  owner: "{{ initiative.owner }}"
source:
  provider: "{{ source.provider }}"
  work_item_id: "{{ source.work_item_id }}"
traceability:
  parents: ["{{ source.provider }}:{{ source.work_item_id }}"]
policy:
  risk_tier: "{{ policy.risk_tier }}"
  data_classification: "{{ policy.data_classification }}"
---

# Requirement: {{ initiative.title }}

## 1. Business summary

{{ requirement.business_outcome }}

## 2. Problem statement

{{ requirement.problem_statement }}

## 3. Users, consumers, and stakeholders

| Group | Need or responsibility | Priority |
|---|---|---|
| Primary user / consumer | | Must |
| Business owner | | Must |
| Supporting teams | | Should |

## 4. Desired user or system outcome

Describe what should be possible after this requirement is delivered. Include a
short example or user journey where useful.

## 5. Scope

### In scope

-

### Out of scope

-

## 6. Business rules and domain terms

Record the rules that must be preserved and link important terms to the shared
business glossary where possible.

| Rule or term | Meaning / expected behaviour | Source or owner |
|---|---|---|
| | | |

## 7. Functional requirements

<!-- Use REQ-{{ initiative.id }}-NN identifiers. -->

### REQ-{{ initiative.id }}-01

The solution must ...

| ID | Requirement | Priority | Source / rationale |
|---|---|---|---|
| REQ-{{ initiative.id }}-01 | | Must | |

## 8. Non-functional requirements

Capture only known targets. Leave unknown values as questions rather than
inventing numbers.

| Category | Requirement or target | Priority | Owner / source |
|---|---|---|---|
| Security and privacy | | Must | |
| Availability and resilience | | Should | |
| Performance and capacity | | Should | |
| Scalability | | Should | |
| Observability and support | | Should | |
| Compliance or data residency | | Must | |

## 9. Data and information considerations

- Data classification: {{ policy.data_classification }}
- Sensitive or regulated data involved:
- Data owner:
- Source systems or records, if known:
- Retention or deletion requirements:
- Client, tenant, regional, or residency boundaries:

## 10. Integrations and dependencies

List known dependencies without designing the solution yet. The HLD will verify
the relationship with repositories, services, APIs, databases, tables, events,
platform capabilities, and external providers.

| Dependency or integration | Internal / external | Purpose | Known owner |
|---|---|---|---|
| | | | |

## 11. Constraints and approved patterns

- Business constraints:
- Technology or platform constraints:
- Security or regulatory constraints:
- Existing architecture pattern that should be reused:
- Alternatives that are explicitly not allowed:

## 12. Acceptance criteria

Use observable, testable statements. Prefer Given / When / Then where practical.

- **Given** ... **When** ... **Then** ...
- **Given** ... **When** ... **Then** ...

## 13. Initial impact hints

These are business or product estimates. The HLD agent must verify them against
the full context.

| Dimension | Initial view | Confidence / notes |
|---|---|---|
| Expected change size: small / medium / large / program-level | | |
| Expected complexity/risk: low / moderate / high / critical | | |
| Services or repositories likely involved | | |
| Internal integrations | | |
| External integrations | | |
| Data or security impact | | |
| Deployment or migration impact | | |

## 14. Assumptions and open questions

-

## 15. Business approval

Product Owner: pending

Decision: pending

Date: pending

Notes:
