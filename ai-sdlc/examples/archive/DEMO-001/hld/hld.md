---
das_version: "0.1"
artifact:
  id: "HLD-DEMO-001"
  type: hld
  version: 1
  status: draft
  title: "Payment status notification improvement"
  initiative: "DEMO-001"
  owner: "team.architecture"
traceability:
  parents: ["REQ-DEMO-001"]
  satisfies: ["REQ-DEMO-001-01", "REQ-DEMO-001-02"]
approvals:
  required: [architecture]
  records: []
policy:
  implementation_locked_until: architecture.approved
---

# HLD: Payment status notification improvement

## Status

Draft. Implementation is locked until a Solution Architect approves this exact version.

## Problem space

Payment status consumers currently rely on inconsistent notification behavior or polling.

## Option 1 — Publish an event from the payment service

The payment service publishes a versioned status event when its authoritative state changes.

## Option 2 — Add a notification adapter

A separate adapter observes payment state changes and publishes a normalized notification contract.

## Trade-off summary

| Criterion | Option 1 | Option 2 |
|---|---:|---:|
| Simplicity | High | Medium |
| Separation of concerns | Medium | High |
| Migration effort | Medium | High |
| Operational complexity | Medium | High |
| Reversibility | Medium | High |

## Recommendation

Pending Solution Architect review.

## Risks and mitigations

- Duplicate delivery: define idempotency key and consumer guidance.
- Consumer compatibility: publish a versioned contract and contract tests.
- State correctness: identify the authoritative state transition.

## Migration and rollback

Start in the test environment with one consumer. Roll back by disabling publication or routing consumers to the previous polling behavior.

## Proposed ADRs

- `ADR-DEMO-001-01`: notification contract ownership.
- `ADR-DEMO-001-02`: event delivery and idempotency strategy.

## Architecture approval

Solution Architect: pending
Approval hash: pending
