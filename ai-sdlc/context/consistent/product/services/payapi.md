---
context_id: service-payapi
context_type: consistent
authority: service-catalog-and-repository-discovery
status: imported-snapshot
owner: banking-live-api-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7400423715/Teams+vs+BL+Services
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/10010918939/PECA-1056+-+Migrate+PayAPI+PayScheduler+Integration+from+DB+Socket+to+REST+API
  - https://github.com/Paymentology/payapi
retrieved: 2026-08-10
---

# PayAPI

## Service role

Banking.Live API/application boundary and integration surface. The service is
owned in the Confluence catalogue by Admin APIs & Portals.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/payapi](https://github.com/Paymentology/payapi) | confirmed | Primary service repository |

## Dependencies and boundaries

- Exposes and consumes approved APIs and platform integrations.
- Existing PayScheduler integration has been moving from direct PayCore writes
  and sockets to PayScheduler REST APIs.
- Reuse approved IMS/API Gateway, authentication, client-context, and
  observability patterns.

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | Java; Maven `uber-jar`; Kubernetes Helm chart |
| Data stores | PostgreSQL is supported by the chart; exact databases and schemas are feature-specific |
| Database connectivity/pool | Configuration is repository-managed; driver, pool, and timeout values require service configuration discovery |
| Communication | HTTP/API surface; PayScheduler target integration is REST; historical DB-plus-TCP-socket integration is being replaced |
| Internal dependencies | PayScheduler, PayCore, IMS/API Gateway, client context, and observability services as applicable |
| External dependencies | Feature-specific partner integrations require discovery |
| Security/observability | Gateway/authentication, secrets, NetworkPolicy, probes, metrics, traces, and logs require feature confirmation |

## Deployment context

Runs as part of the Banking.Live estate and is also a target service for Lume
and Kubernetes deployments. Confirm the active deployment model for each
initiative.

## HLD implications

Identify API contracts, authorization, client/tenant context, data access,
downstream services, deployment target, and backward compatibility.

## Context gaps

- Confirm current service owner and repository default branch before a change.
- Confirm the exact API and database path from the repository for each feature.
- Confirm HTTP port, connection pool, downstream integration list, and
  deployment values from the affected branch/chart.
