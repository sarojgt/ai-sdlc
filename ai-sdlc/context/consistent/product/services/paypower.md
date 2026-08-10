---
context_id: service-paypower
context_type: consistent
authority: service-catalog-and-repository-discovery
status: imported-snapshot
owner: banking-live-authorization-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7400423715/Teams+vs+BL+Services
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/9493741661/Analysis+of+PayPower+Changes+to+Support+Client-Specific+Segregated+Database+Connections
  - https://github.com/Paymentology/paypower
retrieved: 2026-08-10
repository_commit: 2e89209
scan_scope: readme-build-source-database-deployment-observability
---

# PayPower

## Service role

Banking.Live authorization and core processing component. The Confluence
catalogue assigns it to the Authorizations team.

## Business capability

PayPower evaluates and processes authorization-related transaction decisions
for Banking.Live. It is a high-throughput, client/tenant-sensitive boundary
that may invoke rules, decisioning, card/token data, queues, and operational
logging. Changes must preserve authorization outcomes, isolation, and recovery.

For rules and decisioning, PayPower is the transaction-time evaluation and
authorization-check consumer. Rule changes therefore require analysis of
PayCore definitions/procedures, PayAPI actions, PayControl setup, evaluation
ordering, cache/version refresh, and transaction performance.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/paypower](https://github.com/Paymentology/paypower) | confirmed | Primary service repository |

## Dependencies and boundaries

- Uses client-specific data-source and tenant-routing concerns.
- Rule Engine and Decision Engine integration points exist and must be
  distinguished from PayPower-owned authorization behavior.
- Each queue may map to a client-specific PayLog database; confirm current
  runtime configuration before relying on this behavior.

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | Java 21; Maven `uber-jar`; Kubernetes Helm deployment |
| Data stores | PostgreSQL databases: PayCore, PayLog, and PayTok |
| Database connectivity/pool | Helm configuration documents per-database SSL and connection settings including maximum connections; confirm effective Hikari values per environment |
| Communication | Application/API endpoints plus queue-based processing; exact TCP/socket use is not confirmed |
| Internal dependencies | PayCore, PayTok, PayLog, Rule Engine, Decision Engine, and shared platform services |
| External dependencies | Scheme/partner integrations are feature-specific and require discovery |
| Security/observability | SSL database connections, NetworkPolicy, pod security, Datadog tracing/metrics/logs, and health probes |

## Deployment context

Part of the Banking.Live estate and local Dockerized environment. Confirm the
BL2 or Lume deployment and client isolation model for each initiative.

## HLD implications

Cover authorization flow, client routing, database isolation, queue behavior,
  logging, and operational recovery.

## Scan-confirmed delivery profile

The repository and chart confirm Java 21, Helm deployment, PayCore/PayTok/PayLog
database configuration, SSL, connection limits, NetworkPolicy, pod security,
health probes, and Datadog telemetry. Queue/topic and partner details remain
flow-specific.

## Scan-confirmed implementation anchors

- Repository areas include transaction, card, account, product, tokenization,
  client, fee, reversal, SCA, dynamic-block, and PayLog data-access paths.
- PayPower commonly combines authorization orchestration with database-backed
  validation and downstream decisioning; a feature should identify whether it
  changes the transaction path, an asynchronous queue, or a supporting lookup.
- The repository contains Decision Engine OpenAPI schema material and a
  PayRoute certificate asset, so decisioning and network-routing changes need
  separate contract and certificate-rotation analysis.

These anchors are from commit `2e89209`. Exact queue names, transaction stages,
and partner protocols must still be confirmed from the affected flow.

## Context gaps

- Confirm current rule/decision engine versions and integration contracts.
- Confirm current deployment manifests and regional topology.
- Confirm queue/topic names, HTTP ports, pool timeouts, transaction boundaries,
  and external partner protocols from configuration and runtime evidence.
