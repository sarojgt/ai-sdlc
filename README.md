# AI-Native SDLC

This repository contains the reusable, human-governed AI-SDLC framework.

The current implementation is repository-first: enterprise context, guardrails,
initiative requirements, HLDs, LLDs, feedback, and approvals are maintained in
GitHub. Confluence is intentionally not required yet. A future Confluence
connector can populate or refresh the repository context without changing the
initiative workflow.

Start here: [AI-SDLC usage guide](ai-sdlc/README.md)

## Prerequisites

Required for the repository-first workflow:

- Git
- `just` command runner
- Bash or a compatible shell
- A local checkout with permission to write initiative artifacts

Required when using the Codex adapter:

- Codex CLI installed and available as `codex`
- Authenticated Codex CLI session
- Access to the requested model/provider

Required for GitHub publishing and PR automation:

- GitHub CLI (`gh`)
- Authenticated GitHub CLI session with repository write access
- A configured `origin` remote pointing to the target repository

Optional provider integrations may require their own CLI, SDK, credentials, or
MCP connector. Claude, Gemini, Copilot, Qwen, local models, Jira, and Confluence
are not required for the repository-first flow.

Optional tools such as Mermaid rendering, Docker, repository scanners, schema
tools, and cloud CLIs are only required when the corresponding workflow step is
enabled.

## Project status

The maintained implementation and delivery checklist is in
[docs/AI-SDLC-STATUS.md](docs/AI-SDLC-STATUS.md). It records completed work,
current limitations, roadmap items, and the target end state.

## Commit and semantic release standard

Use Conventional Commits for PR titles and commits:

```text
feat(ai-sdlc): add a workflow capability       # minor release
fix(ai-sdlc): correct a workflow defect         # patch release
docs(ai-sdlc): improve the operating guide      # no release
```

Breaking changes use `feat!:` or a `BREAKING CHANGE:` footer and create a major
release. Merges to `main` are evaluated by the semantic release workflow; when
the commit range requires a release, it creates a `vMAJOR.MINOR.PATCH` tag and
GitHub release with generated notes. The tag is the release version authority.

## End-to-end flow

```text
Business requirement
  → small intake initiative PR
  → business approval
  → merge trigger
  → automated boilerplate scaffold PR
  → context assembly and impact assessment
  → AI-generated HLD with standards-based recommendation
  → bounded AI review loop
  → human Solution Architect / ARB approval
  → LLD
  → engineering plan and implementation PRs
  → security, release, and deployment gates
```

The HLD gate is mandatory. AI cannot approve the HLD or begin implementation.

## Start a new initiative

Interactive intake:

```text
just ai-sdlc-new
```

Direct template bootstrap:

```text
just ai-sdlc-init \
  PAY-4567 \
  "Payment status notification improvement" \
  "Allow clients to receive timely payment status updates" \
  "Clients cannot reliably see payment status changes" \
  team.payments \
  PAY-4567 \
  medium \
  internal \
  intake
```

The direct command requires a title, business outcome, problem statement,
owner, source work-item, risk tier, data classification, and profile.
Use `intake` for a small business-review PR and `full` only when you
explicitly want the entire scaffold up front. `just ai-sdlc-new` uses the same
intake-first flow interactively.

Complete:

```text
ai-sdlc/initiatives/PAY-4567/requirement.md
ai-sdlc/initiatives/PAY-4567/context/relative/
```

The intake PR is intentionally small. After merge, one post-merge automation
workflow expands the initiative with reusable boilerplate, including HLD and
LLD templates, and synchronizes valid human approval metadata in a single
follow-up PR.

The requirement captures business outcome, problem, stakeholders, scope,
business rules, functional and non-functional requirements, data, integrations,
constraints, acceptance criteria, and initial impact hints.

## Validate

```text
just ai-sdlc-validate ai-sdlc/initiatives/PAY-4567
just ai-sdlc-validate-all
```

## Generate an HLD

After the Product Owner approves `requirement.md`:

```text
just ai-sdlc-hld PAY-4567 codex gpt-5.6-luna codex gpt-5.6-terra
```

The command loads context, assesses impact, applies enterprise standards and
approved patterns, generates `hld/hld.md` with useful embedded Mermaid diagrams,
runs a bounded independent AI review loop, and stops for human architecture
approval.

Generator and reviewer providers/models can be overridden independently:

```text
just ai-sdlc-hld PAY-4567 claude claude-sonnet-4 codex gpt-review-model
```

The loop is bounded by iteration, time, unchanged-output, and repeated-feedback
guards. A passing AI review is not architecture approval.

## Human feedback and next stages

The architect reviews:

```text
ai-sdlc/initiatives/PAY-4567/hld/hld.md
ai-sdlc/initiatives/PAY-4567/feedback/
```

An approved initiative PR can automatically flip `initiative.yaml` and
`initiative.md` to `approved` and record the approval trail in
`approvals.yaml`.

Only after the HLD approval record is present should the LLD flow be enabled.
The LLD contains detailed APIs, schemas, classes, implementation sequencing,
test strategy, and migration details.

## Current versus target integration

Current: GitHub/repository artifacts, Markdown requirements and HLDs, `just`
commands, provider adapters, and human review.

Future: GitHub Issue and Actions triggers, automatic draft HLD PRs, Jira intake
and traceability, Confluence context synchronization, multi-repository
orchestration, and implementation/deployment evidence automation.

See the [project checklist](docs/AI-SDLC-STATUS.md) for the full roadmap.
