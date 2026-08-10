---
context_id: service-paycoredb
context_type: consistent
authority: service-catalog-and-repository-discovery
status: imported-snapshot
owner: banking-live-data-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7400423715/Teams+vs+BL+Services
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/8452800578/BL+Accessing+Production+Databases
  - https://github.com/Paymentology/paycoredb
retrieved: 2026-08-10
---

# PayCore DB

## Service role

Core Banking.Live operational database. The Confluence catalogue assigns it to
the Data team and identifies PayCore as a tenant-routed database type.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/paycoredb](https://github.com/Paymentology/paycoredb) | confirmed | Database schema and delivery repository |

## Dependencies and boundaries

- Treat schema and stored-procedure ownership as explicit design concerns.
- PayAPI and PayScheduler have documented historical coupling to PayCore.
- Client isolation, CHD classification, read/write ownership, and migration
  impact must be assessed for every change.

## Deployment context

PayCore is deployed per the Banking.Live client/environment model. Confirm RDS,
regional, dedicated/shared, and CHD/common-zone placement.

## HLD implications

Identify tables, query paths, indexes, ownership, migration/rollback,
replication/read strategy, and data-retention requirements.

## Context gaps

- Confirm the exact schema/table and current production topology from the
  repository or approved runtime evidence.
