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
---

# PayPower

## Service role

Banking.Live authorization and core processing component. The Confluence
catalogue assigns it to the Authorizations team.

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

## Context gaps

- Confirm current rule/decision engine versions and integration contracts.
- Confirm current deployment manifests and regional topology.
- Confirm queue/topic names, HTTP ports, pool timeouts, transaction boundaries,
  and external partner protocols from configuration and runtime evidence.
