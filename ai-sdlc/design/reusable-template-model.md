# Reusable AI-SDLC Template Model

## The correction

The framework must not be designed around one initiative. `DEMO-001` is only a sample generated instance. The reusable platform consists of templates, context packs, skills, policies, and lifecycle definitions. A new requirement creates a new instance from those reusable assets.

```text
Reusable platform assets
  ├── context layers
  ├── skills
  ├── guardrails and policies
  ├── artifact templates
  ├── gate definitions
  └── provider adapters
          ↓ instantiate
New requirement: PAY-4567
          ↓
Initiative instance: initiatives/PAY-4567/
```

## Reusable versus instance-specific

| Reusable once | Created for every requirement |
|---|---|
| Requirement/HLD/LLD/ADR templates | Requirement artifact |
| Context layer definitions | Relative context pack |
| Business/domain/product knowledge | Initiative context manifest |
| Technology and security guardrails | HLD options and recommendation |
| Agent skills and output schemas | Approvals and review history |
| Gate and invalidation policies | LLD and implementation workstreams |
| GitHub/Jira/Confluence adapters | Traceability links |
| PR and issue templates | Repository-specific PRs |

## The template engine

The platform should provide one generic operation:

```text
initiate(requirement_source, provider_context)
```

It should:

1. create a unique initiative ID;
2. create the initiative directory from templates;
3. attach the source work item;
4. load applicable context layers;
5. classify risk and data;
6. assign human roles;
7. create the first requirement draft;
8. start the lifecycle state machine.

The workflow never contains `DEMO-001` or any other fixed initiative ID. IDs are runtime data.

## Recommended repository layout

```text
ai-sdlc/
  config/
    lifecycle.yaml
    gates.yaml
    roles.yaml
    context-layers.yaml
    skills.yaml
  templates/
    initiative/
      initiative.yaml
      context-manifest.yaml
      requirement.md
      hld/hld.md
      lld/lld.md
      approvals.yaml
      traceability.yaml
  initiatives/
    PAY-4567/              # generated instance
    PAY-8910/              # another generated instance
  examples/
    DEMO-001/              # optional fixture only
```

## How the diagrams map to the reusable model

The diagrams' “AI Consistent Context,” “AI Guardrails,” “AI Relative Context,” “AI Output,” and “Human Milestone” become platform-level template categories:

```text
Consistent Context  → context-layers.yaml + curated knowledge
Guardrails          → policy files + skills + tool permissions
Relative Context    → generated context-manifest.yaml
AI Output           → DAS artifact templates and output schemas
Human Milestones    → lifecycle.yaml + gates.yaml + review adapters
```

This is the key abstraction. A new requirement changes the relative context and generated artifacts, not the SDLC design.
