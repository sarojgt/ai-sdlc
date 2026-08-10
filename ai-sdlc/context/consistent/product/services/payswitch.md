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
---

# PaySwitch

## Service role

Switching and network-integration capability. The Dockerized environment
describes PaySwitch as appearing to PayRoute like a Mastercard MIP or another
configured network and injecting the Common Message Object into the adapted
ISO-8583 message.

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

## Deployment context

The Dockerized guide includes PaySwitch in the Banking.Live local environment.
Confirm the production/Lume deployment units and regional topology.

## HLD implications

Map the exact repository subset, message flow, scheme boundary, key path,
deployment units, compatibility, and rollback.

## Context gaps

- Confirm the primary runtime repository and deployment manifest for PaySwitch.
