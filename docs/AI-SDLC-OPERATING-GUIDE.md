# AI-SDLC Operating Guide

This is the concise guide to the currently implemented repository-first flow.
The repository is an evolving engineering standard, not an application project
and not limited to a one-off proof of concept. Older research and adoption
documents remain useful background; this guide is the source for day-to-day
operation.

## Current lifecycle

```text
Business requirement
  -> intake initiative PR
  -> Product Owner / CODEOWNER approval
  -> intake PR merge
  -> post-merge metadata and context PR
  -> scaffold PR auto-merge (when repository settings allow it)
  -> HLD workflow starts from the merged scaffold PR
  -> preflight impact assessment selects small/medium/large detail profile
  -> HLD generation with shared and relative context
  -> Mermaid and HLD contract validation
  -> bounded independent AI review loop
  -> draft HLD PR
  -> Solution Architect / ARB review and approval
  -> approval metadata synchronization
  -> LLD and implementation planning (gated next stage)
```

The HLD approval is the primary architecture gate. AI may discover context,
assess impact, draft, revise, and review; it cannot approve architecture or
start implementation.

## What is automated and what is human

| Stage | Automation | Human decision |
|---|---|---|
| Intake | Template creation, structure validation, PR checks | Business scope and requirement approval |
| Post-merge | Approval-history lookup, metadata/context scaffold PR, optional auto-merge | Repository settings and exception handling |
| HLD preparation | Context loading, preflight assessment, profile selection | Correct missing context when a gap is found |
| HLD | Provider invocation, Mermaid/contract validation, bounded review loop, draft PR | Solution Architect/ARB architecture approval |
| HLD feedback | One submitted review becomes one bounded rerun on the same branch | Architect decides whether feedback is sufficient |
| LLD onward | Gated artifact creation is planned/partial | Engineering, security, release, and deployment approvals |

## Repository artifacts

For a new intake PR, keep the change small:

```text
ai-sdlc/initiatives/<ID>/requirement.md
ai-sdlc/initiatives/<ID>/context/relative/<optional-context>.md
```

Post-merge automation adds metadata and the context manifest. HLD generation
creates only the design artifacts it needs, including:

```text
ai-sdlc/initiatives/<ID>/hld/hld.md
ai-sdlc/initiatives/<ID>/evidence/hld-assessment.yaml
ai-sdlc/initiatives/<ID>/evidence/hld-run.yaml
ai-sdlc/initiatives/<ID>/evidence/design-baseline.yaml
ai-sdlc/initiatives/<ID>/feedback/reviews/ai-review-iteration-<N>.md
```

Markdown is for human decisions. YAML is for metadata, approvals, hashes,
validation, and execution evidence.

## GitHub triggers

| Workflow | Current trigger | Purpose |
|---|---|---|
| `initiative-approval-sync.yml` | Merged initiative PR; manual recovery | Records valid intake approval and opens the scaffold PR |
| `generate-hld.yml` | Merged `chore/initiative-post-merge-*` PR; manual dispatch | Generates and reviews an HLD |
| `hld-trigger-reconciler.yml` | Manual dispatch only | Recovers a missed HLD handoff without scheduled model runs |
| `hld-review-feedback.yml` | Submitted architect `Request changes` review | Batches its summary and inline comments into one bounded HLD revision |
| `hld-approval-sync.yml` | Merged `feat/hld-*` PR; manual recovery | Records current-head architect approval |
| `das-gate.yml` | Initiative/config/schema/workflow PR | Validates structure and publishes the repository gate summary |

The HLD workflow deliberately does not run for the initial intake merge. It
waits for the separately merged scaffold PR, ensuring requirements approval,
metadata, and context manifest exist first. It also skips an initiative that
already has loop evidence unless `force` or `resume` is explicitly selected.

## Commands

Prerequisites are Git, `just`, Bash, and the selected provider CLI for local
runs. Use `gh` for GitHub branches and pull requests. GitHub Actions perform
structural Mermaid checks without requiring browser rendering; local runs can
enable rendering when Mermaid CLI and Chromium are available.

```text
just ai-sdlc-new
just ai-sdlc-validate ai-sdlc/initiatives/<ID>
just ai-sdlc-validate-all
just ai-sdlc-test
just ai-sdlc-context <ID>
just ai-sdlc-context-drift <ID>
just ai-sdlc-hld <ID> codex <generator-model> codex <reviewer-model> auto
AI_SDLC_HLD_RESUME=1 just ai-sdlc-hld <ID> codex <generator-model> codex <reviewer-model> auto
just ai-sdlc-hld-feedback <ID> <provider> <model>
```

Local adapters currently include Codex and GitHub Copilot. Other providers
must implement the shared adapter contract; examples using Claude, Gemini, or
Qwen are future adapter examples unless the provider exists in
`ai-sdlc/tooling/providers/`.

For GitHub Actions, use **Actions → Generate HLD with Copilot → Run workflow**
to provide the initiative, generator model, different reviewer model, profile,
timeouts, and resume/force options. The model catalog is a convenience
reference, not a guarantee of availability under every GitHub plan or policy.

## Context handling

The HLD request combines:

```text
consistent context + guardrails + initiative-relative context
  + requirement + approved artifact history
  -> evidence-backed context used by the generator
```

Shared context is under `ai-sdlc/context/consistent/` and
`ai-sdlc/context/guardrails/`. Initiative context is under
`ai-sdlc/initiatives/<ID>/context/relative/`. Missing facts are recorded as
context gaps with an owner and retrieval action; the agent must not invent
enterprise components to hide an incomplete context pack. Confluence and Jira
connectors are future integrations and are not required by the current flow.

## Recovery and guardrails

- GitHub HLD runs push checkpoint commits after generation, review, and failure
  handling; a rerun with `resume` can continue from the latest pushed state.
- Failed or interrupted checkpoints are automatically eligible for resume;
  successful checkpoints remain skipped. Resume is refused if the requirement
  or context manifest hash has changed.
- The workflow restores repository tooling after the AI run so generated
  agents cannot delete lifecycle validators or workflow files.
- HLD branches are updated with normal commits; the workflow does not force-push.
- Inline comments are collected with their submitted `Request changes` review;
  questions and individual comment edits do not start model runs.
- Feedback and approval workflows validate the reviewer against the repository
  allowlist. Production use also requires the [GitHub governance setup](GITHUB-GOVERNANCE-SETUP.md).
- The loop stops on its configured iteration/time limits, repeated feedback,
  unchanged output, escalation, or a review-ready result.
- AI review is advisory. A result such as `ready_for_human_review` means the
  draft is ready for an architect, not that it is approved.
- HLD evidence records the selected context-package tags and commits. Context
  drift is evaluated explicitly and writes evidence only; it never regenerates
  or invalidates an HLD automatically.
- Use the manual reconciler only for a missed handoff; it is intentionally not
  scheduled because scheduled scans can consume model tokens unexpectedly.

## Known boundaries

Implemented: repository artifacts, context separation, provider boundary,
intake/scaffold automation, HLD generation, preflight sizing, Mermaid and
contract validation, bounded AI review, resume, and human approval metadata.

Still evolving: full relevance-based context retrieval, Jira/Confluence sync,
LLD generation, multi-repository orchestration, implementation PR creation,
security/release gates, and deployment evidence.

See [AI-SDLC-STATUS.md](AI-SDLC-STATUS.md),
[`ai-sdlc/README.md`](../ai-sdlc/README.md), and the
[HLD generation runbook](../ai-sdlc/design/hld-generation-runbook.md) for
detailed reference material.
