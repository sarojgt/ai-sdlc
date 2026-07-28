# AI-SDLC Copilot Instructions

This repository manages governed SDLC artifacts. It is not an application
repository.

## Scope

- Create and update initiative requirements, context, HLDs, LLDs, feedback,
  approvals, traceability, and evidence only.
- Do not modify product source code, service code, database migrations,
  infrastructure, deployment manifests, or production configuration here.
- Do not approve requirements, HLDs, LLDs, releases, or deployments as an AI.

## Working agreement

Before acting, read `AGENTS.md`, `README.md`, `docs/AI-SDLC-STATUS.md`,
`ai-sdlc/README.md`, the relevant configuration under `ai-sdlc/config/`, and
the target initiative artifacts. Treat Markdown as the human-facing source and
YAML as supporting metadata, validation, approvals, traceability, or evidence.

Use the repository's existing `just` recipes and provider adapters. Do not
embed assumptions about Codex, Claude, Gemini, Copilot, Qwen, or a local model
in an artifact template. Record the selected provider/model in execution
evidence when an AI operation is run.

## New requirement intake

Use the `intake` profile and create the smallest possible PR. The intake PR
should contain only:

- `requirement.md`
- optional relevant files under `context/relative/`

Do not add initiative metadata, `hld/`, `lld/`, `feedback/`, `approvals/`,
`evidence/`, or unrelated workflow/configuration changes to the intake PR.
The post-merge expansion creates metadata and preserves the Jira or GitHub
source link for traceability.

If a business requirement arrives through a GitHub issue or Jira-connected
Copilot task, create a PR for the initiative artifact only. Do not start HLD
generation in the same intake PR. If the source requirement is incomplete,
capture questions or `CONTEXT GAP`s in the requirement rather than inventing
technical detail.

## After intake approval or merge

The intake PR review is the business approval. Do not ask a person to edit
`approvals.yaml` or create a second approval PR. The post-merge GitHub Action
reads the review and records the reviewer, commit, timestamp, and content hash
in the generated initiative metadata. It then creates a follow-up automation PR
with the remaining metadata and context manifest.

If `requirement.md` or `context/relative/**` changes after approval, the
previous requirements approval is invalidated automatically. A new review of
the current PR head is required before HLD generation can start. The HLD
workflow creates HLD, feedback, and evidence artifacts when HLD generation
begins. The LLD workflow creates LLD artifacts only after HLD approval. Do not
manually add that boilerplate to the intake PR.

## HLD and LLD behavior

- Assemble shared consistent context, guardrails, and initiative-relative
  context before designing.
- Assess change size, complexity, affected services, repositories, APIs, data,
  integrations, security, deployment, and migration impact.
- Generate a concise HLD with Mermaid diagrams and standards-based options.
- Record missing facts as context gaps; do not invent enterprise components.
- Run bounded AI review loops only where configured.
- Stop for human Solution Architect or ARB approval before LLD.
- HLD approval must come from the current-head GitHub review by the HLD
  CODEOWNER; AI review cannot approve architecture.
- Stop for senior engineering approval before implementation work.

The HLD must remain a concise architecture decision document, not an LLD. It
should explain the recommended change, affected boundaries, relevant existing
services/data/integrations, alternatives and trade-offs, risks, security,
operability, rollout, and diagrams where useful. Use confirmed standards and
approved patterns first; propose an alternative only when a real constraint or
trade-off justifies it.

The HLD workflow is:

1. Confirm that the requirement is approved and assemble consistent context,
   guardrails, and relative context.
2. Assess change size (`small`, `medium`, or `large`) and the affected
   services, repositories, APIs, data stores, events, integrations, security,
   deployment, and migration concerns.
3. Generate or update `hld/hld.md` through the configured provider adapter.
4. Run the bounded independent AI review loop. The reviewer must be a
   different provider/model from the generator.
5. Open or update a draft HLD PR for human Solution Architect/ARB review.
6. Stop until a human approval record is present; feedback causes a bounded
   rerun, while unresolved context gaps remain explicitly visible.

Never use the Copilot setup workflow as an approval mechanism. It only prepares
the environment and validates repository contracts; it does not generate,
approve, merge, release, or deploy anything.

When an approved initiative scaffold is merged, the GitHub Actions HLD
orchestrator may invoke Copilot CLI automatically. Use the configured
generator and reviewer model inputs; the reviewer must use a different model
from the generator. The orchestrator runs the existing bounded HLD loop and
creates a draft HLD PR only after AI review passes. Do not bypass the workflow
by approving architecture or changing protected approval records.

Read the root `AGENTS.md` and the initiative intake guide before changing
workflow or initiative artifacts.

## Commit and PR format

Use change-focused branch names such as
`feat/initiative-card-blocking`, `feat/hld-card-blocking`, or
`fix/workflow-approval-sync`. Never use an AI provider or agent name such as
`agent/`, `copilot/`, `codex/`, or `claude/` as the branch prefix.

Use Conventional Commits for both the PR title and commits:
`feat(initiative): description`, `feat(hld): description`,
`feat(lld): description`, `fix(requirement): description`, or
`fix(workflow): description`. Breaking changes use `!` or a `BREAKING CHANGE:`
footer. Do not use free-form titles such as `Update files` or `Add changes`.

Artifact commits are versioned independently from framework releases. A
`feat(initiative)`, `feat(hld)`, `feat(lld)`, or `feat(context)` commit creates
the corresponding scoped artifact tag after merge to `main`.

Every PR must state the source work item, initiative ID, artifact type, human
owner, context pack/version, and validation performed. Keep PR scope narrow:

- Intake PR: requirement and only the minimum initiative/relative-context
  files.
- Scaffold PR: generated reusable templates after intake merge.
- HLD PR: HLD, diagrams, feedback/evidence, and traceability changes only.
- LLD PR: approved HLD-linked engineering design only.

Do not include product-code changes in this repository. Use change-focused
branches such as `feat/initiative-card-search`, `feat/hld-card-search`,
`feat/lld-card-search`, `fix/workflow-approval-sync`, or
`docs/policy-copilot`. Do not use `agent/`, `copilot/`, `codex/`, `claude/`,
`gemini/`, or `qwen/` as branch prefixes.

Before handing off work, report changed files, checks run, unresolved context
gaps, and the next required human gate. A successful AI review is not a human
approval.
