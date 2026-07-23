---
context_id: disputes-management
context_type: consistent
authority: architecture-review-board
status: imported-snapshot-arb-approved-with-comments
owner: disputes-product-and-engineering
review_cadence: verify-against-confluence-before-material-design
source: https://paymentology.atlassian.net/wiki/spaces/pa/pages/9941025233/SDD+Disputes+Management+System+-+Phase+1+and+2
retrieved: 2026-07-22
---

# Disputes Management Platform

The Disputes Management Platform centralizes the dispute lifecycle across
regional and legacy payment platforms and provides a consistent issuer and
operations experience.

## Reference architecture

- Event-driven ingestion through Kafka.
- A central Dispute Management Service owns the stateful dispute lifecycle.
- A Transaction Query Service abstracts transaction-store search from the UI.
- A Disputes BFF provides the frontend-facing contract.
- A microfrontend integrates the Disputes UI into the strategic portal.
- A Chargeback Worker submits disputes asynchronously through scheme adapters.
- Scheme adapters isolate scheme-specific protocols and integrations.
- A Disputes Sync Service keeps central case state aligned with scheme systems.

## Security and data boundaries

- The central system is designed to operate in a PCI-free environment using
  only essential non-sensitive information.
- Client data remains in-region.
- The source describes row-level client segregation in the database; initiatives
  must confirm whether stronger isolation is required by their risk tier.
- Least privilege, threat modeling, audits, and secure scheme integration are
  required.

## HLD implications

Dispute-related HLDs should preserve the separation between ingestion, case
management, search, frontend/BFF, scheme adapters, and synchronization. They
must describe event contracts, lifecycle ownership, client and regional
boundaries, PCI scope, asynchronous failure handling, and operational recovery.

## Source

[Disputes Management System Phase 1 and 2](https://paymentology.atlassian.net/wiki/spaces/pa/pages/9941025233/SDD+Disputes+Management+System+-+Phase+1+and+2)
