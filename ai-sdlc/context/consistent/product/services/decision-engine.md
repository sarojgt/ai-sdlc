---
context_id: service-decision-engine
context_type: consistent
authority: service-catalog-and-repository-discovery
status: imported-snapshot
owner: banking-live-decisioning-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/9865330792/Decision+Engine+PayControl+to+Atlas+migration+guide
  - https://github.com/Paymentology/decision-engine
  - https://github.com/Paymentology/decision-engine-dsl
  - https://github.com/Paymentology/decision-engine-atlas
retrieved: 2026-08-10
---

# Decision Engine

## Service role

Decision Engine owns transaction rule-configuration capability. It is being
migrated from PayControl into Atlas surfaces including Helm and PayPortal.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/decision-engine](https://github.com/Paymentology/decision-engine) | confirmed | Existing Decision Engine implementation |
| [Paymentology/decision-engine-dsl](https://github.com/Paymentology/decision-engine-dsl) | confirmed | DSL-related implementation or shared artifact |
| [Paymentology/decision-engine-atlas](https://github.com/Paymentology/decision-engine-atlas) | confirmed | Atlas migration/integration repository |

## Dependencies and boundaries

- One shared frontend capability is intended for Helm and PayPortal, subject
  to Atlas topology confirmation.
- Atlas-facing BFFs sit between the frontend and downstream services such as
  PayAPI.
- Helm is private; PayPortal is public. Shell authentication and context come
  from Atlas, while Decision Engine owns internal routing and flows.

## Deployment context

Public MFEs follow the S3/CloudFront delivery model. Private MFEs are bundled
through the Atlas UI router. BFFs and remote services run on EKS.

## HLD implications

Cover host surface, shared frontend/BFF topology, authorization, client scope,
DSL compatibility, deployment path, and behavior preservation.

## Context gaps

- Confirm the final Atlas repository topology and BFF split before approval.
