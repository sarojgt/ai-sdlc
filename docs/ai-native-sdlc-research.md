# Enterprise AI-Native SDLC with Human-Governed Architecture

**Research and reference architecture — 21 July 2026**

## Executive recommendation

Adopt a **design-first, evidence-producing AI SDLC**. AI is an engineering participant, not the owner of engineering decisions. The system of record is a versioned set of design artifacts; the orchestration layer turns those artifacts into controlled work across repositories; normal repository controls remain the final enforcement point.

The recommended operating model has five properties:

1. A business requirement is converted into a versioned, testable requirement artifact.
2. Context is assembled from authoritative sources and recorded with provenance, freshness, and access policy.
3. AI produces several HLD options and a trade-off analysis. A named human Solution Architect approves one option, or the workflow stops.
4. Only an approved HLD can unlock LLD generation and implementation planning. This is a machine-enforced state transition, not a process reminder.
5. AI may implement, test, review, and prepare deployment evidence, but humans retain approval for requirements, architecture, security exceptions, merge, and release.

This is deliberately model-neutral. Models, coding agents, retrieval systems, and MCP servers are replaceable adapters behind stable artifact and workflow contracts.

## What current approaches teach us

| Approach | Useful contribution | Limitation for this enterprise use case | Recommendation |
|---|---|---|---|
| Spec-Driven Development (GitHub Spec Kit, OpenSpec-style workflows) | Moves the source of truth from an informal prompt toward persistent specifications and plans. GitHub describes Spec Kit as a specification-driven development toolkit with lifecycle automation and extensions. | Usually optimizes the project/repository loop; it does not by itself solve enterprise architecture authority, cross-repository coordination, or release governance. | Adopt the discipline; extend it with DAS, architecture gates, and an initiative-level orchestrator. |
| AI-first / AI-assisted SDLC | Applies AI across requirements, coding, testing, documentation, and operations. | Often remains a collection of assistants. Context, provenance, approvals, and model changes are easily lost. | Use as a capability layer, not as the operating model. |
| Human-in-the-loop engineering | Makes accountability, exception handling, and review explicit. Research on human-in-the-loop software agents frames human guidance as part of plan and code generation, not just a final override. | “Human in the loop” is weak if the person only rubber-stamps output or cannot see evidence. | Use risk-based, evidence-led gates with named decision rights. |
| Agentic software factory | Treats business intent, architecture, development, assurance, release, and learning as one integrated flow. | Factory language can encourage excessive automation and vendor-specific platforms. | Adopt the operating-model view while keeping artifacts and adapters open. |
| Multi-agent orchestration | Specialized roles can critique one another and divide work by bounded capability. | Role proliferation, coordination overhead, correlated model errors, and unclear accountability. | Use a small set of role prompts with deterministic workflow states; add specialists only when their evidence is distinct. |
| General-purpose coding agent | Fast to deploy, flexible, and good for implementation loops. | Weak at enterprise memory, architecture consistency, and multi-repository planning without a harness. | Permit any agent through the same DAS and tool policy. |

The strongest common lesson is that the central problem has shifted from code completion to **delegated execution under human supervision**. Recent research identifies evaluation, governance, technical debt, skill redistribution, and attention economics as open problems. IEEE P26044 is also organizing generative-AI software-engineering capabilities across governance, project, technical, and organizational processes, covering requirements, architecture, implementation, verification, integration, and maintenance. These are useful corroborating directions, but neither is a complete enterprise implementation blueprint.

## Target operating model

### Lifecycle states

```text
INTAKE
  -> REQUIREMENTS_DRAFT
  -> REQUIREMENTS_APPROVED       [Business/Product Owner]
  -> HLD_DRAFT
  -> HLD_REVIEW                  [Solution Architect iterates with AI]
  -> HLD_APPROVED                [mandatory architecture gate]
  -> LLD_DRAFT
  -> LLD_APPROVED                [Senior Engineer; Security as required]
  -> IMPLEMENTATION_PLANNED
  -> IMPLEMENTING
  -> PR_REVIEW                   [AI checks + human engineering review]
  -> RELEASE_CANDIDATE
  -> RELEASE_APPROVED            [Release owner; risk-based security sign-off]
  -> DEPLOYED
  -> OPERATING / LEARNINGS
```

