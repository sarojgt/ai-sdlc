# AI-SDLC Agent Instructions

These instructions apply to any AI provider or coding agent working in this
repository.

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
