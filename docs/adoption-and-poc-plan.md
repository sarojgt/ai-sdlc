# AI-Native SDLC Adoption and Live Workflow POC

## The adoption decision

Do not try to transform the whole engineering estate first. Establish one repeatable control loop around a real, medium-sized change:

```text
Jira requirement
  -> versioned requirement
  -> AI-generated HLD options
  -> Solution Architect approval
  -> AI-generated LLD
  -> implementation plan
  -> linked PRs
  -> tests and evidence
  -> human release approval
```

The first pilot should prove five things:

1. Enterprise context can be assembled with evidence and source versions.
2. AI can produce useful requirements and multiple HLD options.
3. A human can iterate on the HLD in a normal review workflow.
4. Implementation is technically blocked until the HLD approval exists.
5. The initiative remains traceable across Jira, design artifacts, commits, PRs, CI, and deployment.

The pilot should not attempt autonomous production deployment, broad enterprise indexing, or a large multi-agent marketplace.

## Recommended pilot selection

Choose one feature that is important enough to exercise architecture but safe enough to contain:

- one primary service and one dependent service;
- one API or event contract;
- one shared library or infrastructure change, if possible;
- a test environment and observable deployment;
- a willing Product Owner, Solution Architect, Senior Engineer, Security reviewer, and Release Owner;
- no irreversible production migration in the first iteration.

Good candidates are a new internal endpoint, an event-driven notification change, a small cross-service workflow, or a bounded monolith extraction. Avoid a trivial CRUD ticket and avoid a high-consequence payment/identity migration for the first pilot; neither exposes the right learning-to-risk ratio.

## Target pilot flow

### 1. Intake and requirement

The Product Owner creates a Jira epic or feature with business outcome, users, constraints, and success measures. The orchestrator creates an initiative directory and records the Jira issue as the parent.

The Requirements agent receives only the approved intake plus a generated context pack. It drafts:

- functional requirements with `REQ-*` IDs;
- measurable NFRs;
- acceptance scenarios;
- assumptions and open questions;
- glossary terms and impacted domains;
- initial risk classification.

The Product Owner resolves business ambiguity and approves the requirement artifact. If the scope changes materially, the artifact is versioned and re-reviewed.

### 2. Context discovery

For the pilot, start with five adapters rather than a full enterprise platform:

1. Jira issue and linked issues;
2. design repository;
3. service/repository metadata and dependency manifests;
4. API specifications and ADRs;
5. selected Confluence standards or team documentation.

The context assembler creates `evidence/context-pack.yaml`. Every item records its URI, commit/page version, retrieval time, authority, classification, and reason for inclusion. The Solution Architect can see what was used and what was excluded.

### 3. HLD generation and review

The Solution Architect invokes the HLD workflow. The architecture agent generates at least two options, diagrams, trade-offs, risks, security considerations, migration/rollback, cost/operational impact, and proposed ADRs.

The HLD is submitted as a draft design PR. The architect can comment:

- “Regenerate option 2 with an asynchronous boundary.”
- “Add consumer compatibility evidence.”
- “Show failure behavior when the dependency is unavailable.”
- “Reject this technology because it violates standard X.”

The agent updates the draft and preserves the diff. The architect then approves the exact artifact version and hash. The workflow changes from `hld.in_review` to `hld.approved` only through a human approval action.

### 4. HLD gate enforcement

The implementation unlock is validated in two places:

- the orchestrator refuses to create LLD/implementation work without a valid HLD approval;
- repository CI rejects a design or implementation PR whose DAS parent hash is missing, superseded, or not architecture-approved.

This dual enforcement is essential. The orchestrator controls the normal path; CI prevents bypass.

### 5. LLD and work decomposition

After approval, the LLD agent receives the approved HLD, relevant repository context, and standards. It produces repository-specific LLD sections and contracts:

- API/event schemas;
- persistence and migration changes;
- sequence and component diagrams;
- package/module changes;
- test strategy and acceptance mapping;
- monitoring, alerting, and runbook changes;
- rollout and rollback plan;
- workstreams for each repository.

The Senior Engineer reviews the LLD. Security, database, platform, or performance reviewers are added by risk rules, not by default for every ticket.

### 6. Incremental implementation

The orchestrator creates an initiative workspace and one branch per repository. The implementation agent works in small, bounded tasks. Each task contains:

