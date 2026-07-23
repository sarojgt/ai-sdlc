---
context_id: enterprise-capabilities-and-reuse
context_type: consistent
authority: platform-architecture-and-engineering
status: imported-snapshot
owner: platform-engineering
review_cadence: verify-against-platform-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/pa/pages/9129656332/Event+Streaming+Platform+Principles
  - https://paymentology.atlassian.net/wiki/spaces/PP/pages/8647639127/Cloud+Strategy+2026+-+MSK
  - https://paymentology.atlassian.net/wiki/spaces/pa/pages/10079567875/Webhook+Architecture+Principles
  - https://paymentology.atlassian.net/wiki/spaces/pa/pages/10101522482/Webhook+Service+-+Initial+Adoption+and+Delivery+Plans
  - https://paymentology.atlassian.net/wiki/spaces/pa/pages/8933310674/SDD+Enterprise+Notification+Platform
retrieved: 2026-07-22
---

# Enterprise Capabilities and Reuse Before Build

New designs should first discover and reuse an existing enterprise capability.
Creating a local Kafka cluster, webhook delivery engine, notification system,
identity flow, observability pipeline, or artifact repository requires an
explicit reason and human architecture approval.

## Capability catalogue

| Capability | Default reuse direction | Do not build locally when |
| --- | --- | --- |
| Event streaming | Enterprise Event Streaming Platform using Kafka/MSK patterns | The requirement is asynchronous domain events, retry, DLQ, or fan-out already supported by the platform |
| Webhooks | Shared webhook subscription and orchestrator services | The requirement is outbound event delivery with retries, signatures, subscriptions, or delivery status |
| API exposure | API Gateway/API Hub and approved BFF patterns | A new service needs authenticated external or portal access |
| Identity | Auth0, API Gateway, IMS, and approved security libraries | The requirement is user, client, service, role, grant, or tenant authorization |
| Certificates | Zero Touch PKI and approved certificate automation | The requirement is mTLS or managed TLS lifecycle |
| Databases | Approved RDS/Aurora and client-isolation patterns | A service needs relational persistence or read scaling |
| Artifacts | JFrog Artifactory, Xray, and build provenance | A service needs container, Helm, library, or release artifact storage |
| Observability | Shared Datadog/CloudWatch or emerging OpenTelemetry/Grafana platform standards | A service needs logs, metrics, traces, dashboards, alerts, or SLO evidence |

## Reuse decision sequence

Before proposing a new component, the AI must:

1. Identify the capability category and search the enterprise context,
   platform catalogue, and existing repositories.
2. Find the owning team, supported interfaces, deployment model, security
   boundary, region, tenancy model, and operational SLO.
3. Compare reuse, extension, adapter, and new-build options.
4. Prefer an adapter when the existing capability is close but not an exact
   fit; document the boundary and ownership.
5. Treat “not found” as an information gap, not proof that the capability does
   not exist.
6. Require the HLD to record the reuse decision and the reason for any
   exception.

## Event streaming reuse rules

- Use Kafka/MSK as the default event-streaming direction in AWS.
- Use the approved portable Kafka pattern for multi-cloud designs; managed GCP
  Kafka remains subject to the technology and platform context.
- Topics, schemas, ACLs, consumer groups, retries, DLQs, quotas, ownership,
  retention, and observability are platform-governed concerns.
- Client isolation may be logical or dedicated depending on approved scale,
  data sensitivity, and operational requirements.
- A product team must not create ad-hoc topic naming, schema, or retry
  conventions.

## Webhook reuse rules

- Webhook delivery is a shared platform capability, not duplicated in each
  product domain.
- Reuse the shared subscription and orchestrator services for subscription
  lifecycle, delivery, retries, signatures, delivery outcomes, and operational
  controls.
- Producers publish approved events; they do not own custom outbound delivery
  loops unless an exception is approved.
- CHD producers must publish only approved, sanitized, tokenized, or referenced
  event data to the shared platform.

## Required HLD section

Every HLD must include a “Reuse and Platform Fit” section containing:

- capability categories considered;
- existing services and repositories searched;
- reuse/extend/adapter/new-build decision;
- owner and onboarding path;
- compatibility and migration impact;
- exception rationale, if any;
- operational ownership and support model.

## Sources

- [Event Streaming Platform Principles](https://paymentology.atlassian.net/wiki/spaces/pa/pages/9129656332/Event+Streaming+Platform+Principles)
- [Cloud Strategy 2026 - MSK](https://paymentology.atlassian.net/wiki/spaces/PP/pages/8647639127/Cloud+Strategy+2026+-+MSK)
- [Webhook Architecture Principles](https://paymentology.atlassian.net/wiki/spaces/pa/pages/10079567875/Webhook+Architecture+Principles)
- [Webhook Service Adoption and Delivery Plans](https://paymentology.atlassian.net/wiki/spaces/pa/pages/10101522482/Webhook+Service+-+Initial+Adoption+and+Delivery+Plans)
- [Enterprise Notification Platform](https://paymentology.atlassian.net/wiki/spaces/pa/pages/8933310674/SDD+Enterprise+Notification+Platform)
