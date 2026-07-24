# AI-SDLC Copilot Instructions

This repository manages governed SDLC artifacts. It is not an application
repository.

## Scope

- Create and update initiative requirements, context, HLDs, LLDs, feedback,
  approvals, traceability, and evidence only.
- Do not modify product source code, service code, database migrations,
  infrastructure, deployment manifests, or production configuration here.
- Do not approve requirements, HLDs, LLDs, releases, or deployments as an AI.

## New requirement intake

Use the `intake` profile and create a small PR. The intake PR may contain only:

- `initiative.md`
- `requirement.md`
- `initiative.yaml`
- `traceability.yaml`
- `approvals.yaml`
- `context-manifest.yaml`
- relevant files under `context/relative/`

Do not add `hld/`, `lld/`, `feedback/`, `approvals/`, `evidence/`, or unrelated
workflow/configuration changes to the intake PR. Preserve the Jira or GitHub
source link for traceability.

## After intake approval or merge

The post-merge GitHub Action creates a follow-up automation PR with the
remaining scaffold, including human-readable HLD and LLD templates. Do not
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
- Stop for senior engineering approval before implementation work.

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
