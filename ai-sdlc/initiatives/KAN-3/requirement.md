---
das_version: "0.1"
artifact:
  id: "REQ-KAN-3"
  type: requirement
  version: 1
  status: draft
  title: "Add backfill trigger for initiative approval sync and post-merge processing"
  initiative: "KAN-3"
  owner: "team.ai-sdlc"
source:
  provider: "jira"
  work_item_id: "KAN-3"
  url: "https://randomtry.atlassian.net/browse/KAN-3"
traceability:
  parents: ["jira:KAN-3"]
policy:
  risk_tier: "medium"
  data_classification: "internal"
---

# Requirement: Add backfill trigger for initiative approval sync and post-merge processing

## 1. Business summary

Ensure initiative approval and downstream automation still runs for PRs that were
created before the approval-sync workflow existed in `main`, or for any PR that
misses the original `pull_request_review` event.

## 2. Problem statement

The current approval-sync workflow only reacts to future approval events. If a PR
already existed before the workflow was merged, GitHub will not retroactively
trigger approval sync. That leaves initiative status stale even though the PR may
already be approved or merged.

## 3. Users, consumers, and stakeholders

| Group | Need or responsibility | Priority |
|---|---|---|
| Initiative owners | Recover missed approval sync for existing or merged initiative PRs | Must |
| Human approvers | Remain the source of truth for valid approval decisions | Must |
| AI-SDLC automation maintainers | Provide a safe, traceable reconciliation path without rewriting the approval policy | Must |
| Repository maintainers | Confirm GitHub Actions permissions and branch protection behavior for backfill commits | Should |

## 4. Desired user or system outcome

A maintainer can manually run an approval-sync recovery workflow for an existing
initiative PR. If the PR has a human approval, the workflow reconciles the
initiative artifacts to approved state and records the reviewer, review ID,
content hash, and timestamp in Git history.

## 5. Scope

### In scope

- Add a manual backfill path for approval-sync recovery.
- Add a `workflow_dispatch` trigger for the approval sync workflow.
- Re-scan the selected initiative PR for human approvals.
- Update `initiative.yaml`, `initiative.md`, and `approvals.yaml` when approval
  evidence is present.
- Support old merged initiative PRs by reconciling against the base branch after
  merge.
- Preserve the existing `pull_request_review` event path.
- Keep the human approval gate as the source of truth.

### Out of scope

- Changing the approval policy itself.
- Removing human review requirements.
- Rewriting the existing approval-sync workflow.
- Introducing automated business or architecture approval.

## 6. Business rules and domain terms

| Rule or term | Meaning / expected behaviour | Source or owner |
|---|---|---|
| Backfill | Manual recovery run that reconciles an existing PR after the original review event was missed | Jira KAN-3 |
| Human approval gate | A GitHub PR approval by a human reviewer remains the source of truth for approval sync | AI-SDLC governance |
| Initiative artifacts | `initiative.yaml`, `initiative.md`, and `approvals.yaml` for one initiative directory | AI-SDLC repository conventions |
| Traceable update | Approval reconciliation must be committed so the decision trail is visible in Git history | Jira KAN-3 |

## 7. Functional requirements

<!-- Use REQ-KAN-3-NN identifiers. -->

### REQ-KAN-3-01

The solution must add a manual `workflow_dispatch` trigger to recover missed
initiative approval sync for a specified pull request.

### REQ-KAN-3-02

The backfill workflow must inspect the selected pull request and identify exactly
one changed initiative directory before updating artifacts.

### REQ-KAN-3-03

The backfill workflow must inspect pull request reviews and only reconcile
approval state when a human approval is present.

### REQ-KAN-3-04

The reconciliation path must update `initiative.yaml`, `initiative.md`, and
`approvals.yaml` consistently with the existing approval-sync behavior.

### REQ-KAN-3-05

The reconciliation path must be safe to re-run and must not duplicate approvals
or overwrite an initiative approval that has already been recorded.

### REQ-KAN-3-06

The reconciliation path must preserve the existing `pull_request_review`
automation for future approval events.

### REQ-KAN-3-07

The workflow must commit approval reconciliation changes so the update remains
traceable in Git history.

| ID | Requirement | Priority | Source / rationale |
|---|---|---|---|
| REQ-KAN-3-01 | Add manual workflow dispatch approval-sync recovery for a specified PR. | Must | Jira KAN-3 scope |
| REQ-KAN-3-02 | Identify exactly one initiative directory from the selected PR. | Must | Prevent broad or ambiguous updates |
| REQ-KAN-3-03 | Reconcile only when human approval evidence exists. | Must | Human approval gate remains source of truth |
| REQ-KAN-3-04 | Update initiative metadata, markdown summary, and approval record consistently. | Must | Jira KAN-3 acceptance criteria |
| REQ-KAN-3-05 | Make reconciliation idempotent for already-approved initiatives. | Must | Avoid duplicates and overwrites |
| REQ-KAN-3-06 | Keep current event-driven approval sync intact. | Must | Complement, not replace, existing automation |
| REQ-KAN-3-07 | Commit reconciliation updates for auditability. | Must | Traceable Git history |

