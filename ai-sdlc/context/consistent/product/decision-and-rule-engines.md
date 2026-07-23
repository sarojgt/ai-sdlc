---
context_id: decision-and-rule-engines
context_type: consistent
authority: banking-live-decisioning-architecture
status: imported-snapshot
owner: decision-engine-product-and-engineering
review_cadence: verify-against-decision-engine-team-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7877165110/Rules+Engine+V3+Decision+Engine
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/8825897119/Decision+Engine+Foundational+Knowledge
  - https://paymentology.atlassian.net/wiki/spaces/pa/pages/8722907214/Decision+Engine+System+Analysis+Architecture+Overview
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7530840551/Decision+Engine+Architecture+ie+Rule+engine+v3
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/8718516699/Decision+Engine+Monitoring
retrieved: 2026-07-22
---

# Rule Engine and Decision Engine

The Decision Engine (DE) is the evolution of the Banking.Live Rule Engine. It
is a reusable financial decisioning capability for evaluating transaction and
client-specific rules, predicates, operators, and decision trees.

## Capability boundary

- Rules express business decision logic.
- Predicates and operators evaluate transaction, card, client, product, and
  contextual inputs.
- The Decision Engine DSL provides a structured way to define predicates and
  rules.
- Decision trees organize hierarchical rule evaluation and actions.
- PayPower invokes the Decision Engine and handles the resulting actions in the
  transaction flow.
- The engine can have non-orchestrated and Kubernetes/orchestrated deployment
  topologies; the target must be confirmed for the affected estate.

## Reuse before build

Use the existing Decision Engine when a requirement concerns configurable
transaction decisioning, client rules, limits, waivers, approvals, or action
selection. Do not embed a second rules engine inside PayPower, PayAPI, a new
service, or a portal without an explicit architecture decision.

An adapter or new capability may be appropriate when the requirement is outside
the engine’s supported domain, latency, availability, or rule lifecycle model.
The HLD must compare reuse, extension, adapter, and new-build options.

## Rule lifecycle and governance

Rule changes are production behavior changes. Designs must address:

- authoring, validation, versioning, approval, and promotion;
- rule ownership and client scope;
- simulation, shadow mode, UAT, and active production rollout;
- backward compatibility between Rule Engine V1 and Decision Engine;
- rollback and audit of the effective rule set;
- deterministic evaluation, ordering, timeouts, and failure behavior;
- sensitive inputs and safe decision traces.

## HLD requirements

Every decisioning HLD must show:

- caller and synchronous/asynchronous position in the transaction flow;
- rule/decision ownership and domain boundary;
- input contract and data classification;
- decision tree/DSL lifecycle;
- response actions and downstream responsibility;
- latency, availability, scaling, and fail-open/fail-closed behavior;
- migration path from Rule Engine V1 if applicable;
- dashboards, alerts, audit, and operational runbook.

## Sources

- [Rules Engine V3 / Decision Engine](https://paymentology.atlassian.net/wiki/spaces/TS/pages/7877165110/Rules+Engine+V3+Decision+Engine)
- [Decision Engine Foundational Knowledge](https://paymentology.atlassian.net/wiki/spaces/TS/pages/8825897119/Decision+Engine+Foundational+Knowledge)
- [Decision Engine Architecture Overview](https://paymentology.atlassian.net/wiki/spaces/pa/pages/8722907214/Decision+Engine+System+Analysis+Architecture+Overview)
- [Decision Engine Architecture](https://paymentology.atlassian.net/wiki/spaces/TS/pages/7530840551/Decision+Engine+Architecture+ie+Rule+engine+v3)
- [Decision Engine Monitoring](https://paymentology.atlassian.net/wiki/spaces/TS/pages/8718516699/Decision+Engine+Monitoring)
