---
context_id: service-paykeydb
context_type: consistent
authority: service-catalog-and-repository-discovery
status: imported-snapshot
owner: banking-live-data-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7400423715/Teams+vs+BL+Services
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/8452800578/BL+Accessing+Production+Databases
  - https://github.com/Paymentology/paykeydb
retrieved: 2026-08-10
repository_commit: 5c86b3e
scan_scope: readme-migrations-functions-deployment-data-model
---

# PayKey DB

## Service role

Database supporting PayKey cryptographic/key-management operations and related
configuration. It is separate from PayCore, PayTok, and PayLog and must be
treated as a security-sensitive data boundary.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/paykeydb](https://github.com/Paymentology/paykeydb) | confirmed | PayKey PostgreSQL schema and delivery repository |
| [Paymentology/paykeyserv](https://github.com/Paymentology/paykeyserv) | confirmed | Service and database-client integration |

## Business capability

PayKey DB supports key-service metadata, key lifecycle/configuration, and
security-operation records. It is a high-sensitivity security boundary and
must never become a source for exposing cryptographic material to application
or AI consumers.

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | PostgreSQL schema delivered through Liquibase SQL-formatted changelogs |
| Connectivity | PayKey service documents a dedicated PayKey datasource alongside PayCore and PayLog; pool settings belong to the service/environment configuration |
| Schema objects | Tables, sequences, composite types, functions, and staged migration/prepare SQL |
| Security | Cryptographic material, key references, access credentials, and audit data require strict classification, least privilege, encryption, and redaction |

## Data model profile

| Area | Confirmed context |
| --- | --- |
| Business data | Key metadata, key lifecycle/configuration, key-service users/authorisation data, and cryptographic operation support records |
| Representative objects | Repository types and functions expose key-list, key-template, key-user, authentication-code, and key-copy operations. The migration repository is the authority for exact tables and fields. |
| Sensitive data | Key values, encrypted material, authentication data, and security metadata may be present. Never copy production values or cryptographic material into AI context. |
| Source of truth | `Paymentology/paykeydb` migrations plus PayKey service configuration and approved security evidence |

For an initiative, confirm the exact object, access path, tenant/instance
scope, key hierarchy, audit requirement, retention, and security-owner approval.

## Scan-confirmed change anchors

- The database repository is delivered through staged Liquibase SQL containing
  schema objects, functions, key templates, key users, authentication-code,
  and key-copy operation support.
- PayKeyService is the expected access boundary; direct application access to
  PayKey DB requires explicit security and ownership justification.
- Changes require encryption, least privilege, audit, redaction, migration/
  rollback, backup/recovery, and regional placement analysis.

These anchors are from commit `5c86b3e`; exact objects and security controls
must be confirmed against the affected migration and environment.

## Deployment context

Confirm regional placement, dedicated/shared environment, CHD/common-zone
boundary, backup/recovery, and key-management controls before design approval.

## HLD implications

Identify the service boundary, authorization path, cryptographic trust boundary,
pool/availability impact, migration/rollback, audit events, and redaction rules.

## Context gaps

- Confirm the complete domain-to-table inventory and current production
  topology from the database repository and approved runtime evidence.
