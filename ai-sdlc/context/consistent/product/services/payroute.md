---
context_id: service-payroute
context_type: consistent
authority: service-catalog-and-repository-discovery
status: imported-snapshot
owner: banking-live-switching-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7400423715/Teams+vs+BL+Services
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/6762659879/Banking+Live+dockerized+environment
  - https://github.com/Paymentology/payroute
retrieved: 2026-08-10
repository_commit: baa6db1
scan_scope: readme-build-source-deployment-networking
---

# PayRoute

## Service role

Banking.Live transaction-routing component used with PaySwitch and PayPower.
The Confluence catalogue assigns it to Switching.

## Business capability

PayRoute selects and forwards transaction traffic between Banking.Live
processing components and switching/network boundaries. It is a routing and
transport boundary, not automatically the owner of card state or transaction
data. Changes must preserve message compatibility, routing, retries, and
certificate identity.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/payroute](https://github.com/Paymentology/payroute) | confirmed | Primary service repository |

## Dependencies and boundaries

- Receives or forwards transaction messages through approved switching paths.
- PaySwitch and scheme/network integrations are related but not automatically
  PayRoute-owned.
- Routing, SAF, and client context must be confirmed for the affected flow.

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | Java 21; Maven/Maven Wrapper; Kubernetes Helm chart |
| Data stores | No primary database ownership confirmed from the repository README |
| Database connectivity/pool | Unknown; do not assume PayCore access without configuration evidence |
| Communication | Transaction-routing and network/switching communication; exact HTTP, TCP, socket, or message protocol is flow-specific |
| Internal dependencies | PaySwitch, PayPower, client context, certificates, and shared observability |
| External dependencies | Card/network/scheme endpoints are flow-specific |
| Security/observability | JKS certificates/secrets, NetworkPolicy, pod security, probes, and telemetry are supported by the chart |

## Deployment context

Part of the Banking.Live estate and local Dockerized environment. Confirm the
target Lume/Kubernetes workload and sensitive-data zone.

## HLD implications

Describe message flow, routing decisions, failure handling, replay/SAF,
  security boundary, and observability.

## Scan-confirmed delivery profile

The repository is a Java 21 Helm workload with JFrog images, non-root/pod
security settings, NetworkPolicy, probes, and JKS/certificate configuration.
Actual network protocol, peer list, ports, and persistence are route-specific.

## Scan-confirmed implementation anchors

- The repository is a Java/Maven workload with a Helm deployment and explicit
  certificate/network configuration rather than a domain database model.
- Routing changes should be traced through the PayRoute boundary, PaySwitch
  adaptor or scheme path, PayPower interaction, and configured network peer.
- Certificate identity, NetworkPolicy, pod security, probes, and telemetry are
  part of the deployable contract and must be included in route changes.

These anchors are from commit `baa6db1`; the affected configuration is still
required to confirm peers, ports, protocol, retries, and SAF behavior.

## Context gaps

- Confirm current PaySwitch-to-PayRoute contract and runtime topology.
- Confirm ports, protocol, connection pools, database access, network peers,
  retry/SAF behavior, and certificate identity from affected configuration.
