---
reviewer: codex
model: gpt-5.6-terra
iteration: 1
decision: changes_requested
---

# HLD Review — DEMO-003

## Blocking findings

1. **Stable partner-visible event identity is not specified.** The HLD proposes
   the internal uniqueness key `event_id + partner_id` (section 3), but does
   not require that a stable event identifier be sent to the partner, nor that
   the same identifier be preserved for every retry, authorized replay, and
   coexistence/migration path. This leaves the acceptance criterion for safe
   partner deduplication only partially covered. The wording that partner
   support is an assumption is insufficient because this is a stated
   requirement, not an optional capability.

## Non-blocking findings

1. The HLD correctly identifies signing/authentication, retention, delivery
   semantics, and estate/platform facts as unresolved. These must remain
   explicit review gates; no architecture approval should be inferred from the
   proposed direction.
2. Only a context diagram is supplied. A target/sequence diagram showing
   creation, attempt, retry, dead-lettering, operator-authorized replay, and
   partner-visible identity would make the control and deduplication boundaries
   materially clearer before human architecture review.
3. No prior feedback artifact was present. Shared architecture and security
   context is a draft baseline, and the initiative context contains no current
   API, repository, or runtime evidence; the proposal appropriately labels
   those limitations rather than presenting them as facts.

## Affected sections

- `generated/hld/hld.md`: sections 3, 4, 7, and 8; open questions 1, 2, and 9.
- `generated/hld/options/option-01.md`: Flow and High-level safeguards.
- `generated/hld/diagrams/context.mmd`.
- `generated/hld/risks.md`: R-03 and R-10.

## Required changes

1. Define the partner-facing deduplication contract at HLD level: the stable
   identity field/header, its meaning (accepted payment-status transition), and
   the rule that it is unchanged across retries, authorized replays, and any
   overlapping migration path. State that it is available to partners for
   deduplication without exposing credentials or sensitive authentication data.
2. Align the internal uniqueness boundary, outbound contract, delivery-state
   record, replay procedure, and migration rule to that one identity model;
   retain domain confirmation only for the exact event/version composition.
3. Add a target or sequence diagram that shows the identity crossing the
   partner boundary and the retry/DLQ/replay lifecycle.

## Recommendation

Revise the bounded identity and diagram gaps, then rerun independent review.
The async direction, security guardrails, retry/DLQ approach, observability,
and approval gating are otherwise consistent with the approved requirement and
available context. Human architecture and security decisions remain required
for the unresolved signing, retention, platform, and estate facts.
