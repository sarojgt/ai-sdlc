---
context_id: service-paytokdb
context_type: consistent
authority: service-catalog-and-repository-discovery
status: imported-snapshot
owner: banking-live-data-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7400423715/Teams+vs+BL+Services
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/8452800578/BL+Accessing+Production+Databases
  - https://github.com/Paymentology/paytokdb
retrieved: 2026-08-10
---

# PayTok DB

## Service role

Banking.Live token-related database. The Confluence catalogue assigns it to
the Data team.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/paytokdb](https://github.com/Paymentology/paytokdb) | confirmed | Database schema and delivery repository |

## Dependencies and boundaries

- Apply tokenization, key ownership, access policy, retention, and residency
  rules before exposing or querying data.
- PayScheduler documents PayTok as one of the tenant-routed database types.
- Do not treat token data as ordinary application data.

## Deployment context

Confirm client/environment placement, regional residency, RDS topology, and
CHD/common-zone boundary for the affected workload.

## HLD implications

Cover token boundary, authorization, data classification, query/index impact,
retention, migration, and auditability.

## Context gaps

- Confirm the owning service and exact schema/table for each initiative.
