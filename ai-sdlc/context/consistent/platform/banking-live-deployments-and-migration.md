---
context_id: banking-live-deployments-and-migration
context_type: consistent
authority: banking-live-platform-and-lume-strategy
status: imported-snapshot
owner: banking-live-platform-and-migration
review_cadence: verify-against-current-environment-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/pa/pages/9218850872/LUME+-+Deployment+Offering+Strategy
  - https://paymentology.atlassian.net/wiki/spaces/PH/pages/9590800386/Lume
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7824244738/Banking+Live+Release+Cycle
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/8680505532/Production+Environment+Component+Versions
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7588348005/BL+Platform+-+Client+Environments
  - https://paymentology.atlassian.net/wiki/spaces/pa/pages/9870344196/Approach+BL+2.0+to+Lume+Client+Migration
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/9960948009/Migration+Strategy+e2e
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/9952460858/Migration+strategy+Bl2+Lume
retrieved: 2026-07-22
---

# Banking.Live Deployments, Environments, and Migration

Banking.Live has a supported legacy estate and a strategic Lume estate. AI
must not collapse them into one deployment model.

## Strategic direction

- New clients and new platform capabilities should target Lume.
- Existing BL2 clients remain supported until their migration is planned,
  approved, executed, and accepted.
- BL2 support work is valid when required for client operations, regulatory or
  scheme commitments, incidents, security, or migration readiness.
- New feature work for BL2 should normally be treated as a compatibility,
  maintenance, or migration-enablement decision rather than the default target
  architecture.
- A design affecting both estates must define the common contract, coexistence
  period, migration path, and retirement signal.

## BL2 / legacy deployment models

The legacy offering has at least two important client service models:

| BL2 model | Typical meaning | Design implications |
| --- | --- | --- |
| Professional / shared | Multiple clients hosted on a shared Banking.Live instance or shared environment | Shared application/runtime and often shared data topology; client boundaries, noisy-neighbor behavior, release coordination, and migration sequencing are critical |
| Enterprise / dedicated | Client-specific or dedicated application/environment resources | Stronger isolation and client-specific release/access needs; confirm exactly which compute, database, scheme, HSM, DR, and network components are dedicated |

The legacy estate may include AWS, Azure, OCI, and other historical footprints.
The current target platform direction favors AWS and GCP regional hubs, but
legacy client support and migration may require continued operation and
connectivity to older platforms.

## Environment lifecycle

The environment names and inventory vary by platform and client. The common
delivery progression is:

```text
Development → Stage/QA → UAT → OAT/Pre-production → Production → DR
```

BL documentation also references shared UAT, dedicated UAT, shared production,
dedicated production, inactive environments, and client-specific environments.
The exact environment must be resolved from the current environment catalog;
AI must not infer it from a hostname or branch name alone.

Every environment reference should identify:

- platform generation: BL2 or Lume;
- cloud/provider and region;
- shared or dedicated classification;
- client or client group;
- CHD/Common Workload zone;
- application and database versions;
- deployment repository and configuration branch;
- access, VPN, mTLS, API hostname, and portal endpoint;
- backup, DR, monitoring, and support owner.

## Lume offering models

The Lume offering is graduated rather than a single topology:

| Lume tier | Default deployment direction |
| --- | --- |
| Professional | Shared compute and platform services with a dedicated logical client database; tactical client-specific compute may be used temporarily |
| Enterprise | Dedicated compute/workload boundary, database cluster, and selected middleware; shared network hub and portals may remain |
| Enterprise Plus | Dedicated network hub, compute, database, middleware, scheme connectivity, HSM, and DR where required |

Shared observability, CI/CD, artifact repositories, security tooling, and
platform management may remain shared. The HLD must state every shared and
dedicated boundary instead of describing a tier as simply “shared” or
“dedicated.”

## Migration model

BL2-to-Lume migration is a client/environment transformation, not only an
application deployment. Depending on the client, it may require:

- source database extraction, full load, CDC, replication, and staging;
- migration from shared BL2 data into isolated Lume data;
- client hierarchy and tenant mapping;
- scheme, HSM, tokenization, 3DS, SFTP, and partner connectivity changes;
- UAT and production parity/readiness;
- cutover, rollback, reconciliation, and post-migration support;
- coexistence of shared and dedicated environments while the back book is
  migrated.

For hierarchy-based clients, migration must be treated as a coordinated tenant
migration rather than independent row or client moves. For shared environments,
the final client may require a special extraction and cleanup plan after other
clients have migrated.

## AI SDLC decision rules

At requirement intake, the context assembler must classify the initiative as
one or more of:

- `lume-greenfield`: new client or new capability targeting Lume;
- `bl2-support`: legacy maintenance, security, incident, scheme, or client
  support;
- `migration-enablement`: changes required to make a client or environment
  migratable;
- `coexistence`: shared contracts or operations spanning BL2 and Lume;
- `platform-modernization`: replacement of legacy infrastructure or deployment
  capability.

The HLD must then include:

- target generation and source generation;
- current environment and target environment;
- Pro/Professional, Enterprise, or Enterprise Plus classification;
- shared/dedicated resource matrix;
- client data and CHD boundary;
- cloud, region, network, identity, certificate, and endpoint model;
- release and version compatibility;
- migration, coexistence, rollback, and retirement plan;
- explicit reason if new functionality must be added to BL2.

## Sources

- [Lume Deployment Offering Strategy](https://paymentology.atlassian.net/wiki/spaces/pa/pages/9218850872/LUME+-+Deployment+Offering+Strategy)
- [Lume Strategic Focus](https://paymentology.atlassian.net/wiki/spaces/PH/pages/9590800386/Lume)
- [Banking.Live Release Cycle](https://paymentology.atlassian.net/wiki/spaces/TS/pages/7824244738/Banking+Live+Release+Cycle)
- [Production Environment Component Versions](https://paymentology.atlassian.net/wiki/spaces/TS/pages/8680505532/Production+Environment+Component+Versions)
- [BL Platform Client Environments](https://paymentology.atlassian.net/wiki/spaces/TS/pages/7588348005/BL+Platform+-+Client+Environments)
- [BL2 to Lume Client Migration](https://paymentology.atlassian.net/wiki/spaces/pa/pages/9870344196/Approach+BL+2.0+to+Lume+Client+Migration)
- [Lume Migration Strategy](https://paymentology.atlassian.net/wiki/spaces/TS/pages/9960948009/Migration+Strategy+e2e)
- [BL2 to Lume Migration Architecture](https://paymentology.atlassian.net/wiki/spaces/TS/pages/9952460858/Migration+strategy+Bl2+Lume)
