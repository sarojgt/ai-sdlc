# Proposed ADRs

All records are proposals. No architecture approval is recorded.

## ADR-01 — Existing PayAPI boundary and authorization

- Status: proposed
- Decision: add the versioned collection to existing PayAPI; reuse Gateway/Auth0 validation and the existing IMS client/region authorization helper.
- Constraint: authorization is enforced server-side; no caller-controlled tenancy or portal/BFF decision replaces it.
- Owners: Identity, Platform, Payments, API governance.

## ADR-02 — Existing PayCore access path

- Status: proposed
- Decision: use Option 1, the existing PayAPI-to-PayCore query path, unless PayCore verifies an already-existing read capacity/access abstraction for Option 2.
- Constraint: both options query existing `t_core`; neither creates a service, store, projection, event/CDC pipeline, or alternate source.
- Owners: Payments, PayCore/data owner, Platform, SRE.

## ADR-03 — Card-token filter boundary

- Status: proposed
- Decision: use the approved card-token reference only after Tokenization/Security confirm its exact non-sensitive, non-reversible representation and handling policy.
- Constraint: until approved, do not accept, persist, return, or log raw/reversible token values, PAN, SAD, or raw Apple Pay payloads.
- Owners: Tokenization, Security, Payments.

## ADR-04 — Query and contract bounds

- Status: proposed
- Decision: reuse existing API pagination, error, stable-ordering, maximum date-range, page-size, timeout, and rate-limit conventions; reject invalid bounds before PayCore access.
- Constraint: exact values remain a context gap and must be confirmed before LLD.
- Owners: API governance, Product, PayAPI owner, SRE.

## ADR-05 — BL/Lume deployment reuse

- Status: proposed
- Decision: release the same PayAPI endpoint through the existing BL standard and existing Lume standard where applicable.
- Constraint: region, account/project, data classification, ingress/egress allow-list, and runtime evidence must come from the existing deployment catalogue.
- Owners: Platform, Security, Payments.