## 8. Non-functional requirements

| Category | Requirement or target | Priority | Owner / source |
|---|---|---|---|
| Security and privacy | Do not grant approval without human GitHub review evidence; do not introduce secrets or external credential handling. | Must | Jira KAN-3; AI-SDLC governance |
| Availability and resilience | Recovery should work for PRs created before the workflow existed and for missed review events. | Must | Jira KAN-3 |
| Performance and capacity | Backfill may target a single PR and should avoid repository-wide scans in the first version. | Should | Automation maintainer |
| Scalability | The workflow should leave room for future scheduled reconciliation without changing artifact contracts. | Should | Automation maintainer |
| Observability and support | Workflow logs should show when no approval is found, when an initiative is already approved, or when a commit is created. | Should | Repository maintainer |
| Compliance or data residency | No customer, regulated, or production data is introduced; only repository metadata and PR review metadata are processed. | Must | AI-SDLC governance |

## 9. Data and information considerations

- Data classification: internal.
- Sensitive or regulated data involved: none expected; workflow processes GitHub
  PR metadata, reviewer login, review ID, timestamps, and repository artifacts.
- Data owner: AI-SDLC repository maintainers.
- Source systems or records, if known: GitHub pull request files and reviews for
  `sarojgt/ai-sdlc`.
- Retention or deletion requirements: approval updates are retained in Git
  history according to repository retention practices.
- Client, tenant, regional, or residency boundaries: not applicable for this
  repository automation change.

## 10. Integrations and dependencies

| Dependency or integration | Internal / external | Purpose | Known owner |
|---|---|---|---|
| GitHub Actions | External SaaS | Run review-event and manual backfill workflows | Repository maintainers |
| GitHub Pull Requests API | External SaaS | Read PR file scope and review approvals | Repository maintainers |
| AI-SDLC approval sync tooling | Internal | Update initiative artifacts consistently | AI-SDLC automation maintainers |
| Git history | Internal repository record | Preserve traceability of approval updates | Repository maintainers |

## 11. Constraints and approved patterns

- Business constraints: existing and merged initiative PRs must be recoverable
  after the workflow is introduced.
- Technology or platform constraints: reuse GitHub Actions and the existing
  approval-sync script; avoid changing artifact contracts.
- Security or regulatory constraints: do not bypass human approvals and do not
  add secrets to source control.
- Existing architecture pattern that should be reused: repository-first Markdown
  and YAML artifacts with Git history as the traceable evidence store.
- Alternatives that are explicitly not allowed: automatic approval without human
  review evidence, removal of review requirements, or wholesale workflow rewrite.

## 12. Acceptance criteria

- **Given** an existing initiative PR with a human approval, **When** a maintainer
  runs approval-sync recovery for that PR, **Then** the initiative approval state
  can be backfilled.
- **Given** a PR missed the original `pull_request_review` event, **When** the
  manual recovery job runs, **Then** it reconciles missed approval state when a
  human approval exists.
- **Given** an initiative PR was merged before the workflow existed, **When** the
  recovery job is run for that PR, **Then** the initiative can still be marked
  approved on the target branch.
- **Given** an initiative approval has already been recorded, **When** recovery is
  run again, **Then** the workflow does not duplicate the approval or overwrite
  the recorded valid human decision.
- **Given** approval reconciliation updates artifacts, **When** the workflow
  completes, **Then** the update is traceable as a Git commit.

## 13. Initial impact hints

These are business or product estimates. The HLD agent must verify them against
the full context.

| Dimension | Initial view | Confidence / notes |
|---|---|---|
| Expected change size: small / medium / large / program-level | Small | One workflow extension and a small script safety change |
| Expected complexity/risk: low / moderate / high / critical | Moderate | GitHub review state and branch target handling must avoid unsafe writes |
| Services or repositories likely involved | `sarojgt/ai-sdlc` | Current repository only |
| Internal integrations | AI-SDLC initiative artifacts and approval sync script | Existing artifact contracts should be reused |
| External integrations | GitHub Actions and Pull Requests API | Used by repository automation |
| Data or security impact | Low | No customer data; approval authority must remain human GitHub review evidence |
| Deployment or migration impact | Low | Workflow-only change; no runtime service deployment |

## 14. Assumptions and open questions

- Should future hardening add a scheduled reconciliation mode that scans recent
  initiative PRs, or is per-PR manual dispatch sufficient for the first version?
- Are branch protection rules configured to allow the GitHub Actions token to
  commit post-merge reconciliation updates to the base branch?
- Should future policy validation distinguish reviewer roles beyond the current
  workflow's human PR approval signal?

## 15. Business approval

Product Owner: pending

Decision: pending

Date: pending

Notes: Business approval is required before HLD generation. This requirement
captures Jira KAN-3 intake and does not approve architecture, implementation, or
release.
