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
repository_commit: fc5ead8
scan_scope: readme-migrations-functions-deployment-data-model
---

# PayCore DB

## Service role

Core Banking.Live operational database. The Confluence catalogue assigns it to
the Data team and identifies PayCore as a tenant-routed database type.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/paycoredb](https://github.com/Paymentology/paycoredb) | confirmed | Database schema and delivery repository |

## Business capability

PayCore is the operational Banking.Live data boundary for core account,
product, card, transaction, limit, rule, and client/tenant processes. Database
changes support an existing domain capability; they must not introduce a
parallel source of truth without architecture approval.

## Dependencies and boundaries

- Treat schema and stored-procedure ownership as explicit design concerns.
- PayAPI and PayScheduler have documented historical coupling to PayCore.
- Client isolation, CHD classification, read/write ownership, and migration
  impact must be assessed for every change.

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | PostgreSQL schema delivery through Liquibase SQL-formatted changelogs |
| Data stores | PayCore PostgreSQL database with initialise, prepare, migrate, and replace stages |
| Database connectivity/pool | Client services own connection pools; database deployment uses Liquibase host/credential configuration |
| Communication | PostgreSQL/JDBC connections; callers and read/write paths must be identified per feature |
| Internal dependencies | PayAPI, PayPower, PayScheduler, and other BL services depending on the affected schema |
| External dependencies | RDS/Aurora or approved PostgreSQL placement is environment-specific |
| Security/observability | CHD/data isolation, least privilege, migration audit, backup/recovery, and database telemetry are required |

## Data model profile

This is a structural inventory, not a complete schema catalogue. Confirm the
current migration repository and runtime schema before designing a query or
change.

| Area | Confirmed context |
| --- | --- |
| Business data | Core banking operational data, including accounts, products, cards, transactions, limits, rules, and client/tenant configuration. |
| Representative objects | `t_txn_ext_rid` stores transaction-to-external-reference mapping; `p_account_balance_records` stores account balance record history; `ps_tasks_configurations` stores task configuration. These examples are not exhaustive. |
| Schema objects | Tables, sequences, indexes, views, triggers, PostgreSQL functions, and typed records are delivered through the staged Liquibase SQL tree. |
| Functions and procedures | Repository evidence includes card/product creation, rules, limits, reporting, authorization/session, currency, health, and operational helper functions. |
| Sensitive data | May include CHD, payment, account, customer, and security-related data. Do not copy columns, values, credentials, or secrets into this context. |
| Source of truth | The database repository changelog plus approved runtime/schema evidence; service documentation alone is insufficient for table selection. |

For card blocking specifically, repository evidence includes the
`T_BLOCKED_ENTITIES_TOKS` model, `f_act_BlockCard`,
`pws_get_card_block_expiry`, and `pws_set_card_block_expiry`. The model stores a
token reference, block-established time, expiry time, matching scope fields,
and precedence information. Confirm the active schema migration, access
wrapper, expiry processing, indexes, and tenant/client semantics before reuse.

For an initiative, record the exact table/view/function, access path, tenant
scope, indexes, and classification only after confirming them from the relevant
schema version and service owner.

For the Rules Engine capability, PayCore DB is the authoritative persistence
and procedure surface. PayControl configures rules, PayAPI exposes related
actions, and PayPower consumes the rules during transaction evaluation. Record
the exact rule family, function/procedure, versioning, and rollout behavior for
each change.

## Deployment context

PayCore is deployed per the Banking.Live client/environment model. Confirm RDS,
regional, dedicated/shared, and CHD/common-zone placement.

## HLD implications

Identify tables, query paths, indexes, ownership, migration/rollback,
replication/read strategy, and data-retention requirements.

## Context gaps

- Confirm the exact schema/table and current production topology from the
  repository or approved runtime evidence.
- Confirm the complete domain-to-table inventory and retention policy; the
  examples above are intentionally representative rather than exhaustive.
- Confirm card-state versus dynamically-blocked-entity ownership and the
  approved restoration/reconciliation mechanism.
