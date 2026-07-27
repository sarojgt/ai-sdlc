---
das_version: "0.1"
artifact:
  id: "REQ-KAN-4"
  type: requirement
  version: 1
  status: draft
  title: "Temporary card blocking API"
  initiative: "KAN-4"
  owner: "team.cards"
source:
  provider: "jira"
  work_item_id: "KAN-4"
  url: "https://randomtry.atlassian.net/browse/KAN-4"
traceability:
  parents: ["jira:KAN-4"]
policy:
  risk_tier: "high"
  data_classification: "confidential"
---

# Requirement: Temporary card blocking API

## 1. Business summary

Allow an authorized client or operations user to temporarily block a card for a
defined period of time. The temporary block must expire automatically at the end
of the requested duration, and the card should return to its previous usable
state without manual intervention.

## 2. Problem statement

There is no confirmed governed API capability for temporarily blocking a card
with automatic expiry. Clients and operations users need a secure, auditable, and
observable way to suspend card usability for a bounded duration while reusing the
existing payments/card-management platform patterns and avoiding unnecessary new
platform components.

## 3. Users, consumers, and stakeholders

| Group | Need or responsibility | Priority |
|---|---|---|
| Authorized client applications | Request a temporary card block for eligible cards within their tenant/client boundary | Must |
| Operations users | Temporarily block cards during approved support or risk workflows | Must |
| Card service/API owners | Confirm the card-state owner, endpoint location, block/unblock behavior, validation contract, and deployment path | Must |
| Security and identity owners | Confirm authentication, authorization, requester identity, tenant isolation, and safe logging requirements | Must |
| Operations/SRE | Confirm audit event, metrics, traces, alerts, and automatic expiry supportability | Should |
| Product and compliance owners | Confirm maximum duration, notification expectations, and customer-impact policy | Should |

## 4. Desired user or system outcome

An authorized actor can call a card-management API with a card identifier and
valid temporary-block duration. The platform blocks the card, records requester
and expiry metadata, emits safe audit and observability signals, and
automatically restores the card to its prior usable state when the temporary
block expires.

## 5. Scope

### In scope

- Add a new authenticated card-blocking API capability.
- Support a temporary block with an explicit expiry duration.
- Record who requested the block, when it was created, and when it expires.
- Preserve enough prior-state information to restore the card after temporary
  block expiry without manual intervention.
- Enforce existing authentication, authorization, client/tenant isolation,
  validation, error handling, and idempotency standards where applicable.
- Reuse existing payments/card-management platform patterns, audit logging,
  observability, and deployment standards.
- Document the API behavior, validation errors, authorization requirements, audit
  behavior, and operational expectations.

### Out of scope

- New standalone card-control platform.
- Changes to card issuance or tokenization logic unless the HLD proves they are
  required.
- Manual unblocking as the only mechanism for restoration.
- Redesign of existing authentication, authorization, observability, or
  deployment standards.
- Notification delivery changes unless the HLD confirms an approved existing
  notification requirement or pattern.

## 6. Business rules and domain terms

| Rule or term | Meaning / expected behaviour | Source or owner |
|---|---|---|
| Temporary card block | A time-bounded card state restriction requested by an authorized actor | Jira KAN-4 |
| Expiry duration | The explicit period requested by the caller; approved minimum/maximum bounds require confirmation | Product, Risk, and Card owners to confirm |
| Previous usable state | The card usability state that existed before the temporary block and must be restored after expiry when still valid | Card service/API owner to confirm |
| Requester | The authenticated client, operations user, or service principal that requested the block | Security/Identity owner to confirm |
| Automatic restoration | The platform must remove the temporary block after expiry without relying on manual unblocking as the only mechanism | Jira KAN-4 |
| Tenant isolation | A requester must only act on cards permitted by existing client/tenant boundaries | Security and Card owners to confirm |

## 7. Functional requirements

<!-- Use REQ-KAN-4-NN identifiers. -->

### REQ-KAN-4-01

The solution must add an authenticated API endpoint in the existing
payments/card-management API surface for requesting a temporary card block.

### REQ-KAN-4-02

The endpoint must accept a card identifier and an explicit temporary-block
duration or expiry input using the approved API validation and error contract.

### REQ-KAN-4-03

The endpoint must reject malformed requests, missing required fields, invalid
card identifiers, and durations outside the approved policy bounds with a safe
validation error.

### REQ-KAN-4-04

The endpoint must enforce existing authentication, authorization, and
client/tenant isolation so unauthorized actors cannot block a card or infer card
existence outside their permitted scope.

### REQ-KAN-4-05

