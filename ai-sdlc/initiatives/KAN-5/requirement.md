---
das_version: "0.1"
artifact:
  id: "REQ-KAN-5"
  type: requirement
  version: 1
  status: approved
  title: "Add API endpoint for temporary card blocking"
  initiative: "KAN-5"
  owner: "team.cards"
source:
  provider: "jira"
  work_item_id: "KAN-5"
  url: "https://randomtry.atlassian.net/browse/KAN-5"
traceability:
  parents: ["jira:KAN-5"]
policy:
  risk_tier: "high"
  data_classification: "confidential"
---

# Requirement: Add API endpoint for temporary card blocking

## 1. Business summary

Reduce fraud exposure while allowing customers or operations users to restore
card usage without permanent card replacement. An authorized portal user must be
able to suspend a card for a bounded period when suspicious activity is detected,
and the platform must restore the card automatically when the temporary block
expires.

## 2. Problem statement

Authorized portal users need to temporarily block a card for a selected period
when suspicious activity is detected. There is currently no governed API
capability for temporarily blocking a card with automatic expiry. The block
should automatically expire after the configured duration unless removed earlier
by an authorized user. The solution must reuse existing card-management
platform patterns and avoid introducing unnecessary new platform components.

## 3. Users, consumers, and stakeholders

| Group | Need or responsibility | Priority |
|---|---|---|
| Authorized portal users (client-facing) | Request a temporary card block for a selected period when suspicious activity is detected | Must |
| Operations users | Temporarily block cards during approved support or risk workflows | Must |
| Card service / API owners | Confirm card-state ownership, endpoint location, block/unblock behavior, validation contract, and deployment path | Must |
| Security and identity owners | Confirm authentication, authorization, requester identity, tenant/region isolation, and safe logging requirements | Must |
| Operations / SRE | Confirm audit events, metrics, traces, alerts, and automatic expiry supportability | Should |
| Product and compliance owners | Confirm maximum duration, notification expectations, and customer-impact policy | Should |

## 4. Desired user or system outcome

An authorized portal user or operations actor can call a card-management API
with a card identifier and a valid temporary-block duration. The platform blocks
the card, records requester and expiry metadata, emits safe audit and
observability signals, and automatically restores the card to its prior usable
state when the temporary block expires, without requiring manual intervention.

## 5. Scope

### In scope

- Add a client-facing, authenticated API endpoint for requesting a temporary
  card block.
- Accept a card identifier or token and an explicit block duration as input.
- Validate that the caller is authorized for the card and the relevant
  client/region boundary.
- Reuse existing card lifecycle and authorization patterns.
- Reject invalid durations and already-blocked cards using existing API error
  conventions.
- Record requester, request timestamp, block creation timestamp, expiry
  timestamp, and correlation/audit identifiers.
- Automatically remove the temporary block after expiry without requiring manual
  intervention as the only restoration path.
- Preserve existing audit and observability standards.

### Out of scope

- Permanent card cancellation.
- Card replacement.
- Changes to authentication or client access models.
- New infrastructure or deployment environments.
- New standalone card-control platform.
- Manual unblocking as the only mechanism for restoration.
- Redesign of existing authentication, authorization, observability, or
  deployment standards.
- Notification delivery changes unless the HLD confirms an approved existing
  pattern.

## 6. Business rules and domain terms

| Rule or term | Meaning / expected behaviour | Source or owner |
|---|---|---|
| Temporary card block | A time-bounded card state restriction requested by an authorized actor | Jira KAN-5 |
| Block duration | The explicit period requested by the caller; approved minimum/maximum bounds require confirmation | Product, Risk, and Card owners to confirm |
| Previous usable state | The card usability state that existed before the temporary block and must be restored after expiry when still valid | Card service / API owner to confirm |
| Requester | The authenticated portal user, operations user, or service principal that requested the block | Security / Identity owner to confirm |
| Automatic restoration | The platform must remove the temporary block after expiry without relying on manual unblocking as the only mechanism | Jira KAN-5 |
| Client / region isolation | A requester must only act on cards permitted by existing client/region boundaries | Security and Card owners to confirm |
| Already-blocked card | A card that already has a temporary block in effect; must be rejected with an existing API error convention | Jira KAN-5 acceptance criteria |

## 7. Functional requirements

<!-- Use REQ-KAN-5-NN identifiers. -->

### REQ-KAN-5-01

The solution must add a client-facing, authenticated API endpoint in the
existing card-management API surface for requesting a temporary card block.

### REQ-KAN-5-02

The endpoint must accept a card identifier or token and an explicit temporary-
block duration using the approved API validation and error contract.

