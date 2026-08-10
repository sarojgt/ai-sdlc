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
---

# PayControl

## Service role

Banking.Live operational control and portal surface. The Confluence service
catalogue assigns it to Portals & Digital Transformation.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/paycontrol](https://github.com/Paymentology/paycontrol) | confirmed | Primary service repository |

## Dependencies and boundaries

- Distinguish internal operational access from public client-facing access.
- Preserve client context, authorization, and sensitive-data filtering.
- Decision Engine functionality is being migrated from PayControl into Atlas;
  the migration guide is the source for that boundary.

## Deployment context

The Dockerized Banking.Live guide identifies PayControl as a local estate
service. Confirm whether a new initiative targets BL2, Lume, Atlas, or a
coexistence path.

## HLD implications

State the host surface, authentication, client context, downstream APIs, data
classification, and migration impact.

## Context gaps

- Confirm which remaining capabilities are still PayControl-owned.
- Confirm current production deployment and repository ownership.
