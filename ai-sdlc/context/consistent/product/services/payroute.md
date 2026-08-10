---
context_id: service-payroute
context_type: consistent
authority: service-catalog-and-repository-discovery
status: imported-snapshot
owner: banking-live-switching-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7400423715/Teams+vs+BL+Services
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/6762659879/Banking+Live+dockerized+environment
  - https://github.com/Paymentology/payroute
retrieved: 2026-08-10
---

# PayRoute

## Service role

Banking.Live transaction-routing component used with PaySwitch and PayPower.
The Confluence catalogue assigns it to Switching.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/payroute](https://github.com/Paymentology/payroute) | confirmed | Primary service repository |

## Dependencies and boundaries

- Receives or forwards transaction messages through approved switching paths.
- PaySwitch and scheme/network integrations are related but not automatically
  PayRoute-owned.
- Routing, SAF, and client context must be confirmed for the affected flow.

## Deployment context

Part of the Banking.Live estate and local Dockerized environment. Confirm the
target Lume/Kubernetes workload and sensitive-data zone.

## HLD implications

Describe message flow, routing decisions, failure handling, replay/SAF,
security boundary, and observability.

## Context gaps

- Confirm current PaySwitch-to-PayRoute contract and runtime topology.
