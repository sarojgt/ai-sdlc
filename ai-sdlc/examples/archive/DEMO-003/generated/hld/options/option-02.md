# Option 02 — Synchronous handoff with durable recovery

## Concept and flow

When `payment-service` accepts a status transition, it calls a
`partner-webhook-service` orchestration endpoint. The service durably records
the event and delivery intent keyed by `(partner_id,event_id)` before invoking
the partner. The partner receives the same `event_id` and
`X-Payment-Event-Id` on the initial call and every retry/replay. A recovery job
finds incomplete deliveries and applies bounded retry or dead-letter handling.

Payment acceptance must never be reversed because webhook delivery fails.

## Strengths

- Smaller initial topology where no approved event transport exists.
- Lower fixed platform cost at very low volume and fan-out.
- Direct handoff may be simple to integrate initially.

## Trade-offs

- Partner timeout, throttling, or outage couples to the payment request path.
- Tail latency and burst handling are weaker and may threaten the five-minute
  acceptance target.
- Recovery, reconciliation, and duplicate prevention carry more operational
  responsibility.
- Growth toward high fan-out likely requires later asynchronous migration.

## Required safeguards

Use a short timeout, circuit breaker, durable pre-send state, explicit pending
state, bounded retry, reconciliation, and a DLQ equivalent. Preserve the same
stable partner-visible identity across retries, authorized replay, and any
coexistence period. Do not allow the synchronous call to make payment-state
acceptance depend on partner success.

## Suitability

Fallback for measured low volume, limited fan-out, and an unavailable or
disallowed durable transport. It requires Solution Architect acceptance of
payment-path coupling and evidence that availability and latency remain safe.
