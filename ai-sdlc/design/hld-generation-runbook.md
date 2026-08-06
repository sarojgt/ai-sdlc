# HLD Generation Runbook

## Purpose

Generate a reviewable HLD proposal from an approved requirement while keeping architecture approval fully human-owned.

The AI does not directly “decide the HLD.” It produces an HLD proposal, opens a design PR, and waits for the Solution Architect.

## Target-state trigger options

The following section preserves the future integration design. It is not the
current trigger contract; use the operating guide for the implemented GitHub
workflow.

The framework should support three equivalent triggers:

### Option 1 — GitHub label

In a future issue-driven integration, an intake system could add a label such
as `ai-sdlc:generate-hld` to an approved issue.

### Option 2 — GitHub Actions manual dispatch

```text
Actions → Generate HLD → Run workflow

initiative_id: DEMO-001
requirement_version: 2
mode: governed
```

### Option 3 — Control-plane command

```bash
ai-sdlc hld generate \
  --initiative DEMO-001 \
  --requirement REQ-DEMO-001@v2 \
  --mode governed
```

The command is a target interface. It can initially be implemented by a GitHub Action or a small service.

## Preconditions

The HLD workflow must stop before calling the model if any precondition fails:

```text
initiative exists
requirement exists
requirement status == approved
business approval exists
requirement content hash is current
context policy is available
Solution Architect is assigned
agent profile is approved
```

The HLD generator must not accept a raw Jira/GitHub description as its only input. It must use the versioned requirement artifact and context manifest.

## End-to-end execution

```text
1. Trigger received
2. Load initiative and approved requirement
3. Discover impacted context
4. Build context pack
5. Validate context pack and permissions
6. Invoke Solution Architect agent skill
7. Write a concise HLD proposal and only the diagrams needed for the decision
8. Validate HLD structure and traceability
9. Run architecture quality checks
10. Open a reviewable design PR
11. Request Solution Architect review
12. Pause workflow
```

### Step 1 — Load the requirement

Resolve:

```yaml
requirement:
  id: REQ-DEMO-001
  version: 2
  status: approved
  content_sha256: sha256:...
  source: initiatives/DEMO-001/requirement.md
```

If the requirement changes during the run, the run is cancelled and a new context/HLD run is required.

### Step 2 — Assemble context

The context builder retrieves:

- enterprise architecture principles;
- business and product context;
- payments domain context;
- relevant security and regulatory rules;
- impacted repositories;
- APIs and event contracts;
- direct dependencies;
- relevant ADRs and prior approved designs;
- recent incidents and runtime evidence where available.

The builder produces:

```text
initiatives/DEMO-001/evidence/context-pack-CTX-DEMO-001-v3.yaml
initiatives/DEMO-001/evidence/context-report-CTX-DEMO-001-v3.md
```

The context report must show included, excluded, stale, and unauthorized sources.

### Step 3 — Invoke the AI adapter

The workflow invokes a provider-neutral adapter:

```text
SolutionArchitectAgent.generate_hld(
  requirement_artifact,
  context_pack,
  guardrails,
  output_schema,
  tool_policy
)
```

The adapter may call any approved model or coding agent. The workflow records:

```yaml
agent_run:
  run_id: RUN-DEMO-001-HLD-003
  role: solution_architect
  skill: hld-generation
  model_provider: provider-adapter-id
  model_id: approved-model-id
  prompt_version: hld-generation-v1
  context_pack_id: CTX-DEMO-001
  context_pack_version: 3
  tools_allowed:
    - read_context
    - read_repository
    - read_api_contract
    - render_diagram
  tools_denied:
    - merge_code
    - approve_architecture
    - deploy_production
  started_at: 2026-07-21T00:00:00Z
  completed_at: 2026-07-21T00:10:00Z
```

## Agent output contract

The agent must return a concise human-readable HLD plus machine-verifiable
metadata, not only free text:

```yaml
hld_generation_result:
  artifact_id: HLD-DEMO-001
  status: draft
  selected_recommendation: OPT-01
  files:
    - hld/hld.md                         # primary review artifact; diagrams embedded
    - hld/options.md                     # optional; only for material alternatives
  requirements_covered:
    - REQ-DEMO-001-01
    - REQ-DEMO-001-02
  open_questions:
    - Q-DEMO-001-01
  risks:
    - RISK-DEMO-001-01
```

The agent must label statements as:

- `fact` — supported by a context source;
- `inference` — derived from facts;
- `proposal` — a design suggestion;
- `unknown` — requires human or external confirmation.

## HLD content minimum

The generated HLD must include the following decision content, using the
reference section names from the template. It must not include every available
section:

1. A concise change-size and impact summary.
2. Motivation, Solution Overview, Solution Design, and Risks.
3. Confirmed context and explicit context gaps with owners and retrieval actions.
4. Current-state and target architecture at decision level where the change requires it.
5. Only the options needed for an architectural decision and a trade-off summary.
6. Recommended direction, risks, and human decision points.
7. Only the applicable security, Non-Functional Requirements, operations, rollout, and cost content.
8. Optional Mermaid diagrams embedded directly in `hld.md` when they clarify a decision.
9. Only optional sections selected by the impact assessment.

