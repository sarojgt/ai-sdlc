---
context_id: service-payswitch
context_type: consistent
authority: service-catalog-and-repository-discovery
status: repository-family
owner: banking-live-switching-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/6762659879/Banking+Live+dockerized+environment
  - https://github.com/Paymentology/payswitch-orchestration
  - https://github.com/Paymentology/payswitch-context
  - https://github.com/Paymentology/payswitch-iso8583-core
retrieved: 2026-08-10
repository_commit: 9bb8159
scan_scope: readme-repository-family-scheme-tooling
---

# PaySwitch

## Service role

Switching and network-integration capability. The Dockerized environment
describes PaySwitch as appearing to PayRoute like a Mastercard MIP or another
configured network and injecting the Common Message Object into the adapted
ISO-8583 message.

## Business capability

PaySwitch represents scheme and network behavior for issuer-processing flows.
It adapts messages and scheme rules across a family of repositories. A change
must identify the exact scheme, adaptor, parser, key path, and deployable unit.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/payswitch-orchestration](https://github.com/Paymentology/payswitch-orchestration) | confirmed family member | Orchestration |
| [Paymentology/payswitch-context](https://github.com/Paymentology/payswitch-context) | confirmed family member | Context/runtime support |
| [Paymentology/payswitch-iso8583-core](https://github.com/Paymentology/payswitch-iso8583-core) | confirmed family member | ISO-8583 core |
| [Paymentology/payswitch-scheme-parser](https://github.com/Paymentology/payswitch-scheme-parser) | confirmed family member | Scheme parsing |
| [Paymentology/payswitch-paypower-adaptor](https://github.com/Paymentology/payswitch-paypower-adaptor) | confirmed family member | PayPower integration |
| [Paymentology/payswitch-pks-adaptor](https://github.com/Paymentology/payswitch-pks-adaptor) | confirmed family member | PKS integration |
| [Paymentology/payswitch-keymanager](https://github.com/Paymentology/payswitch-keymanager) | confirmed family member | Key management |

## Dependencies and boundaries

- PayRoute, network/scheme adapters, CMO, ISO-8583, and cryptographic services
  are related boundaries, not one deployable by default.
- Preserve message compatibility, mTLS/PKI, key custody, and observability.

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | Repository family includes orchestration, ISO-8583 core, scheme parser, and adaptors; primary runtime is not one repository |
| Data stores | No single PaySwitch database ownership confirmed |
| Database connectivity/pool | Unknown; inspect the affected family repository and deployment manifest |
| Communication | ISO-8583 and scheme/network message processing; exact TCP, socket, HTTP, or queue paths are flow-specific |
| Internal dependencies | PayRoute, PayPower adaptor, PKS adaptor, key manager, CMO, and scheme parsers |
| External dependencies | Card schemes, networks, and issuer/processor endpoints are feature-specific |
| Security/observability | mTLS/PKI, key custody, message redaction, correlation, metrics, and operational tracing are required |

## Deployment context

The Dockerized guide includes PaySwitch in the Banking.Live local environment.
Confirm the production/Lume deployment units and regional topology.

## HLD implications

Map the exact repository subset, message flow, scheme boundary, key path,
  deployment units, compatibility, and rollback.

## Scan-confirmed delivery profile

The local scan confirms that `payswitch-orchestration` synchronizes related
repositories and supports scheme onboarding/ingestion tooling. The family
includes ISO8583 core, scheme parser, PayPower and PKS adaptors, key manager,
and context repositories. The primary runtime/deployment repository remains a
change-specific discovery item.

## Scan-confirmed implementation anchors

- `payswitch-orchestration` coordinates the repository family and scheme
  onboarding/ingestion tooling; it is not automatically the runtime owner for
  every PaySwitch change.
- The family separates ISO-8583 core processing, scheme parsing, PayPower and
  PKS adaptors, key management, and shared context. A design must name the
  affected repository subset and deployable units.
- Message changes require compatibility analysis for the Common Message Object,
  ISO-8583 fields, scheme parser behavior, adaptor contracts, and key/certificate
  handling.

These anchors are based on the local family scan and orchestration commit
`9bb8159`; exact runtime configuration, peers, ports, and deployment ownership
remain flow-specific.

## Context gaps

- Confirm the primary runtime repository and deployment manifest for PaySwitch.
