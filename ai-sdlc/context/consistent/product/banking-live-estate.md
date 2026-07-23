---
context_id: banking-live-estate
context_type: consistent
authority: banking-live-platform-and-architecture
status: imported-snapshot
owner: banking-live-platform
review_cadence: verify-against-service-catalog-and-repository-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/6762659879/Banking+Live+dockerized+environment
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/6471712798/Installing+Banking.Live+on+AWS+-+Application+Installation
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/6878461959/Banking.Live+-+PayControl+PayApi+PayCore+etc+-+local+Portals+knowhow
  - https://paymentology.atlassian.net/wiki/spaces/pa/pages/9872343046/Tactical+Model+-+Transaction+Routing
  - https://paymentology.atlassian.net/wiki/spaces/pa/pages/9218850872/LUME+-+Deployment+Offering+Strategy
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/8814788609/TECH-709+B.L.+Strategic+Platform+3.0
retrieved: 2026-07-22
---

# Banking.Live Estate Context

This is a reusable estate map for BL/Banking.Live initiatives. It is a
starting catalogue, not a replacement for repository discovery, runtime
inventory, or service-owner confirmation. Individual components have tactical,
legacy, and strategic deployment variants; an HLD must identify which variant
is affected.

## Application components

| Component | Working responsibility/context | Design caution |
| --- | --- | --- |
| PaySwitch | Switching/passthrough gate and transaction-routing boundary in the target direction | Confirm current deployment and scheme-specific routing before reuse |
| PayRoute | Transaction routing component used with PaySwitch and PayPower | Routing and SAF behavior differ between tactical and target models |
| PayPower | Core processing/application logic in the BL data plane | Confirm client isolation, database access, and observability before changes |
| PayKeyService / PayKeyServ | Key and cryptographic-support service used by BL components | Treat key material and certificate flows as security-sensitive; never expose keys to AI context |
| PayAPI | BL API/application boundary and integration surface | Reuse approved API Gateway, Auth0/IMS, read-replica, and telemetry patterns |
| PayScheduler | Job and scheduling application logic, including stored-procedure/job concerns | PayCore coupling and cross-client job isolation require explicit analysis |
| PayControl | Portal/UI and operational control surface for BL | Distinguish public/internal exposure and CHD field filtering |

## Database estate

| Database | Working context | HLD questions |
| --- | --- | --- |
| PayCore | Core Banking.Live operational data and job-related data | CHD classification, client isolation, read/write ownership, migration and reader endpoints |
| PayTok | Tokenization or token-related data used by BL components | Token boundary, key ownership, access policy, retention and residency |
| PayLog | Operational/log or supporting BL data | Whether data belongs in a database or centralized telemetry platform; retention and sensitive data |
| PayKey | Key-service data referenced in local/install documentation | Confirm current name and ownership; do not infer key custody from database presence |

The source material uses both PayKey and PayKeyService naming. Repository and
runtime discovery must resolve the canonical component and database names before
implementation.

## Reuse and modernization rules

- Do not create a new service when the change belongs in an existing BL
  component, shared platform capability, or approved adapter.
- Do not assume a local Docker or installation topology is the production
  target topology.
- Prefer approved RDS/Aurora, Kubernetes, API Gateway, Kafka/MSK, webhook,
  mTLS/PKI, JFrog, and observability platform patterns.
- For cross-component changes, the HLD must map callers, databases, events,
  transactions, deployment units, client boundaries, and rollback behavior.
- For legacy-to-strategic migration, keep the legacy behavior explicit and
  define the target boundary, coexistence approach, and decommission signal.

## Required estate discovery for an initiative

The context assembler should discover:

- affected GitHub repositories and owners;
- current service and database deployment manifests;
- APIs, Kafka topics, webhooks, certificates, and external integrations;
- client/region/CHD classification;
- existing ADRs, runbooks, dashboards, monitors, and recent incidents;
- current versus target/Lume deployment model.

If any of these are unknown, the HLD must record the uncertainty and assign a
human owner rather than inventing a dependency.

## Sources

- [Banking.Live Dockerized Environment](https://paymentology.atlassian.net/wiki/spaces/TS/pages/6762659879/Banking+Live+dockerized+environment)
- [Banking.Live AWS Installation](https://paymentology.atlassian.net/wiki/spaces/TS/pages/6471712798/Installing+Banking.Live+on+AWS+-+Application+Installation)
- [Banking.Live Local Portals Knowhow](https://paymentology.atlassian.net/wiki/spaces/TS/pages/6878461959/Banking.Live+-+PayControl+PayApi+PayCore+etc+-+local+Portals+knowhow)
- [Tactical Transaction Routing](https://paymentology.atlassian.net/wiki/spaces/pa/pages/9872343046/Tactical+Model+-+Transaction+Routing)
- [Lume Deployment Offering Strategy](https://paymentology.atlassian.net/wiki/spaces/pa/pages/9218850872/LUME+-+Deployment+Offering+Strategy)
- [B.L. Strategic Platform 3.0](https://paymentology.atlassian.net/wiki/spaces/TS/pages/8814788609/TECH-709+B.L.+Strategic+Platform+3.0)