- requirement IDs;
- HLD and LLD artifact hashes;
- repository and base commit;
- files or components in scope;
- acceptance criteria;
- test commands;
- “stop and escalate” conditions.

Agents may create commits and draft PRs. They may not merge, approve, change the HLD, access production credentials, or expand repository scope without a new work item.

### 7. Review and release

AI performs deterministic checks and review triage: tests, lint, SAST, dependency checks, contract compatibility, IaC validation, and design traceability. Humans review the PRs through normal CODEOWNERS and protected-branch rules.

The release agent assembles evidence. The Release Owner approves a test or production deployment according to existing change policy. After deployment, the system records deployment ID, commit SHA, artifact hashes, metrics, incidents, and learnings.

## Minimal implementation architecture

```text
                         +----------------------+
Jira / human portal ---->| Initiative API       |
                         +----------+-----------+
                                    |
                  +-----------------+------------------+
                  |                                    |
          +-------v--------+                  +--------v-------+
          | Policy + gates |                  | Workflow engine |
          +-------+--------+                  +--------+--------+
                  |                                    |
          +-------v--------+                  +--------v--------+
          | DAS artifact   |<---------------->| Agent gateway   |
          | service        |                  | model-neutral   |
          +-------+--------+                  +--------+--------+
                  |                                    |
          +-------v------------------------------------v-------+
          | Context assembler: Git, Jira, catalog, Confluence  |
          +----------------------+-----------------------------+
                                 |
          +----------------------v-----------------------------+
          | Repo workers + CI + PRs + deployment evidence      |
          +----------------------------------------------------+
```

For a POC, implement this as a small service or CLI plus CI checks. A durable workflow engine is valuable once human waits, retries, fan-out, and multi-day work appear; it is not required before the artifact contract and gate semantics are validated.

## POC repository layout

```text
ai-sdlc-platform-ai-sdlc/
  README.md
  schemas/
    das.schema.json
  templates/
    initiative.yaml
    requirement.md
    hld.md
    lld.md
    adr.md
    approvals.yaml
    traceability.yaml
  tooling/
    validate-das
    check-hld-gate
    build-context-pack
    render-diagrams
  examples/
    DEMO-001/
  .github/
    workflows/das-gates.yml
    CODEOWNERS
```

The POC should have one reusable starter copied into each participating service repository:

```text
.ai-sdlc/
  repository.yaml
  design-links.yaml
  implementation-policy.yaml
```

The service repository stores only local metadata and references. The full initiative design remains in the design repository.

## Iterative implementation plan

### Iteration 0 — operating agreement (1 week)

**Outcome:** people and decision rights are ready.

- choose the pilot initiative;
- name Product Owner, Solution Architect, Senior Engineer, Security reviewer, and Release Owner;
- define low/medium/high risk rules;
- agree that HLD approval is mandatory and architecture approvals are human-only;
- select the first model/agent only as an implementation detail;
- document prohibited actions: merge, production write, secret access, design bypass.

**Exit criteria:** signed pilot charter, named approvers, selected repositories, agreed success metrics.

### Iteration 1 — DAS and templates (1–2 weeks)

**Outcome:** artifacts are machine-readable and reviewable.

- implement DAS v0.1 schema and validation;
- create requirement, HLD, LLD, ADR, approval, evidence, and traceability templates;
- compute immutable content hashes;
- implement status transitions and supersession rules;
- add sample initiative `DEMO-001`.

**Exit criteria:** invalid approvals and missing parent hashes fail validation; valid artifacts render cleanly in Markdown.

### Iteration 2 — design repository and Git workflow (1–2 weeks)

**Outcome:** humans can review the design in a familiar workflow.

- create design repository;
- add design PR templates and CODEOWNERS;
- protect main branches;
- add required `das-validate` and `architecture-gate` checks;
- publish approved artifacts to Confluence or an internal page as read-only links;
- add Jira IDs and backlinks.

**Exit criteria:** an HLD can move from draft to approved through a human PR review; implementation PRs without an approved HLD fail CI.

### Iteration 3 — context pack builder (2–3 weeks)

**Outcome:** AI receives relevant, inspectable enterprise context.

- connect Jira, Git, API specs, ADRs, repository metadata, and selected documentation;
- build dependency and ownership lookup;
- add lexical and metadata filtering first; add vector search only where it improves recall;
- generate `context-pack.yaml` with provenance;
- add a human-visible context report.

