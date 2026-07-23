# Proposed ADR — Payment terminal status notification integration

## Status

**Proposed — awaiting human Solution Architect decision.** This ADR records a decision candidate and does not approve architecture.

## Context

Customers need a consistent notification within 30 seconds of a payment entering `completed` or `failed`. Duplicate terminal events must result in one customer notification. The requirement prohibits payment credentials and sensitive authentication data in the notification path. Available context identifies `payment-service` and `notification-service`, but does not provide current event contracts, platform choices, volumes, channels, or runtime evidence.

## Options considered

1. **Durable event-driven pipeline:** publish a minimal terminal event, consume asynchronously, persist idempotency/notification intent, and deliver through a channel adapter.
2. **Synchronous notification orchestration:** call notification orchestration from payment processing, with durable idempotency and reconciliation.

## Proposed decision

Use the durable event-driven pipeline as the working architecture direction for HLD review. It provides better retry isolation, burst tolerance, independent scaling, and a safer path to gradual migration. It carries additional transport, dead-letter, replay, and operational cost that must be validated against the existing platform estate and expected volume.

## Consequences

Positive:

- Payment processing is less coupled to provider latency and outages.
- At-least-once delivery plus a durable idempotency boundary supports the duplicate-event requirement.
- Consumers, retries, and provider integration can scale and evolve independently.
- Shadowing, cohort rollout, replay, and reconciliation support a controlled migration.

Negative:

- Operators must manage queue lag, retries, dead letters, replay permissions, and retention.
- Durable payloads create additional security and data-governance surfaces.
- Managed transport and persistence add cost and platform dependencies.

## Constraints and guardrails

- No credentials, PAN, CVV, authentication secrets, or equivalent sensitive authentication data in events, stores, logs, traces, DLQs, or provider requests.
- Notification creation must be idempotent for the confirmed business key.
- Payment state remains authoritative; notification failure must not change payment state.
- Implementation, LLD, merge, and deployment remain blocked until human architecture approval.

## Revisit triggers

- Existing platform standards disallow or materially constrain the proposed transport.
- Measured volume or provider behavior makes the 30-second p95 target unattainable.
- Domain confirms terminal-state transitions that require a different idempotency key or ordering model.
- Compliance, residency, channel, or cost constraints change the option ranking.

## Open questions

- What is the authoritative event contract and payment-state lifecycle?
- Which channel/provider and customer preference rules apply to release one?
- What are the volume, burst, region, retention, availability, and cost constraints?
- Which team owns transport, consumer, provider, replay, and reconciliation operations?
