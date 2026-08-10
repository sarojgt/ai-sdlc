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
---

# PayScheduler

## Service role

Banking.Live scheduling, jobs, and reporting support. The Confluence catalogue
assigns it to Clearing & Reporting.

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

## Deployment context

Runs in the Banking.Live estate and has a Lume/Kubernetes service shape. Confirm
the active runtime and job execution boundary before design approval.

## HLD implications

Cover scheduling ownership, tenant routing, database writes, job idempotency,
failure recovery, and operational visibility.

## Context gaps

- Confirm current REST contract and deployment manifest.
- Confirm whether a feature changes scheduler ownership or only its API client.
