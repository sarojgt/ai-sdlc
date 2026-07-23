# ADR-DEMO-004-01 — Transaction status event handoff for client webhooks

## Status

Proposed for human Solution Architect review. Not approved.

## Context

The approved requirement needs near-real-time client-scoped status webhooks,
shared Webhook Platform delivery, API Gateway/Auth0/IMS authorization, stable
idempotency, bounded recovery, and no PAN, SAD, secrets, tokens, or unrestricted
production payloads. BL2 remains supported while Lume is the strategic target
for new capability. The current producer, estate, platform contract, runtime,
rate, and SLO evidence is not available in the initiative context.

## Decision options

1. Authoritative producer → sanitized governed Kafka/MSK event boundary → shared Webhook Platform.
2. BL2 transactional outbox or durable journal → controlled adapter → the same platform.

## Proposed direction

Select Option 1 for Lume and BL2 cohorts that support direct governed
publication. Select Option 2 only for a proven BL2 capability gap with an
approved durable handoff, explicit cohort scope, owner, and retirement milestone.
This is a conditional recommendation, not an architecture decision.

## Consequences

Positive: delivery is decoupled from the transaction path; shared ownership
standardizes subscription, retry, DLQ, replay, signing, and delivery status; a
common contract supports coexistence and cohort migration.

Negative: Option 1 adds governed topic/schema/replay/DLQ/telemetry surfaces.
Option 2 adds source access, database load, checkpoints, bespoke operations,
and a second migration to retire the bridge.

## Conditions before LLD

- Confirm producer, statuses, ordering, corrections, identity, rate, fan-out, and SLO.
- Confirm CHD/CW classification, sanitization, connectivity direction, and security approval.
- Confirm platform ingress, schema/ACL, signing, retry, DLQ, replay, regional, quota, and residency contracts.
- Confirm Gateway route, Auth0 issuer/audience/scopes, M2M identity, IMS permissions, audit, and failure behavior.
- Confirm BL2/Lume cohorts, environment, region, tier, shared/dedicated resources, owners, dashboards, runbooks, and rollback evidence.

**Decision authority: human Solution Architect. Current decision: pending.**
