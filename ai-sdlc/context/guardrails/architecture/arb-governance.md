---
context_id: arb-governance
context_type: guardrail
authority: architecture-review-board
status: imported-snapshot
owner: architecture-board
review_cadence: verify-against-confluence-before-material-design
source: https://paymentology.atlassian.net/wiki/spaces/pa/pages/8385232953/ARB+-+Architecture+Review+Board
retrieved: 2026-07-22
---

# Architecture Review Governance

This snapshot describes the Architecture Review Board process. It complements
the AI SDLC gate: AI can prepare and revise artifacts, but humans own approval.
Confluence remains authoritative for the operating process.

## When review is expected

Significant architectural changes, solution designs, technology-stack changes,
new principles or standards, and changes with material risk should be brought
through architecture governance. When scope is unclear, use the Architecture
Working Group for guidance.

## Submission expectations

- The change must have a design page or equivalent design artifact containing
  the details.
- Review discussions and decisions must be recorded against the design.
- Major issues mean rework and normally require resubmission.
- Minor issues may be addressed without returning to the board when the board
  explicitly permits that path.
- The responsible architect remains involved after approval to help align
  stories, LLDs, delivery, and operational acceptance with the approved design.

## AI SDLC mapping

The AI-generated HLD is a reviewable proposal, not an approval. The HLD gate
must remain pending until the authorized Solution Architect or ARB process
records a decision. AI review can identify gaps and request bounded revisions,
but cannot approve architecture or unlock LLD generation.

## Source

[ARB - Architecture Review Board](https://paymentology.atlassian.net/wiki/spaces/pa/pages/8385232953/ARB+-+Architecture+Review+Board)
