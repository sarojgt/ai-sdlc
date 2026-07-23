---
context_id: portal-atlas
context_type: consistent
authority: portals-platform
status: imported-snapshot
owner: portals-platform-and-product-engineering
review_cadence: verify-against-confluence-before-material-design
source: https://paymentology.atlassian.net/wiki/spaces/TS/pages/9212821562/SDLC+Atlas+aka+Portals+Infrastructure
retrieved: 2026-07-22
---

# Atlas Portals Architecture

Atlas, also called Portals Infrastructure, is the platform for developing,
integrating, deploying, and operating portals and their backend-for-frontend
services.

## Frontend structure

- An MFE is an independently owned microfrontend or mini-portal.
- The Internal Shell App, also called Helm in product terminology, hosts
  employee-only internal portals.
- The Public Shell App, also called PayPortal Shell App, hosts client-facing
  public portals.
- Internal portals are reachable through internal network routing and approved
  employee browser access.
- Public portals are exposed through CloudFront and public endpoints.
- A shared UI library provides React components, hooks, Material UI themes,
  and common user-experience conventions.

## BFF pattern

- Each MFE is paired with a BFF owned by the relevant product team.
- The BFF exposes a GraphQL schema tailored to that MFE.
- The frontend should not access domain services or databases directly.
- The API Gateway/API Hub validates the incoming request before it reaches the
  BFF.
- The BFF receives identity context and uses the approved authorization model.
- BFFs should keep frontend composition separate from domain ownership.

## Ownership and delivery

- Each portal has its own GitHub repository and a clearly assigned product
  engineering owner.
- Portals Platform co-owns the integration standards and provides common
  infrastructure and libraries.
- Portal CI/CD must include integration and end-to-end testing.
- Teams must coordinate shared permissions, roles, and UX to prevent
  authorization fragmentation and inconsistent user experience.

## HLD implications

Portal HLDs must identify internal versus public audience, shell application,
MFE and BFF ownership, GraphQL schema, API Gateway path, IMS authorization,
shared UI dependencies, repository boundaries, deployment model, and
end-to-end test strategy.

## Source

[SDLC Atlas / Portals Infrastructure](https://paymentology.atlassian.net/wiki/spaces/TS/pages/9212821562/SDLC+Atlas+aka+Portals+Infrastructure)
