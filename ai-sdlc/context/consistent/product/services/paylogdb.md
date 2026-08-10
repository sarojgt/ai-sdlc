---
context_id: service-paylogdb
context_type: consistent
authority: service-catalog-and-repository-discovery
status: imported-snapshot
owner: banking-live-data-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7400423715/Teams+vs+BL+Services
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/10010918939/PECA-1056+-+Migrate+PayAPI+PayScheduler+Integration+from+DB+Socket+to+REST+API
  - https://github.com/Paymentology/paylogdb
retrieved: 2026-08-10
---

# PayLog DB

## Service role

Banking.Live operational/log-supporting database. The Confluence catalogue
assigns it to the Data team.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/paylogdb](https://github.com/Paymentology/paylogdb) | confirmed | Database schema and delivery repository |

## Dependencies and boundaries

- PayScheduler documents PayLog as a tenant-routed database type.
- PayPower analysis indicates client-specific queue/database relationships.
- Assess whether new data belongs here or in the centralized observability
  platform; do not use PayLog as a default telemetry store.

## Deployment context

Confirm client/environment placement, retention, regional residency, and
sensitive-data boundary.

## HLD implications

State data purpose, classification, retention, query ownership, access path,
observability relationship, and migration impact.

## Context gaps

- Confirm the current schema and whether the database remains the correct home
  for the proposed data.
