# Repository Context

This directory contains the shared context used by AI agents before they
propose requirements, designs, or implementation plans.

## Context types

- `consistent/` — reusable enterprise, business, domain, and architecture
  knowledge that applies across initiatives.
- `guardrails/` — security, architecture, engineering, and delivery rules
  that constrain what agents may propose or do.

Initiative-specific context does not belong here. It lives under:

```text
initiatives/<initiative-id>/context/relative/
```

The context is Markdown-first. Machine-readable manifests or generated
snapshots may be added by tooling when needed for validation and auditability.

HLD generation does not load the whole context directory. The context builder
uses `config/context-index.yaml` and `config/context-sources.yaml` to select a
small, deterministic set of relevant sources and Markdown sections. It always
records the selected paths, sections, versions, hashes, and selection reasons
in the initiative manifest and writes the generated excerpts to
`evidence/context-pack.md`.

The configured token budget is advisory. It helps the builder report and
reduce unnecessary context, but exceeding it must never block requirement,
assessment, HLD, or review work. Missing facts remain context gaps and are
handled through the normal human discovery gate.

## Maintaining the catalog

When a new source is added to `config/context-sources.yaml`, run:

```text
just ai-sdlc-context-catalog-check
```

To append non-destructive `review-required` stubs for new sources, run:

```text
just ai-sdlc-context-catalog-update
```

Refine the generated summary, keywords, applicable initiative types, selected
sections, priority, and dependencies before merging the context change. The
update command never deletes or overwrites an existing catalog entry.

## Confluence snapshots

Confluence is currently the upstream source of truth for enterprise standards.
This repository contains curated, human-reviewed Markdown snapshots so HLD
generation is reproducible and can record exactly which context was used.

Each imported document records its Confluence source and retrieval date. A
snapshot is not automatically authoritative: refresh it against Confluence
before a material design, and resolve conflicts with the owning human team.

Every shared context document should also carry front matter with a
`context_id`, `context_type`, `authority`, `status`, `owner`, and
`review_cadence`. The context catalog validates these identifiers where they
are present and remains the source registry for provider-backed entries that
do not have a local Markdown file yet.

Future automation should place retrieved candidates under
`context/proposed/confluence/` and create a GitHub PR. It must not silently
promote Confluence content into `consistent/` or `guardrails/`.
