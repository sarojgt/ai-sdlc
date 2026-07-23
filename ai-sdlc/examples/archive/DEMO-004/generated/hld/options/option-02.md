# Option 2 — BL2 transactional outbox or durable-journal adapter

**Status:** Compatibility option; not approved.

Where BL2 cannot publish directly, the source transaction writes a minimal
outbox record atomically, or an existing approved durable status journal is
consumed. A controlled adapter reads the record, sanitizes it at the CHD/CW
boundary, and hands it to the same shared Webhook Platform. The adapter never
calls client endpoints directly.

## Trade-offs

- Security: limits immediate event-platform coupling, but expands source-data
  access and makes outbox/journal classification, credentials, redaction,
  backups, and checkpoint protection critical.
- Performance/scalability: polling or journal consumption adds lag and source
  database load; reader scaling, indexes, checkpoints, and shared BL2 noisy
  neighbors constrain throughput.
- Cost: may lower initial integration cost, but adds bespoke runtime,
  database capacity, checkpointing, reconciliation, support, and retirement
  cost.
- Operations: requires adapter health, lag, checkpoint, schema-drift, source
  database, DLQ, replay, and reconciliation runbooks in addition to platform
  operations.
- Migration: enables a bounded BL2 cohort while Lume uses Option 1, but creates
  a second migration and a duplicate-send risk unless `event_id` is shared.

## Select only when

An approved durable source handoff and defined BL2 capability gap are evidenced.
The HLD/LLD must name the owner, cohort, source access, retention, recovery
policy, retirement milestone, and convergence path. It is not the default for
new Lume capability.
