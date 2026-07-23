# Proposed ADR — Reliable payment webhook delivery

## Status

**Proposed; awaiting human Solution Architect decision.** This record does not
approve architecture or unlock implementation.

## Context

The approved requirement calls for delivery after accepted payment-status
transitions, safe idempotent retries, bounded backoff, a dead-letter path, and
visible delivery state. At least 99% of eligible downstream acceptances should
occur within five minutes. Available context has no current contracts, rates,
runtime topology, platform facts, or signing rules.

## Decision candidates

1. Durable asynchronous pipeline with transport, delivery state, workers,
   bounded retry, and DLQ.
2. Synchronous handoff to webhook orchestration with durable state and
   reconciliation/recovery.

## Proposed direction

Use Option 1 as the working HLD direction for review. It better isolates partner
behavior, absorbs bursts, scales independently, and provides explicit recovery.
Its additional infrastructure, data-governance, and operations cost must be
checked against the estate and measured volume.

## Identity guardrail

`event_id` is the identity of the accepted status transition and is sent in the
webhook envelope and `X-Payment-Event-Id` header. It is created/adopted once and
is unchanged for retries, authorized replays, and migration coexistence. The
delivery uniqueness boundary is `(partner_id,event_id)`; attempt IDs are
separate. The payment domain must confirm the exact immutable composition and
revision/version semantics before implementation.

## Consequences

Positive: payment processing is less coupled to partners; state, retries, DLQ,
replay, and partner throttling are explicit; cohort migration is feasible.

Negative: transport, persistence, replay, and monitoring need ownership;
durable payloads add security and retention surfaces; managed services add cost.

## Guardrails and revisit triggers

- Exclude credentials, PAN/CVV, authentication secrets, and equivalent
  sensitive authentication data from payloads and evidence.
- Keep payment state authoritative; webhook failure must not change it.
- Bound retry count/backoff and DLQ retention; audit replay and operator access.
- Revisit if no approved durable platform exists, measurements invalidate the
  target, identity semantics differ, or security/residency/cost constraints
  materially change the ranking.
- LLD, implementation, merge, and deployment remain gated on approval.

## Open questions

- What exact event/version composition is authoritative for `event_id`?
- Which partner signing/authentication standard and key lifecycle are required?
- What are volume, fan-out, endpoint SLA, retention, residency, and cost limits?
- Who owns workers, registry, DLQ/replay, reconciliation, and support?
