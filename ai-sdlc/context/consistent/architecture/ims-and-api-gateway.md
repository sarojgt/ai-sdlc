---
context_id: ims-and-api-gateway
context_type: consistent
authority: identity-and-platform-architecture
status: imported-snapshot
owner: identity-platform-and-portals
review_cadence: verify-against-confluence-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/9311945174/Identity+Management+Service
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/9331671050/Identity+Management+Service+API+Internal+Design
retrieved: 2026-07-22
---

# Identity Management Service and API Gateway

IMS is the centralized authorization and identity-management backend for Atlas
and the BL3.0 domain. It separates BFFs and services from direct Auth0
Management API coupling.

## Responsibility boundaries

- Auth0 issues tokens.
- API Gateway/API Hub validates Auth0 JWTs and acts as the secure entry point.
- IMS authorizes permission-sensitive requests and stores authorization data.
- IMS manages client hierarchies, roles, permissions, grants, and downstream
  synchronization.
- BFFs query IMS through GraphQL or the approved SDK/library.
- Backend services enforce authorization at their own policy-enforcement
  boundaries.
- IMS does not issue tokens, validate JWTs, or own login/logout flows.

## Internal service shape

The source describes three services following CQRS:

- Authorization Service for runtime permission queries.
- Management Query Service for read-only identity and permission data.
- Management Command Service for user, client, role, grant, and permission
  changes.

## HLD implications

Identity-related HLDs must show token issuer, JWT validation boundary, API
Gateway route, IMS authorization call, client/tenant context, caching and rate
limits, permission ownership, audit, failure behavior, and the difference
between authentication and authorization.

## Sources

- [Identity Management Service](https://paymentology.atlassian.net/wiki/spaces/TS/pages/9311945174/Identity+Management+Service)
- [IMS API and Internal Design](https://paymentology.atlassian.net/wiki/spaces/TS/pages/9331671050/Identity+Management+Service+API+Internal+Design)