The transition service must reject an LLD, implementation plan, branch, or PR if its `design.hld` does not point to an immutable artifact version with `status: approved`. A later HLD revision invalidates downstream artifacts and requires re-approval. A human approval is valid only when the approver has the required role, the approved content hash is recorded, and the approval has not been superseded.

### Decision rights

| Gate | Human owner | AI may do | AI must not do |
|---|---|---|---|
| Business intent | Product Owner / Business Owner | Clarify ambiguity, propose acceptance criteria, identify glossary terms and assumptions | Invent business policy or accept scope on behalf of the business |
| Requirements | Product Owner + Requirements Engineer | Draft functional/non-functional requirements, scenarios, traceability, contradictions | Mark requirements approved |
| HLD | Solution Architect / Architecture Board | Discover impact, generate options, diagrams, risks, cost and trade-offs, challenge assumptions | Choose the architecture, accept material risk, or unlock implementation |
| LLD | Senior Engineer / Tech Lead; Security/DB reviewers when triggered | Generate API/schema/sequence/package/test/observability detail from approved HLD | Change HLD intent silently or waive standards |
| Implementation | Engineers | Edit branches, run tests, make incremental commits, repair failures | Merge to protected branches or expand scope without a new artifact |
| Security | Security owner for high-risk changes | Threat model, SAST/SCA/IaC checks, misuse cases, findings triage | Accept unresolved critical risk or grant an exception |
| Release | Release owner / Operations | Assemble evidence, rollout/rollback plan, canary analysis, release notes | Authorize production release where policy requires human approval |

The HLD gate is the primary governance gate. The other gates are complementary: a good HLD cannot replace business approval, security risk acceptance, or release accountability.

## Context engineering

### Context is a supply chain, not a prompt

Build an enterprise context plane with four layers:

1. **Authoritative sources:** requirements and decisions in Git; service metadata and ownership in a catalog; API specifications; standards and policies; Jira work items; Confluence knowledge pages; source, infrastructure, observability, and incident data.
2. **Normalized index:** parse Markdown/YAML/JSON/OpenAPI, code symbols, dependency graphs, ownership, runtime relationships, ADR links, and Jira/PR/deployment references into a searchable graph plus keyword/vector indexes.
3. **Feature context pack:** for each initiative, resolve the domain, owners, impacted systems, relevant standards, recent ADRs, APIs, data classifications, SLOs, incidents, examples, and repository slices. Rank and cap content; do not dump the enterprise into the model context window.
4. **Evidence bundle:** persist the exact sources, commits/page versions, timestamps, retrieval queries, snippets, and policy decisions used to produce each artifact.

Use hybrid retrieval: graph traversal for “what depends on this service?”, lexical search for exact identifiers and standards, vector search for semantic similarity, and deterministic filters for ownership, classification, environment, and freshness. Retrieval should be scoped by the human initiative and the agent's least-privilege identity. Treat all retrieved content as untrusted input; repository text must not be allowed to override system policy or tool authorization.

### Relevance algorithm

For a feature, select context in this order:

1. Explicit references from the requirement and Jira issue.
2. Owning domain, system, component, API, data store, and infrastructure relations.
3. Transitive dependencies up to a configured depth, with impact analysis from build manifests and catalog relationships.
4. Applicable standards based on technology, data classification, risk tier, and deployment target.
5. Similar approved designs and ADRs, weighted by recency and owner.
6. Recent incidents, reliability signals, and examples of existing features.

Every context item gets `source_uri`, `source_version`, `authority`, `retrieved_at`, `freshness_sla`, `classification`, and `why_included`. Context quality is testable: coverage of impacted components, stale-source rate, unsupported-claim rate, and architect-reported omissions.

### Catalog and knowledge

Use a catalog such as Backstage or an equivalent open API as an index, not the ultimate source of truth. Backstage models domains, systems, components, APIs, resources, ownership, and dependency relations; its own documentation describes the catalog as a hub/cache fed from authoritative sources. This is a good pattern for discovery at hundreds of services, provided repository descriptors and runtime/infrastructure facts are reconciled and conflicts are surfaced.

## HLD workflow

