---
context_id: target-platform-architecture
context_type: consistent
authority: architecture-board-and-platform
status: imported-snapshot
owner: architecture-and-platform-engineering
review_cadence: verify-against-confluence-before-material-design
source: https://paymentology.atlassian.net/wiki/spaces/pa/pages/8560705540/SDD+Target+Platform+Architecture
retrieved: 2026-07-22
---

# Target Platform Architecture

This snapshot captures the target platform direction for Lume and Banking.Live
3.0 workloads. The source contains a mixture of approved decisions,
requirements, and design guidance. Initiative evidence must confirm which
parts apply to the specific service or region.

## Platform shape

- The target is cloud-native, service-driven, scalable, resilient, and
  automation-oriented.
- Kubernetes is the application orchestration boundary, with namespaces used
  to separate workloads and ownership boundaries.
- The platform follows a hub-and-spoke network direction, with separate
  considerations for production, non-production, UAT, and sensitive or PCI
  zones.
- Services should be deployed through repeatable Infrastructure as Code and
  automated CI/CD pipelines.
- Use zone redundancy and multi-AZ deployment where the target environment and
  service criticality require it.
- Client access may use public or private connectivity patterns, subject to
  approved security and client requirements.

## Cloud direction

- AWS is the primary cloud direction for the target platform.
- GCP is a supported alternative or exception where regional availability,
  client requirements, or business constraints require it.
- Application architecture should minimize provider-specific coupling.
- Cloud-specific infrastructure can be isolated behind platform and IaC
  boundaries.

## Shared services

The platform provides or integrates with shared capabilities such as API and
client access services, identity and access management, secrets management,
event streaming and messaging, caching, centralized observability, network and
connectivity services, and deployment automation.

Shared services must have clear ownership, service boundaries, security
controls, availability expectations, and regional deployment behavior.

## Data and isolation

- Client data isolation is a design requirement, not an afterthought.
- Shared compute and shared platform services may be used where appropriate.
- Operational client data should use a dedicated database or an explicitly
  approved stronger isolation boundary.
- Sensitive or PCI workloads may require dedicated zones, namespaces,
  accounts, clusters, or other stronger controls.
- The target platform must not assume that a shared database is acceptable for
  every client or data classification.

## HLD implications

Every HLD targeting this platform should state the cloud, region, Kubernetes
namespace or workload boundary, shared services used, data isolation level,
network path, availability zones, sensitive-data boundary, deployment owner,
and evidence required to validate capacity and operational readiness.

## Source

[Target Platform Architecture](https://paymentology.atlassian.net/wiki/spaces/pa/pages/8560705540/SDD+Target+Platform+Architecture)
