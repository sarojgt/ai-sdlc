# Option 01 — Durable event-driven notification pipeline

## Concept

`payment-service` publishes a minimal terminal-status event to a durable event transport. `notification-service` consumes it, performs validation and duplicate suppression, persists notification intent, and invokes the selected channel/provider adapter. Retries and poison messages are isolated through retry queues and a dead-letter queue.

## High-level flow

Payment state transition → durable event publication → transport → notification consumer → idempotency/notification record → channel adapter/provider → customer-visible notification.

## Key characteristics

- At-least-once delivery is expected; exactly-once customer outcome is achieved at the notification boundary through durable idempotency.
- A minimal allow-listed event avoids credentials and sensitive authentication data.
- Stateless consumers can scale separately from payment processing.
- Queue age, end-to-end p95 latency, duplicate suppression, retry count, dead-letter count, and provider outcomes are observable.

## Trade-offs

- Strongest fit for the 30-second target under bursts because payment processing is decoupled from provider latency.
- More operational components: transport, retry/dead-letter handling, idempotency persistence, replay, and reconciliation.
- Requires careful access control and redaction for durable events, dead letters, logs, and replay tooling.
- Managed infrastructure may cost more at very low volume, but the option reduces coupling and likely operational risk as volume grows.
- Migration can use shadow consumption, cohort enablement, and controlled replay.

## Major decisions still required

- Existing enterprise transport and persistence choices.
- Event ordering and terminal-state transition semantics.
- Channel/provider contract and delivery definition.
- Retention, residency, deletion, and replay policy.

## Suitability

Preferred working direction, pending Solution Architect approval and validation of the current estate. It is not an implementation authorization.