For an authorized valid request, the platform must apply the temporary block and
record the requester, request timestamp, block creation timestamp, expiry
timestamp, and correlation/audit identifiers required by existing standards.

### REQ-KAN-4-06

The platform must preserve the card's previous usable state or equivalent
restoration context so the card can return to that state when the temporary block
expires, unless another valid card state transition prevents usability.

### REQ-KAN-4-07

The temporary block must expire automatically at the end of the approved duration
without requiring manual unblocking as the only restoration path.

### REQ-KAN-4-08

The solution must handle repeated, overlapping, or concurrent temporary-block
requests according to an approved idempotency and state-conflict policy confirmed
during HLD.

### REQ-KAN-4-09

The block action, expiry, denial, and validation-failure paths must be auditable
and visible in logs, metrics, and traces without exposing PAN, authentication
secrets, unnecessary customer data, or other sensitive data.

### REQ-KAN-4-10

The API documentation must describe the route, request and response fields,
duration constraints, authorization requirements, validation errors, audit and
observability behavior, and automatic-expiry semantics.

| ID | Requirement | Priority | Source / rationale |
|---|---|---|---|
| REQ-KAN-4-01 | Add an authenticated temporary card-blocking endpoint in the existing card-management API surface. | Must | Jira KAN-4 scope |
| REQ-KAN-4-02 | Accept card identifier and explicit expiry duration or expiry input. | Must | Jira KAN-4 scope |
| REQ-KAN-4-03 | Reject malformed input and invalid durations with safe validation errors. | Must | Jira KAN-4 acceptance criteria |
| REQ-KAN-4-04 | Enforce existing authentication, authorization, and tenant isolation. | Must | Jira KAN-4 acceptance criteria |
| REQ-KAN-4-05 | Record requester, timestamps, expiry, and audit/correlation metadata. | Must | Jira KAN-4 scope |
| REQ-KAN-4-06 | Preserve prior usable state or restoration context. | Must | Jira KAN-4 automatic restoration requirement |
| REQ-KAN-4-07 | Automatically expire the temporary block without manual intervention as the only path. | Must | Jira KAN-4 acceptance criteria |
| REQ-KAN-4-08 | Define idempotency and conflict handling for repeated or overlapping block requests. | Should | State-changing API safety |
| REQ-KAN-4-09 | Emit safe audit logs, metrics, and traces for block lifecycle events. | Must | Jira KAN-4 observability/audit acceptance criteria |
| REQ-KAN-4-10 | Document API behavior, constraints, authorization, errors, and expiry semantics. | Must | API delivery standard |

## 8. Non-functional requirements

| Category | Requirement or target | Priority | Owner / source |
|---|---|---|---|
| Security and privacy | Reuse existing authentication, authorization, tenant isolation, and secure logging standards; do not log PAN, secrets, authentication headers, or unnecessary customer data. | Must | Jira KAN-4; Security owner |
| Availability and resilience | Temporary block creation and automatic expiry must be reliable enough for card usability operations; fallback/retry behavior must be defined during HLD. | Must | Card service/API and Operations owners |
| Performance and capacity | Endpoint and expiry processing must use bounded validation and existing scalable card-management patterns; capacity expectations require HLD confirmation. | Should | Card service/API owner |
| Scalability | Expiry mechanism must scale with expected temporary-block volume without introducing a new component unless justified by HLD. | Should | Architecture and Operations owners |
| Observability and support | Block request, denial, validation error, expiry, and restoration outcomes must be visible through approved logs, metrics, traces, and operational dashboards without sensitive data leakage. | Must | Operations/SRE owner |
| Compliance or data residency | Preserve existing card-data retention, audit retention, client/tenant, regional, and residency boundaries. | Must | Compliance, Security, and Data owners |

## 9. Data and information considerations

- Data classification: confidential.
- Sensitive or regulated data involved: card identifiers, card status, requester
  identity, tenant/client identifiers, timestamps, and audit/correlation metadata;
  PAN, SAD, secrets, and unnecessary customer data must not be exposed.
- Data owner: Card data owner and Security/Identity owners to confirm.
- Source systems or records, if known: existing card-management/card-state service
  and audit logging platform; exact owner and persistence model require HLD
  confirmation.
- Retention or deletion requirements: reuse existing card-state and audit-retention
  policies; no new retention policy is requested by this requirement.
- Client, tenant, regional, or residency boundaries: must reuse existing
  authorization, isolation, and residency controls for card-management operations.

## 10. Integrations and dependencies

