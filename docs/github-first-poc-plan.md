# GitHub-First AI-SDLC POC and Context Management Plan

## Objective

Build the smallest working system that proves the core pattern:

```text
GitHub Issue
  -> Requirement artifact
  -> HLD options in a design PR
  -> human Solution Architect approval
  -> HLD gate check
  -> LLD and implementation plan
  -> implementation PR
  -> automated checks + human review
```

Jira and Confluence are not required for the first POC. The POC should use GitHub as the initial work, review, automation, and publication surface, but it must define provider-neutral interfaces so future adapters can be added without changing DAS, approval semantics, or context-pack structure.

## Recommended POC shape

Use three repositories, even if they initially live in one GitHub organization:

```text
ai-sdlc-design-ai-sdlc/       # authoritative requirements, HLD, LLD, ADRs, context manifests
ai-sdlc-control-plane/    # validators, policy, context builder, GitHub Actions/scripts
demo-service/              # a small real service changed by the pilot
```

If three repositories are too much for the first week, start with two: combine the design and control-plane repositories. Keep the demo service separate so the multi-repository pattern is exercised from the beginning.

## POC scope

### Include

- GitHub Issue as business requirement intake.
- Markdown + YAML DAS artifacts.
- GitHub draft PR for requirements and HLD review.
- Human Solution Architect approval through CODEOWNERS/required review.
- GitHub Action that blocks LLD and implementation PRs without an approved HLD hash.
- Context pack generated from selected files in the design repository and demo service.
- One AI adapter for requirements/HLD/LLD generation.
- One implementation PR created by the agent.
- Unit tests, lint, traceability, and gate checks.

### Exclude initially

- Autonomous production deployment.
- Full enterprise vector search.
- Automatic editing of Confluence or Jira.
- Many specialized agents.
- Cross-organization repository access.
- Complex legacy modernization.
- Automatic architecture approval.

## GitHub-first lifecycle

### 1. Issue intake

Create a GitHub Issue using an issue form with these fields:

- business outcome;
- user/problem statement;
- acceptance criteria;
- known constraints;
- data classification;
- expected repositories;
- requested Product Owner and Solution Architect;
- risk tier;
- `ai-sdlc:ready-for-analysis` label.

The issue form writes a structured body with stable identifiers. A `issues.opened` or label event starts the workflow.

### 2. Initiative initialization

GitHub Actions or a small control-plane service:

1. validates the issue fields;
2. creates `initiatives/<issue-number>/initiative.yaml`;
3. creates a requirement branch;
4. records the issue URL and issue number;
5. builds the initial context pack;
6. opens a draft requirements PR;
7. requests the Product Owner.

The workflow posts a comment containing the current lifecycle state and a link to the context evidence.

### 3. Requirement generation and approval

The Requirements agent receives:

- the issue body;
- the context pack;
- requirements template;
- approved standards relevant to the demo service.

It creates `requirement.md` and updates `traceability.yaml`. An Action validates IDs, required sections, acceptance criteria, and source references.

The Product Owner reviews and either:

- approves the PR;
- requests changes;
- asks a blocking question.

Approval is represented by a GitHub review plus a generated `approvals.yaml` record containing reviewer identity, role, commit SHA, and content hash. A new commit invalidates the previous approval.

### 4. HLD generation and architecture gate

After requirements approval, the workflow invokes the architecture agent. It must generate:

- at least two options;
- option scorecard;
- current and target diagrams;
- risks and trade-offs;
- security and data considerations;
- performance, scalability, cost, and operational impacts;
- migration and rollback;
- proposed ADRs;
- explicit recommendation and unresolved questions.

The HLD is opened as a draft PR. CODEOWNERS requests the Solution Architect. The architect comments and the agent updates the branch until the architect approves.

The architecture gate Action verifies:

```text
HLD status == approved
architecture reviewer has required role
approval commit SHA == current HLD commit SHA
approval content hash == current HLD hash
no blocking review comments remain
requirements traceability is complete
```

