# Option 02 — Synchronous notification orchestration

## Concept

When `payment-service` records a terminal state, it synchronously calls an orchestration endpoint in `notification-service`. The orchestration service applies idempotency and invokes the selected notification channel/provider. A limited retry or reconciliation mechanism handles provider failures.

## High-level flow

Payment state transition → synchronous call to notification orchestration → idempotency/notification record → channel adapter/provider → response to payment service.

## Trade-offs

- Lower initial topology and potentially lower fixed infrastructure cost for small volumes.
- Straightforward initial integration if no durable event transport exists.
- Couples payment-path availability and tail latency to notification service and provider behavior; timeouts and partial failures require careful handling.
- Burst handling and retry isolation are weaker unless additional asynchronous buffering is later introduced.
- Operational recovery is more dependent on reconciliation jobs and request logs, increasing the risk of missed or duplicate customer notifications.
- Migration is quick for a first release but creates future decoupling work if volumes, channels, or provider count increase.

## Required safeguards

- Strict timeout and circuit-breaker behavior so customer notification cannot block or reverse payment state processing.
- Durable idempotency before provider invocation.
- Reconciliation from authoritative payment terminal states.
- A path to asynchronous retry that does not reintroduce duplicate notifications.

## Suitability

Viable fallback when measured volume is low, an approved durable event platform is unavailable, and the payment team accepts the coupling. It requires stronger evidence that provider latency and failures will not compromise the 30-second target or payment-path availability.
