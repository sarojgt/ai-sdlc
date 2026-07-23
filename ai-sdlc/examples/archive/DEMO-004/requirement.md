---
das_version: "0.1"
artifact:
  id: "REQ-DEMO-004"
  type: requirement
  version: 1
  status: approved
  title: "Client-scoped Banking.Live transaction status webhooks"
  initiative: "DEMO-004"
  owner: "team.banking-live"
source:
  provider: "github"
  work_item_id: "DEMO-004"
traceability:
  parents: ["github:DEMO-004"]
policy:
  risk_tier: "medium"
---

# Requirement: Client-scoped Banking.Live transaction status webhooks

## Business outcome

Give Banking.Live clients reliable, near-real-time transaction status
notifications without requiring continuous polling of PayAPI, while reusing
the enterprise Webhook Platform.

## Problem statement

Clients currently need to poll transaction status or implement product-specific
notification integrations. This creates unnecessary API traffic and makes
delivery, retry, authorization, and operational visibility inconsistent.

## Functional requirements

<!-- Use REQ-DEMO-004-NN identifiers. -->

### REQ-DEMO-004-01

The solution must publish an approved, client-scoped transaction status event
when a relevant Banking.Live transaction state changes.

### REQ-DEMO-004-02

The solution must use the shared Webhook subscription and orchestration
capability for subscription management, delivery, retries, and delivery status.

### REQ-DEMO-004-03

Subscription management must use the approved API Gateway, Auth0, and IMS
authorization model for the selected client and region.

### REQ-DEMO-004-04

Webhook payloads must contain only approved tokenized or reference data and
must not expose PAN, SAD, private keys, tokens, or unrestricted production
payloads.

## Non-functional requirements

- Delivery must be idempotent and use a stable event identity.
- Retry, dead-letter, reconciliation, and manual recovery behavior must be
  bounded and observable.
- The design must support the current BL estate and identify the Lume target
  path for new capability work.
- Logs, metrics, and traces must follow the shared observability context.

## Acceptance criteria

- Given an eligible transaction status change and an active subscription, the
  shared Webhook Platform receives the approved event.
- Given a transient client endpoint failure, the shared orchestrator retries
  using the approved bounded policy and records delivery state.
- Given an unauthorized subscription request, API Gateway/IMS denies it for
  the selected client context.
- Given a CHD-sensitive source event, the published event contains only approved
  non-sensitive data or references.
- Given repeated delivery, the client can deduplicate using the stable event
  identity.

## Assumptions and open questions

- Which Banking.Live component is the authoritative producer for each status?
- What are the required retention periods for delivery history and dead letters?
- Which client webhook authentication and signing standard is mandatory?
- Does the BL2 path require an adapter while the Lume path uses the strategic
  event boundary?

## Business approval

Product Owner: demo-product-owner@example.com  
Decision: approved for HLD generation  
Date: 2026-07-22  
Note: Demonstration requirement selected to exercise Webhook Platform,
Banking.Live/Lume, Auth0/IMS, CHD/Common Workload, and observability context.
