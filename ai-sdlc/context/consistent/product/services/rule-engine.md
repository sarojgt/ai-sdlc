---
context_id: service-rule-engine
context_type: consistent
authority: service-catalog-and-repository-discovery
status: partial-mapping
owner: banking-live-decisioning-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7400423715/Teams+vs+BL+Services
  - https://github.com/Paymentology/rule-engine-v1-load-test
retrieved: 2026-08-10
---

# Rule Engine

## Service role

The Confluence service catalogue identifies a Rules Engine under the Decision
Engine team. It is a decisioning capability related to PayPower and Decision
Engine workflows.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| `paymento/source/bl2.0/rules-engine.git` | legacy reference | Repository name in Confluence |
| [Paymentology/rule-engine-v1-load-test](https://github.com/Paymentology/rule-engine-v1-load-test) | confirmed auxiliary | Load-test repository only; not the service implementation |

## Dependencies and boundaries

- Reuse an existing rules capability before creating a new one.
- Separate rule definition, evaluation, decision ownership, and UI concerns.
- Apply versioning, rollout, audit, tenant, and observability controls.

## Deployment context

Confirm whether the affected flow is BL2, Lume, or an Atlas/Decision Engine
target workload.

## HLD implications

Describe rule ownership, evaluation path, versioning, data inputs, failure
behavior, performance, and operational controls.

## Context gaps

- The primary GitHub repository for `rules-engine.git` was not found in the
  accessible Paymentology repository search. Do not use the load-test repo as a
  substitute; obtain service-owner confirmation.
