---
reviewer: codex
model: gpt-5.6-terra
iteration: 2
decision: pass
---

# Independent HLD review

## Assessment

The HLD is a sufficiently complete provisional architecture proposal. It covers all approved requirements with backend IMS enforcement, bounded query behaviour, a safe tokenisation gate, conditional source/read-model designs, regional data-placement controls, resilience, telemetry, cost controls, rollout/rollback, ownership, risks, ADRs, and requirement traceability. The source, token representation, consumer exposure, NFR, runtime, and regional facts that remain open are assigned to named owners with fail-safe fallbacks and pre-LLD gates; they are normal human approval decisions, not a reason to escalate.

The previous blocking issues are resolved. The option-specific request and ingestion paths are consistently labelled across the C4, context, deployment, and sequence diagrams. The ERD now makes the lookup key conditional on Tokenization/Security approval, prohibits sensitive/reversible token data, and correctly keeps IMS authorization outside the projection.

## Blocking findings

None. No architecture approval is implied by this review, and the HLD/architecture gate remains pending human Solution Architect or ARB decision.

## Non-blocking findings

1. **The evidence-posture statement is inaccurate.** The HLD says that the manifest-referenced imported source snapshots are absent from the checkout, but the repository contains them under `context/consistent/` and `context/guardrails/`; the relevant items are marked `imported-snapshot` with explicit refresh cadences. This does not undermine the safeguards in the design, but it weakens audit accuracy.
   - Affected section: `hld/hld.md` — *Review status and evidence posture* and *Ownership and reuse*.
   - Required change: State that the repository-local imported snapshots were reviewed, identify that upstream Confluence/catalogue/repository verification is still required before a material decision, and retain the existing reuse-discovery gates. Do not describe the shared patterns as merely unavailable candidates.

2. **Make asynchronous projection ingestion unambiguously independent of an API request.** The sequence diagram places the source-to-feed-to-projection steps inside the authorized-request branch. While its labels make Option 2 understandable, the visual order can be read as request-triggered ingestion, whereas the HLD describes a durable, independently operated event/CDC pipeline.
   - Affected section: `hld/diagrams/sequence.mmd`; consequentially, the *Diagrams* description in `hld/hld.md`.
   - Required change: Show the Option 2 ingestion lifecycle in a separate sequence or clearly separate asynchronous `par`/background flow, including its retry/quarantine, replay, reconciliation, and lag-to-alert path. Preserve the current request sequence as query-only after the projection is available.

3. **Record the Banking.Live/Lume classification and shared/dedicated-resource matrix as an explicit gated deliverable.** The HLD correctly avoids inventing the estate, region, tier, and tenancy model, but the shared deployment context requires a classification such as `lume-greenfield`, `bl2-support`, `migration-enablement`, or `coexistence`, plus an explicit shared/dedicated boundary record before material design.
   - Affected sections: `hld/hld.md` — D-04, *Migration, rollout, and rollback*, and *Open questions before LLD*; `hld/diagrams/deployment.mmd`.
   - Required change: Add the classification and resource matrix to the D-04 verification evidence (with a “not yet determined” value where appropriate), covering compute, database, network, observability, DR, client isolation, and the target/legacy coexistence decision.

## Requirements coverage and traceability

`REQ-DEMO-005-01` through `-05` are explicitly traced to design responses and test evidence. The proposal covers authenticated, client/region-isolated listing; bounded date and approved lookup-key filtering; stable opaque pagination; Gateway/Auth0 plus backend IMS authorization; and exclusion of PAN, SAD, secrets, raw/reversible token data, and unsafe telemetry. The optional projection has a bounded fallback to the source-owned adapter if its feed, ownership, freshness, or placement gates do not close.

## Concise recommendation

Pass the HLD as a provisional architecture proposal for human review. Address the three non-blocking documentation/diagram refinements in the next generated revision or before LLD; do not begin LLD or implementation until the documented owner gates and formal architecture approval are complete.
