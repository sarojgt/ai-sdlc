---
context_id: lume-deployment-models
context_type: consistent
authority: platform-strategy
status: imported-snapshot
owner: platform-engineering-and-architecture
review_cadence: verify-against-confluence-before-material-design
source: https://paymentology.atlassian.net/wiki/spaces/pa/pages/9218850872/LUME+-+Deployment+Offering+Strategy
retrieved: 2026-07-22
---

# Lume Deployment Models

Lume supports a graduated deployment strategy. The correct choice depends on
client isolation, performance, compliance, sovereignty, cost, and resilience
requirements.

## Professional

The recommended standard offering for most clients:

- Shared Network Hub and shared application services in the target model.
- Dedicated logical client database.
- Shared compute is used where appropriate.
- The tactical model may temporarily use a client-specific application stack
  in an isolated Kubernetes namespace and a dedicated database on a shared
  cluster.

The tactical model is a controlled bridge, not the long-term destination. It
must have an owner, risk assessment, and convergence path to the target model.

## Enterprise

For clients requiring stronger compute and middleware isolation:

- Shared Network Hub and portals.
- Dedicated compute, EKS workload boundary, database cluster, and middleware
  such as Kafka per client.
- Dedicated API hostname and client-facing endpoint considerations.
- Potential client-dedicated disaster-recovery site and controlled failover.
- Scheme connectivity may remain shared; HSM may be shared or dedicated based
  on requirements and commercial agreement.

## Enterprise Plus

An exception tier for clients requiring the strongest isolation or sovereignty:

- Dedicated Network Hub.
- Dedicated compute, database, middleware, scheme connectivity, and HSM.
- Dedicated disaster recovery and client-controlled failover/failback may be
  required.
- This is not the default offering and requires explicit justification.

## Shared services and governance

Application code, CI/CD, artifact repositories, testing, security tooling,
platform management, and observability may remain shared across tiers. The
HLD must identify which components are shared and how tenant isolation,
availability, noisy-neighbor control, access, and operational ownership are
enforced.

## HLD implications

An HLD must not select a deployment tier implicitly. It should compare the
tiers, explain cost and operational impact, record the required isolation level,
and identify whether a tactical exception needs an explicit convergence plan.

## Source

[Lume Deployment Offering Strategy](https://paymentology.atlassian.net/wiki/spaces/pa/pages/9218850872/LUME+-+Deployment+Offering+Strategy)
