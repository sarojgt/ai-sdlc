# Initiative-relative implementation context

## Confirmed feature boundary

This initiative adds a client-facing read endpoint to the existing PayAPI.
It is not a new service or platform capability.

## Confirmed source and query

- Source system: PayCore.
- Source table: `t_core`.
- Apple Pay predicate: `wallet = APPLE_PAY`.
- Additional filters: approved card-token reference and inclusive date range.
- The endpoint must use the existing PayAPI-to-PayCore access pattern.
- Do not create a projection, event/CDC pipeline, new database, or token
  service for this feature.

## Consumer and deployment

- The endpoint is client-facing through PayAPI.
- Existing PayAPI authentication, authorization, client isolation, regional
  routing, rate limiting, observability, and error conventions are mandatory.
- New capability targets Lume where applicable.
- Existing BL clients remain supported and the endpoint must deploy using the
  existing BL standard when enabled for BL environments.
- BL and Lume are runtime variants of the same PayAPI feature, not separate
  HLD architectures.

## Context gaps to resolve before LLD

- Exact PayAPI route and API version.
- Existing PayAPI package/controller/service/repository location.
- Exact `t_core` column names and approved card-token representation.
- Existing indexes/query plans and maximum safe date range/page size.
- Existing authorization helper and client/region predicate implementation.
- Required response fields, pagination contract, error envelope, SLOs, and
  production rollout owner.

These gaps must be filled from the PayAPI/PayCore repositories and approved
standards before LLD; they must not be replaced with a new architecture.
