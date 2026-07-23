# Consistent Architecture Context

Add shared architecture knowledge here, for example:

- Architecture principles
- Approved technology stack
- API and event standards
- Integration patterns
- Cloud and platform patterns
- Reference architectures
- Approved ADRs and reusable design patterns
- Authentication, authorization, mTLS, PKI, portal exposure, and CHD/Common
  Workload zone boundaries

The current imported architecture baseline includes target-platform direction,
AWS/GCP positioning, Kubernetes and regional deployment guidance, API
standards, client data isolation, and Lume deployment models. Each imported
document links to its Confluence source and identifies whether it is approved,
current guidance, or WIP. Identity and security-sensitive context is split
into authentication/authorization, mTLS/PKI, and CHD/Common Workload zone
documents so the context assembler can include only what a design needs.
