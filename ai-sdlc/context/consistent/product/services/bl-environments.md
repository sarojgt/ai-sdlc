---
context_id: platform-banking-live-environments
context_type: consistent
authority: release-platform-and-repository-discovery
status: imported-snapshot
owner: banking-live-release-platform
review_cadence: verify-against-repository-and-release-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/6975914067/Banking.Live+Release+Management
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/6762659879/Banking+Live+dockerized+environment
  - https://github.com/Paymentology/bl-environments
retrieved: 2026-08-10
repository_commit: 2ec927d
scan_scope: readme-actions-helm-terraform-environments-release
---

# Banking.Live Environments

## Service role

Environment and release configuration for the Banking.Live component estate.
The Dockerized guide states that concrete component versions are controlled by
the `bl-environments` repository.

## Business capability

BL Environments is the controlled promotion and deployment boundary for
Banking.Live. It selects compatible component versions and deploys them to a
named environment/client. It does not define application behavior; changes
arrive after application/database artifacts and approvals.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/bl-environments](https://github.com/Paymentology/bl-environments) | confirmed | Environment manifests and release selection |

## Dependencies and boundaries

- Coordinates versions of PayAPI, PayPower, PayScheduler, PayCore DB, PayTok DB,
  PayControl, PayKeyServ, PayRoute, PayLog DB, and related components.
- It is an orchestration/configuration boundary, not the owner of application
  behavior.
- Do not modify environment manifests before the approved HLD/LLD and release
  gates.

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | GitHub Actions, Helm, Terraform, and environment configuration rather than an application runtime |
| Data stores | No application database ownership; deployment state is held by Kubernetes/Helm and platform systems |
| Database connectivity/pool | Not applicable to the environment repository |
| Communication | GitHub Actions, container registry, Kubernetes API, Helm, Terraform, and service endpoints during deployment |
| Internal dependencies | PayAPI, PayPower, PayRoute, PayScheduler, PayControl, database components, and environment manifests |
| External/platform dependencies | AWS is current Terraform scope; GCP remains an extension point; JFrog/container registry is used |
| Security/observability | GitHub environments, protected approvals, secrets, deployment evidence, rollout health, and rollback history are required |

## Deployment context

Supports Banking.Live development, test, UAT, production, and local Dockerized
variants. Confirm BL2 versus Lume, region, client model, and sensitive zone.

## HLD implications

Map component versions, environment promotion, compatibility, rollback,
secrets, deployment ownership, and regional/client impact.

## Scan-confirmed delivery profile

The local scan confirms GitHub Actions workflows for dry-run/deploy operations,
environment and client inputs, service selection, Helm/Terraform configuration,
JFrog images, Kubernetes deployment, approvals, rollout health, and rollback.

## Context gaps

- Confirm the current release manifest and environment branch for each change.
- Confirm whether Lume uses this repository directly or a separate platform
  orchestration path.
