# HLD Risks and Mitigations

| ID | Risk | Impact | Mitigation / decision needed | Owner |
|---|---|---|---|---|
| R-01 | Event semantics or terminal-state authority are unclear. | Incorrect, missing, or repeated notifications. | Confirm source of truth, transition rules, event identity, ordering, and versioning before LLD. | Payment domain owner |
| R-02 | Sensitive payment data is copied into events, logs, DLQs, or provider payloads. | Security, compliance, and customer harm. | Use an allow-list contract, schema validation, redaction tests, least privilege, encryption, and audited replay access. | Security + service owners |
| R-03 | Duplicate events or concurrent consumers create multiple notifications. | Requirement failure and customer confusion. | Durable unique idempotency boundary; define conflict behavior and test retries, races, and replays. | Notification owner |
| R-04 | Provider throttling or outage breaches the 30-second p95 target. | Missed business outcome and support contacts. | Measure provider latency, isolate provider calls, use bounded retries, alert on queue age, and define fallback/channel policy. | Notification owner |
| R-05 | Queue backlog or burst volume is underestimated. | Latency breach or resource exhaustion. | Obtain rate/burst data, capacity-test consumers and transport, autoscale on age/rate, and define back-pressure. | Engineering owner |
| R-06 | Dead-letter/replay operations are undefined. | Permanent loss or duplicate delivery during recovery. | Define runbook, retention, authorization, replay filtering, audit trail, and reconciliation before production. | Operations owner |
| R-07 | Context pack lacks current-state contracts and runtime evidence. | Design assumptions may conflict with the estate. | Treat this HLD as conditional; validate repositories, interfaces, platform standards, and SLOs during architecture review. | Solution Architect |
| R-08 | Channel or preference rules are unresolved. | Notification is unavailable or sent through an unsuitable channel. | Resolve first-release channels, consent/preferences, delivery definition, and provider data handling. | Product + compliance |
| R-09 | Migration dual-publishing causes two customer notifications. | Customer confusion and acceptance failure. | Use one authoritative notification boundary, dedupe across paths, pilot with shadow mode, and make cutover reversible. | Delivery team |
| R-10 | Provider or regional dependency changes cost/residency profile. | Budget or regulatory variance. | Confirm region, retention, provider pricing, residency, and exit strategy before commitment. | Architecture + procurement |
