---
context_id: mtls-and-zero-touch-pki
context_type: consistent
authority: security-and-platform-architecture
status: imported-snapshot
owner: security-and-platform-engineering
review_cadence: verify-against-confluence-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/pa/pages/8662712353/SDD+Client+Certificate+Management+PKI
  - https://paymentology.atlassian.net/wiki/spaces/pa/pages/8654946494/SDD+FAST+Manager
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/9657679884/Tactical+Internal+TLS+Certificates+for+Kubernetes
  - https://paymentology.atlassian.net/wiki/spaces/PH/pages/9590800386/Lume
retrieved: 2026-07-22
---

# mTLS and Zero Touch PKI

Mutual TLS is the preferred modern pattern for trusted client, partner, and
service connectivity where transport-level identity is required. Venafi Zero
Touch PKI is the documented cloud PKI direction for automated certificate
issuance and lifecycle management.

## Use mTLS when

- a client or partner must prove possession of a certificate before an API
  connection is accepted;
- a service-to-service channel needs cryptographic workload identity in
  addition to application authorization;
- a private or regional connection must be restricted to approved clients;
- a legacy VPN or static trust model is being replaced by certificate-based
  connectivity.

mTLS authenticates the connecting party at the transport layer. It does not
replace Auth0 user authentication or IMS authorization. The HLD must show
both layers when both are required.

## Certificate lifecycle

- The client or workload generates a key pair and CSR according to the
  approved onboarding pattern.
- Zero Touch PKI issues the client certificate from the approved CA hierarchy.
- Certificate authorities, revocation lists, renewal, expiry, and rotation are
  managed through the PKI lifecycle rather than manually copied into services.
- Private keys must remain in the owning client or approved secret-management
  boundary; do not place keys in Git, container images, logs, or AI context.
- Kubernetes certificate automation must use the approved platform integration
  and short-lived certificate principles where supported.

## HLD requirements

Every mTLS design must define:

- client and server identity;
- trust anchor and CA ownership;
- certificate issuance and CSR path;
- certificate storage and key access;
- renewal, rotation, revocation, and outage behavior;
- gateway/load-balancer termination point;
- whether mTLS is end-to-end or terminated and re-established;
- mapping from certificate identity to client, tenant, region, or service;
- observability without exposing private keys or certificate-sensitive data.

## Relationship to Auth0 and IMS

For a portal or API, mTLS may establish that a client system is trusted, while
Auth0 establishes the human or application identity and IMS resolves effective
permissions. A valid certificate is not permission to perform every business
operation.

## Sources

- [Client Certificate Management / PKI](https://paymentology.atlassian.net/wiki/spaces/pa/pages/8662712353/SDD+Client+Certificate+Management+PKI)
- [FAST Manager](https://paymentology.atlassian.net/wiki/spaces/pa/pages/8654946494/SDD+FAST+Manager)
- [Internal TLS Certificates for Kubernetes](https://paymentology.atlassian.net/wiki/spaces/TS/pages/9657679884/Tactical+Internal+TLS+Certificates+for+Kubernetes)
- [Lume](https://paymentology.atlassian.net/wiki/spaces/PH/pages/9590800386/Lume)
