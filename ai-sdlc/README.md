# Repository-First AI-Native SDLC

This directory is the reusable framework for a governed, AI-native Software
Development Lifecycle.

## Prerequisites

The base workflow requires Git, `just`, Bash or a compatible shell, and write
access to the repository. The current Codex implementation additionally
requires Codex CLI available as `codex`, an authenticated Codex session, and
access to the selected model.

For GitHub branches, commits, and pull requests, install and authenticate
GitHub CLI:

```text
gh auth login -h github.com
gh auth status
```

Provider-specific CLIs and credentials are optional. Jira, Confluence, MCP
connectors, Mermaid rendering, Docker, cloud CLIs, and repository scanners are
workflow-specific integrations, not base prerequisites.

## Initial rollout objective

Prove one complete vertical slice:

```text
GitHub Issue
  → Requirement artifact
  → HLD options
  → Human Solution Architect approval
  → Gate check
  → LLD and implementation plan
  → Implementation PR
```

The current operating model is repository-first. Human-facing artifacts and
shared context are Markdown in GitHub. Confluence, Jira, vector search, and
other enterprise integrations can be added later without changing the
initiative artifact structure or human approval gates.

New intake PRs should stay small: capture the requirement and the minimum
initiative metadata first, then let the post-merge automation expand the
reusable boilerplate and synchronize approval metadata in one follow-up PR.

## Directory map

```text
ai-sdlc/
  context/                 # shared business, architecture, and guardrail context
  config/                  # roles, context sources, lifecycle gates
  design/                  # framework architecture and workflow design
  schemas/                 # machine validation contracts
  templates/initiative/    # reusable artifact templates
  initiatives/<ID>/        # generated initiative instances
  tooling/                 # validators, context builder, and provider adapters
```

## First setup in GitHub

1. Create a new GitHub repository.
2. Copy the contents of this `ai-sdlc/` directory into the repository root.
3. Replace team names in `.github/CODEOWNERS` and `config/roles.yaml`.
4. Enable branch protection on `main`.
5. Require the `das-gate` status check.
6. Add the real Solution Architect team as the CODEOWNER for `initiatives/**/hld/**`.
7. Configure an approved provider/model adapter in `config/agent-providers.yaml` and `tooling/providers/`.
8. Create one real GitHub Issue from the AI-SDLC issue form.

## Context model

The agent does not start with only the requirement. The workflow assembles:

```text
Shared consistent context
  + initiative relative context
  + AI guardrails
  + approved artifact history
  → versioned context pack
  → selected agent and model
```

Shared context is maintained in:

```text
context/consistent/business/
context/consistent/architecture/
context/guardrails/
```

Initiative-specific context is maintained in:

```text
initiatives/<ID>/context/relative/
```

The requirement is deliberately outside the context directory:

```text
initiatives/<ID>/requirement.md
```

Markdown is the human source of truth. YAML or JSON may be generated for
machine validation, hashes, and agent evidence, but humans should normally
review Markdown documents.

## Create a new initiative instance

For interactive requirement intake:

```text
just ai-sdlc-new
```

The command asks for the initiative ID, title, team, business outcome, problem statement, risk tier, and data classification, then creates a reusable initiative instance.

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

The direct command captures the title, business outcome, problem statement,
owner, source work-item, risk tier, data classification, and bootstrap
profile. Use `intake` for the small business-review PR and `full` only when
you explicitly want the scaffold up front. `just ai-sdlc-new` uses the same
intake-first flow interactively.

This copies the reusable templates into `ai-sdlc/initiatives/PAY-4567/`. The
generated directory is the instance; the templates and configuration remain
shared by every initiative.

The intake profile creates only the core files needed for business review.
After the PR is approved or merged, one post-merge workflow expands the
reusable boilerplate, including HLD and LLD templates, and synchronizes valid
human requirement approval in a single follow-up PR.

For assistant-driven intake, see
[Initiative Intake Agent Guide](design/initiative-intake-agent-guide.md).

