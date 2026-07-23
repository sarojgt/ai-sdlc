---
context_id: lume-strategic-platform
context_type: consistent
authority: platform-strategy
status: imported-snapshot
owner: platform-engineering-and-architecture
review_cadence: verify-against-confluence-before-material-design
source: https://paymentology.atlassian.net/wiki/spaces/PH/pages/9590800386/Lume
retrieved: 2026-07-22
---

# Lume Strategic Platform

Lume is Paymentology's strategic cloud-native, service-driven platform
direction for building, deploying, migrating, and scaling client environments.

## Strategic outcomes

- Cloud-native and service-driven delivery.
- Repeatable, low-error environments.
- Near-zero-downtime release and migration direction.
- Multi-cloud capability and regional hubs for resilience, performance, and
  compliance.
- Fully segregated client data.
- Faster and safer releases and upgrades.
- Independent service scaling and stronger access controls.

## Deployment and migration direction

- New clients are intended to onboard to Lume.
- Existing Banking.Live 2.0 clients are migrated through a structured,
  risk-based process.
- Clients are assigned to regional hubs based on geography, compliance,
  connectivity, performance, and operational considerations.
- Migration planning may include scheme dependencies, shared environments or
  databases, re-carding, tokenization, 3DS providers, cloud provider, seasonal
  activity, and transaction volume.
- UAT and production replication are part of the migration readiness model.

## Client connectivity direction

- mTLS certificates are the preferred modern client connectivity direction.
- Auth0 is identified as the authentication and authorization direction for
  the platform.
- Existing VPN connectivity may remain during transition or where required,
  but it is not the preferred long-term pattern.
- Azure-hosted clients may migrate to AWS or GCP according to the migration and
  regional strategy.

## HLD implications

Lume-related HLDs must identify the target region, client and tenant boundary,
connectivity model, migration path, UAT strategy, downtime or zero-downtime
expectation, and dependencies on platform services. Timeline statements from
the source are program guidance and should not be treated as a delivery
commitment without current program confirmation.

## Source

[Lume Strategic Focus](https://paymentology.atlassian.net/wiki/spaces/PH/pages/9590800386/Lume)