The HLD must not become an LLD. Executable SQL, class/package structure, exact
test cases, migration scripts, and detailed deployment manifests belong after the
architecture gate in the LLD.

## Automated validation before human review

The workflow must run these checks before opening the PR:

```text
das-schema-valid
mandatory-core-present-and-nonempty
assessment-profile-consistent
requirement-context-and-baseline-hashes-consistent
single-risk-and-context-gap-registers
no-unresolved-template-placeholders
optional-mermaid-advisory-checks
```

If validation fails, the workflow sends the findings back to the agent for one bounded repair attempt. After the retry budget is exhausted, it opens a `needs-human-input` issue instead of continuing silently.

## Draft PR creation

The workflow creates a branch such as:

```text
ai-sdlc/DEMO-001/hld-v3
```

The PR body contains:

```text
Initiative: DEMO-001
Requirement: REQ-DEMO-001@v2
Context pack: CTX-DEMO-001@v3
Agent run: RUN-DEMO-001-HLD-003
Artifact: HLD-DEMO-001@v1
Status: Ready for Solution Architect review

The AI produced a recommendation for human review. No architecture decision has been approved.
```

The PR is assigned to the Solution Architect through CODEOWNERS. The workflow then pauses.

## Human review outcomes

### Approve

The Solution Architect approves the PR. The control plane:

1. verifies reviewer identity and role;
2. verifies the review applies to the current commit;
3. calculates the HLD content hash;
4. appends the architecture approval record;
5. changes HLD status to `approved`;
6. emits `architecture.approved`;
7. unlocks LLD generation.

### Request changes

The architect comments on the PR. The workflow classifies comments:

- factual correction;
- missing context;
- trade-off question;
- required design change;
- non-blocking suggestion.

For blocking comments, it invokes a bounded rerun with the comment and affected section. It does not regenerate the entire HLD unnecessarily.

### Reject

The workflow records the reason, marks the HLD rejected, and returns the initiative to HLD discovery. No LLD or implementation workflow can start.

### Ask question

The workflow creates a blocking question in the initiative and pauses only the dependent branch of work.

## Example GitHub Action interface

```yaml
name: Generate HLD

on:
  workflow_dispatch:
    inputs:
      initiative_id:
        required: true
        type: string
      requirement_version:
        required: true
        type: string
      mode:
        required: true
        default: governed
        type: choice
        options: [governed]
  issues:
    types: [labeled]

jobs:
  generate-hld:
    if: github.event.label.name == 'ai-sdlc:generate-hld' || github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v4
      - name: Validate preconditions
        run: ./ai-sdlc/tooling/hld-preconditions.sh "${{ inputs.initiative_id }}"
      - name: Build context pack
        run: ./ai-sdlc/tooling/build-context.sh "${{ inputs.initiative_id }}"
      - name: Generate HLD through model adapter
        run: ./ai-sdlc/tooling/generate-hld.sh "${{ inputs.initiative_id }}"
      - name: Validate generated HLD
        run: ./ai-sdlc/tooling/validate-hld.sh "${{ inputs.initiative_id }}"
      - name: Open design pull request
        run: ./ai-sdlc/tooling/open-design-pr.sh "${{ inputs.initiative_id }}"
```

The scripts are intentionally separated. Each can later become a service or workflow activity without changing the lifecycle.

## What the model receives

The agent should receive a structured request similar to:

```yaml
request:
  role: solution_architect
  task: generate_hld
  initiative: DEMO-001
  requirement:
    artifact_id: REQ-DEMO-001
    version: 2
    content_sha256: sha256:...
  context_pack:
    id: CTX-DEMO-001
    version: 3
    content_sha256: sha256:...
  guardrails:
    - architecture-principles
    - security-baseline
    - payments-domain-rules
  output_schema: hld.v0.1
  constraints:
    - generate_at_least_two_options: true
    - implementation_is_locked: true
    - approval_must_be_human: true
```

This request is stable across Claude, Codex, GPT, Gemini, Qwen, local models, or future agents.

## The key distinction

There are three separate actions:

```text
AI generates HLD proposal
        ≠
Human approves HLD
        ≠
System unlocks implementation
```

The AI performs the first. The Solution Architect performs the second. The policy/gate system performs the third only after verifying the second.

## First implementation steps

1. Implement `hld-preconditions.sh`.
2. Implement `build-context.sh` using the existing `context-manifest.yaml` format.
3. Implement one `generate-hld.sh` adapter using the approved AI tool.
4. Implement `validate-hld.sh` with deterministic checks.
5. Implement `open-design-pr.sh`.
6. Add HLD paths to CODEOWNERS.
7. Protect the `architecture-gate` check.
8. Run the workflow on `DEMO-001`.
9. Approve the HLD manually.
10. Verify that the `architecture.approved` event enables LLD generation.

The first successful demonstration is a generated HLD PR that a Solution Architect can iterate on, approve, and then use to unlock the next stage—without the agent ever approving or implementing its own architecture.
