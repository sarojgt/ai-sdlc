# AI-SDLC Project Status and Delivery Checklist

This is the living checklist for the AI-native SDLC framework. Update it as the
framework evolves. Status values are:

- `[x]` complete and validated
- `[~]` started or partially implemented
- `[ ]` planned
- `[!]` blocked or requiring a decision

## End goal

Create a vendor-neutral engineering operating model in which AI participates
throughout delivery while humans retain ownership of business, architecture,
security, engineering, and release decisions.

The target lifecycle is:

```text
Business input
  → Requirement capture and business approval
  → Context discovery and impact assessment
  → AI HLD options and standards-based recommendation
  → AI review and bounded feedback loop
  → Human Solution Architect / ARB approval
  → LLD and implementation planning
  → Human engineering review
  → Incremental implementation and PR review
  → Security and release gates
  → Deployment evidence and traceability
```

The HLD approval gate must prevent LLD, implementation, merge, and deployment
from starting early.

## Prerequisites

- [x] Git repository and shell-based command interface.
- [x] `just` recipes for supported lifecycle commands.
- [x] Bash-compatible tooling for the current scripts.
- [~] Codex CLI adapter; local Codex installation and authentication are
      required to run generation and review.
- [~] GitHub CLI authentication for branch, push, and PR automation.
- [~] Provider-specific adapters and credentials for Claude, Gemini, Copilot,
      Qwen, local models, or other providers.
- [ ] Optional Mermaid, Docker, cloud, repository-scanning, Jira, Confluence,
      and MCP tooling as each integration is introduced.

## Completed foundation

- [x] Repository-first operating model established.
- [x] Vendor-neutral provider adapter concept established.
- [x] Codex provider adapter implemented with configurable model selection.
- [x] Provider-neutral adapter boundary documented for future providers.
- [x] Human-readable Markdown as the primary artifact format.
- [x] YAML metadata and evidence model established.
- [x] DAS metadata and schema foundation added.
- [x] Shared context separated into consistent context and guardrails.
- [x] Initiative-relative context separated from the requirement.
- [x] Initiative bootstrap templates created.
- [x] Requirement and HLD approval gates defined.
- [x] Bounded AI HLD feedback loop implemented.
- [x] Loop limits include iteration, elapsed time, repeated feedback, and
      unchanged-output protection.
- [x] AI progress messages added during long-running generation and review.
- [x] HLD impact assessment added for size, complexity/risk, services,
      repositories, integrations, data, security, deployment, and governance.
- [x] HLD recommendation uses enterprise principles, guardrails, standards,
      and approved patterns.
- [x] HLD alternatives are limited to meaningful trade-offs or constraints.
- [x] Mermaid diagrams embedded in the primary HLD document.
- [x] Canonical HLD path standardized as `initiatives/<ID>/hld/hld.md`.
- [x] Older demo initiatives archived under `ai-sdlc/examples/archive/`.
- [x] Incidental `.DS_Store` and graph workspace artifacts removed/ignored.
- [x] DEMO-005 used as the current reference initiative.
- [x] Process merged initiative PRs through one post-merge automation PR.
- [x] Auto-mark requirements approved from valid human review history.
- [x] Manual backfill path for missed initiative processing.
- [x] Post-merge scaffold creates reusable HLD and LLD Markdown templates.
- [x] Cross-agent repository and Copilot instructions define artifact boundaries.
- [x] Conventional Commit policy and PR title guidance added.
- [x] Change-focused branch naming policy and validation added.
- [x] Semantic release tag workflow added for merges to `main`.
- [x] Scoped semantic versions added for initiatives, HLDs, LLDs, and context.
- [x] HLD design baseline records exact parent versions and context hashes.
- [x] Human-readable version matrix command and GitHub summary added.
- [x] GitHub workflow actions upgraded for the Node 24 runner transition.
- [x] Initiative processing restricted to merged pull requests.
- [x] HLD and initiative bootstrap scripts work with BSD and GNU `sed`.
- [x] Copilot provider adapters are executable through local and CI entry points.
- [x] Copilot cloud-agent setup workflow prepares the repository toolchain and
      validates lifecycle/provider interfaces with read-only permissions.
- [x] `just` recipes use a portable Bash shell for GitHub-hosted runners.
- [x] HLD loop hashing supports Linux `sha256sum` and macOS `shasum`.
- [x] Generated evidence links use repository-relative paths instead of local
      machine paths.
- [x] Intake bootstrap creates only `requirement.md`; post-merge expansion
      creates metadata and the reusable initiative scaffold.

## Current repository workflow

- [x] Create initiative from template.
- [x] Capture title, business outcome, problem statement, owner, source,
      risk tier, and data classification at initiative creation.
