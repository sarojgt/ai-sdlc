---
context_id: service-paycredit
context_type: consistent
authority: service-catalog-and-repository-discovery
status: imported-snapshot
owner: paycredit-product-and-engineering
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://github.com/Paymentology/paycredit
  - https://github.com/Paymentology/paycredit-ui
  - https://github.com/Paymentology/paycredit-test-automation
retrieved: 2026-08-10
---

# PayCredit

## Service role

PayCredit product capability and its client-facing application surfaces. The
existing PayCredit product context remains the domain source; this page adds
repository discovery metadata.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/paycredit](https://github.com/Paymentology/paycredit) | confirmed | Primary PayCredit service/application |
| [Paymentology/paycredit-ui](https://github.com/Paymentology/paycredit-ui) | confirmed | PayCredit UI |
| [Paymentology/paycredit-test-automation](https://github.com/Paymentology/paycredit-test-automation) | confirmed | Test automation |
| [Paymentology/paycredit-team-shared-resources](https://github.com/Paymentology/paycredit-team-shared-resources) | confirmed | Team-shared resources |

## Dependencies and boundaries

Confirm client-facing exposure, identity, APIs, data classification, and
integration with Banking.Live or Atlas before selecting a repository.

## Deployment context

Confirm whether the initiative targets a public portal, internal portal, Lume,
or a dedicated/shared client deployment.

## HLD implications

Identify product boundary, UI/API repositories, client context, data stores,
security, deployment, and test ownership.

## Context gaps

- Confirm which PayCredit repositories are production-owned versus supporting
  or experimental.
