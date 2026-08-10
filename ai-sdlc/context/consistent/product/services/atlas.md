---
context_id: platform-atlas-services
context_type: consistent
authority: atlas-platform-and-service-discovery
status: imported-snapshot
owner: atlas-platform-and-application-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/9865330792/Decision+Engine+PayControl+to+Atlas+migration+guide
  - https://github.com/Paymentology/atlas-environments
  - https://github.com/Paymentology/atlas-payportal
retrieved: 2026-08-10
---

# Atlas Services and Portals

## Service role

Atlas provides public and private portal shells, shared UI/platform services,
identity, client context, and deployment orchestration for microfrontends and
remote services.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [atlas-payportal](https://github.com/Paymentology/atlas-payportal) | confirmed | Public portal surface |
| [atlas-environments](https://github.com/Paymentology/atlas-environments) | confirmed | Environment/release configuration |
| [atlas-config-hub](https://github.com/Paymentology/atlas-config-hub) | confirmed | Configuration hub |
| [atlas-ui-kit](https://github.com/Paymentology/atlas-ui-kit) | confirmed | Shared UI layer |
| [atlas-identity-management](https://github.com/Paymentology/atlas-identity-management) | confirmed | Identity-management capability |
| [atlas-pub-user-management](https://github.com/Paymentology/atlas-pub-user-management) | confirmed | Public user management |
| [atlas-priv-client-directory](https://github.com/Paymentology/atlas-priv-client-directory) | confirmed | Private client directory |
| [atlas-transaction-insights](https://github.com/Paymentology/atlas-transaction-insights) | confirmed | Transaction insights |
| [atlas-auth-transaction-insights](https://github.com/Paymentology/atlas-auth-transaction-insights) | confirmed | Auth transaction insights |
| [decision-engine-atlas](https://github.com/Paymentology/decision-engine-atlas) | confirmed | Decision Engine Atlas integration |

## Dependencies and boundaries

- PayPortal is the public shell; Helm is the private shell.
- Shells own authentication orchestration, navigation, shared context, and
  token propagation; MFEs own internal routing and feature flows.
- Public MFEs use S3/CloudFront; private MFEs use the shared private UI router;
  BFFs and remote services run on EKS.

## Deployment context

Atlas environment configuration and orchestration determine release behavior.
Confirm the target surface, region, environment, and public/private boundary.

## HLD implications

Identify shell, MFE, BFF, identity, client context, shared UI, deployment, and
rollback boundaries. Avoid direct frontend-to-downstream calls when the Atlas
BFF pattern applies.

## Context gaps

- Confirm the final repository topology and ownership for each Atlas initiative.
- Confirm whether a named repository is a shell, shared platform, MFE, BFF, or
  environment repository before implementation.