Only after this check passes may the LLD workflow run.

### 5. LLD and implementation plan

The LLD agent reads only:

- the approved HLD;
- its exact context pack;
- demo-service repository metadata;
- API/database/security standards.

It produces the LLD, implementation plan, test strategy, and traceability links. A Senior Engineer reviews the LLD. The control plane does not allow implementation PR creation until the LLD has an approved HLD parent.

### 6. Implementation PR

The implementation agent gets a bounded task:

```yaml
task:
  initiative: "DEMO-001"
  repository: "demo-service"
  base_sha: "abc123"
  hld: "HLD-DEMO-001@sha256:..."
  lld: "LLD-DEMO-001@sha256:..."
  requirements: ["REQ-DEMO-001-01"]
  allowed_paths: ["src/**", "tests/**", "docs/**"]
  prohibited_actions:
    - merge
    - production_deploy
    - modify_approved_hld
```

The agent creates a branch and draft PR. GitHub Actions run validation, tests, security checks, and traceability checks. Human reviewers approve and merge.

## GitHub repository layout

```text
ai-sdlc-design-ai-sdlc/
  .github/
    CODEOWNERS
    workflows/
      validate-das.yml
      architecture-gate.yml
      generate-artifact.yml
      traceability-check.yml
  schemas/
    das.schema.json
    policy.schema.json
  standards/
    architecture-principles.md
    security-baseline.md
    service-patterns.md
  initiatives/
    001-demo-feature/
      initiative.yaml
      requirement.md
      hld/hld.md
      lld/lld.md
      adrs/
      approvals.yaml
      traceability.yaml
      context-manifest.yaml
      evidence/
  templates/
  tooling/
    validate_das.sh
    check_gate.sh
    build_context.sh
```

## Provider-neutral boundaries

The POC should use GitHub adapters internally but expose these interfaces:

```text
WorkItemProvider
  create_item()
  get_item()
  update_status()
  add_comment()
  link_items()

ReviewProvider
  create_review_request()
  list_reviews()
  record_approval()
  list_blocking_comments()

RepositoryProvider
  get_file()
  create_branch()
  create_commit()
  open_pull_request()
  add_check()

KnowledgeProvider
  search()
  get_document_version()
  get_owner()

DeploymentProvider
  deploy()
  get_status()
  get_health_evidence()
```

For GitHub, implement these with Issues, PRs, commits, Actions, and repository APIs. Later:

- Jira implements `WorkItemProvider`;
- Confluence implements `KnowledgeProvider` and publication;
- GitLab/Bitbucket implement `RepositoryProvider` and `ReviewProvider`;
- Backstage or an internal catalog implements ownership and dependency discovery;
- Kubernetes/cloud/observability adapters implement deployment evidence.

The workflow must consume the interface, not GitHub-specific fields. GitHub issue numbers and PR URLs can remain in the adapter metadata and DAS traceability as external references.

## Context management

### Context principles

Context should be:

- **authoritative:** source and owner are known;
- **relevant:** selected for the current initiative, not dumped wholesale;
- **versioned:** commit SHA, tag, page version, or API revision is recorded;
- **classified:** access and data sensitivity are explicit;
- **fresh:** staleness is measurable;
- **traceable:** every material AI claim can point to evidence;
- **rebuildable:** derived indexes can be regenerated from source;
- **bounded:** each agent receives only what its role needs.

### POC context layers

For the GitHub-only POC, use four simple layers:

```text
Layer 1: Source files
  issue body, standards, service code, APIs, ADRs

Layer 2: Manifest
  what sources exist, owner, version, classification, freshness

Layer 3: Context pack
  selected excerpts, dependency facts, design references, open questions

Layer 4: Evidence
  retrieval time, hashes, queries, included/excluded sources, agent run metadata
```

Do not start by indexing every file into a vector database. First prove that a deterministic, manifest-driven context pack is sufficient. Add semantic search when the team can identify a recall problem that keyword/graph retrieval cannot solve.

