# HLD Proposal: Payment Status Notification

## Document control

- Initiative: `DEMO-002`
- Requirement: `REQ-DEMO-002`, version 1, approved 2026-07-22
- Proposal status: **Reviewable proposal — pending human Solution Architect approval**
- Scope: high-level architecture only
- Approval authority: Solution Architect / applicable architecture review board

This document is a design proposal. It does not approve the architecture, unlock implementation, create an LLD, or authorize deployment.

## 1. Outcome and scope

The initiative should make a customer-visible notification available within 30 seconds of a payment entering `completed` or `failed`, for at least 95% of status changes. Repeated delivery of the same terminal event must produce one customer notification. Payment credentials and sensitive authentication data must never enter the notification path.

In scope:

- Detecting terminal payment status changes.
- Transporting a terminal status event to notification processing.
- Durable duplicate suppression and retry handling.
- Publishing the customer-visible notification.
- Operational visibility for latency, failures, retries, and duplicates.

Out of scope for this HLD:

- Selection of first-release notification channels; this remains an approved-requirement open question.
- Detailed API schemas, database schemas, code structure, IaC, test cases, or deployment manifests.
- Changes to payment authorization, capture, settlement, or credential handling.

## 2. Inputs and confidence

Confirmed from the approved requirement and context:

- Candidate capabilities are `payment-service` and `notification-service`.
- Existing payment events are assumed to be available to the notification service.
- The notification path must be idempotent and must exclude payment credentials and sensitive authentication data.
- Requirement risk tier is medium; implementation is locked until architecture approval.
- The context pack is draft and contains no shared context items. No current-state diagram, contract, ADR, runtime evidence, repository link, or channel decision was supplied.

Consequently, broker choice, persistence technology, delivery channel, ownership boundaries, retention, regional behavior, and current event semantics are proposals to validate—not established facts.

## 3. Proposed solution concept

The preferred concept is an event-driven notification path:

1. `payment-service` emits a minimal terminal status event after its state transition is durably accepted.
2. A managed event transport provides buffering, delivery, retry, and dead-letter handling.
3. `notification-service` validates the event, removes/ rejects disallowed data, and records an idempotency key before creating a notification.
4. A notification provider/channel adapter delivers the customer-visible notification.
5. The service exposes status and metrics without exposing payment credentials or sensitive authentication data.

The proposed idempotency key is `(payment_id, terminal_state)` with an event/version discriminator only if the domain confirms that a payment can legitimately re-enter or revise a terminal state. The exact key and ordering rules require domain confirmation.

The context relationship is shown in [context.mmd](diagrams/context.mmd). Option details and trade-offs are in [option-01.md](options/option-01.md) and [option-02.md](options/option-02.md).

## 4. Quality attributes and guardrails

| Attribute | HLD target / guardrail |
|---|---|
| Security | Minimize event fields; allow-list payment identifier, terminal state, event identity, occurred-at, and customer-notification reference. Encrypt transport/storage, authenticate producers/consumers, least privilege, redact payloads in logs, and reject credentials/SAD. |
| Performance | Budget the 30-second target across event acceptance, queueing, processing, provider delivery, and customer availability. Alert on p95 end-to-end latency and age of oldest queued event. |
| Reliability | Durable event acceptance, at-least-once processing, bounded retries, dead-letter queue, replay procedure, and idempotent notification creation. |
| Scalability | Stateless consumers with independently scalable workers; partition/order only where required by payment identity; provider throttling must be isolated. |
| Operations | Correlation IDs, payment-safe event IDs, metrics, traces with redaction, dashboards, runbooks, and ownership for replay/dead-letter queues. |
| Data governance | Define retention, residency, access audit, deletion behavior, and provider data handling before implementation. |
| Cost | Prefer managed transport and existing notification infrastructure; size by status-change rate, burst factor, retention, provider fees, and operational support load. |

