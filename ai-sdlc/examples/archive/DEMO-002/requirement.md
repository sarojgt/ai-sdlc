---
das_version: "0.1"
artifact:
  id: "REQ-DEMO-002"
  type: requirement
  version: 1
  status: approved
  title: "Payment status notification"
  initiative: "DEMO-002"
  owner: "team.payments"
source:
  provider: "github"
  work_item_id: "DEMO-002"
traceability:
  parents: ["github:DEMO-002"]
policy:
  risk_tier: "medium"
---

# Requirement: Payment status notification

## Business outcome

Reduce customer support requests caused by unclear payment state by giving
customers a consistent status notification within 30 seconds of a status
change.

## Problem statement

Customers currently need to refresh or contact support to understand whether a
payment is pending, completed, or failed. Status information is inconsistent
across the payment and notification services.

## Functional requirements

<!-- Use REQ-DEMO-002-NN identifiers. -->

### REQ-DEMO-002-01

The system must publish a customer-visible notification when a payment enters
the completed or failed terminal state.

### REQ-DEMO-002-02

The notification must be idempotent for a payment and terminal state.

## Non-functional requirements

- Notification delivery target: within 30 seconds for 95% of status changes.
- No payment credentials or sensitive authentication data may be included.
- The design must support retry and duplicate event handling.

## Acceptance criteria

- Given a payment enters a terminal state, when the event is accepted, then a
  notification is available to the customer within 30 seconds for 95% of cases.
- Given the same terminal event is delivered more than once, then only one
  customer notification is produced.

## Assumptions and open questions

- Existing payment events are available to the notification service.
- Which notification channels are enabled for the first release?

## Business approval

Product Owner: demo-product-owner@example.com  
Decision: approved for HLD generation  
Date: 2026-07-22  
Note: Demonstration approval for the repository-first flow.