The HLD generator must produce a decision brief, not a single answer. The minimum output is:

- problem statement, scope, goals, non-goals, assumptions, and open questions;
- impacted business capabilities, domains, systems, components, APIs, data, and repositories;
- at least two materially different options, including “change the existing system” and “do nothing/defer” where credible;
- C4 context/container diagrams and relevant sequence/data-flow diagrams;
- option scorecard across requirement fit, consistency, security, privacy, resilience, performance, scalability, operability, migration complexity, delivery risk, reversibility, cost, and team ownership;
- threat model, failure modes, data classification, regulatory considerations, and abuse cases;
- migration, rollout, rollback, observability, and support implications;
- proposed ADRs, each capturing one decision, rationale, alternatives, and consequences;
- a recommendation that explicitly states what remains uncertain and what evidence would change it.

The architect reviews in a PR or design workspace. AI may answer comments, regenerate one option, update diagrams, and run consistency checks. It must preserve review history and show a diff between artifact versions. Approval applies to a content hash, not to a mutable page.

Architecture review checklist:

- Does the design satisfy every approved requirement and NFR?
- Are boundaries, ownership, data authority, and integration contracts explicit?
- Are failure, retry, idempotency, consistency, and back-pressure behavior defined?
- Are security controls, trust boundaries, secrets, privacy, and abuse cases addressed?
- Are operability, SLOs, alerts, runbooks, support ownership, and cost understood?
- Is the migration reversible and safe for existing consumers?
- Are the ADRs complete and are deviations from enterprise standards explicit?

## LLD workflow

After HLD approval, an LLD agent creates repository-scoped details and validates them against the HLD. Typical outputs are OpenAPI and/or AsyncAPI contracts, resource and database changes, class/package/module structure, sequence diagrams, event schemas, migration scripts and backfill plans, test strategy, test data constraints, observability, deployment configuration, and a repository-by-repository implementation plan.

LLD review remains human-owned for database ownership and destructive migrations, public API compatibility, security-sensitive flows, concurrency and consistency, operational controls, and any design deviation. The LLD validator should fail on orphan requirements, undeclared repositories, unapproved technology choices, missing compatibility plans, or HLD contradictions.

Use OpenAPI as the language-neutral HTTP contract; the current published specification is 3.2.0. Use AsyncAPI or an equivalent event contract where applicable. Use Mermaid or PlantUML for diagrams stored beside the artifact so they render in GitHub and can be regenerated. Use ADRs for decisions, not for dumping a whole design into an unreviewable narrative.

## Multi-repository orchestration

Represent an initiative as one graph with many workstreams, not as unrelated Jira stories. The orchestrator discovers repositories from the catalog and dependency graph, creates a workspace per repository, passes the same approved HLD and relevant LLD slice to each agent, and creates linked PRs. It must support dependency ordering and parallelism:

```text
approved HLD
   |
   +-- shared contract / library PR
   +-- provider or database migration PR
   +-- service A PR ----+
   +-- service B PR ----+--> integration test environment
   +-- infrastructure PR+
                         --> release evidence --> human release approval
```

Each workstream has a bounded scope, repository commit base, design-artifact references, acceptance criteria, and status. Cross-repository changes are merged only when contract tests, compatibility checks, and the orchestration policy pass. A PR cannot change the approved HLD silently; a change request creates a new HLD revision or ADR and re-runs impact analysis.

For monolith modernization, use the same model but add strangler-boundary evidence: extracted capability, source-of-truth transition, dual-write/read strategy if any, reconciliation, traffic migration, rollback, and decommission criteria.

## Design Repository and documentation strategy

Choose a **hybrid Git-first design repository**:

- Git is authoritative for Requirements, HLD, LLD, ADRs, diagrams-as-code, manifests, schemas, and approvals.
- Service repositories contain a small, immutable reference file and local implementation ADRs, not duplicate copies of the full initiative design.
- An orchestration service indexes the design repository, Jira, catalog, source, CI/CD, and Confluence.
- Confluence is the human-friendly publication and knowledge surface for executive summaries, team guidance, glossary, onboarding, and links to immutable Git artifacts.