### Context manifest

```yaml
das_version: "0.1"
initiative: "DEMO-001"
context_pack:
  id: "CTX-DEMO-001"
  version: 1
  status: "ready"
  generated_at: "2026-07-21T00:00:00Z"
  generated_by: "context-builder/0.1"
  items:
    - id: "CTX-001"
      uri: "github://org/demo-service/blob/abc123/README.md"
      source_type: "repository_file"
      source_version: "abc123"
      authority: "service-repository"
      classification: "internal"
      freshness_sla: "30d"
      why_included: "service purpose and current behavior"
      selected_sections: ["Overview", "Dependencies"]
      content_sha256: "sha256:..."
    - id: "CTX-002"
      uri: "github://org/ai-sdlc-design-ai-sdlc/blob/main/standards/security-baseline.md"
      source_type: "standard"
      source_version: "main@def456"
      authority: "enterprise-standard"
      classification: "internal"
      freshness_sla: "90d"
      why_included: "security requirements for the HLD"
      selected_sections: ["API Security", "Logging"]
      content_sha256: "sha256:..."
  exclusions:
    - uri: "github://org/demo-service/blob/abc123/test/fixtures/customer-data.json"
      reason: "contains unnecessary sensitive data"
```

### Context assembly algorithm

For `DEMO-001`, the context builder should:

1. Read the issue body and extract domain terms, requirements, APIs, repositories, data, and constraints.
2. Load explicit references from the issue and initiative manifest.
3. Load applicable standards based on risk tier, technology, data classification, and deployment target.
4. Inspect repository metadata, README, manifests, API definitions, ADRs, and ownership descriptors.
5. Resolve direct dependencies from build files and declared service metadata.
6. Select only relevant sections and symbol/file slices.
7. Remove secrets, credentials, production data, and irrelevant generated files.
8. Create the context manifest and evidence bundle.
9. Pass the context pack to the selected agent.
10. Store the context hash in the output artifact metadata.

### Context selection rules

Use deterministic rules first:

```text
include explicit issue references
include relevant standards
include owning service metadata
include direct API and dependency relationships
include ADRs linked to impacted components
include recent incidents only when the affected component matches
exclude secrets, credentials, fixtures, binaries, generated output
exclude files outside the agent's authorization scope
```

Then use semantic retrieval for:

- similar approved HLDs;
- examples of existing features;
- related terminology in the business glossary;
- previous incidents with equivalent failure modes.

Semantic results must still carry source URI, version, owner, classification, and relevance reason.

### Context freshness

Set freshness policies by source type:

| Source | Suggested POC freshness rule |
|---|---|
| Service source and manifests | Always use a specific commit SHA |
| API specifications | Specific commit or tagged release |
| ADRs | Latest approved version, with supersession check |
| Standards | Latest approved branch/tag, maximum 90 days without review |
| Incident data | Last 12 months, unless requirement references older incident |
| Similar designs | Approved artifacts, prefer last 24 months |

If a source violates its freshness SLA, the context pack should be marked `needs_review`, not silently used as current truth.

### Context tiers by agent

| Agent | Context it receives |
|---|---|
| Requirements | Issue, glossary, business standards, relevant examples, known constraints |
| Solution Architect | Requirements, service map, APIs, dependencies, standards, ADRs, incidents, cost/SLO information |
| LLD | Approved HLD, impacted repository slices, API/database standards, implementation conventions |
| Implementation | Approved HLD/LLD slices, task scope, allowed paths, local code, tests, relevant contracts |
| Security reviewer | Data classification, trust boundaries, threat model, changed files, policies, dependency findings |
| Release reviewer | Merged commit set, artifact hashes, CI/security evidence, rollout/rollback, deployment health |

Avoid giving every agent every source. More context is not automatically better context.

## POC GitHub Actions

### `validate-das.yml`

