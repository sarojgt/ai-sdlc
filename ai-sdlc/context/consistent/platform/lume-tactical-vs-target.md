---
context_id: lume-tactical-vs-target
context_type: consistent
authority: platform-strategy
status: imported-snapshot
owner: platform-engineering-and-architecture
review_cadence: verify-against-confluence-before-material-design
source: https://paymentology.atlassian.net/wiki/spaces/TS/pages/10061644376/Lume+Tactical+Model+vs+Target+Model
retrieved: 2026-07-22
---

# Lume Tactical and Target Models

Lume has a target operating model and a tactical bridge. AI must distinguish
them explicitly in requirements, HLD options, risks, and delivery plans.

## Target model

- Shared compute and shared platform services where appropriate.
- Dedicated per-client databases for isolation by design.
- Tenant-aware standard routing.
- Control-plane-led onboarding and provisioning.
- Strong automation, repeatability, and operational consistency.
- Reduced client-specific deployments across regions and customers.

## Tactical model

The tactical model enables delivery before every target capability is ready. It
may include dedicated client databases, temporary client-specific deployments
or namespaces, partially manual provisioning, and interim routing or control-
plane gaps.

Tactical is not a permanent architecture. Every tactical deviation requires a
clear reason, accountable owner, risk assessment, convergence path into the
target model, and migration or retirement trigger.

## Required design questions

For any tactical proposal, the HLD must address schema drift, data migration,
ID collisions, shared hierarchy boundaries, future routing, operational burden,
and the cost of converging to the target model.

## Source

[Lume: Tactical Model vs Target Model](https://paymentology.atlassian.net/wiki/spaces/TS/pages/10061644376/Lume+Tactical+Model+vs+Target+Model)
