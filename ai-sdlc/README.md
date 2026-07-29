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

The GitHub workflow automatically starts after a validated approved initiative
scaffold is merged. It can also be started manually with an initiative ID and
separate Copilot generator and reviewer models. Demo defaults are the lower-cost
`claude-haiku-4.5` generator and `gemini-3.5-flash` reviewer. The workflow uses
the same bounded `hld_loop.sh` as local execution and refuses identical model
selections. It uses the Actions `GITHUB_TOKEN` by default, with an optional
`COPILOT_GITHUB_TOKEN` Actions secret as a personal-token fallback when the
organization has not enabled Copilot CLI for Actions.

With the `auto` profile, the loop first runs a lightweight impact assessment
and records `evidence/hld-assessment.yaml`. That assessment selects the detail
profile before the full HLD is generated. The profile guides the amount of
decision detail and diagram depth; it is not a hard line-count limit. Small
HLDs should remain concise, while medium and large HLDs may link supporting
documents for security, migration, deployment, options, or other detail.

New intake PRs should stay minimal: capture only `requirement.md` and optional
initiative-relative context. The post-merge automation creates the initiative
metadata, reusable boilerplate, and approval metadata in one follow-up PR.

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

The intake profile creates only `requirement.md` for business review. After the
PR is approved or merged, one post-merge workflow creates initiative metadata
and the context manifest, then synchronizes valid human requirement approval in
a single follow-up PR. HLD and LLD artifacts are created only by their gated
lifecycle workflows.

The metadata-only follow-up PR may be auto-merged after required checks pass.
Enable repository auto-merge and configure `AI_SDLC_AUTOMATION_TOKEN` with
`Contents: write` and `Pull requests: write` permissions when downstream
workflow events must be triggered by the merge. HLD and LLD PRs remain human
gated.

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
is `codex gpt-5.6-terra`; both generator and reviewer can be overridden. An
optional profile controls how much detail is expected:

```text
just ai-sdlc-hld PAY-4567 codex gpt-5.6-luna codex gpt-5.6-terra
# Optional final argument: small, medium, or large
just ai-sdlc-hld PAY-4567 codex gpt-5.6-luna codex gpt-5.6-terra small
```

The HLD review skill can be run independently:

```text
just ai-sdlc-skill hld-review PAY-4567 codex gpt-5.6-terra
```

If generation fails after `hld/hld.md` has been created, resume with the
existing artifact instead of regenerating it:

```text
AI_SDLC_HLD_RESUME=1 just ai-sdlc-hld PAY-4567 github-copilot claude-haiku-4.5 github-copilot gemini-3.5-flash auto
```

The resume path repairs or creates the preflight assessment, records the
selected profile in the HLD metadata, and continues with the bounded review
loop. It does not grant architecture approval.

After the Product Owner has reviewed and approved the requirement, the command
prepares the context and request, generates the HLD, invokes the AI reviewer,
and reruns the same generator adapter only when the reviewer requests useful
changes:

```text
just ai-sdlc-hld PAY-4567 codex gpt-5.6-luna
```

The loop is bounded by `config/hld-loop-policy.yaml`. A passing AI review only
creates a human architecture review request; it never approves the HLD.

HLD generation also creates `evidence/design-baseline.yaml`, which records the
exact requirement, initiative, HLD, LLD, and context versions and hashes used by
the design. Run `just ai-sdlc-version-view` to render the current repository
version matrix.

An approved initiative PR can automatically flip `initiative.yaml` and
`initiative.md` to `approved` and record the approval trail in
`approvals.yaml`.

The `auto` profile is the default. The HLD agent must classify the change as
small, medium, or large in the HLD metadata; the orchestrator then applies the
matching detail and safety limits. Automatic runs allow up to 45 minutes and
15 minutes per model call so context-heavy work is not cut off prematurely.
Explicit `small`, `medium`, and `large` profiles remain available when a
workflow owner intentionally overrides the default.

After architect feedback:

```text
just ai-sdlc-hld-feedback PAY-4567 claude claude-sonnet
AI_SDLC_HLD_RESUME=1 just ai-sdlc-hld PAY-4567 claude claude-sonnet
```

The second command can use a different AI provider while preserving the same initiative, context, artifacts, and approval rules.

## Run a bounded AI HLD review loop

An AI reviewer can critique the generated HLD before the human architect
review. The generator and reviewer can use different models. GitHub Actions
accepts free-form model IDs because Copilot availability varies by plan,
client, and organization policy:

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

The latest review is saved as `feedback/ai-review.md`, replacing the previous
review for that run. The loop checkpoint is `evidence/hld-loop.yaml`, so a
timed-out or interrupted run can be resumed with `AI_SDLC_HLD_RESUME=1`.
The loop stops when:

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

Use `auto` as a model value when Copilot should choose the model. In GitHub,
use **Actions → Generate HLD with Copilot → Run workflow** to type the
generator model, a different reviewer model, profile, per-call timeout, and
whether to resume. Automatic scaffold-merge runs use the configured defaults.
The human-readable model catalog is in
[`config/copilot-model-catalog.md`](config/copilot-model-catalog.md), including
copyable model IDs and economical/balanced/advanced routing guidance. The
machine-readable equivalent is `config/copilot-model-catalog.json`.
It is a convenience catalog, not an allow-list; GitHub may add, retire, or
restrict models without this repository changing. Unsupported or
policy-blocked IDs fail during the Copilot call under the account's normal
availability rules.
Human comments are captured with `just ai-sdlc-hld-feedback`; they do not
approve architecture and must be followed by an explicit bounded rerun.
Inline comments on an HLD PR are also captured automatically by the guarded
`Rerun HLD from Architect Review Comment` workflow. It records the comment in
`feedback/human-review.md`, reruns the bounded loop on the same HLD branch, and
updates the same PR. Human Solution Architect approval is still required.

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
