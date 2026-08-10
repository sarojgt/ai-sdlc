---
context_id: service-paykeyservice
context_type: consistent
authority: service-catalog-and-repository-discovery
status: imported-snapshot
owner: banking-live-cryptography-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7400423715/Teams+vs+BL+Services
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/6762659879/Banking+Live+dockerized+environment
  - https://github.com/Paymentology/paykeyserv
  - https://github.com/Paymentology/paykeydb
retrieved: 2026-08-10
---

# PayKeyService / PayKeyServ

## Service role

Banking.Live key and cryptographic-support service. The service catalogue uses
both PayKeyService and PayKeyServ naming.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/paykeyserv](https://github.com/Paymentology/paykeyserv) | confirmed | Key-service repository |
| [Paymentology/paykeydb](https://github.com/Paymentology/paykeydb) | confirmed | Key-service database repository |

## Dependencies and boundaries

- Treat key material, certificates, and cryptographic operations as highly
  sensitive.
- Apply mTLS, Zero Touch PKI, secrets, and access-control guardrails.
- Never place key material, secrets, or production credentials in AI context.

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | Java service; Maven `uber-jar`; API specification is under `docs/asciidoc` |
| Data stores | PayCore, PayKey, and PayLog PostgreSQL datasources are documented |
| Database connectivity/pool | HikariCP is documented with per-datasource min-idle, max-connections, timeout, keepalive, idle-timeout, and max-lifetime settings |
| Communication | Service API is documented; exact HTTP/TCP/socket contract requires API source confirmation |
| Internal dependencies | PayCore, PayKey DB, PayLog, certificates, and cryptographic consumers |
| External dependencies | No external partner endpoint confirmed |
| Security/observability | Encrypted connections, certificate/PKI controls, and audit logging are mandatory; never expose key values |

## Deployment context

The Dockerized environment exposes PayKeyServ as a separate service and PayKey
DB as a separate database. Confirm production zone and deployment ownership.

## HLD implications

Identify key custody, trust boundaries, certificate lifecycle, access paths,
availability, rotation, and audit evidence.

## Context gaps

- Confirm the canonical service and database names in the target platform.
- Confirm whether `paykeygui` is in scope for the initiative.
