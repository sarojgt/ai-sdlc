# AI-SDLC Agent Instructions

These instructions apply to any AI provider or coding agent working in this
repository.

## Repository boundary

This repository contains the AI-SDLC operating model and initiative artifacts;
it is not an application repository. Do not modify product source code,
service code, database migrations, infrastructure, deployment manifests, or
production configuration here. The implementation phase may create linked
workstreams and PRs in the affected application repositories only after the
approved HLD and LLD gates have passed.

Use Markdown for human-facing artifacts. Use YAML only for metadata,
validation, approvals, traceability, and execution evidence.

## Lifecycle operating rules

1. For a new requirement, create an intake initiative using the `intake`
   profile.
2. The intake PR may contain only the minimum initiative metadata, the
   requirement Markdown, and initiative-relative context. Do not add HLD, LLD,
   feedback, evidence, or boilerplate README files in that PR.
3. After the intake PR is approved or merged, post-merge automation creates a
   follow-up automation PR containing the reusable HLD and LLD templates plus
   the remaining initiative scaffold.
4. HLD generation may begin only after requirements approval and context
   assembly. HLD review and its bounded AI feedback loop are allowed, but only
   a human Solution Architect or ARB can approve architecture.
5. LLD generation may begin only after the HLD approval record is present.
6. No implementation, application-code change, merge, release, or deployment
   may be performed by an agent from this repository without the corresponding
   human gate.

For the exact intake file allowlist and handoff behavior, read
`ai-sdlc/design/initiative-intake-agent-guide.md`.

## Commit and release conventions

- Use change-focused branch names in the form
  `type/scope-short-description`, for example
  `feat/initiative-card-blocking`, `feat/hld-card-blocking`,
  `fix/workflow-approval-sync`, or `ci/release-semantic-tags`.
- Never use an AI provider or agent name as the branch prefix, including
  `agent/`, `copilot/`, `codex/`, `claude/`, `gemini/`, or `qwen/`.
- Use Conventional Commit titles and commit messages:
  `type(scope): description`.
- Use lifecycle scopes such as `initiative`, `requirement`, `context`, `hld`,
  `lld`, `approval`, and `traceability` for artifacts. Use `workflow`,
  `policy`, `release`, `ai-sdlc`, or `repo` for framework changes.
- Use `feat` for a new capability, `fix` for a correction, and the other
  supported types documented in `ai-sdlc/config/conventional-commits.yaml`.
- Mark breaking changes with `type(scope)!:` or a `BREAKING CHANGE:` footer.
- Pull requests and commits are checked by GitHub Actions.
- Merges to `main` create semantic release tags for both tracks. Framework
  scopes create the global version; initiative, requirement, context, HLD, LLD,
  approval, and traceability scopes create their scoped artifact version.
  Breaking changes increment major, `feat` increments minor, and
  `fix`/`perf`/`refactor`/`revert` increment patch on each applicable track.

## Mission

Help build and operate a vendor-neutral, human-governed AI-native SDLC. AI may
discover context, draft artifacts, review designs, and implement approved work.
Humans retain ownership of business, architecture, security, engineering, and
release decisions.

## Required reading

Before making a workflow or artifact change, read:

1. `README.md`
2. `docs/AI-SDLC-STATUS.md`
3. `ai-sdlc/README.md`
4. The relevant files under `ai-sdlc/config/`
5. The initiative's `requirement.md`, context manifest, and relative context

## Artifact rules

- Requirements are human-readable Markdown in `initiatives/<ID>/requirement.md`.
- Shared enterprise knowledge is under `ai-sdlc/context/`.
- Initiative-specific knowledge is under `initiatives/<ID>/context/relative/`.
- The canonical HLD is `initiatives/<ID>/hld/hld.md`.
- HLD generation must create and preserve
  `initiatives/<ID>/evidence/design-baseline.yaml`.
- The design baseline is the authoritative link between requirement, context,
  HLD, LLD, tags, hashes, and source commit.
- The LLD is locked until human architecture approval.
- Keep diagrams embedded in the HLD when they are part of the human decision.
- Use YAML only for metadata, validation, traceability, and execution evidence.
- Never grant business or architecture approval through an AI-generated file.

## HLD behavior

Before proposing a design, assess change size, complexity/risk, affected
services, repositories, APIs, data stores/tables, events, jobs, infrastructure,
channels, integrations, security, deployment, and migration impact.

Use confirmed enterprise principles, guardrails, standards, and approved
patterns. Prefer the smallest compliant design. Record missing facts as
`CONTEXT GAP`s with an owner and retrieval action. Do not invent components to
hide incomplete context.

## Safe execution

- Do not modify protected requirements or approval records unless explicitly
  instructed.
- Do not implement before HLD approval and LLD completion.
- Do not merge, release, or deploy without the corresponding human gate.
- Run `just ai-sdlc-validate <initiative-directory>` after structural changes.
- Preserve unrelated worktree changes.
- Use the configured provider adapter rather than embedding provider-specific
  assumptions in templates or lifecycle rules.

## Current project state

The maintained checklist is `docs/AI-SDLC-STATUS.md`. Update it whenever a
capability is completed, changed, deferred, or discovered to be incomplete.
