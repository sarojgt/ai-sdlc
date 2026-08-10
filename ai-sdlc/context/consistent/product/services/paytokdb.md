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

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | PostgreSQL schema delivery through Liquibase SQL-formatted changelogs |
| Data stores | PayTok PostgreSQL database with staged schema migration |
| Database connectivity/pool | Client services own pools; exact pool and timeout values require caller configuration |
| Communication | PostgreSQL/JDBC connections; token service and caller paths require discovery |
| Internal dependencies | PayPower, PayAPI, PayScheduler, tokenization services, and PayKey-related controls as applicable |
| External dependencies | Token partners or networks are feature-specific |
| Security/observability | Token handling, encryption, residency, retention, access audit, and secure logging are mandatory |

## Data model profile

This is a safe structural summary. It must not be used as a substitute for
reviewing the current PayTok migrations before selecting a table or field.

| Area | Confirmed context |
| --- | --- |
| Business data | Tokenization and card/token lifecycle data, card and account processing support data, product/configuration data, delivery/personalisation data, and token-related operational records. |
| Representative objects | Repository functions reference card creation, card files, card status, token/account generation, product data, delivery-customer data, and reporting flows. Exact table ownership must be confirmed from the migration files. |
| Schema objects | PostgreSQL tables, sequences, composite types, functions, and staged Liquibase SQL changelogs. |
| Sensitive data | Token, encrypted payment, key-reference, customer, and card-related data may be present. Do not place PAN, secrets, token values, cryptographic material, or production examples in context documents. |
| Source of truth | `Paymentology/paytokdb` migrations and approved tokenization/security evidence. Service names or function names alone do not prove a safe query path. |

For an initiative, identify the exact table/view/function, token boundary,
tenant scope, indexes, retention, and authorization path from the approved
schema and service owner.

## Deployment context

Confirm client/environment placement, regional residency, RDS topology, and
CHD/common-zone boundary for the affected workload.

## HLD implications

Cover token boundary, authorization, data classification, query/index impact,
retention, migration, and auditability.

## Context gaps

- Confirm the owning service and exact schema/table for each initiative.
- Confirm the complete domain-to-table inventory and retention/residency policy;
  this page intentionally provides categories rather than a sensitive schema
  dump.
