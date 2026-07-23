---
context_id: acs-3ds-apata
context_type: consistent
authority: authentication-and-card-platform-architecture
status: imported-snapshot
owner: 3ds-product-and-implementations
review_cadence: verify-against-3ds-and-partner-team-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7605420568/ACS+Implementation+Guide+Apata+ACS+Provider
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/6990823457/BL+Apata+3DS
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7894368585/3DS+Apata+for+Voucher+Engine+-+Product
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/6958809151/Paymentology+ACS+3DS+Implementation+Guide+for+Issuers
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/8838119570/Implementations+Banking.live+Implementation+Client+Onboarding+Implementation+Checklist
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7087685770/3+DS+-+Guides
retrieved: 2026-07-22
---

# ACS and 3DS: Apata

Apata is the documented strategic ACS partner for Paymentology’s Banking.Live
Pro and Enterprise 3DS capability. It provides Access Control Server capability
for e-commerce authentication, including 3DS1 and 3DS2 support, with
Paymentology remaining responsible for the issuer-processing integration and
client-facing enablement boundary.

## Responsibility model

- Merchant, scheme, issuer, Paymentology, and Apata responsibilities must be
  separated in the HLD.
- Apata performs ACS-side authentication and challenge-related processing.
- Paymentology integrates BL/card lifecycle and authorization data with Apata
  through approved APIs and credentials.
- Client onboarding includes ACS configuration, API/certificate/key exchange,
  UAT testing, and production readiness.
- PayControl and/or approved Paymentology APIs may manage enrollment and card
  3DS lifecycle operations; the exact API must be confirmed for the affected
  product and generation.
- Out-of-band authentication is a distinct flow and requires an explicit
  sequence, callback, failure, and responsibility model.

## Typical BL lifecycle

```text
Card creation or explicit enrollment
  → Paymentology validates request
  → Paymentology calls Apata ACS
  → ACS enrollment/reference is returned
  → 3DS authentication during e-commerce transaction
  → Authentication result returned through scheme/Paymentology flow
  → Authorization and transaction outcome handled by BL
```

The exact protocol, API version, challenge method, encryption, and response
mapping must come from the current Apata contract and the affected BL/VE
implementation. Do not infer production behavior from an old implementation
guide or a Jira issue.

## HLD requirements

Every ACS/3DS design must include:

- 3DS version and scheme scope;
- ACS, issuer processor, client, merchant, and scheme responsibilities;
- enrollment and authentication sequence diagrams;
- API, mTLS/certificate, API-key, and secret lifecycle;
- challenge, frictionless, failure, timeout, retry, and out-of-band paths;
- card/token reference and CHD handling;
- authorization-data feedback or reporting needed by authentication rules;
- UAT certification and partner sign-off;
- monitoring, reconciliation, support, and rollback plan.

## Reuse and partner rules

- Reuse the approved Apata integration boundary for BL Pro and Enterprise
  clients before introducing another ACS provider.
- A different ACS provider requires explicit product, security, partner, and
  architecture review.
- Keep Apata-specific mapping and protocol details behind an adapter or
  integration boundary so the core transaction domain does not become tightly
  coupled to partner-specific behavior.
- Partner credentials, certificates, encrypted PAN, and authentication data
  must be stored only in approved secret and certificate-management systems.

## Sources

- [Apata ACS Implementation Guide](https://paymentology.atlassian.net/wiki/spaces/TS/pages/7605420568/ACS+Implementation+Guide+Apata+ACS+Provider)
- [BL Apata 3DS](https://paymentology.atlassian.net/wiki/spaces/TS/pages/6990823457/BL+Apata+3DS)
- [Apata 3DS for Voucher Engine](https://paymentology.atlassian.net/wiki/spaces/TS/pages/7894368585/3DS+Apata+for+Voucher+Engine+-+Product)
- [Paymentology ACS 3DS Issuer Guide](https://paymentology.atlassian.net/wiki/spaces/TS/pages/6958809151/Paymentology+ACS+3DS+Implementation+Guide+for+Issuers)
- [BL Implementation and Client Onboarding Checklist](https://paymentology.atlassian.net/wiki/spaces/TS/pages/8838119570/Implementations+Banking.live+Implementation+Client+Onboarding+Implementation+Checklist)
- [3DS Guides](https://paymentology.atlassian.net/wiki/spaces/TS/pages/7087685770/3+DS+-+Guides)
