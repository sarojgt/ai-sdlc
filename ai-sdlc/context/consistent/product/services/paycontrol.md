---
context_id: service-paycontrol
context_type: consistent
authority: service-catalog-and-repository-discovery
status: imported-snapshot
owner: banking-live-portal-and-control-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7400423715/Teams+vs+BL+Services
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/6762659879/Banking+Live+dockerized+environment
  - https://github.com/Paymentology/paycontrol
retrieved: 2026-08-10
repository_commit: fde0aac
scan_scope: readme-build-source-deployment-security
---

# PayControl

## Service role

Banking.Live operational control and portal surface. The Confluence service
catalogue assigns it to Portals & Digital Transformation.

## Business capability

PayControl provides operational and client-control workflows for Banking.Live.
It is a user-facing control surface rather than the authoritative owner of
card, transaction, or decision data. New work must identify whether the actor
is internal or external and whether the capability remains in PayControl or
moves to Atlas.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/paycontrol](https://github.com/Paymentology/paycontrol) | confirmed | Primary service repository |

## Dependencies and boundaries

- Distinguish internal operational access from public client-facing access.
- Preserve client context, authorization, and sensitive-data filtering.
- Decision Engine functionality is being migrated from PayControl into Atlas;
  the migration guide is the source for that boundary.

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | React-based frontend; npm dependencies are obtained from JFrog |
| Data stores | No direct database ownership confirmed from the repository README |
| Database connectivity/pool | Not applicable to the frontend based on current evidence; confirm backend/BFF paths |
| Communication | Browser/API calls; exact HTTP clients and downstream endpoints require source discovery |
| Internal dependencies | PayAPI and portal/shared libraries; Atlas migration introduces shell/BFF boundaries |
| External dependencies | Auth0 is used for login; other partner integrations are not confirmed |
| Security/observability | Auth0, CHD feature controls, bundle filtering, and frontend telemetry require confirmation |

## Deployment context

The Dockerized Banking.Live guide identifies PayControl as a local estate
service. Confirm whether a new initiative targets BL2, Lume, Atlas, or a
coexistence path.

## HLD implications

State the host surface, authentication, client context, downstream APIs, data
  classification, and migration impact.

## Scan-confirmed delivery profile

The repository is a React/npm frontend with JFrog-managed dependencies and a
Helm workload. The chart uses a non-root container, a `/paycontrol` health
path, and Datadog/environment configuration. Backend, BFF, and database
ownership are outside this frontend repository.

## Context gaps

- Confirm which remaining capabilities are still PayControl-owned.
- Confirm current production deployment and repository ownership.
- Confirm API clients, backend ownership, browser-to-service protocol, and
  production CHD feature configuration.
