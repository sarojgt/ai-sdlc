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

Read the root `AGENTS.md` and the initiative intake guide before changing
workflow or initiative artifacts.

## Commit and PR format

Use Conventional Commits for both the PR title and commits:
`feat(ai-sdlc): description`, `fix(ai-sdlc): description`, or
`docs(ai-sdlc): description`. Breaking changes use `!` or a `BREAKING CHANGE:`
footer. Do not use free-form titles such as `Update files` or `Add changes`.
