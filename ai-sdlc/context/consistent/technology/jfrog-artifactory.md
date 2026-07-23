---
context_id: jfrog-artifactory
context_type: consistent
authority: engineering-platform
status: imported-snapshot-stable-use-case
owner: maestro-and-engineering-platform
review_cadence: verify-against-confluence-before-material-delivery-decision
source: https://paymentology.atlassian.net/wiki/spaces/PP/pages/8374616338/SDLC+Use+Case+-+store+binaries+in+JFrog+Platform
retrieved: 2026-07-22
---

# JFrog Platform and Artifactory

JFrog Platform is the strategic binary repository for application artifacts,
including container images, Helm charts, and language packages. Xray provides
security and quality scanning in the artifact workflow.

## Delivery conventions

- Branch and PR builds publish to snapshot repositories.
- Git tag builds publish to release repositories.
- A JFrog Project Build should register all deployable artifacts for a version.
- Production CD should use the Release Artifact Assurance process.
- Runtime environments should pull from the approved JFrog virtual repository,
  such as the production Docker virtual repository.

## Authentication and ownership

- GitHub Actions should use the approved OIDC-based JFrog token action or the
  supported JFrog CLI action.
- Do not hard-code Artifactory credentials in repositories or workflow files.
- Repository enablement and project assignment are governed through the
  platform/Maestro process.

## HLD implications

Implementation and deployment designs should define artifact repositories,
snapshot/release promotion, image and Helm-chart provenance, Xray checks,
retention, rollback artifacts, and the platform ownership needed to enable a
repository.

## Source

[SDLC Use Case - store binaries in JFrog Platform](https://paymentology.atlassian.net/wiki/spaces/PP/pages/8374616338/SDLC+Use+Case+-+store+binaries+in+JFrog+Platform)
