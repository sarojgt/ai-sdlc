---
context_id: cloud-platform-principles
context_type: consistent
authority: architecture-and-platform
status: imported-snapshot
owner: architecture-and-platform-engineering
review_cadence: verify-against-confluence-before-material-design
source: https://paymentology.atlassian.net/wiki/spaces/pa/pages/8408105033/Cloud+Strategy+-+Principles
retrieved: 2026-07-22
---

# Cloud and Platform Principles

This is a curated snapshot of the current cloud strategy and target-platform
direction. Several items in the source are explicitly assumptions or future-
state guidance, so agents must not present them as confirmed implementation
facts without repository or platform evidence.

## Direction

- Keep regional application environments self-contained where required by
  residency, latency, and operational boundaries.
- Centralize observability, monitoring, and metrics where that improves
  operational efficiency.
- Prefer local integration to client and scheme connectivity where latency is
  material.
- Design for horizontal application scaling.
- Build strong client or tenant data isolation by design.
- Treat PCI-DSS and data protection as architecture constraints.

## Portability and automation

- AWS is the preferred cloud direction, with alternatives required where
  regional availability or business constraints demand them.
- Minimize cloud-specific coupling in the application architecture.
- Prefer Kubernetes-native capabilities over cloud-specific workload APIs when
  portability is a stated requirement.
- Externalize configuration and use Infrastructure as Code.
- Prefer cloud-agnostic CI/CD and deployment automation where practical.
- Make cross-platform testing part of engineering practice when portability is
  a requirement.

## Platform responsibilities

- Platform Engineering owns environment and namespace concerns.
- Engineering owns application packaging and service-level configuration.
- Environment-specific details should not be hard-coded into application
  deployment templates.
- Deployment promotion should be repeatable and minimize manual intervention.

## HLD implications

HLDs must distinguish strategic direction from verified estate facts. They must
state regionality, tenancy and data isolation, scaling, observability,
portability, deployment ownership, cloud assumptions, and the evidence needed
before implementation.

## Source

[Cloud Strategy - Principles](https://paymentology.atlassian.net/wiki/spaces/pa/pages/8408105033/Cloud+Strategy+-+Principles)
