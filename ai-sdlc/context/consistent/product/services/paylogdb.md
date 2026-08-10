---
context_id: service-paylogdb
context_type: consistent
authority: service-catalog-and-repository-discovery
status: imported-snapshot
owner: banking-live-data-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7400423715/Teams+vs+BL+Services
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/10010918939/PECA-1056+-+Migrate+PayAPI+PayScheduler+Integration+from+DB+Socket+to+REST+API
  - https://github.com/Paymentology/paylogdb
retrieved: 2026-08-10
---

# PayLog DB

## Service role

Banking.Live operational/log-supporting database. The Confluence catalogue
assigns it to the Data team.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/paylogdb](https://github.com/Paymentology/paylogdb) | confirmed | Database schema and delivery repository |

## Dependencies and boundaries

- PayScheduler documents PayLog as a tenant-routed database type.
- PayPower analysis indicates client-specific queue/database relationships.
- Assess whether new data belongs here or in the centralized observability
  platform; do not use PayLog as a default telemetry store.

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | PostgreSQL schema delivery through Liquibase; repository notes RDS compatibility testing |
| Data stores | PayLog PostgreSQL database |
| Database connectivity/pool | Client services own pools; exact values require caller and environment configuration |
| Communication | PostgreSQL/JDBC connections and queue-driven service flows where configured |
| Internal dependencies | PayPower and PayScheduler are documented consumers; other callers require repository discovery |
| External dependencies | No external endpoint confirmed |
| Security/observability | Retention, sensitive-data filtering, tenant isolation, database audit, and centralized observability boundaries are required |

## Data model profile

PayLog is treated as an operational logging/supporting store. The following is
the repository-backed shape, not a complete production data dictionary.

| Area | Confirmed context |
| --- | --- |
| Business data | Application/API traces, errors, diagnostic records, PayKey and PayPower traces, timing/support records, and operational lookup data. |
| Representative objects | `debug_log`, `log_payapi_error`, `log_payapi_trace`, and PayKey error/trace families are present in the initial migration. |
| Schema objects | PostgreSQL tables, sequences, composite types, functions, and staged Liquibase SQL changelogs. |
| Sensitive data | Logs can contain request identifiers, client identifiers, stack traces, and message details. Treat payloads as potentially sensitive and redact by policy. |
| Source of truth | `Paymentology/paylogdb` migrations, service logging configuration, and approved retention/observability policy. |

For an initiative, confirm the exact log family, write path, retention/partition
strategy, tenant scope, redaction rules, indexes, and whether the data belongs
in PayLog or the central observability platform.

## Deployment context

Confirm client/environment placement, retention, regional residency, and
sensitive-data boundary.

## HLD implications

State data purpose, classification, retention, query ownership, access path,
observability relationship, and migration impact.

## Context gaps

- Confirm the current schema and whether the database remains the correct home
  for the proposed data.
- Confirm the complete table/retention inventory and production partitioning;
  this page intentionally avoids copying operational log payloads.
