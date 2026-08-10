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
repository_commit: e404386
scan_scope: readme-load-test-only
---

# Rule Engine

## Service role

The Confluence service catalogue identifies a Rules Engine under the Decision
Engine team. It is a decisioning capability related to PayPower and Decision
Engine workflows.

## Business capability

The Rules Engine evaluates configurable rules that influence authorization and
transaction decisions. Rule definition, rule evaluation, decision ownership,
versioning, rollout, tenant scope, and audit must remain explicit in every
initiative.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| `paymento/source/bl2.0/rules-engine.git` | legacy reference | Repository name in Confluence |
| [Paymentology/rule-engine-v1-load-test](https://github.com/Paymentology/rule-engine-v1-load-test) | confirmed auxiliary | Load-test repository only; not the service implementation |

## Dependencies and boundaries

- Reuse an existing rules capability before creating a new one.
- Separate rule definition, evaluation, decision ownership, and UI concerns.
- Apply versioning, rollout, audit, tenant, and observability controls.

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | Primary implementation runtime and framework are not confirmed; the listed load-test repository is not the service implementation |
| Data stores | No authoritative database mapping confirmed |
| Database connectivity/pool | Unknown; requires the primary repository and runtime configuration |
| Communication | Evaluation protocol and transport are not confirmed |
| Internal dependencies | PayPower and Decision Engine are related capabilities |
| External dependencies | No external dependency confirmed |
| Security/observability | Rule versioning, audit, tenant scope, sensitive inputs, and evaluation telemetry are required |

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
- The local scan confirms only the auxiliary load-test repository; no service
  implementation, database, API, deployment, or protocol facts were inferred
  from it.
