---
das_version: "0.1"
artifact:
  id: "HLD-DEMO-003"
  type: hld
  version: 2
  status: draft
  title: "Payment webhook delivery reliability"
  initiative: "DEMO-003"
  owner: "team.solution-architecture"
traceability:
  parents: ["REQ-DEMO-003"]
  satisfies: ["REQ-DEMO-003-01", "REQ-DEMO-003-02"]
  impacts: ["payment-service", "partner-webhook-service", "platform-observability"]
approvals:
  required: [architecture]
  records: []
policy:
  implementation_locked_until: architecture.approved
---

# HLD Proposal: Payment webhook delivery reliability

## 1. Status and outcome

This is a draft for review, not an architecture approval. The human Solution
Architect owns the decision. LLD creation, implementation, merge, and
deployment remain blocked until the architecture gate passes.

The proposal aims to provide reliable, observable delivery of payment-status
webhooks to enabled partners, with bounded and recoverable retries and no
payment credentials or sensitive authentication data in payloads or evidence.

## 2. Evidence, facts, assumptions, and scope

### Confirmed facts

- `REQ-DEMO-003`, version 1, is approved for HLD generation on 2026-07-22.
- An eligible enabled partner must receive a webhook after an accepted payment
  status transition (`REQ-DEMO-003-01`).
- Retries must be idempotent, bounded, observable, and dead-letterable
  (`REQ-DEMO-003-02`).
- At least 99% of eligible deliveries should be accepted by the downstream
  endpoint within five minutes.
- Initiative context identifies payment status processing, partner webhook
  delivery, and operations/observability; candidate repositories are
  `payment-service`, `partner-webhook-service`, and `platform-observability`.
- Payment credentials and sensitive authentication data must not appear in
  webhook payloads, logs, or operational evidence.

### Context limitations and assumptions

The context pack `CTX-DEMO-003-v1` is marked draft and contains no shared
context items. Initiative-relative context contains no current APIs, event
schemas, repository evidence, runtime topology, traffic measurements, or
deployment facts. The following are therefore design assumptions to validate:

- An accepted transition can produce a durable event or an equivalent outbox
  record.
- A durable transport, persistence store, secret manager, and observability
  platform are available or can be introduced.
- The partner registry can provide enabled status, destination, and delivery
  configuration without exposing secrets to the workflow.
- Partners can consume a stable event identity for deduplication.

In scope: transition-to-webhook handoff, fan-out, delivery attempts, identity,
idempotency, bounded retry, dead-letter/recovery, delivery state, monitoring,
and migration. Out of scope: payment-state processing, partner business logic,
provider selection, detailed schemas, infrastructure manifests, and LLD/tests.

## 3. Proposed target concept

The working direction is a durable asynchronous delivery pipeline:

1. After an accepted status transition, `payment-service` emits a minimal event
   or writes an equivalent durable outbox record.
2. `partner-webhook-service` validates the event, resolves enabled partners,
   and creates a delivery intent before attempting delivery.
3. A worker sends the signed webhook with bounded timeout and per-partner
   concurrency/rate controls. Each attempt writes durable state and redacted
   outcome metadata.
4. Transient failures use bounded exponential backoff with jitter. Permanent
   failures and exhausted retries enter a controlled dead-letter path.
5. Operations query delivery state and may perform an authorized, audited
   replay. Replay reuses the original identity; it is not a new business event.

### Stable partner-visible identity contract

The HLD contract is a transition-level identifier named `event_id`, sent both
in the webhook envelope and as the `X-Payment-Event-Id` header. It identifies
the accepted payment-status transition represented by that webhook, not a
delivery attempt. It must be generated or adopted once at the authoritative
transition boundary and remain unchanged across all retries, authorized
replays, and any overlapping migration path. Partners may use it to
deduplicate effects; it contains no credentials or authentication data.

Internally, the delivery uniqueness boundary is `(partner_id, event_id)` and
the delivery-state record stores that same `event_id`, partner, status, attempt
history, and redacted failure metadata. An attempt ID is separate and unique
per HTTP attempt. Before implementation, the payment domain must confirm the
exact event/version composition, including whether a revised status transition
is a new event or a new version of the same event.

See the [lifecycle diagram](diagrams/context.mmd), [Option 1](options/option-01.md),
and [Option 2](options/option-02.md).

## 4. Requirement and quality-attribute response

| Requirement | HLD response | Status/evidence |
|---|---|---|
| REQ-DEMO-003-01 | Durable accepted-transition event fans out to each enabled partner. | Proposal; source and registry contracts unknown. |
| REQ-DEMO-003-02 | Durable state keyed by `(partner_id,event_id)`, bounded retry, DLQ, and audited replay. | Proposal; technology unknown. |
| 99% within five minutes | Measure end-to-end acceptance latency, queue age, and partner response; alert and capacity-test against the target. | Requirement target; volume and partner SLA unknown. |
| Idempotent partner deduplication | `event_id` plus `X-Payment-Event-Id` is stable across retry, replay, and coexistence. | HLD contract; exact domain identity requires confirmation. |
| Security/privacy | Allow-list payload, reference-only secret handling, encryption, least privilege, and redaction. | Required guardrail; signing standard unresolved. |
| Operations | State view, metrics, traces, DLQ, replay runbook, and reconciliation. | Proposal; owner and thresholds unknown. |

