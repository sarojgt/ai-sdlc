---
context_id: tokenization-and-token-service-partners
context_type: consistent
authority: tokenization-and-card-platform-architecture
status: imported-snapshot
owner: tokenization-product-and-implementations
review_cadence: verify-against-tokenization-and-partner-teams-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/8120696857/Implementations+Training+guide+Tokenization+using+Meawallet+OBO+Service+for+internal+use
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/6996754454/PTY+Tokenization+x+MeaWallet+API+Overview
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/6996328580/BL+MeaWallet+Tokenisation+API
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7339048976/BL+MADA+Tokenization+Implementation
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7569702913/Steps+to+Implement+a+Pro+and+Enterprise+Tokenization+Project
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/6577455271/Tokenization+Projects+Roll+Out
retrieved: 2026-07-22
---

# Tokenization and Token-Service Partners

Tokenization is a multi-party capability. A design must distinguish
Paymentology issuer-processing responsibilities, the token service provider,
the integration/token platform, the client application, and scheme ownership.

## Ecosystem and boundaries

- Mastercard MDES and Visa VTS are scheme token service providers (TSPs).
- MeaWallet is documented as an issuer token service platform/iTSP and a
  strategic integration partner for tokenization flows.
- Paymentology services expose approved tokenization and token-lifecycle
  capabilities to BL, Voucher Engine, portals, and implementation teams.
- PayTok is part of the BL token-related data estate; its exact current data
  ownership and CHD classification must be confirmed for each design.
- Clients may require token lifecycle management, digitization, push
  provisioning, device binding, suspend/unsuspend, update, delete, and
  enrollment flows.
- Other partners may be required for scheme-specific or push-provisioning
  scenarios. The HLD must identify the partner and contract rather than
  assuming MeaWallet covers every scheme or use case.

## Security and data handling

Tokenization designs are CHD-sensitive. They must define:

- PAN/fPAN and token/dPAN boundaries;
- where encryption, decryption, mapping, and key custody occur;
- client, Paymentology, MeaWallet, and scheme responsibilities;
- API, mTLS, certificate, pre-shared-key, and secret-management requirements;
- token reference versus raw card data in logs, events, databases, and AI
  context;
- data residency, retention, replay, idempotency, and audit requirements.

Private keys, pre-shared keys, encrypted PAN, raw PAN, and production token
payloads must not be included in AI context or repository documentation.

## Reuse and integration rules

- Reuse approved tokenization APIs, PayTok integration patterns, partner
  adapters, and portal lifecycle capabilities before creating new token logic.
- Keep scheme-specific behavior behind the approved integration boundary.
- Do not make a portal or product directly depend on scheme APIs when the
  Paymentology tokenization boundary already provides the required capability.
- Partner APIs and callbacks must define authentication, idempotency, timeout,
  retry, reconciliation, webhook/event behavior, and support ownership.

## HLD requirements

Every tokenization HLD must include:

- sequence diagrams for enrollment and lifecycle operations;
- actor and responsibility matrix;
- data-flow and CHD boundary diagram;
- scheme and partner contracts;
- token/PAN storage and key lifecycle;
- failure, retry, reconciliation, and manual support process;
- UAT certification and production rollout plan;
- observability without sensitive data exposure;
- migration and backward compatibility for existing clients.

## Sources

- [Tokenization using MeaWallet OBO](https://paymentology.atlassian.net/wiki/spaces/TS/pages/8120696857/Implementations+Training+guide+Tokenization+using+Meawallet+OBO+Service+for+internal+use)
- [Paymentology Tokenization and MeaWallet API Overview](https://paymentology.atlassian.net/wiki/spaces/TS/pages/6996754454/PTY+Tokenization+x+MeaWallet+API+Overview)
- [BL MeaWallet Tokenisation API](https://paymentology.atlassian.net/wiki/spaces/TS/pages/6996328580/BL+MeaWallet+Tokenisation+API)
- [BL MADA Tokenization](https://paymentology.atlassian.net/wiki/spaces/TS/pages/7339048976/BL+MADA+Tokenization+Implementation)
- [Pro and Enterprise Tokenization Project](https://paymentology.atlassian.net/wiki/spaces/TS/pages/7569702913/Steps+to+Implement+a+Pro+and+Enterprise+Tokenization+Project)
- [Tokenization Project Rollout](https://paymentology.atlassian.net/wiki/spaces/TS/pages/6577455271/Tokenization+Projects+Roll+Out)
