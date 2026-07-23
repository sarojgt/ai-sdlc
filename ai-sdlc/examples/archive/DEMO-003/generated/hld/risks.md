# HLD Risks and Mitigations

| ID | Risk | Impact | Mitigation / decision needed | Owner |
|---|---|---|---|---|
| R-01 | Accepted-transition source, ordering, or `event_id` composition is unknown. | Missing, reordered, or incorrectly deduplicated deliveries. | Confirm immutable transition identity, version semantics, ordering, and replay rules before LLD. | Payment domain owner |
| R-02 | Credentials or sensitive authentication data enter payloads, logs, DLQs, or traces. | Security/compliance exposure. | Allow-list schema, validation, redaction tests, encryption, least privilege, and audited access. | Security + service owners |
| R-03 | Retry, replay, or migration paths use different identities or race. | Duplicate partner effects or missed effects. | Use partner-visible `event_id` and `X-Payment-Event-Id`; enforce `(partner_id,event_id)` uniqueness across all paths; race-test. | Webhook owner |
| R-04 | Partner outage, throttling, or slow responses breach five minutes. | Delayed deliveries and SLO breach. | Measure latency, cap attempts, use backoff/jitter, isolate partners, and alert on queue age. | Webhook owner |
| R-05 | Traffic, fan-out, or burst volume is underestimated. | Backlog, exhaustion, and capacity failure. | Obtain rate data, capacity-test, autoscale workers, and define backpressure. | Engineering owner |
| R-06 | Signing/authentication standard and key lifecycle are unresolved. | Rejected requests or secret leakage. | Select approved standard, storage, rotation, clock-skew, and failure policy before implementation. | Security + partner owner |
| R-07 | DLQ retention and recovery are undefined. | Permanent loss or unsafe replay. | Define retention, authorization, filtering, audit, reconciliation, and runbook. | Operations owner |
| R-08 | Context pack has no current APIs, runtime evidence, or repository links. | HLD may conflict with the estate. | Treat all interfaces and platform choices as conditional; validate at human review. | Solution Architect |
| R-09 | Delivery history or endpoint configuration has unsuitable residency/retention. | Governance and cost variance. | Confirm classification, residency, deletion, access audit, and cost model. | Architecture + compliance |
| R-10 | Existing sender is not identified during migration. | Double sends or missed events. | Inventory current path, select one authoritative sender, share identity/dedup boundary, and use safe cohorts. | Delivery team |