Git provides commit identity, branching, diff, code review, automation, and offline portability. Confluence provides collaborative editing, page history, comparison, comments, and discovery; Atlassian explicitly recommends pages with drafts and version history for specs that require approvals. It is therefore useful for collaboration and publication, but mutable page state should not be the authorization token that unlocks implementation. Synchronize one directionally: approved Git artifacts publish to Confluence, while Confluence proposals link back to a Git change. Avoid two editable masters.

Recommended design repository:

```text
design-repository/
  standards/                 # versioned enterprise policies and patterns
  glossary/                  # business terms and domain vocabulary
  initiatives/
    PAY-1234-example/
      initiative.yaml
      requirement.md
      hld/
        hld.md
        diagrams/
        options/
      lld/
        service-a.md
        service-b.md
        contracts/
      adrs/
      approvals.yaml
      traceability.yaml
      evidence/
  schemas/                   # DAS JSON Schema and validation rules
  tooling/                   # render, lint, index, and gate checks
```

## Design Artifact Specification (DAS) v0.1

DAS is the stable contract between people, agents, orchestrators, and repositories. Markdown is the human body; YAML front matter or a companion YAML file is the machine envelope. The normative identity is `artifact_id + version + content_sha256`.

### Required envelope

```yaml
das_version: "0.1"
artifact:
  id: "PAY-1234"
  type: "hld"              # requirement | hld | lld | adr | plan | approval | evidence
  version: 3
  status: "approved"        # draft | in_review | approved | superseded | rejected
  title: "Idempotent payment status notifications"
  initiative: "PAY-1234"
  owner: "team.payments"
  created_at: "2026-07-21T00:00:00Z"
  updated_at: "2026-07-21T00:00:00Z"
  content_sha256: "sha256:..."
  canonical_uri: "git+https://git.example/design-repository//initiatives/PAY-1234/hld/hld.md@v3"
scope:
  domains: ["payments"]
  systems: ["payment-platform"]
  repositories: ["payments-api", "notifications", "platform-infra"]
  environments: ["test", "production"]
traceability:
  parents: ["jira:PAY-1234"]
  satisfies: ["REQ-PAY-1234-01", "REQ-PAY-1234-NFR-02"]
  impacts: ["service:payments-api", "api:payment-status-v2"]
  produces: ["ADR-PAY-1234-01", "LLD-PAY-1234-payments-api"]
context:
  items:
    - uri: "git+https://git.example/payments-api@abc123"
      version: "abc123"
      authority: "repository"
      retrieved_at: "2026-07-21T00:00:00Z"
      why_included: "current API and persistence implementation"
approvals:
  required: ["business", "architecture"]
  records: []
policy:
  risk_tier: "high"
  data_classification: "confidential"
  allowed_models: ["enterprise-approved-any"]
  implementation_locked_until: "architecture.approved"
```

An approval record is append-only and contains `gate`, `decision`, `principal`, `role`, `identity_provider`, `timestamp`, `artifact_version`, `content_sha256`, `evidence_uris`, and optional `conditions`. Conditions become traceable requirements; they do not disappear into a comment. The schema should reject an `approved` HLD without a valid architecture approval, and reject any implementation plan whose parent HLD is not approved.

### Markdown conventions

Requirements use IDs (`REQ-*`), SHALL/MUST language for mandatory behavior, measurable NFRs, scenarios, acceptance criteria, assumptions, and open questions. HLDs use `DEC-*` and `OPT-*` IDs; LLD sections cite the HLD decision and requirement IDs they implement. Every diagram has a source file and renderer version. Generated content must label claims as `fact`, `inference`, `proposal`, or `unknown` and link facts to evidence.

### Minimal gate rule

```pseudo
if artifact.type in ["lld", "plan", "implementation"]:
    hld = resolve_parent(artifact, type="hld")
    require hld.status == "approved"
    require valid_approval(hld, gate="architecture")
    require artifact.parent_hash == hld.content_sha256
```

## Orchestration and integration architecture

Use a thin, durable orchestration service with these components:

