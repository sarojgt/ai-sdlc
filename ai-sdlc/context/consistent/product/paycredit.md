---
context_id: paycredit
context_type: consistent
authority: product-and-platform-architecture
status: imported-snapshot-partial
owner: paycredit-product-and-engineering
review_cadence: verify-against-confluence-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/8215134239/PayCredit+Platform+Overview
  - https://paymentology.atlassian.net/wiki/spaces/pa/pages/8619458637/SDD+PayCredit+Identity+and+Access+Management
retrieved: 2026-07-22
---

# PayCredit

PayCredit is a credit capability that is being developed on the target
platform. The available platform-overview page is explicitly incomplete, so
this file is context rather than an approved reference architecture.

## Known platform themes

The source identifies the following areas for PayCredit design:

- Microservices and Kubernetes.
- Kafka or equivalent messaging.
- Database and multi-tenancy.
- Scalability and resilience.
- APIs and Banking.Live integration APIs.
- FAST interface integration.
- PayCredit user interface and portal access.

## Identity and access

- Auth0 is the identity-provider direction.
- PayCredit services apply access control based on the role and context in the
  access token.
- The PayCredit IAM design describes an Identity Management Service as a
  Spring Boot service exposing REST APIs for user, application, role, and
  permission management, integrated with Auth0 Management API.
- The scope and timing of IMS adoption must be confirmed for each PayCredit
  initiative; the source notes that IMS was not in scope for an earlier MVP.

## HLD implications

PayCredit HLDs must clarify the target-platform boundary, Banking.Live or FAST
integration, event and API contracts, tenant model, data ownership, portal
authentication, authorization, operational readiness, and whether the design
uses an MVP exception or the strategic target pattern.

## Sources

- [PayCredit Platform Overview](https://paymentology.atlassian.net/wiki/spaces/TS/pages/8215134239/PayCredit+Platform+Overview)
- [PayCredit Identity and Access Management](https://paymentology.atlassian.net/wiki/spaces/pa/pages/8619458637/SDD+PayCredit+Identity+and+Access+Management)