**Exit criteria:** the architect can identify source, version, and reason for every material HLD fact; stale or unauthorized sources are excluded.

### Iteration 4 — Requirements and HLD agents (2–3 weeks)

**Outcome:** AI accelerates analysis while architecture remains human-owned.

- define role prompts and structured outputs;
- generate requirement drafts and HLD option sets;
- add contradiction, NFR coverage, standards, and traceability checks;
- support comment-driven regeneration;
- record model, prompt version, tools, context hash, and output hash.

**Exit criteria:** pilot HLD has at least two options, trade-off evidence, diagrams, risks, proposed ADRs, and an explicit human approval.

### Iteration 5 — LLD and implementation planning (2–3 weeks)

**Outcome:** approved architecture becomes executable repository work.

- generate LLD from approved HLD only;
- generate API/event/database/test/observability artifacts;
- create repository workstreams and dependency order;
- add senior-engineer approval and conditional specialist review;
- validate every workstream against the HLD hash.

**Exit criteria:** no LLD or implementation plan can be generated from a draft or superseded HLD; all workstreams have traceability.

### Iteration 6 — implementation workers and PR evidence (3–4 weeks)

**Outcome:** AI implements incrementally in real repositories.

- create isolated workspace/branch workers;
- allow scoped read/write access;
- run tests and static/security checks;
- create draft PRs with DAS metadata;
- add AI review as non-authoritative evidence;
- require human CODEOWNERS review and protected-branch status checks.

**Exit criteria:** one real feature reaches a merged PR with linked requirements, approved HLD/LLD, test evidence, human review, and no bypass.

### Iteration 7 — release evidence and learning loop (1–2 weeks)

**Outcome:** the lifecycle closes after deployment.

- assemble release checklist and artifact hashes;
- link deployment and runtime evidence;
- require human release approval;
- capture post-release metrics and incidents;
- create ADR or superseding design artifact for learning.

**Exit criteria:** a complete trace exists from Jira epic to deployed commit and operational evidence.

## What to build versus what to integrate

### Build internally

- DAS schema and validators;
- lifecycle state machine and gate policy;
- context-pack contract and evidence model;
- traceability model;
- enterprise role/tool permissions;
- reusable templates and CI checks;
- evaluation datasets and scorecards.

### Integrate initially

- Git provider;
- Jira;
- Confluence read/publish;
- existing CI/CD;
- service catalog or Backstage;
- existing security and observability tools;
- one approved model gateway or coding agent.

Do not build a model, a new ticketing system, a new source control system, or a custom vector database before the workflow proves value.

## Pilot success criteria

The pilot is successful when all are true:

- 100% of implementation PRs include a valid approved HLD hash;
- the gate blocks a deliberately invalid implementation attempt;
- requirement, HLD, LLD, PR, CI, and deployment links are queryable;
- the HLD contains multiple options and a human-recorded decision rationale;
- context sources are visible and versioned;
- at least one cross-repository dependency is coordinated;
- human reviewers report that AI reduced analysis or implementation effort without reducing decision quality;
- no production credentials or unapproved write tools are exposed to the agent;
- the team records defects, omissions, rework, cost, latency, and review time.

Suggested initial targets are 90%+ traceability, zero HLD-gate bypasses, less than 20% context items rejected as irrelevant, and measurable reduction in requirement/HLD preparation time. Treat these as pilot targets, not enterprise-wide promises.

## Operating cadence

- **Daily:** agent run status, blocked approvals, failed validations, cost and tool-use alerts.
- **Per artifact:** human review with explicit decision and conditions.
- **Per PR:** automated evidence first, then human review.
- **Weekly:** pilot retrospective, context omissions, agent failure patterns, and policy exceptions.
- **Monthly:** architecture governance review, model/provider evaluation, and template/schema changes.

## The first live demonstration

The best demonstration is not a chatbot. It is a button or command such as:

```text
start-initiative PAY-1234 --source jira --mode governed
```

It should create the initiative, assemble the context pack, draft the requirement, ask the Product Owner for approval, generate HLD options, pause for Solution Architect review, and visibly refuse to generate implementation work until the HLD approval hash exists. Once approved, it should generate LLD and linked workstreams, create draft PRs, and show the complete traceability view.

That is the smallest credible proof that this is an AI-native engineering operating model rather than another coding assistant workflow.
