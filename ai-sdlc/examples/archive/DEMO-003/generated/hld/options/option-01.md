# Option 01 — Durable asynchronous webhook pipeline

## Concept and flow

After an accepted payment-status transition, `payment-service` publishes a
minimal durable event (or equivalent outbox record). `partner-webhook-service`
resolves enabled partners, creates a delivery intent keyed by
`(partner_id,event_id)`, and sends the webhook through workers. Delayed retry
and dead-letter facilities handle failure; operations can perform audited
replay.

The partner receives `event_id` in the envelope and `X-Payment-Event-Id` in the
header. This is the identity of the accepted transition, not an attempt. It is
unchanged across every retry, authorized replay, and migration coexistence
path. Each HTTP attempt has a separate internal attempt ID.

## Strengths

- Isolates payment processing from partner latency and outages.
- Buffers bursts and permits independent worker scaling and partner throttling.
- Makes queue age, attempts, state, DLQ, and replay outcomes observable.
- Supports cohort rollout and reconciliation without changing event identity.

## Trade-offs

- More components and persistent data to secure, operate, retain, and pay for.
- At-least-once processing still requires partner deduplication and race-tested
  uniqueness at `(partner_id,event_id)`.
- Ordering, fan-out, backpressure, and replay authorization need explicit
  design.

## High-level safeguards

Allow-list the payload, validate the identity, redact all secret-bearing data,
use approved signing with secret references, encrypt transport/storage, and
apply least privilege. Use bounded timeout/backoff with jitter, retry
classification, circuit breaking, and per-partner concurrency/rate limits.

## Suitability

Preferred working direction if the estate can support durable transport and
state. Confirm event semantics, identity composition, traffic, platform,
retention, and ownership before LLD. This option is not implementation
authorization.
