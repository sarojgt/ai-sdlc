# Option 1 — Governed durable event boundary

**Status:** Strategic working direction; not approved.

The authoritative BL2 or Lume producer emits a minimal, schema-versioned,
allow-listed status event to the enterprise Kafka/MSK pattern after the source
state is durably accepted. The shared Webhook Platform consumes the event and
owns subscription lifecycle, tenant routing, signing, HTTPS delivery,
timeouts, bounded retries, DLQ, delivery history, and authorized replay.

## Trade-offs

- Security: strong CHD-to-CW sanitization and least-privilege topic ACLs, but
  topic, replay, DLQ, and telemetry access become governed security surfaces.
- Performance/scalability: asynchronous buffering isolates the transaction path
  and lets consumers and delivery workers scale independently; partitioning,
  ordering, queue age, and client quotas need capacity evidence.
- Cost: maximizes reuse and reduces bespoke operations, with variable event,
  retention, delivery-history, DLQ, and telemetry cost.
- Operations: platform-standard lag, delivery outcome, retry, replay, and
  reconciliation signals; producer and platform ownership must be explicit.
- Migration: one contract serves Lume and BL2 cohorts and supports shadow and
  cohort rollout. If source publication is not atomic, an approved outbox may
  still be needed behind this option.

## Select when

Use when direct governed publication, schema/ACL onboarding, regional routing,
quotas, signing, and platform SLOs are confirmed. This is the target for Lume
and any BL2 cohort that supports the same durable contract.