| Dependency or integration | Internal / external | Purpose | Known owner |
|---|---|---|---|
| Existing payments/card-management API | Internal | Host the temporary card-blocking endpoint | Card service/API owner to confirm |
| Card state/block-unblock capability | Internal | Apply temporary block and restore previous usable state after expiry | Card platform owner to confirm |
| Existing identity and authorization model | Internal | Authenticate requesters and enforce authorized client/operations access | Security/Identity owner |
| Existing tenant/client isolation controls | Internal | Prevent cross-client or cross-tenant card operations | Security/Card owner |
| Existing audit logging platform | Internal | Record requester, block, expiry, and restoration events | Operations/Security owner |
| Existing observability platform | Internal | Emit logs, metrics, and traces for supportability | Operations/SRE owner |
| API documentation platform | Internal | Publish route, request/response, errors, auth, and examples | API owner |

## 11. Constraints and approved patterns

- Business constraints: card blocking affects card usability and customer impact;
  duration limits, requester types, and notification expectations require human
  confirmation.
- Technology or platform constraints: reuse the existing payments/card-management
  platform, API standards, authorization model, audit logging, observability, and
  deployment standards.
- Security or regulatory constraints: enforce tenant isolation and secure logging;
  avoid exposing PAN, SAD, secrets, authentication headers, unrestricted card
  state, or unnecessary customer data.
- Existing architecture pattern that should be reused: existing card-management
  state ownership, block/unblock behavior, API validation/error contracts, audit
  events, metrics, traces, and deployment path.
- Alternatives that are explicitly not allowed: a new standalone card-control
  platform, auth/observability redesign, card issuance/tokenization changes unless
  required by HLD, or manual unblocking as the only restoration mechanism.

## 12. Acceptance criteria

- **Given** an authorized requester and a valid temporary-block request, **When**
  the requester calls the API, **Then** the card is blocked for the requested
  approved duration and requester/expiry metadata is recorded.
- **Given** a temporary block reaches its expiry time, **When** the expiry process
  runs, **Then** the temporary block is removed and the card returns to its prior
  usable state unless another valid card state prevents usability.
- **Given** an unauthorized requester or a requester outside the card's
  client/tenant boundary, **When** the requester calls the API, **Then** access is
  denied using the standard authorization behavior without revealing sensitive
  card details.
- **Given** a malformed request, missing required field, invalid card identifier,
  or invalid duration, **When** the requester calls the API, **Then** the API
  returns a safe validation error and does not apply a block.
- **Given** a block request, denial, validation error, expiry, or restoration
  event, **When** the event is logged or traced, **Then** it is auditable and
  observable without exposing sensitive data.

## 13. Initial impact hints

These are business or product estimates. The HLD agent must verify them against
the full context.

| Dimension | Initial view | Confidence / notes |
|---|---|---|
| Expected change size: small / medium / large / program-level | Medium | Likely one state-changing API plus expiry behavior, audit, observability, documentation, and tests |
| Expected complexity/risk: low / moderate / high / critical | High | Incorrect blocking or restoration can affect card usability, tenant isolation, and customer impact |
| Services or repositories likely involved | Existing payments/card-management or card-state service/API repository | Exact service owner and repository require confirmation |
| Internal integrations | Card state/block-unblock capability, identity/authorization, tenant isolation, audit logging, metrics/tracing, API documentation | Existing platform patterns should be reused |
| External integrations | None identified | Confirm whether client-facing API gateway or notifications are involved during HLD |
| Data or security impact | High | Card status, requester identity, tenant boundaries, and audit data require strict controls and safe logging |
| Deployment or migration impact | Low to moderate | No new standalone platform expected; persistence or scheduler/expiry mechanism impact requires HLD confirmation |

## 14. Assumptions and open questions

- Which existing service owns card state and block/unblock behavior?
- What is the approved maximum and minimum temporary block duration?
- Should the capability be client-driven, operations-driven, or both?
- Which roles, scopes, claims, or entitlements authorize temporary card blocking?
- What are the exact audit event, metric, trace attribute, log redaction, and
  dashboard requirements?
- Is there already an approved card-control pattern, state machine, or expiry
  mechanism that should be reused?
- How should overlapping or repeated temporary-block requests be handled?
- What should happen if the card transitions to a non-usable state for another
  reason before the temporary block expires?
- Are customer or operations notifications required when a block is created or
  expires?
- What API route, version, request/response schema, and idempotency key standard
  should be used?

## 15. Business approval

Product Owner: pending

Decision: pending

Date: pending

Notes: Business approval is required before HLD generation. This requirement
captures Jira KAN-4 intake and does not approve architecture, implementation, or
release.