### REQ-KAN-5-03

The endpoint must validate that the caller is authorized for the card and the
relevant client and region boundary before applying any block.

### REQ-KAN-5-04

The endpoint must reject invalid durations and already-blocked cards using
existing API error conventions and must not apply a block on a rejected request.

### REQ-KAN-5-05

The endpoint must reuse existing card lifecycle and authorization patterns
rather than introducing a new service or new authorization model.

### REQ-KAN-5-06

For an authorized valid request, the platform must apply the temporary block and
record the requester, request timestamp, block creation timestamp, expiry
timestamp, and correlation/audit identifiers required by existing standards.

### REQ-KAN-5-07

The temporary block must expire automatically at the end of the approved
duration and restore the card to its prior usable state without requiring manual
unblocking as the only restoration path.

### REQ-KAN-5-08

The solution must preserve existing audit and observability standards; block
request, expiry, denial, and validation-failure paths must be auditable and
visible in logs, metrics, and traces without exposing PAN, authentication
secrets, or unnecessary customer data.

| ID | Requirement | Priority | Source / rationale |
|---|---|---|---|
| REQ-KAN-5-01 | Add a client-facing, authenticated temporary card-blocking endpoint in the existing card-management API surface. | Must | Jira KAN-5 scope |
| REQ-KAN-5-02 | Accept card identifier or token and explicit block duration as input. | Must | Jira KAN-5 acceptance criteria |
| REQ-KAN-5-03 | Validate caller authorization for the card and client/region boundary. | Must | Jira KAN-5 acceptance criteria |
| REQ-KAN-5-04 | Reject invalid durations and already-blocked cards with existing API error conventions. | Must | Jira KAN-5 acceptance criteria |
| REQ-KAN-5-05 | Reuse existing card lifecycle and authorization patterns; do not create a new service. | Must | Jira KAN-5 acceptance criteria |
| REQ-KAN-5-06 | Record requester, timestamps, expiry, and audit/correlation metadata on block creation. | Must | Jira KAN-5 scope |
| REQ-KAN-5-07 | Automatically expire the temporary block and restore the card without manual intervention as the only path. | Must | Jira KAN-5 acceptance criteria |
| REQ-KAN-5-08 | Preserve existing audit, observability, and safe-logging standards for all block lifecycle events. | Must | Jira KAN-5 acceptance criteria |

## 8. Non-functional requirements

| Category | Requirement or target | Priority | Owner / source |
|---|---|---|---|
| Security and privacy | Reuse existing authentication, authorization, client/region isolation, and secure logging; do not log PAN, secrets, authentication headers, or unnecessary customer data. | Must | Jira KAN-5; Security owner |
| Availability and resilience | Temporary block creation and automatic expiry must be reliable enough for card usability operations; fallback/retry behavior must be defined during HLD. | Must | Card service / API and Operations owners |
| Performance and capacity | Endpoint and expiry processing must use bounded validation and existing scalable card-management patterns; capacity expectations require HLD confirmation. | Should | Card service / API owner |
| Scalability | Expiry mechanism must scale with expected temporary-block volume without introducing a new component unless justified by HLD. | Should | Architecture and Operations owners |
| Observability and support | Block request, denial, validation error, expiry, and restoration outcomes must be visible through approved logs, metrics, traces, and dashboards without sensitive data leakage. | Must | Operations / SRE owner |
| Compliance or data residency | Preserve existing card-data retention, audit retention, client/region, and residency boundaries. | Must | Compliance, Security, and Data owners |

## 9. Data and information considerations

- Data classification: confidential.
- Sensitive or regulated data involved: card identifiers or tokens, card status,
  requester identity, client/region identifiers, timestamps, and audit/correlation
  metadata; PAN, SAD, secrets, and unnecessary customer data must not be exposed.
- Data owner: Card data owner and Security/Identity owners to confirm.
- Source systems or records, if known: existing card-management or card-state
  service and audit logging platform; exact owner and persistence model require
  HLD confirmation.
- Retention or deletion requirements: reuse existing card-state and audit-retention
  policies; no new retention policy is requested by this requirement.
- Client, tenant, regional, or residency boundaries: must reuse existing
  authorization, isolation, and residency controls for card-management operations.

## 10. Integrations and dependencies

