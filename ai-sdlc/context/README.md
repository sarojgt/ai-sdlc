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

## Confluence snapshots

Confluence is currently the upstream source of truth for enterprise standards.
This repository contains curated, human-reviewed Markdown snapshots so HLD
generation is reproducible and can record exactly which context was used.

Each imported document records its Confluence source and retrieval date. A
snapshot is not automatically authoritative: refresh it against Confluence
before a material design, and resolve conflicts with the owning human team.

Future automation should place retrieved candidates under
`context/proposed/confluence/` and create a GitHub PR. It must not silently
promote Confluence content into `consistent/` or `guardrails/`.
