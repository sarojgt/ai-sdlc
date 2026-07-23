# HLD risks, assumptions, and mitigations

| ID | Risk / uncertainty | Impact | Mitigation / review gate | Owner |
|---|---|---|---|---|
| R-01 | Authoritative producer and eligible statuses are unknown | Missing or incorrect events | Map ownership, ordering, correction, and identity before LLD | BL domain |
| R-02 | CHD/CW classification and network direction are not initiative-evidenced | PCI/security breach or rejected design | Classify source, event, stores, backups, DLQ, logs, and traces; security review unknowns | Security/platform |
| R-03 | Client/region context could be spoofed or lost | Cross-client delivery | Derive from trusted source; enforce IMS policy; fail closed; test isolation | Identity/BL |
| R-04 | Auth0 route, audience/scopes, M2M identity, and IMS grants are unknown | Unauthorized subscription changes | Confirm Gateway/Auth0/IMS contract, audit, cache, rate limits, and regional resolution | Identity/platform |
| R-05 | Stable event identity and correction semantics are undefined | Duplicate or stale client effects | Domain-approve immutable `event_id`, separate attempt ID, and reconciliation rules | BL domain |
| R-06 | Event/Webhook ingress, quotas, retry, replay, and SLOs are unknown | Backlog or missed near-real-time expectation | Obtain platform contract and capacity-test peak rate/fan-out | Platform engineering |
| R-07 | Signing and key lifecycle are unknown | Impersonation or rejected delivery | Confirm approved signing/mTLS standard, storage, rotation, revocation, and audit | Webhook Platform |
| R-08 | BL2/Lume environment, region, tier, and shared/dedicated model are unknown | Wrong deployment or migration path | Inventory current catalog, versions, cloud, repositories, and cohort owners | BL migration |
| R-09 | Option 2 adapter becomes permanent | Duplicate logic and lifecycle cost | Time-box with owner, cohort, retirement signal, and convergence milestone | Solution Architect |
| R-10 | Retention, residency, deletion, and telemetry policy are unknown | Compliance, cost, or unrecoverable incidents | Set event/history/DLQ/replay/telemetry policy before production | Compliance/platform |
| R-11 | No repository/runtime/incident/dashboard/runbook evidence is supplied | Invalid capacity and operability assumptions | Treat HLD as conditional; complete discovery and operational readiness review | Initiative owner |
