---
context_id: chd-and-common-workload-zones
context_type: consistent
authority: cloud-security-and-platform-architecture
status: imported-snapshot
owner: security-and-platform-engineering
review_cadence: verify-against-confluence-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/PP/pages/9493479521/Cloud+Strategy+2025+-+Network+Connectivity+Patterns
  - https://paymentology.atlassian.net/wiki/spaces/SEC/pages/8610250890/Security+Segmentation+requirements+for+PCI+and+non-PCI+zones
  - https://paymentology.atlassian.net/wiki/spaces/pa/pages/8408105033/Cloud+Strategy+-+Principles
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/9781575686/howto+Create+and+connect+to+AWS+RDS+DB
  - https://paymentology.atlassian.net/wiki/spaces/pa/pages/8654946494/SDD+FAST+Manager
retrieved: 2026-07-22
---

# CHD and Common Workload Zones

The platform separates cardholder-data workloads from non-PCI/common workload
components. Names vary across documents, including CHD, PCI, CDE, red zone,
Common Workload, Common Zone, and CW. HLDs should use the current platform
environment naming and explicitly state the mapping.

## Zone model

- The CHD/PCI/CDE zone hosts workloads and data that process or store
  cardholder data and therefore require the PCI security boundary.
- The Common Workload (CW) zone hosts non-CHD shared services and workloads
  that do not require the same PCI boundary.
- A workload must not be placed in CW merely because it does not currently
  read PAN; its logs, caches, backups, traces, messages, support tooling, and
  third-party dependencies must also be assessed.
- CHD and non-CHD workloads are isolated by account/project, VPC/network,
  cluster, namespace, data store, identity, and access controls as required by
  the approved platform pattern.

## Connectivity direction

Cross-zone connectivity is an explicit architecture decision. The documented
pattern allows controlled, authenticated flows such as Banking.Live in CHD
calling approved non-CHD services in CW. The HLD must define direction,
allow-list, protocol, gateway, data classification, tokenization/redaction,
failure behavior, and monitoring.

Do not assume bidirectional network access. Do not send CHD to common services
unless the data flow is explicitly approved. Prefer tokenized or reference data
for downstream non-PCI services.

## Data and database placement

- An RDS/Aurora or equivalent database containing CHD must be deployed in the
  CHD boundary and selected using the approved environment naming convention.
- Non-CHD databases belong in the Common Workload boundary unless a stronger
  isolation requirement applies.
- Database, object storage, event, backup, observability, and support-data
  placement must be assessed together.
- Public or non-PCI portals must not expose CHD fields by default. Filtering
  and response shaping must be enforced at the approved API/BFF boundary.

## AI SDLC guardrails

The context assembler must:

- classify the initiative and every affected repository or data store as CHD,
  non-CHD, or unknown;
- exclude PAN, SAD, secrets, private keys, tokens, production payloads, and
  unrestricted logs from AI prompts;
- include this context for initiatives affecting Banking.Live, payment
  processing, RDS/Aurora, network routes, portals, APIs, or observability;
- require security review when the zone or data classification is unknown;
- require the HLD to show a data-flow diagram crossing or staying within zones.

## HLD requirements

Every affected HLD must state:

- zone and account/project for each component;
- CHD data elements and classification;
- storage, backup, event, cache, log, and observability boundaries;
- ingress and egress paths;
- network and identity controls;
- tokenization or redaction strategy;
- PCI/security review and evidence required before implementation.

## Sources

- [Cloud Strategy: Network Connectivity Patterns](https://paymentology.atlassian.net/wiki/spaces/PP/pages/9493479521/Cloud+Strategy+2025+-+Network+Connectivity+Patterns)
- [PCI and Non-PCI Segmentation Requirements](https://paymentology.atlassian.net/wiki/spaces/SEC/pages/8610250890/Security+Segmentation+requirements+for+PCI+and+non-PCI+zones)
- [Cloud Strategy Principles](https://paymentology.atlassian.net/wiki/spaces/pa/pages/8408105033/Cloud+Strategy+-+Principles)
- [Create and Connect to AWS RDS](https://paymentology.atlassian.net/wiki/spaces/TS/pages/9781575686/howto+Create+and+connect+to+AWS+RDS+DB)
- [FAST Manager](https://paymentology.atlassian.net/wiki/spaces/pa/pages/8654946494/SDD+FAST+Manager)
