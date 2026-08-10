---
context_id: service-payscheduler
context_type: consistent
authority: service-catalog-and-repository-discovery
status: imported-snapshot
owner: banking-live-clearing-and-reporting-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7400423715/Teams+vs+BL+Services
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/10010918939/PECA-1056+-+Migrate+PayAPI+PayScheduler+Integration+from+DB+Socket+to+REST+API
  - https://github.com/Paymentology/payscheduler
retrieved: 2026-08-10
repository_commit: 95e7ff4
scan_scope: readme-build-source-jobs-database-deployment
---

# PayScheduler

## Service role

Banking.Live scheduling, jobs, and reporting support. The Confluence catalogue
assigns it to Clearing & Reporting.

## Business capability

PayScheduler runs time-based Banking.Live work such as clearing, reporting,
maintenance, and integration jobs. It owns scheduling and job execution while
business data remains owned by the relevant domain or database service. A
report initiative must identify both job owner and source-data owner.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/payscheduler](https://github.com/Paymentology/payscheduler) | confirmed | Primary service repository |

## Dependencies and boundaries

- Owns scheduler lifecycle and Quartz-related operations.
- The documented target integration is REST-based, with PayScheduler owning
  the transactional database and scheduling operation.
- Tenant routing uses client context and applies to PayCore, PayTok, and
  PayLog database types.

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | Java service; Maven `uber-jar`; Helm chart includes service and scheduler ports |
| Data stores | PayCore, PayTok, and PayLog tenant-routed database types; scheduler/job tables are service-owned in the target flow |
| Database connectivity/pool | Database routing uses tenant/client context; pool values require current chart/config discovery |
| Communication | REST APIs on the target PayAPI integration; Quartz scheduling; historical TCP daemon socket path is legacy |
| Internal dependencies | PayAPI, Quartz, database consumers, and client-context/IAM routing |
| External dependencies | SFTP/file destinations may be job-specific; confirm per task type |
| Security/observability | Basic Auth is documented for PayAPI REST integration; secrets, certificates, probes, and scheduler metrics require confirmation |

## Confirmed scheduling capability

Quartz and the PayAPI REST migration are confirmed platform patterns. The
repository context does not yet prove that PayScheduler owns card-block expiry
or another particular delayed-job flow. Treat expiry, retry, concurrency,
reconciliation, and job persistence as discovery items rather than assuming a
new scheduler is required.

## Deployment context

Runs in the Banking.Live estate and has a Lume/Kubernetes service shape. Confirm
the active runtime and job execution boundary before design approval.

## HLD implications

Cover scheduling ownership, tenant routing, database writes, job idempotency,
  failure recovery, and operational visibility.

## Scan-confirmed delivery profile

The repository contains Quartz/job configuration, report templates, REST
integration support, database routing, and a Helm workload with configurable
storage. The historical socket path is not a default for new work.

## Scan-confirmed implementation anchors

- The repository exposes versioned OpenAPI job and job-chain contracts,
  including job creation and job history paths.
- It contains job families for settlement, chargeback, presentment, cardholder
  reports, billing, SMS, file processing, throttling, and triggered-rule
  reports.
- Job changes should define schedule ownership, tenant/client scope, locking or
  concurrency behavior, retry/backlog handling, idempotency, and report/file
  delivery. Reuse an existing job family when it fits.

These anchors are from commit `95e7ff4`; the exact job, persistence, and
delivery contract must be selected from the requested capability.

## Context gaps

- Confirm current REST contract and deployment manifest.
- Confirm whether a feature changes scheduler ownership or only its API client.
- Confirm REST ports, pool/transaction settings, queue or consumer behavior,
  job persistence, and any SFTP or external delivery protocol.
- Confirm whether an existing job can execute card-state expiry and identify
  its owner, schedule, idempotency, backlog alert, and recovery behavior.
