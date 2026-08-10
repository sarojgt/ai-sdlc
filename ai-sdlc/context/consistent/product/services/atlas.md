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
repository_commit: baac0b2
scan_scope: readme-source-mfe-bff-deployment-identity
---

# Atlas Services and Portals

## Service role

Atlas provides public and private portal shells, shared UI/platform services,
identity, client context, and deployment orchestration for microfrontends and
remote services.

## Business capability

Atlas provides the unified public and private product experience. It composes
microfrontends, shared UI, identity, client context, BFFs, and downstream
Banking.Live capabilities. A portal initiative must identify the shell, MFE,
BFF, downstream API, actor type, and public/private boundary.

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

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | React/JavaScript microfrontend shell and shared UI repositories; backend/BFF runtime is service-specific |
| Data stores | Atlas repositories may own service-specific stores; no single Atlas database is implied |
| Database connectivity/pool | Shells should not connect directly to databases; BFF/remote-service configuration requires discovery |
| Communication | Webpack Module Federation, browser HTTP/GraphQL to BFFs, Auth0, and downstream PayAPI/other APIs |
| Internal dependencies | Atlas environments, UI kit, identity, client directory, transaction insights, Decision Engine, and shared platform services |
| External dependencies | Auth0, AWS S3/CloudFront, and partner/product APIs as applicable |
| Security/observability | Shell token propagation, ACLs, BFF authorization, CSP, telemetry, and public/private separation are required |

## Deployment context

Atlas environment configuration and orchestration determine release behavior.
Confirm the target surface, region, environment, and public/private boundary.

## HLD implications

Identify shell, MFE, BFF, identity, client context, shared UI, deployment, and
rollback boundaries. Avoid direct frontend-to-downstream calls when the Atlas
BFF pattern applies.

## Scan-confirmed delivery profile

The `atlas-payportal` scan confirms a shell, Webpack Module Federation,
Auth0-based AAA, shared libraries, dedicated GraphQL BFF direction, and
downstream PayAPI integration. Terraform and environment repositories control
deployment; exact MFE/BFF ownership is feature-specific.

## Scan-confirmed implementation anchors

- The local repository family separates public portal, environment/configuration,
  identity, user management, client directory, transaction insights, shared UI,
  and Decision Engine integration concerns.
- The portal pattern is shell → microfrontend/shared UI → BFF or downstream
  API; frontend changes should not bypass the applicable BFF authorization and
  client-context boundary.
- Public and private delivery use different hosting/routing paths, so a design
  must state whether it targets PayPortal, the private Helm shell, or both.

These anchors are based on the local Atlas family scan; the affected shell,
MFE, BFF, and environment repository must still be named.

## Context gaps

- Confirm the final repository topology and ownership for each Atlas initiative.
- Confirm whether a named repository is a shell, shared platform, MFE, BFF, or
  environment repository before implementation.
