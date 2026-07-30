# AI-Native SDLC

This repository defines a vendor-neutral, human-governed AI Software
Development Lifecycle. It stores requirements, context, designs, approvals,
feedback, and traceability as repository artifacts.

## Start here

Read the [AI-SDLC Operating Guide](docs/AI-SDLC-OPERATING-GUIDE.md) for the
current flow, commands, GitHub triggers, gates, recovery, and boundaries.

Use the [framework reference](ai-sdlc/README.md) for repository layout and
artifact conventions. The [project status checklist](docs/AI-SDLC-STATUS.md)
shows what is implemented and what remains planned.

## Current flow

```text
Requirement -> intake PR -> business approval and merge
  -> automated scaffold PR -> HLD generation and bounded AI review
  -> Solution Architect / ARB approval -> gated LLD and implementation stages
```

The HLD approval is mandatory. AI can discover context, assess impact, draft,
revise, and review; humans own business, architecture, security, engineering,
release, and deployment decisions.

## Minimum prerequisites

- Git
- `just`
- Bash-compatible shell
- Provider CLI and authentication for local AI runs
- `gh` authenticated for GitHub operations

GitHub Actions installs its own workflow dependencies. Jira, Confluence,
MCP, cloud CLIs, Docker, and repository scanners are optional or future
integrations.

## Useful commands

```text
just ai-sdlc-new
just ai-sdlc-validate ai-sdlc/initiatives/<ID>
just ai-sdlc-validate-all
just ai-sdlc-hld <ID> codex <generator-model> codex <reviewer-model> auto
just ai-sdlc-hld-feedback <ID> <provider> <model>
```

## Repository boundary

This repository contains the SDLC operating model and design artifacts. It
does not contain application code, database migrations, infrastructure code,
or deployment configuration. Approved HLD/LLD work may create workstreams and
PRs in affected application repositories later.

## Documentation map

| Document | Purpose |
|---|---|
| [Operating Guide](docs/AI-SDLC-OPERATING-GUIDE.md) | Current process and usage |
| [Framework reference](ai-sdlc/README.md) | Layout, artifacts, interfaces |
| [Status checklist](docs/AI-SDLC-STATUS.md) | Implemented and planned work |
| [Automation and gates](docs/automation-and-gates.md) | Detailed automation design |
| [HLD runbook](ai-sdlc/design/hld-generation-runbook.md) | HLD design reference |
| [Agent runner design](ai-sdlc/design/agent-runner.md) | Provider adapter design |

Use Markdown for human-facing decisions. Use YAML only for metadata,
approvals, validation, hashes, and execution evidence.