No credentials, PAN, CVV, authentication secrets, or equivalent sensitive authentication data may be added to the event, idempotency record, logs, traces, dead-letter payload, or provider request.

## 5. Option comparison

| Dimension | Option 1 — durable event-driven pipeline | Option 2 — synchronous notification orchestration |
|---|---|---|
| Security | Narrow, brokered event contract; dead-letter and replay surfaces require strict controls. | Fewer durable transport surfaces, but payment request path has direct coupling to notification/provider trust boundaries. |
| Performance | Absorbs bursts; predictable processing, subject to queue/provider age. | Low nominal hop count, but provider latency directly affects payment flow and tail latency. |
| Scalability | Consumers and transport scale independently; strongest fit for bursts and retries. | Scales with payment request traffic and provider capacity; back-pressure is harder to isolate. |
| Cost | Managed transport, storage, monitoring, and DLQ cost; lower coupling reduces support cost at scale. | Lower initial infrastructure cost, but higher risk of payment-path capacity and incident cost. |
| Operations | Explicit retries, replay, and lag operations are required. | Simpler initial topology; failure recovery and reconciliation are more application-specific. |
| Migration | Can dual-publish/shadow-consume and cut over gradually. | Easier first integration, but later decoupling requires moving behavior out of the payment path. |
| Recommendation | **Preferred for review**, pending validation of existing event infrastructure and volume. | Viable fallback for low volume or when durable event transport is unavailable. |

## 6. Migration and rollback approach

Migration should be incremental and observable:

- Confirm terminal-state semantics, event availability, channel choice, data classification, and ownership.
- Define and version the minimal event contract and idempotency behavior.
- Deploy notification processing in disabled/shadow mode where feasible; measure event volume, duplicate rate, provider latency, and payload redaction.
- Enable a controlled cohort or feature flag, then expand after the p95 target and duplicate-suppression acceptance criteria are demonstrated.
- Retain reconciliation between terminal payment states and notification records for the agreed migration window.

Rollback should disable notification creation for the new path while preserving payment processing, stop or quarantine new consumers, and retain unprocessed events for controlled replay. A rollback must not delete idempotency records or discard the dead-letter queue. If dual-publishing is used, disable the new publication/consumer path independently to avoid duplicate customer notifications.

## 7. Delivery boundaries

The HLD does not prescribe detailed implementation. A subsequent approved LLD should define event schema/versioning, storage consistency, provider/channel contracts, retry classes, retention, SLO measurement, access controls, and test strategy. Implementation remains blocked until human architecture approval.

## 8. Proposed decision

Adopt Option 1 as the working direction for review because it best satisfies durable retry, duplicate handling, burst tolerance, and independent scaling without coupling customer delivery latency to the payment transaction path. This is a recommendation only. The Solution Architect owns the decision and may select Option 2 or request changes.

## Open questions

1. Which notification channels are enabled for the first release, and what does “available to the customer” mean for each channel?
2. What is the authoritative source and exact event contract for `completed` and `failed` terminal states?
3. Are terminal states immutable, and can a payment transition between terminal states?
4. What are expected steady-state rate, peak burst, ordering, and regional distribution?
5. Does an approved enterprise event bus, queue, notification provider, or idempotency store already exist?
6. What retention, residency, deletion, and customer preference rules apply?
7. Who owns the event producer, consumer, provider integration, dead-letter queue, and reconciliation process?
8. What existing payment and notification repository interfaces can be used, and what compatibility constraints apply?
9. What availability target applies to the notification service and provider, beyond the stated p95 latency target?
10. What operational evidence is required before expanding from pilot to full traffic?

## Concise summary

This proposal recommends an event-driven, durable, idempotent notification pipeline between payment status processing and customer notification delivery. It excludes sensitive payment data, isolates retries and provider failures from the payment path, and supports gradual migration and replay. The recommendation is not approved; it requires Solution Architect review, resolution of the open questions, and a later LLD before implementation.
