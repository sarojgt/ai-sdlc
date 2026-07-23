---
context_id: client-data-isolation
context_type: consistent
authority: architecture-and-platform
status: imported-snapshot
owner: architecture-and-platform-engineering
review_cadence: verify-against-confluence-before-material-design
source: https://paymentology.atlassian.net/wiki/spaces/pa/pages/9302868154/Client+Data+Isolation
retrieved: 2026-07-22
---

# Client Data Isolation

Client data isolation is a bank-grade architecture requirement and a key
platform differentiator. It must be designed across application, database,
storage, messaging, access, observability, and operations.

## Baseline direction

- Each client's operational data should have a dedicated database or an
  explicitly approved stronger isolation boundary.
- Dedicated databases may run on shared infrastructure such as an Aurora or
  RDS cluster to balance isolation and cost.
- Shared tables that do not belong to a specific client should be isolated as
  platform shared data rather than mixed into client data without an explicit
  ownership model.
- Client-specific object storage and access controls should be considered
  alongside database isolation.
- Application, data, namespace, event, and observability boundaries must be
  analyzed together; database separation alone is not sufficient.

## Platform and cloud requirements

- Isolation patterns should work across AWS and GCP where portability is
  required.
- Deployment, scaling, configuration, and promotion should be automated and
  repeatable.
- Kubernetes namespaces, IAM, network controls, secrets, and storage access
  must prevent cross-client access.
- Sensitive or PCI workloads may require dedicated zones, accounts, clusters,
  or infrastructure beyond a dedicated database.

## HLD implications

Every HLD must define the isolation unit, tenant identity source, database and
storage ownership, cross-tenant access policy, backup/restore boundary,
observability redaction, migration path, and evidence needed to prove that one
client cannot access another client's data.

## Source

[Client Data Isolation](https://paymentology.atlassian.net/wiki/spaces/pa/pages/9302868154/Client+Data+Isolation)