- **Initiative API:** creates initiatives, state transitions, and human tasks.
- **Policy engine:** evaluates risk, data access, required approvers, allowed tools, and gate predicates.
- **Context assembler:** queries catalog, design repository, Git providers, Jira, Confluence, databases, OpenAPI registries, Kubernetes, IaC, observability, and knowledge indexes.
- **Artifact service:** validates DAS, computes hashes, stores evidence, renders diagrams, and publishes immutable versions.
- **Agent gateway:** model/provider adapter, prompt/role registry, tool broker, token/cost limits, sandbox, and audit log.
- **Workflow runtime:** durable timers, retries, resumable human waits, fan-out/fan-in across repositories, and compensation. Temporal is a strong choice where durable business workflows and long-lived approvals are central; LangGraph is a strong choice for stateful agent graphs with persistence and interrupts. They are alternatives, not required dependencies.
- **Repository workers:** isolated workspaces, branch/PR operations, build/test execution, contract testing, and evidence collection.
- **Traceability index:** links Jira issue, DAS artifact, commit, PR, CI run, deployment, incident, and approval.

MCP is a useful adapter protocol because its server model separates resources (context), tools (actions), and prompts (templates). It does not replace authorization, identity, provenance, workflow state, or policy. Wrap MCP servers behind the agent gateway, issue scoped credentials, allow-list tools, validate arguments, redact outputs, and log every call. Keep a second adapter interface for non-MCP REST, GraphQL, CLI, and event integrations so the enterprise is not locked to MCP either.

Recommended integration ownership:

| Capability | Integration contract |
|---|---|
| GitHub/GitLab/Bitbucket | Provider-neutral repository/branch/PR interface; provider webhooks normalized into lifecycle events |
| Jira | External issue keys in DAS; create/update links and comments, never make Jira description the only design source |
| Confluence | Publish approved artifact snapshots and links; ingest pages as non-authoritative context with version IDs |
| Git/OpenAPI/AsyncAPI | Parse contracts, history, dependency and ownership metadata; validate generated changes in CI |
| PostgreSQL/Kubernetes/Terraform/cloud | Read-only discovery by default; write tools separated by environment and risk approval |
| Observability | Retrieve SLOs, service health, incidents, traces and rollout evidence to inform design and release gates |
| Vector/graph stores | Derived indexes only; retain source URI/version and support rebuild from authoritative sources |

### Orchestration technology comparison

| Project/family | Best fit | Important trade-off | Position in the reference architecture |
|---|---|---|---|
| Temporal | Long-running, durable workflows with retries, timers, compensation, and human approvals | Requires workflow-service operations and explicit activity boundaries | Preferred workflow backbone when approvals and multi-day initiatives are central |
| LangGraph | Stateful agent graphs, checkpoints, interrupts, and model/tool composition | Agent-centric runtime; enterprise policy and repository controls must be added | Good agent execution runtime behind the gateway |
| Argo Workflows | Kubernetes-native batch/DAG execution | Less natural for rich conversational state and long-lived human decisions | Good for containerized build, analysis, and evidence jobs |
| Backstage | Service catalog, ownership, API and dependency discovery | Not a workflow engine or authoritative architecture repository | Recommended catalog and engineer-facing portal surface |
| OpenHands / SWE-agent / Aider / Continue | Open implementations of coding-agent loops and developer interaction | Repository and model assumptions vary; governance is external | Useful replaceable workers for implementation pilots and evaluation |
| GitHub Spec Kit | Specification-first project workflow and reusable templates | Primarily repository/project scoped | Use as an inspiration and optional local UX, with DAS as the enterprise contract |

No single project should own the whole architecture. Separate the durable workflow, agent runtime, context/catalog, policy, and repository adapters so each can evolve independently.

## GitHub and Jira workflow

For GitHub, put design artifacts through draft PRs and require CODEOWNERS for architecture paths. GitHub PRs support line comments, approval/request-changes states, linked issues, and review history. Protected branches can require reviews, status checks, conversation resolution, signed commits, deployments, and can disallow bypass; make the architecture gate a required external check whose source is the policy application. Do not let an AI reviewer be the sole required approver. An AI review is evidence and triage, not ownership.

Use separate PR types:

- `design`: requirement/HLD/LLD/ADR change;
- `implementation`: code, tests, infrastructure, and contracts linked to approved design;
- `release`: deployment evidence, rollout, rollback, and operational approvals.

The PR template should require DAS IDs, parent artifact hash, impacted repositories, test evidence, security findings, migration/rollback, and an explicit “architecture changed?” answer.

