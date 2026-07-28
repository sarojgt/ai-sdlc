---
das_version: "0.1"
artifact:
  id: "REQ-E2E-001"
  type: requirement
  version: 1
  status: draft
  title: "Card search by customer name"
  initiative: "E2E-001"
  owner: "team.payments"
source:
  provider: "github"
  work_item_id: "E2E-001"
traceability:
  parents: ["github:E2E-001"]
policy:
  risk_tier: "medium"
  data_classification: "confidential"
---

# Requirement: Card search by customer name

## 1. Business summary

Allow authorized users to find cards by customer name through the existing card search capability

## 2. Problem statement

Users cannot efficiently locate a card when they know the customer name but not the card identifier

## 3. Users, consumers, and stakeholders

| Group | Need or responsibility | Priority |
|---|---|---|
| Operations and support users | Find a card using a customer's name when the card identifier is unavailable | Must |
| Payments product owner | Improve card search efficiency without changing the existing authorization boundary | Must |
| Payments engineering team | Confirm the existing search service, API, data source, and indexes | Must |

## 4. Desired user or system outcome

An authorized user can submit a customer name to the existing card-search
capability and receive matching cards subject to the existing client, tenant,
region, masking, and authorization rules. The result should use the existing
search response conventions wherever they already exist.

## 5. Scope

### In scope

- Add customer-name search as an additional supported search criterion.
- Preserve existing authorization, data masking, pagination, and client scope.
- Return a useful empty result when no matching cards are found.

### Out of scope

- A new card-search service or database.
- Changes to card issuance, tokenization, authorization, or card lifecycle.
- Relaxing access to cardholder or sensitive data.

## 6. Business rules and domain terms

Record the rules that must be preserved and link important terms to the shared
business glossary where possible.

| Rule or term | Meaning / expected behaviour | Source or owner |
|---|---|---|
| Authorized search | Only callers already authorized for card search may use this criterion | Product/security owner |
| Customer name | Matching semantics, normalization, and supported fields must be confirmed from the existing domain/API contract | Domain owner |

## 7. Functional requirements

<!-- Use REQ-E2E-001-NN identifiers. -->

### REQ-E2E-001-01

The solution must add customer-name filtering to the existing card-search capability.

| ID | Requirement | Priority | Source / rationale |
|---|---|---|---|
| REQ-E2E-001-01 | The existing card-search capability must accept a customer-name filter without requiring a new service boundary. | Must | Product owner |
| REQ-E2E-001-02 | Existing authorization, client/tenant/region scope, masking, pagination, and error conventions must remain effective. | Must | Security and API owners |
| REQ-E2E-001-03 | The implementation must use the existing authoritative card/customer data path after the HLD confirms the concrete service, schema, and query path. | Must | Architecture owner |

## 8. Non-functional requirements

Capture only known targets. Leave unknown values as questions rather than
inventing numbers.

| Category | Requirement or target | Priority | Owner / source |
|---|---|---|---|
| Security and privacy | No additional data exposure; reuse existing authorization and masking controls. | Must | Security owner |
| Availability and resilience | Preserve existing card-search availability and failure behavior. | Should | Platform owner |
| Performance and capacity | Confirm an indexed/searchable path and query bounds during HLD/LLD. | Should | Engineering owner |
| Scalability | Avoid an unbounded scan as customer-name usage grows. | Should | Engineering owner |
| Observability and support | Reuse existing search metrics, audit, tracing, and error monitoring. | Should | Operations owner |
| Compliance or data residency | Preserve existing client, regional, and sensitive-data handling rules. | Must | Compliance owner |

## 9. Data and information considerations

- Data classification: confidential
- Sensitive or regulated data involved: customer and card-related information; exact fields require confirmation.
- Data owner: payments domain owner to confirm.
- Source systems or records, if known: existing card-search data path; concrete service/schema/table requires context discovery.
- Retention or deletion requirements: unchanged from the existing card-search capability.
- Client, tenant, regional, or residency boundaries: unchanged and must be enforced by the existing path.

## 10. Integrations and dependencies

List known dependencies without designing the solution yet. The HLD will verify
the relationship with repositories, services, APIs, databases, tables, events,
platform capabilities, and external providers.

| Dependency or integration | Internal / external | Purpose | Known owner |
|---|---|---|---|
| Existing card-search API/service | Internal | Receive and authorize the customer-name filter | Payments engineering |
| Existing authoritative card/customer data source | Internal | Resolve matching cards | Payments/data owner to confirm |
| Existing observability and audit controls | Internal | Monitor usage, errors, access, and performance | Platform/security |

## 11. Constraints and approved patterns

- Business constraints: deliver as an additive search capability with existing user behavior preserved.
- Technology or platform constraints: prefer existing service, API, data, deployment, and platform patterns.
- Security or regulatory constraints: do not bypass authorization, masking, client segregation, or regional controls.
- Existing architecture pattern that should be reused: existing card-search API and authoritative data path, subject to evidence.
- Alternatives that are explicitly not allowed: a parallel card database, duplicate search service, or new authorization path without an approved decision.

## 12. Acceptance criteria

Use observable, testable statements. Prefer Given / When / Then where practical.

- **Given** an authorized user and a valid customer-name filter, **when** the existing card-search capability is called, **then** matching permitted cards are returned using existing response and pagination conventions.
- **Given** a caller without permission or outside the permitted client/tenant/region scope, **when** the search is called, **then** the existing access-control response is preserved.
- **Given** no matching permitted cards, **when** the search is called, **then** an empty result is returned without exposing unrelated data.
- **Given** malformed or unsupported search input, **when** the search is called, **then** the existing validation/error convention is returned.

## 13. Initial impact hints

These are business or product estimates. The HLD agent must verify them against
the full context.

| Dimension | Initial view | Confidence / notes |
|---|---|---|
| Expected change size: small / medium / large / program-level | small to medium; HLD must verify | Initial product estimate |
| Expected complexity/risk: low / moderate / high / critical | moderate because customer/card data is involved | Initial product estimate |
| Services or repositories likely involved | Existing card-search API/service and authoritative data repository | To be confirmed by context discovery |
| Internal integrations | Existing authorization, client/tenant/region controls, data source, observability | To be confirmed |
| External integrations | None expected | To be confirmed |
| Data or security impact | Search over sensitive customer/card-related data; no new exposure intended | Security review required |
| Deployment or migration impact | Prefer additive deployment; schema/index changes only if evidence requires them | HLD/LLD to confirm |

## 14. Assumptions and open questions

- Which existing API/service owns card search?
- Which authoritative data source and fields support customer-name matching?
- What normalization, exact/partial matching, pagination, index, masking, and audit conventions already exist?
- Which client, tenant, and regional deployment paths must be exercised?

## 15. Business approval

Product Owner: pending

Decision: pending

Date: pending

Notes:
