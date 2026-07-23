---
das_version: "0.1"
artifact:
  id: "REQ-DEMO-005"
  type: requirement
  version: 2
  status: approved
  title: "Apple Pay transaction listing API"
  initiative: "DEMO-005"
  owner: "team.payments"
source:
  provider: "github"
  work_item_id: "DEMO-005"
traceability:
  parents: ["github:DEMO-005"]
policy:
  risk_tier: "medium"
---

# Requirement: Apple Pay transaction listing API

## Business outcome

Enable client-facing consumers to retrieve Apple Pay transactions through the
existing PayAPI boundary without creating a new transaction source or exposing
sensitive card data.

## Problem statement

Consumers need a governed PayAPI endpoint that can search the existing PayCore
transaction data for Apple Pay activity. The endpoint is an addition to PayAPI;
it must reuse the existing PayCore database, client-facing API security, and
the normal deployment standard for the target BL or Lume environment.

## Users, consumers, and stakeholders

| Group | Need or responsibility | Priority |
|---|---|---|
| Authorized client consumers | Retrieve Apple Pay transaction summaries | Must |
| Payments/Product | Define the business outcome and response fields | Must |
| PayAPI and PayCore owners | Confirm route, source schema, query path, and capacity | Must |
| Identity, Security, Platform, and SRE | Confirm authorization, data handling, and operational standards | Must |

## Desired user or system outcome

An authorized client can search its Apple Pay transactions by approved token
reference and date range through the existing API boundary, with bounded results
and no sensitive data leakage.

## Scope

### In scope

- One read endpoint in the existing PayAPI.
- Existing PayCore `t_core` transaction source.
- Apple Pay, token, date, client, and regional filtering.
- Existing security, observability, and BL/Lume release patterns.

### Out of scope

- New service, database, read model, event pipeline, tokenization flow, or BFF.
- New authentication or authorization mechanism.
- PayCore schema migration unless separately approved after evidence review.

## Data and integration considerations

- Known source: PayCore `t_core`; exact columns require confirmation.
- Known internal integrations: API Gateway, Auth0/IMS, PayAPI, and PayCore.
- New external integrations: none currently identified.
- Sensitive data: card-token references and transaction data; handling policy must
  be confirmed before LLD.
- Client, regional, and deployment boundaries must reuse existing standards.

## Constraints and approved patterns

- Use existing PayAPI client-facing API and authorization patterns.
- Use existing PayCore data access patterns where verified.
- Use the existing BL standard or Lume standard for the target deployment.
- Do not introduce a new source or platform component for this addition.

## Confirmed implementation direction

- Add the endpoint to PayAPI.
- Query the existing PayCore database and `t_core` transaction table.
- Identify Apple Pay transactions using `wallet = APPLE_PAY`.
- Support filtering by an approved card-token reference and date range.
- Reuse existing PayAPI authentication, authorization, client isolation,
  regional routing, observability, and deployment patterns.
- Do not create a new service, event feed, projection, database, tokenization
  flow, or portal BFF for this addition.
- Deploy the same endpoint through the existing BL standard for BL environments
  and the existing Lume standard for Lume environments.

## Functional requirements

<!-- Use REQ-DEMO-005-NN identifiers. -->

### REQ-DEMO-005-01

The solution must add an authenticated client-facing PayAPI endpoint that lists
Apple Pay transactions for an authorized client and region context.

### REQ-DEMO-005-02

The endpoint must query PayCore `t_core` and apply `wallet = APPLE_PAY`, an
approved card-token reference filter, and an inclusive date/time range.

### REQ-DEMO-005-03

The response must use the approved API contract, pagination, stable ordering,
and a bounded maximum date-range and page size.

### REQ-DEMO-005-04

The endpoint must enforce the approved API Gateway, Auth0, and IMS
authentication and authorization model, including client and regional data
isolation.

### REQ-DEMO-005-05

The response and telemetry must exclude PAN, SAD, authentication headers,
secrets, private keys, and unrestricted production payloads. Card-token values
must be handled according to the approved tokenization policy.

## Non-functional requirements

- Query latency and throughput targets must be confirmed before LLD.
- Queries must use bounded filters and avoid unbounded scans or cross-client
  access.
- The design must use the existing PayCore `t_core` source and identify the
  required query indexes or existing access path; it must not introduce a new
  read model for this addition.
- Existing PayAPI client-facing authorization, regional isolation,
  observability, and BL/Lume deployment patterns are reused.
- Logs, metrics, traces, audit events, and errors must follow shared
  observability and secure-logging standards.

## Acceptance criteria

- Given an authorized client and valid date range, the API returns only
  Apple Pay transactions in the authorized client and region scope.
- Given an approved card-token filter, the API returns only matching Apple Pay
  transactions without exposing the raw token or PAN.
- Given an invalid, excessive, or missing date range, the API returns a safe
  validation error and does not perform an unbounded query.
- Given an unauthorized client or region, the API denies access and does not
  reveal transaction existence.
- Given a paginated request, repeated requests with the same cursor contract
  provide stable, bounded results.

## Assumptions and open questions

- What is the exact PayAPI route/version and existing controller/service/repository
  package where the endpoint belongs?
- What is the exact `t_core` column name and approved representation for the
  card-token reference?
- What are the maximum date range, page size, latency, retention, and
  consistency requirements?
- What existing PayAPI pagination, error envelope, authorization helper, query
  index, and observability conventions must the implementation follow?

## Initial impact hints

| Dimension | Initial view | Confidence / notes |
|---|---|---|
| Expected change size | Medium | One existing API, no new platform component |
| Expected complexity/risk | Moderate | Client-facing transaction data and query performance |
| Services/repositories | PayAPI; PayCore dependency | Exact repository paths require confirmation |
| Internal integrations | Gateway, Auth0/IMS, PayCore | Existing patterns should be reused |
| External integrations | None currently identified | Verify during context discovery |
| Data/security impact | Moderate | Token and transaction data handling must be verified |
| Deployment/migration impact | Low / no migration expected | Reuse BL/Lume deployment patterns |

## Business approval

Product Owner: demo-product-owner@example.com  
Decision: approved for HLD generation  
Date: 2026-07-22  
Note: Business approval covers a PayAPI addition using the existing PayCore
`t_core` source and existing BL/Lume deployment patterns. It does not approve
new architecture, implementation, or production release.
