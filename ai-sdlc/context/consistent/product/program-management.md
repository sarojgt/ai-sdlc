---
context_id: program-management
context_type: consistent
authority: product-and-architecture
status: imported-snapshot
owner: program-management-product-and-engineering
review_cadence: verify-against-confluence-before-material-design
source: https://paymentology.atlassian.net/wiki/spaces/pa/pages/8811282674/Program+Management+Solution+Design
retrieved: 2026-07-22
---

# Program Management Platform

The Program Management Platform replaces a complex legacy Acorn/FlexPay
monolith with a modular platform for client, program, product, card, ledger,
fee, and sponsor-bank capabilities.

## Responsibilities and boundaries

- Operates as a FAST client to Banking.Live for payment processing and scheme
  integration.
- Triggers card-issuing processes through Banking.Live.
- Owns client configuration, product propositions, specialized integrations,
  and client-specific reporting.
- Introduces a Debit Ledger based on double-entry bookkeeping principles.
- Uses a data platform for reporting and analytics instead of overloading the
  operational database.
- Uses an orchestration layer for cross-platform integrations.
- Provides a sponsor-bank integration hub for payment instructions and bank-
  level integrations.
- Avoids handling PCI-sensitive PAN data where Banking.Live can provide safe
  card references instead.

## Architecture patterns

- Independent microservices with clear ownership and autonomous deployment.
- Database ownership by service rather than a shared tightly coupled model.
- API-first contracts.
- Kubernetes/EKS for horizontal scaling.
- Resilience and fault isolation between capabilities.
- API Hub enforcement and adapters for legacy Acorn SOAP/REST compatibility.

## HLD implications

An HLD affecting Program Management must identify the FAST boundary, Banking.Live
contract, card-issuing flow, ledger ownership, client/product model, API Hub or
adapter requirements, data-platform boundary, and PCI-data handling model.

## Source

[Program Management Solution Design](https://paymentology.atlassian.net/wiki/spaces/pa/pages/8811282674/Program+Management+Solution+Design)
