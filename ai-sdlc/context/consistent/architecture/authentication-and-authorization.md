---
context_id: authentication-and-authorization
context_type: consistent
authority: identity-platform-and-security-architecture
status: imported-snapshot
owner: identity-platform-and-portals
review_cadence: verify-against-confluence-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/PP/pages/10095296601/Auth0+-+SSO+Self-Service+Architecture+for+Portals
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/9311945174/Identity+Management+Service
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/9314140230/Atlas+Shell+Apps+Design+Private+Internal+and+Public+Client
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/8790409234/PayPortal+Shell+App+and+Microfrontend+Auth+Flow+with+Auth0
  - https://paymentology.atlassian.net/wiki/spaces/pa/pages/9614099019/LUME+-+Cookie+Based+Authentication
retrieved: 2026-07-22
---

# Authentication and Authorization

The current platform direction separates identity from access policy:

> Auth0 answers “who is this principal?” IMS answers “what may this principal
> do, for which client, and in which regional context?”

## Responsibility boundaries

- Auth0 is the identity provider for human login, federation, MFA, session
  handling at the identity-provider boundary, and token issuance.
- Auth0 tenants are environment-tier boundaries. Auth0 Organizations represent
  client login containers, while enterprise SAML/OIDC connections connect a
  client IdP to the tenant and are enabled for selected Organizations.
- API Gateway/API Hub is the protected entry point. It validates Auth0 JWTs,
  checks issuer, audience, expiry and relevant claims, and routes only
  authenticated requests downstream.
- IMS owns authorization data: client hierarchy, memberships, roles, grants,
  permissions, inheritance, and effective access in the relevant region.
- BFFs and protected backend services must enforce authorization at their own
  policy boundary. The Atlas Security Library is the preferred reusable
  integration pattern for BFFs where applicable.
- IMS does not issue user tokens, validate JWTs, or own login/logout flows.

## Internal and public portal model

Internal and public portals use the same conceptual chain, with separate
applications, audiences, routes, and exposure policies:

```text
User -> Internal/Public Shell -> Auth0 -> API Gateway/API Hub -> BFF -> IMS -> service
                                  authentication       JWT validation       authorization
```

- Internal portals are employee-facing and use internal routing and approved
  enterprise access controls.
- Public/client portals use public endpoints and client-facing applications,
  but still route through the approved API Gateway and authorization model.
- A portal or microfrontend must not call Auth0 Management APIs directly.
- A BFF must not invent a separate client hierarchy or permission model.
- MFE design must identify the shell application, Auth0 application/audience,
  API Gateway route, BFF, IMS authorization call, and required permissions.

## Regional authorization

Authentication may be shared through the Auth0 tenant, while IMS is deployed
and persisted regionally. A design must identify the region used to resolve
client hierarchy and permissions. Credentials can be common across regions;
authorization data and portal sessions may remain regional.

## Machine-to-machine access

M2M integrations use an Auth0-registered application and client-credentials
flow or another explicitly approved service identity. Interactive SSO setup
links and browser organization flows do not apply to M2M calls. The HLD must
state how service identity, audience, scopes, client/tenant context, secret or
key storage, rotation, and authorization are managed.

## HLD requirements

Every identity-sensitive HLD must show:

- principal type: human, client, service, or platform operator;
- Auth0 tenant, application, organization, issuer, audience, and protocol;
- internal versus public exposure and API Gateway route;
- JWT validation boundary and failure behavior;
- IMS authorization lookup and client/region resolution;
- permission enforcement in the BFF and downstream service;
- token, secret, certificate, and session lifecycle;
- audit, rate limiting, caching, logging redaction, and security review needs.

## Sources

- [Auth0 SSO Self-Service Architecture](https://paymentology.atlassian.net/wiki/spaces/PP/pages/10095296601/Auth0+-+SSO+Self-Service+Architecture+for+Portals)
- [Identity Management Service](https://paymentology.atlassian.net/wiki/spaces/TS/pages/9311945174/Identity+Management+Service)
- [Atlas Shell Apps: Private and Public](https://paymentology.atlassian.net/wiki/spaces/TS/pages/9314140230/Atlas+Shell+Apps+Design+Private+Internal+and+Public+Client)
- [PayPortal MFE Auth Flow](https://paymentology.atlassian.net/wiki/spaces/TS/pages/8790409234/PayPortal+Shell+App+and+Microfrontend+Auth+Flow+with+Auth0)
- [Lume Cookie-Based Authentication](https://paymentology.atlassian.net/wiki/spaces/pa/pages/9614099019/LUME+-+Cookie+Based+Authentication)