Jira remains the work-system of record for planning and status. Use one initiative/epic ID across artifacts, create stories only after HLD approval, and link rather than copy content. Persist bidirectional references:

```text
Epic -> Requirement -> HLD -> LLD -> Story/Task -> PR/commit -> CI -> Deployment -> Incident
```

Every transition emits an event with source IDs and hashes. Reconciliation jobs flag broken links, stale status, PRs without approved design, and deployments without release evidence. Jira provides visibility and work management; the design repository provides the versioned technical decision record.

## Repository strategy comparison

| Option | Strengths | Weaknesses | Verdict |
|---|---|---|---|
| Platform repo + design repo + service repos | Clear ownership, works with existing estate, central policies and artifacts, independent release cadence | Requires index and cross-repo orchestration | **Recommended target** |
| Single monorepo | Atomic changes, simple discovery, one PR can coordinate code and design | Migration cost, access boundaries, scale/team autonomy, unsuitable for many existing estates | Good for new bounded products, not enterprise default |
| Template repositories | Fast greenfield consistency and bootstrapping | Templates drift; do not solve cross-service design or legacy context | Use as a bootstrap mechanism |
| Workspace orchestration | Preserves repository autonomy while enabling one initiative workspace | More platform investment and failure modes | **Required capability**, implemented over the recommended structure |

Do not centralize all code just to make AI context easier. Centralize the design contract, catalog, indexes, and orchestration; keep source repositories authoritative for implementation.

## Agent roles

Prefer **role-specialized prompts and tools** over fully autonomous agent identities. Start with four durable roles: Requirements Analyst, Solution Architect, Implementation Engineer, and Assurance/Release Reviewer. Add Database, Security, Performance, QA, Documentation, or Frontend specialists when the risk classifier or artifact type calls for their distinct evidence. A general agent may perform several roles, but each step gets a role contract, input/output schema, tool scope, and independent evaluation.

Independent critics are useful for architecture options and security, but do not assume multiple agents create independent judgment: the same model and context can produce correlated errors. For high-risk work, use a different model family or human reviewer, deterministic analysis, and adversarial tests.

## Security and governance controls

Align the AI participation program with a risk framework such as NIST AI RMF and its Generative AI Profile, plus the enterprise SDLC, secure-development, privacy, records, and change-management controls. Apply risk tiers to the *change*, not only to the model:

- Low: documentation, tests, localized refactor; human engineer review.
- Medium: internal behavior or schema changes; owner plus senior engineer review.
- High: public API, sensitive data, payments, identity, security controls, destructive migration, production infrastructure; architecture, security, and release approvals.
- Critical: regulated/high-consequence or irreversible change; explicit architecture board, security/risk owner, staged rollout, and no autonomous production action.

Hard controls include least-privilege identities, isolated execution, secret scanning, prompt and tool-call logging, egress control, data classification, model allow-listing, dependency/license scanning, SAST/DAST/IaC scanning, generated-code attribution, reproducible evidence, and kill switches. Never use a prompt as the enforcement mechanism. The policy engine and protected branches must enforce it.

## Reference lifecycle example

1. A Product Owner creates Jira epic `PAY-1234` with business outcome and known constraints.
2. Requirements agent retrieves the payment glossary, current services, standards, incidents, APIs, and similar features; drafts `REQ-PAY-1234` with acceptance criteria and NFRs.
3. Business Owner approves the requirement artifact. The orchestrator classifies it as high risk because it affects payment status and customer notifications.
4. Architecture agent discovers `payments-api`, `notifications`, shared event library, database migration repo, and platform deployment repo; generates three HLD options with diagrams, scorecard, threat model, cost, and rollback.
5. Solution Architect iterates through a design PR, rejects one option, adds a condition about idempotency and consumer compatibility, and approves HLD version 3. The policy engine records the content hash and unlocks LLD.
6. LLD agents generate OpenAPI/AsyncAPI changes, schema and migration plan, sequence diagrams, package changes, tests, dashboards, and five repository workstreams. Senior Engineer and Security reviewers approve the LLD.
7. The orchestrator creates linked branches and PRs. Agents implement in small commits, run unit/integration/contract/security tests, and update evidence. Human CODEOWNERS review each PR; no AI approval counts as a human approval.
8. A release agent assembles merged commits, artifact hashes, CI results, migration/rollback, SLO dashboards, and canary criteria. Release Owner approves production deployment.
9. Deployment events and post-release metrics link back to the epic. Any incident or design learning creates a new ADR or superseding artifact, preserving history.