- [x] Capture the fuller requirement in the Markdown template.
- [x] Add initiative-relative context.
- [x] Validate initiative structure.
- [x] Generate an HLD through a provider adapter.
- [x] Run an independent AI HLD review.
- [x] Iterate only on useful review feedback.
- [x] Stop at the human architecture gate.
- [~] Generate LLD only after recorded HLD approval.
- [ ] Generate implementation plans from approved LLD.
- [ ] Orchestrate changes across multiple repositories.
- [ ] Create implementation PRs automatically.
- [ ] Add engineering, security, and release review automation.

## Context engineering backlog

- [x] Consistent enterprise context stored in the repository.
- [x] Architecture guardrails stored in the repository.
- [x] Relative context manifest created per initiative.
- [x] Context gaps recorded with owner and retrieval action.
- [ ] Build automated relevance selection for large context sets.
- [ ] Add context freshness and source-hash validation.
- [ ] Add repository/API/schema/ADR discovery adapters.
- [ ] Add secure context filtering for sensitive content.
- [ ] Add Confluence synchronization as a future source connector.
- [ ] Add Jira synchronization as a future requirement and traceability source.
- [ ] Add optional knowledge graph or vector retrieval without changing artifact
      contracts.

## Human governance backlog

- [x] Business approval represented in the requirement artifact.
- [x] Architecture approval represented in HLD metadata and approval records.
- [~] Security, senior engineering, and release gates defined conceptually.
- [ ] Enforce CODEOWNERS and protected-branch rules in GitHub.
- [ ] Add required approval checks to HLD and LLD pull requests.
- [ ] Add architecture review checklists.
- [ ] Add approval invalidation when requirements or context change.

## Automation backlog

- [x] `just` command interface established.
- [x] HLD generation and bounded loop commands established.
- [x] Provider and model overrides supported.
- [x] Dry-run support available.
- [ ] Add GitHub Issue → initiative automation.
- [x] Add automatic and manual HLD workflow triggers.
- [x] Add Copilot cloud-agent setup instructions and repository working agreement.
- [x] Add draft HLD PR creation.
- [~] Add AI review comments to the HLD PR.
- [ ] Add human feedback webhook/command reruns.
- [ ] Add Jira issue and status synchronization.
- [ ] Add Confluence publication or synchronization.
- [ ] Add cross-repository work-plan orchestration.
- [ ] Add deployment and runtime evidence collection.

## Artifact and traceability backlog

- [x] Requirement Markdown template.
- [x] HLD Markdown template with embedded Mermaid diagrams.
- [x] LLD placeholder and approval lock.
- [x] ADR, risk, feedback, evidence, and traceability locations.
- [~] DAS schema validation.
- [ ] Requirement → HLD → LLD → stories → tasks → PR → deployment links.
- [ ] Content hashes for requirement, context, HLD, and LLD.
- [ ] Automated traceability completeness checks.
- [ ] Standard metadata for multi-repository initiatives.
- [ ] Versioned artifact migration strategy.

## Integration roadmap

### Phase 1 — Repository-first

- [x] GitHub repository artifacts, Markdown, `just` commands, provider adapters,
      and human review.

### Phase 2 — GitHub automation

- [ ] GitHub Issue forms for business-friendly intake.
- [~] GitHub Actions post-merge trigger and automation PR.
- [ ] CODEOWNERS and required checks.
- [ ] PR comments mapped to bounded AI reruns.

### Phase 3 — Enterprise work management

- [ ] Jira requirement and status synchronization.
- [ ] Confluence context synchronization.
- [ ] Preserve Jira/Confluence links as source references, not replacement
      artifact formats.

### Phase 4 — Orchestration and scale

- [ ] Impacted repository discovery.
- [ ] Multi-repository workspaces.
- [ ] Specialized agent roles.
- [ ] Cross-repository PR coordination.
- [ ] Release and deployment evidence integration.
- [ ] Metrics for AI contribution, review quality, loop frequency, and human
      decision latency.

## Current decisions

- Repository-first is the initial operating mode.
- Markdown is the human source of truth.
- HLD approval is the primary architecture gate.
- AI may recommend but cannot approve architecture.
- Missing facts become context gaps; AI must not invent enterprise-specific
  architecture.
- Existing enterprise standards and approved patterns are preferred.
- A new component requires evidence and human approval.
- Confluence and Jira are future integration points, not current dependencies.

## Next recommended work

1. Enforce Solution Architect approval through CODEOWNERS and branch rules.
2. Implement the post-HLD LLD gate.
3. Add repository and schema context discovery for a multi-repository initiative.
4. Add Jira and Confluence connectors after the repository-first flow is stable.
