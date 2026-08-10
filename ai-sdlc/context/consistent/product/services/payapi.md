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

## Confirmed implementation map

Repository evidence identifies the existing card-status surface as a likely
extension point for card-state operations:

| Area | Confirmed evidence |
| --- | --- |
| Route family | `CardController` contains `/pws/pws_set_card_status/` and `/pcjs/pcjs_card_status_edit/` routes |
| Processing | `SetCardStatusProcessor` and `EditCardStatusProcessor` validate and authorize card-status changes |
| Data access | `CardDb` owns the card-status database calls and records API timing/log information |
| Database paths | Existing status changes call PayCore and PayTok stored procedures through separate connection pools |
| Authorization | Existing paths use client/session authorization or auth-code validation; exact actor/scopes remain feature-specific |
| Audit | `ApiLogDB` is used for request/response and outcome logging; safe-field policy remains mandatory |

This is evidence for reuse, not a decision that every new card capability must
use an existing route.

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

- Confirm the owning team and target branch for the affected feature.
- Confirm the exact route/version, actor permissions, request/response/error
  contract, idempotency, and gateway exposure.
- Confirm whether the feature uses PayCore, PayTok, both, or another store; name
  the stored procedure/table/function and read/write path.
- Confirm the effective pool, timeout, downstream integration, port, chart, and
  deployment repository from the affected branch/environment.