| Dependency or integration | Internal / external | Purpose | Known owner |
|---|---|---|---|
| Existing payments / card-management API | Internal | Host the temporary card-blocking endpoint | Card service / API owner to confirm |
| Card state / block-unblock capability | Internal | Apply temporary block and restore previous usable state after expiry | Card platform owner to confirm |
| Existing identity and authorization model | Internal | Authenticate requesters and enforce authorized portal/operations access | Security / Identity owner |
| Existing client / region isolation controls | Internal | Prevent cross-client or cross-region card operations | Security / Card owner |
| Existing audit logging platform | Internal | Record requester, block, expiry, and restoration events | Operations / Security owner |
| Existing observability platform | Internal | Emit logs, metrics, and traces for supportability | Operations / SRE owner |
| API documentation platform | Internal | Publish route, request/response, errors, auth, and examples | API owner |

## 11. Constraints and approved patterns

- Business constraints: card blocking affects card usability and customer impact;
  duration limits, requester types, and notification expectations require human
  confirmation before HLD generation.
- Technology or platform constraints: reuse the existing payments/card-management
  platform, API standards, authorization model, audit logging, observability, and
  deployment standards; do not create a new service if an existing card-management
  capability supports this behavior.
- Security or regulatory constraints: enforce client/region isolation and secure
  logging; avoid exposing PAN, SAD, secrets, authentication headers, unrestricted
  card state, or unnecessary customer data.
- Existing architecture pattern that should be reused: existing card-management
  state ownership, block/unblock behavior, API validation/error contracts, audit
  events, metrics, traces, and deployment path.
- Alternatives that are explicitly not allowed: a new standalone card-control
  platform, auth/observability redesign, card issuance/tokenization changes unless
  required by HLD, or manual unblocking as the only restoration mechanism.

## 12. Acceptance criteria

- **Given** an authorized portal user and a valid temporary-block request, **When**
  the user calls the API with a card identifier and valid duration, **Then** the
  card is blocked for the requested approved duration and requester/expiry metadata
  is recorded.
- **Given** a temporary block reaches its expiry time, **When** the expiry process
  runs, **Then** the temporary block is removed and the card returns to its prior
  usable state unless another valid card state prevents usability.
- **Given** an unauthorized requester or a requester outside the card's
  client/region boundary, **When** the requester calls the API, **Then** access is
  denied using the standard authorization behavior without revealing sensitive card
  details.
- **Given** a request with an invalid duration, **When** the requester calls the
  API, **Then** the API returns a safe validation error using existing API error
  conventions and does not apply a block.
- **Given** a card that is already temporarily blocked, **When** a new block
  request is submitted, **Then** the API rejects the request using existing API
  error conventions and does not apply a second block.
- **Given** a block request, denial, validation error, expiry, or restoration
  event, **When** the event is logged or traced, **Then** it is auditable and
  observable without exposing sensitive data.

## 13. Initial impact hints

These are business or product estimates. The HLD agent must verify them against
the full context.

| Dimension | Initial view | Confidence / notes |
|---|---|---|
| Expected change size: small / medium / large / program-level | Medium | Likely one state-changing API plus expiry behavior, audit, observability, documentation, and tests |
| Expected complexity/risk: low / moderate / high / critical | High | Incorrect blocking or restoration can affect card usability, client/region isolation, and customer impact |
| Services or repositories likely involved | Existing payments/card-management or card-state service/API repository | Exact service owner and repository require HLD confirmation |
| Internal integrations | Card state/block-unblock capability, identity/authorization, client/region isolation, audit logging, metrics/tracing, API documentation | Existing platform patterns must be reused |
| External integrations | None identified | Confirm whether client-facing API gateway or notifications are involved during HLD |
| Data or security impact | High | Card status, requester identity, client/region boundaries, and audit data require strict controls and safe logging |
| Deployment or migration impact | Low to moderate | No new standalone platform expected; expiry mechanism impact requires HLD confirmation |

## 14. Assumptions and open questions

- Which existing service owns card state and block/unblock behavior?
- What is the approved maximum and minimum temporary block duration?
- Which roles, scopes, claims, or entitlements authorize temporary card blocking
  for portal users versus operations users?
- What are the exact audit event, metric, trace attribute, log redaction, and
  dashboard requirements?
- Is there already an approved card-control pattern, state machine, or expiry
  mechanism that should be reused?
- How should a new temporary-block request be handled when the card is already
  temporarily blocked?
- What should happen if the card transitions to a non-usable state for another
  reason before the temporary block expires?
- Are customer or operations notifications required when a block is created or
  expires?
- What API route, version, request/response schema, and idempotency key standard
  should be used?
- Should the capability be accessible to portal users only, operations users only,
  or both?

## 15. Business approval

Product Owner: pending

Decision: pending

Date: pending

Notes: Business approval is required before HLD generation. This requirement
captures Jira KAN-5 intake and does not approve architecture, implementation, or
release.