## Measures of success

Measure safety and quality, not only velocity:

- percentage of implementation PRs linked to approved HLD/LLD hashes;
- requirements-to-deployment trace completeness;
- architecture rework after HLD approval;
- escaped defects, security findings, rollback rate, change failure rate, and time to restore;
- context precision/recall and stale-source rate;
- human review load, time-to-decision, and approval reversals;
- agent task success by role, model, repository type, and risk tier;
- cost per accepted change and percentage of agent work requiring human rework;
- design drift detected between approved HLD, implementation, and runtime topology.

## Adoption roadmap

**0–30 days:** choose DAS v0.1, create templates and JSON Schema, define gate roles, protect design and main branches, and pilot one service plus one shared dependency.

**31–90 days:** build the design repository, catalog ingestion, Jira/Git integration, context packs, HLD review workflow, and traceability dashboard. Keep implementation human-led.

**3–6 months:** add LLD generation, repository fan-out, contract tests, security and release evidence, Confluence publishing, and durable human waits.

**6–12 months:** expand to legacy modernization, measure outcomes, add specialist reviewers, introduce model routing, and enforce policy by risk tier across the estate.

Do not begin with autonomous deployment or a large multi-agent marketplace. First make artifacts, approval semantics, context provenance, and repository enforcement reliable.

## Recommended reading and evaluation set

Use this as a due-diligence shortlist rather than a prescribed stack:

- **Open source to evaluate:** GitHub Spec Kit, Backstage, Temporal, LangGraph, Argo Workflows, OpenHands, SWE-agent, Aider, Continue, MADR/adr-tools, Structurizr, OpenAPI tooling, AsyncAPI tooling, OpenTelemetry, and OpenFeature.
- **Research to read:** human-in-the-loop software development agents; *Software Engineering by and for Humans in an AI Era*; *Agentic AI in the Software Development Lifecycle*; and IEEE P26044. The papers are useful for identifying risks and evaluation questions, not as operational controls.
- **Practice and standards:** NIST AI RMF and GenAI Profile, ADR guidance, OpenAPI, AsyncAPI, C4, Mermaid/PlantUML, and the MCP specification.
- **Enterprise examples to study:** GitHub's Spec Kit and agent/code-review documentation, Backstage's catalog model, GOV.UK's ADR practice, and public engineering playbooks from Microsoft and Thoughtworks. Treat vendor case studies and “AI factory” claims as hypotheses to validate with a pilot; they are not evidence that a product can govern an enterprise architecture.

## Selected sources and projects

- [GitHub Spec Kit documentation](https://github.github.com/spec-kit/index.html) and [spec-driven development overview](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) and [Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [IEEE P26044 software-engineering generative-AI reference model](https://standards.ieee.org/ieee/26044/12571/)
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/2025-06-18/server/index)
- [Backstage software catalog and relationships](https://backstage.io/docs/features/software-catalog/well-known-relations/)
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches) and [PR reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)
- [Confluence technical documentation and version history](https://support.atlassian.com/confluence-cloud/docs/use-confluence-for-technical-documentation/)
- [Architectural Decision Records](https://adr.github.io/) and [MADR](https://adr.github.io/madr/)
- [OpenAPI Specification 3.2.0](https://spec.openapis.org/oas/latest.html)
- [LangGraph durable execution and human-in-the-loop](https://langchain-ai.github.io/langgraph/reference/) and [interrupts](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/breakpoints/)
- [Human-In-the-Loop Software Development Agents](https://arxiv.org/abs/2411.12924)
- [Software Engineering by and for Humans in an AI Era](https://doi.org/10.1145/3715111)
- [Agentic AI in the Software Development Lifecycle](https://arxiv.org/abs/2604.26275)

These sources support the component choices and trends; the DAS, lifecycle states, decision rights, and enforcement rules above are the proposed enterprise design synthesized from them.
