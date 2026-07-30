# AI-SDLC Framework Reference

This directory contains the reusable lifecycle framework. The concise current
process is documented in the [AI-SDLC Operating Guide](../docs/AI-SDLC-OPERATING-GUIDE.md).

## Layout

```text
ai-sdlc/
  context/                 shared business, architecture, and guardrails
  config/                  roles, gates, loop policy, provider catalog
  prompts/hld/             versioned assessment, generation, review prompts
  design/                  lifecycle and adapter design references
  schemas/                 machine-readable validation contracts
  templates/initiative/    reusable artifact templates
  initiatives/<ID>/        initiative instances
  tooling/                 validators, orchestration, provider adapters
```

## Initiative artifacts

An intake PR should contain only:

```text
ai-sdlc/initiatives/<ID>/requirement.md
ai-sdlc/initiatives/<ID>/context/relative/<optional-context>.md
```

Post-merge automation adds metadata and the context manifest. HLD generation
creates the HLD, evidence, and feedback artifacts when that stage is reached.
Do not add HLD, LLD, or boilerplate files to an intake PR.

## Context

```text
ai-sdlc/context/consistent/       stable enterprise and architecture context
ai-sdlc/context/guardrails/       standards, policies, and constraints
initiatives/<ID>/context/relative/ requirement-specific context
```

The requirement remains outside the context directory. Markdown is the human
source of truth; YAML records metadata, approvals, hashes, and evidence.

## Local interface

```text
just ai-sdlc-new
just ai-sdlc-init <ID> <title> <outcome> <problem> <owner> <source> <risk> <data> intake
just ai-sdlc-validate ai-sdlc/initiatives/<ID>
just ai-sdlc-validate-all
just ai-sdlc-hld <ID> <generator-provider> <generator-model> <reviewer-provider> <reviewer-model> auto
AI_SDLC_HLD_RESUME=1 just ai-sdlc-hld <ID> <generator-provider> <generator-model> <reviewer-provider> <reviewer-model> auto
just ai-sdlc-hld-feedback <ID> <provider> <model>
```

Current local provider adapters are under `tooling/providers/`. The provider
boundary allows Codex, GitHub Copilot, and future adapters to use the same
artifact and approval contract.

## GitHub interface

- `initiative-approval-sync.yml`: intake merge to scaffold PR
- `generate-hld.yml`: merged scaffold PR or manual HLD dispatch
- `hld-review-feedback.yml`: bounded rerun from architect feedback
- `hld-approval-sync.yml`: merged HLD PR to approval metadata
- `das-gate.yml`: structure and repository gate validation

See the [Operating Guide](../docs/AI-SDLC-OPERATING-GUIDE.md) for exact
conditions, inputs, model selection, and recovery behavior.

## Governance

AI review is advisory. `ready_for_human_review` means the draft can be
reviewed; it does not approve architecture. LLD and implementation work are
locked until the human HLD approval record exists.
