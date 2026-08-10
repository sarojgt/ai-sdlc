---
context_id: service-rule-engine
context_type: consistent
authority: service-catalog-and-repository-discovery
status: distributed-capability
owner: banking-live-decisioning-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7400423715/Teams+vs+BL+Services
  - https://github.com/Paymentology/rule-engine-v1-load-test
  - https://github.com/Paymentology/paycoredb
  - https://github.com/Paymentology/payapi
  - https://github.com/Paymentology/paycontrol
  - https://github.com/Paymentology/paypower
retrieved: 2026-08-10
repository_commit: e404386
scan_scope: readme-load-test-only
---

# Rule Engine

## Service role

The Rules Engine is a distributed Banking.Live capability rather than one
standalone deployable repository. PayControl provides setup/configuration
surfaces, PayAPI provides related APIs/actions, PayCore DB contains the
persisted rule definitions and database procedures, and PayPower evaluates
rules during transaction authorization and checks.

## Business capability

The Rules Engine evaluates configurable rules that influence authorization and
transaction decisions. Rule definition, rule evaluation, decision ownership,
versioning, rollout, tenant scope, and audit must remain explicit in every
initiative.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/paycontrol](https://github.com/Paymentology/paycontrol) | confirmed related surface | Rule setup/configuration UI and operational control |
| [Paymentology/payapi](https://github.com/Paymentology/payapi) | confirmed related surface | Rule APIs/actions and integration boundary |
| [Paymentology/paycoredb](https://github.com/Paymentology/paycoredb) | confirmed authoritative data surface | Rule definitions, procedures, functions, and persistence |
| [Paymentology/paypower](https://github.com/Paymentology/paypower) | confirmed runtime consumer | Transaction-time evaluation and authorization checks |
| `paymento/source/bl2.0/rules-engine.git` | legacy reference | Historical service name in Confluence |
| [Paymentology/rule-engine-v1-load-test](https://github.com/Paymentology/rule-engine-v1-load-test) | confirmed auxiliary | Load-test repository; not the capability owner |

## Dependencies and boundaries

- Reuse the distributed PayControl/PayAPI/PayCore DB/PayPower capability before
  creating a new rules service.
- Separate rule definition, evaluation, decision ownership, and UI concerns.
- Apply versioning, rollout, audit, tenant, and observability controls.

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | Distributed across PayControl setup, PayAPI actions, PayCore DB procedures, and PayPower transaction processing |
| Data stores | PayCore is the authoritative rule-definition and procedure data surface; exact schemas depend on rule family |
| Database connectivity/pool | PayAPI and PayPower use their existing PayCore data paths; exact pools and transaction boundaries are service-specific |
| Communication | PayControl/API setup flows, PayAPI integration, and PayPower transaction-time evaluation; exact route/function contracts require feature discovery |
| Internal dependencies | PayControl, PayAPI, PayCore DB, PayPower, Decision Engine, client/tenant context, and observability |
| External dependencies | No external dependency confirmed |
| Security/observability | Rule versioning, audit, tenant scope, sensitive inputs, and evaluation telemetry are required |

## Deployment context

Confirm whether the affected flow is BL2, Lume, or an Atlas/Decision Engine
target workload, and identify which capability surface is changing.

## HLD implications

Describe rule ownership, evaluation path, versioning, data inputs, failure
behavior, performance, and operational controls.

## Context gaps

- Confirm the rule family, PayCore schema/procedure, PayAPI route/action, and
  PayControl setup surface for each initiative.
- Confirm PayPower evaluation ordering, failure behavior, cache/version refresh,
  and transaction performance impact.
- Confirm whether Decision Engine participates in the specific flow or whether
  the existing PayCore/PayPower rule path is sufficient.