```text
initiatives/PAY-4567/
  initiative.md
  requirement.md
  initiative.yaml
  traceability.yaml
  approvals.yaml
  context-manifest.yaml
  context/relative/
  hld/
  lld/
  feedback/
  approvals/
  evidence/
```

## Validate initiatives

```text
just ai-sdlc-validate ai-sdlc/initiatives/PAY-4567
just ai-sdlc-validate-all
```

The underlying scripts are implementation details. The supported framework interface is the `just` command set.

## Generate HLD and run the bounded feedback loop

The lifecycle commands are skill entry points. For example, the direct HLD
skill can be run with:

```text
just ai-sdlc-skill hld-generation PAY-4567 codex gpt-5.6-luna
```

The readable lifecycle command is:

```text
just ai-sdlc-hld PAY-4567 codex gpt-5.6-luna
```

This command always runs the bounded AI HLD review loop. The default reviewer
is `codex gpt-5.6-terra`; both generator and reviewer can be overridden:

```text
just ai-sdlc-hld PAY-4567 codex gpt-5.6-luna codex gpt-5.6-terra
```

The HLD review skill can be run independently:

```text
just ai-sdlc-skill hld-review PAY-4567 codex gpt-5.6-terra
```

After the Product Owner has reviewed and approved the requirement, the command
prepares the context and request, generates the HLD, invokes the AI reviewer,
and reruns the same generator adapter only when the reviewer requests useful
changes:

```text
just ai-sdlc-hld PAY-4567 codex gpt-5.6-luna
```

The loop is bounded by `config/hld-loop-policy.yaml`. A passing AI review only
creates a human architecture review request; it never approves the HLD.

An approved initiative PR can automatically flip `initiative.yaml` and
`initiative.md` to `approved` and record the approval trail in
`approvals.yaml`.

After architect feedback:

```text
just ai-sdlc-hld-feedback PAY-4567 claude claude-sonnet
just ai-sdlc-hld PAY-4567 claude claude-sonnet
```

The second command can use a different AI provider while preserving the same initiative, context, artifacts, and approval rules.

## Run a bounded AI HLD review loop

An AI reviewer can critique the generated HLD before the human architect
review. The generator and reviewer can use different models:

```text
just ai-sdlc-hld-loop \
  PAY-4567 \
  codex \
  gpt-5.6-luna \
  codex \
  gpt-5.6-terra
```

The loop does the following:

```text
Generate HLD
  → Review with Terra
  → If changes are requested, regenerate
  → Review again
  → Stop when the review passes or a guardrail is reached
```

Each review is saved as `feedback/ai-review-N.md`. The loop stops when:

- The reviewer returns `pass`.
- The reviewer returns `escalate`.
- The configured safety iteration limit is reached.
- The configured time limit is reached.
- The same normalized feedback repeats.
- The HLD does not change after requested revisions.

The safety policy is stored in `config/hld-loop-policy.yaml`. A passing AI
review only creates a human architecture review request; it never approves the
HLD.

Use a dry run to inspect the planned calls without invoking an agent:

```text
AI_SDLC_HLD_LOOP_DRY_RUN=1 just ai-sdlc-hld-loop \
  PAY-4567 codex gpt-5.6-luna codex gpt-5.6-terra
```

## Current Confluence position

Confluence is not required for the current workflow. The repository is the
source of truth for shared context and initiative artifacts.

In a later stage, a Confluence connector may automatically retrieve selected
pages or synchronize approved knowledge into `context/`. That integration must
preserve the same context-pack, versioning, and approval contracts. It must not
require manually copying the whole Confluence knowledge base into every
initiative.

## Initial rollout success condition

An implementation PR without an approved HLD must fail the required check. An approved HLD must be tied to the exact artifact commit/hash and a named human Solution Architect.

For the exact HLD execution sequence, see the [HLD generation runbook](../docs/hld-generation-runbook.md) or the repository copy at `design/hld-generation-runbook.md`.

## Design placeholders

The Codex adapter is the first working provider implementation. Other providers
can be added under `tooling/providers/` by translating the same request contract
and writing the same response/artifact shape. The full DAS validator, context
retrieval, and PR automation are the next hardening layers.