## 5. Options and trade-offs

Scores are directional (1 = weak, 5 = strong) and must be validated against
estate measurements.

| Dimension | Option 1: durable async | Option 2: synchronous handoff + recovery |
|---|---:|---:|
| Security | 4 — clear boundary, but more durable surfaces to protect | 3 — fewer components, but tighter payment-path trust boundary |
| Performance | 5 — buffers bursts and isolates partner latency | 2 — request-path coupling threatens tail latency |
| Scalability | 5 — independent workers and partner throttles | 2 — scales with payment traffic and downstream capacity |
| Cost | 3 — transport, store, workers, and telemetry | 4 initially at low volume; reconciliation cost grows |
| Operations | 4 — explicit lag, state, retry, and DLQ controls | 2 — recovery depends heavily on reconciliation |
| Migration | 4 — cohort/shadow cutover and stable-ID coexistence | 3 — simpler first step, harder later decoupling |

Option 1 is the working recommendation for review because it best supports the
five-minute target, partner isolation, fan-out, and explicit recovery. Option 2
remains viable only if measured volume is low, an approved durable transport is
unavailable, and the Solution Architect accepts the coupling and safeguards.

## 6. Security and operations guardrails

- Send only an allow-listed minimal business payload; exclude credentials,
  PAN/CVV, authentication secrets, and equivalent sensitive data.
- Use the approved partner signing/authentication standard; keep key material in
  an approved secret manager and never in payloads or logs.
- Encrypt transport and persistence; enforce least-privilege service and
  operator access; audit DLQ inspection and replay.
- Redact bodies, authorization headers, signatures, endpoint secrets, and
  sensitive error text from logs, traces, metrics, and DLQs.
- Classify failures, use bounded exponential backoff with jitter, timeouts,
  circuit breaking, and per-partner rate/concurrency limits.
- Alert on acceptance latency, queue age, attempts, duplicate suppression, DLQ
  age/count, replay outcomes, and reconciliation gaps with named owners.

## 7. Migration, rollout, and rollback

1. Inventory the current sender, accepted-transition source, registry,
   authentication, rates, retention, residency, and ownership.
2. Confirm the event identity composition and version the event, webhook
   envelope, delivery-state, and replay contracts in the LLD.
3. Introduce the path in disabled or shadow mode where safe. Shadowing must not
   send a customer-visible duplicate; it may observe and compare outcomes.
4. Enable a small partner cohort, validate latency, duplicate suppression, DLQ
   recovery, redaction, and reconciliation, then expand gradually.
5. During coexistence, designate one authoritative sender. If both paths can
   observe an event, both must carry the same `event_id` and share the
   `(partner_id,event_id)` deduplication boundary.

Rollback disables new delivery creation or the new consumer while preserving
   payment processing, state, identity records, and dead letters. Do not delete
   idempotency state or blindly replay queues. Re-enable the legacy sender only
   after confirming it is authoritative and will not create a second identity
   for the same accepted transition.

## 8. Proposed ADR and decision gate

The decision candidate and consequences are recorded in [adr.md](adr.md). It is
proposed only. Human architecture and security review remain required,
especially for signing, retention, residency, platform, and identity semantics.

## Architecture approval

Solution Architect: **pending**

## Open questions

1. What is the authoritative event source and exact immutable composition of
   `event_id`? Is a revised status a new event or a version?
2. What is the mandatory partner signing/authentication standard and key
   rotation process?
3. What HTTP statuses, redirects, timeouts, and partner acknowledgements count
   as downstream acceptance?
4. What steady-state/peak rates, fan-out, regional distribution, and endpoint
   limits must capacity planning support?
5. What delivery-history and DLQ retention, residency, deletion, and audit
   requirements apply?
6. Which approved transport, store, secret manager, and observability services
   are available?
7. Who owns the producer, registry, workers, DLQ/replay, reconciliation, and
   partner support? What alert thresholds and recovery objectives apply?
8. What legacy delivery path exists, and can shadow/cohort rollout avoid
   customer-visible duplicate sends?

## Concise summary

This reviewable draft compares a durable asynchronous pipeline with a
synchronous handoff. Option 1 is the working direction because it isolates
partner failure, absorbs bursts, and makes retry/DLQ/replay state explicit. The
stable partner-visible `event_id` and `X-Payment-Event-Id` are preserved across
attempts, replay, and migration, subject to domain confirmation of composition.
The context pack lacks estate evidence, so signing, retention, identity,
volume, platform, and ownership remain open review gates. No approval or
implementation authorization is recorded.