Triggered by every design PR. It should:

1. validate YAML and Markdown front matter;
2. validate DAS schema;
3. verify IDs and links;
4. calculate content hashes;
5. detect missing required sections;
6. render Mermaid/PlantUML diagrams;
7. publish a check summary.

### `architecture-gate.yml`

Triggered by HLD PR changes, reviews, and approval events. It should:

1. locate the HLD parent;
2. verify requirements coverage;
3. verify options/trade-offs/risk sections;
4. verify CODEOWNER approval by the current Solution Architect;
5. verify the approval is for the current commit/hash;
6. fail if the HLD is not approved;
7. emit `architecture.approved` only when all conditions pass.

### `implementation-gate.yml`

Triggered by implementation PRs. It should:

1. read DAS IDs from the PR body or changed files;
2. resolve the HLD and LLD;
3. verify HLD architecture approval;
4. verify LLD engineering approval;
5. verify PR scope is within the workstream;
6. run tests and security checks;
7. fail the required check on any mismatch.

### `context-build.yml`

Triggered by:

- `ai-sdlc:ready-for-analysis` label;
- requirement PR updates;
- HLD review comments requesting more context;
- changed service/API/ADR references;
- scheduled freshness scan.

It produces a new context-pack version and comments on the PR with included, excluded, stale, and unauthorized sources.

## Future Jira and Confluence integration

### Jira adapter

When Jira is added, Jira becomes the work-management surface:

- Jira Epic/Feature starts the initiative;
- Jira status changes trigger the control plane;
- stories and tasks are created after LLD approval;
- PRs and deployments update Jira automatically;
- DAS remains the technical source of truth;
- Jira stores links, status, ownership, and summaries.

No workflow rule should depend on a Jira description containing the full HLD. It should depend on the immutable DAS artifact reference and approval hash.

### Confluence adapter

When Confluence is added:

- approved requirements/HLD/LLD summaries are published to Confluence;
- Confluence pages link to immutable Git artifacts;
- Confluence comments can create Git design-change requests;
- page updates are ingested as proposed/non-authoritative context until reviewed;
- glossary and enterprise guidance can be indexed into the context system.

Avoid two editable masters. Git remains authoritative for technical design and approvals; Confluence becomes the collaboration, discovery, and publication layer.

## Implementation sequence

### Phase 1 — GitHub-only skeleton

- create the three repositories;
- copy the DAS templates;
- create issue form, labels, CODEOWNERS, and branch protection;
- implement `validate-das` and `architecture-gate` as scripts;
- run a manually initiated workflow with GitHub Actions.

### Phase 2 — Context pack

- implement the manifest format;
- ingest issue, standards, demo service, APIs, and ADRs;
- generate evidence and hashes;
- test context with the Solution Architect.

### Phase 3 — AI generation

- connect the model through a provider adapter;
- generate requirement, HLD, and LLD drafts;
- store model/run/context metadata;
- add bounded rerun actions from review comments.

### Phase 4 — Real implementation

- create scoped branches;
- generate one real implementation PR;
- run tests/security/traceability checks;
- enforce human review and merge.

### Phase 5 — Jira and Confluence adapters

- implement `WorkItemProvider` for Jira;
- implement `KnowledgeProvider` and publisher for Confluence;
- map existing GitHub references to Jira keys and Confluence page/version IDs;
- keep DAS and approval policies unchanged.

## POC success criteria

- A GitHub Issue creates a complete initiative skeleton automatically.
- Context is visible, versioned, classified, and reproducible.
- AI generates requirements and multiple HLD options.
- A Solution Architect can request changes and rerun only affected sections.
- LLD generation is blocked before HLD approval.
- An implementation PR without a valid HLD hash fails a required check.
- A human can approve, reject, or request changes at each gate.
- Every rerun and approval is auditable.
- The demo feature reaches a merged PR with requirement-to-PR traceability.
- Adding Jira later requires a new adapter, not a new lifecycle.
