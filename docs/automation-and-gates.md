# AI-Native SDLC Automation, Triggers, and Human Gates

## Core rule

Automate **movement, evidence, validation, notifications, context assembly, and bounded execution**. Keep humans responsible for **intent, architecture choice, risk acceptance, exceptions, merge, and release**.

An AI agent should never decide that its own output is approved. It can prepare an approval request, summarize evidence, answer comments, and rerun a failed step. A separate policy service and a named human must create the approval event.

## Operating model: automatic, human, and hybrid

| Lifecycle activity | Automate | Human intervention | Gate / output |
|---|---|---|---|
| Intake | Create initiative from Jira, copy metadata, classify risk, assign owners | Confirm business outcome, scope, priority | `INTAKE_READY` |
| Context discovery | Discover repositories, dependencies, standards, APIs, ADRs, incidents, owners; create context pack | Correct missing or incorrect context | `CONTEXT_READY` or `CONTEXT_NEEDS_INPUT` |
| Requirements | Draft requirements, NFRs, scenarios, glossary terms, contradictions, traceability | Clarify business ambiguity and accept scope | Business approval: `REQUIREMENTS_APPROVED` |
| HLD options | Generate alternatives, diagrams, scorecard, threat model, risks, migration and cost analysis | Discuss, reject, modify, or choose an option | Architecture approval: `HLD_APPROVED` |
| HLD review | Detect missing sections, unsupported claims, standard violations, orphan requirements | Resolve findings and decide trade-offs | `HLD_REWORK` or `HLD_APPROVED` |
| LLD | Generate API/event/database/package/test/observability details from approved HLD | Review significant implementation detail and deviations | Engineering approval: `LLD_APPROVED` |
| Work decomposition | Identify impacted repositories, order dependencies, create Jira stories/tasks and branches | Adjust ownership, sequencing, and capacity | `IMPLEMENTATION_READY` |
| Coding | Edit isolated branches, commit incrementally, run tests, repair failures | Set scope, answer escalations, review risky changes | Draft PRs |
| PR review | Run CI, security, compatibility, architecture-conformance and AI review checks | Human CODEOWNER review, approval, merge | Merge gate |
| Release | Assemble evidence, generate notes, assess rollout signals, prepare rollback | Approve release and production change | Release approval |
| Operations | Monitor deployment, detect regressions, link incidents, propose ADR/rollback | Decide rollback, incident response, design changes | `DEPLOYED` or `ROLLBACK_REQUIRED` |

## State machine

```text
INTAKE
  | work_item.created
  v
CONTEXT_BUILDING --missing source--> CONTEXT_NEEDS_INPUT --human supplies source--> CONTEXT_BUILDING
  | context.ready
  v
REQUIREMENTS_DRAFT --business comments--> REQUIREMENTS_DRAFT
  | business.approved
  v
HLD_GENERATING --> HLD_REVIEW
  | architect comments / rejection
  +------------------------------<-------------------+
  | architecture.approved                         |
  v                                               |
LLD_GENERATING --> LLD_REVIEW --rework ----------+
  | engineering.approved
  v
IMPLEMENTATION_PLANNED --> IMPLEMENTING --> PR_REVIEW
                                             | checks fail
                                             v
                                          REWORK
                                             | checks pass + human approval
                                             v
                                      RELEASE_READY
                                             | release approval
                                             v
                                        DEPLOYING
                                             | health regression
                                             v
                                  ROLLBACK_REQUIRED
```

The workflow runtime should persist state and wait indefinitely for human actions. A timeout creates a reminder or escalation; it does not create an approval.

## Trigger catalog

### Business and Jira triggers

| Trigger | Conditions | Automated action |
|---|---|---|
| Jira epic/feature created | Has business owner and outcome | Create DAS initiative, assign Requirements agent, post design link |
| Jira issue transitions to “AI SDLC” | Project is onboarded | Build initial context pack and risk assessment |
| Requirement field or comment changed | Change affects scope, NFR, priority, or acceptance criteria | Mark requirement stale; rerun contradiction and impact analysis |
| Requirement approved | Required business approver and valid artifact hash | Generate HLD job and assign Solution Architect |
| HLD review requested | Required context present | Generate options and open design PR |
| Human HLD comment added | Comment is actionable or requests regeneration | Classify comment; rerun only affected HLD section and update PR |
| HLD approved | Valid role, current artifact hash, no unresolved blocking comments | Unlock LLD; create LLD work item |
| HLD rejected | Human reason recorded | Return to HLD draft with rejection context; do not generate implementation |
| Jira issue linked/unlinked | Link is a design, dependency, or repository link | Recompute traceability and impact set |

Jira automation already supports triggers such as work item creation, transition, comment, incoming webhook, branch/commit/build/PR events, deployment status, security findings, and manual triggers. Use Jira for work visibility and notifications, while the DAS/policy service remains the authority for artifact state and approvals. [Jira trigger documentation](https://support.atlassian.com/cloud-automation/docs/jira-automation-triggers/)

### Design repository and Git triggers

| Trigger | Conditions | Automated action |
|---|---|---|
| Design PR opened | Contains DAS artifact | Validate schema, links, IDs, diagrams, hashes, and required sections |
| Design PR updated | HLD/requirement changed | Recompute hash, rerun context and traceability checks |
| Architecture CODEOWNER requested | Path matches HLD/ADR | Request Solution Architect review |
| Architecture review approved | Correct human role and current hash | Emit `architecture.approved` event |
| Architecture review dismissed or stale | New commit after approval | Invalidate approval and rerun gate |
| Initiative PR approved | Required human reviewer approved the initiative PR | Update `initiative.yaml`, `initiative.md`, and `approvals.yaml` to `approved` |
| Initiative approval missed by prior workflow | Use `workflow_dispatch` backfill with an initiative directory | Re-run the approval sync on a dedicated backfill branch |
| Implementation PR opened | Contains `hld_id`, `hld_hash`, `lld_id` | Verify parent approvals; fail check if invalid |
| Implementation PR changes design-sensitive paths | Database/API/security/infrastructure path changed | Recalculate risk and request additional reviewers |
| PR merged | All required checks and human reviews pass | Transition Jira story; update traceability; start integration/deployment workflow |

Use provider webhooks to normalize GitHub, GitLab, or Bitbucket events into a common event envelope. On GitHub, protected branches and required status checks should enforce the gate; CODEOWNERS should route reviews; an external `architecture-gate` check should be required before merge. The agent can create a PR but cannot satisfy the human approval requirement. [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)

### CI and security triggers

| Trigger | Automated action | Human action |
|---|---|---|
| Build/test failed | Send failure to implementation agent with logs; allow bounded repair loop | Escalate after retry budget or repeated same failure |
| SAST/SCA/IaC finding | Classify severity, create Jira defect, block critical findings | Security owner accepts, rejects, or grants documented exception |
| Contract compatibility failed | Identify producer/consumer and affected workstreams; pause merge | Engineer decides compatible fix or HLD change |
| Coverage or mutation threshold failed | Ask QA agent to add tests; rerun | Engineer reviews test intent and quality |
| Architecture conformance failed | Point to HLD/ADR rule and affected files | Architect decides whether code or design changes |
| Deployment health check failed | Stop rollout, collect evidence, suggest rollback | Release/operations owner approves rollback or continuation |

### Human triggers

| Human action | System response |
|---|---|
| “Approve” | Validate role and artifact hash, append approval, advance state |
| “Request changes” | Record structured findings, return to draft/rework state, notify agent and owner |
| “Reject” | Stop downstream jobs, preserve evidence, require new design iteration |
| “Ask question” | Create a blocking question; pause only dependent work |
| “Approve with condition” | Convert condition into a traceable requirement/check before the next gate |
| “Override” | Never silently bypass; require explicit exception record, authority, reason, scope, expiry, and audit event |

## How feedback reruns the loop

The workflow should not rerun everything after every comment. Use dependency-aware invalidation.

| Feedback type | Rerun scope |
|---|---|
| Typo or formatting | Render and validation only |
| Requirement wording or acceptance criterion | Requirements checks, context pack, impacted HLD sections, then HLD review |
| New repository or dependency discovered | Context pack, impact analysis, HLD options, workstream map |
| Architect changes selected option | HLD scorecard, ADRs, LLD, implementation plan; invalidate downstream approvals |
| Security finding in implementation | Security checks and affected code; revisit HLD only if control/boundary changes |
| Database schema or public API change | LLD, compatibility tests, migrations, affected repository plans; possibly new HLD version |
| Unit-test failure | Test/code repair loop only, unless the failure exposes a design assumption |
| Production regression | Pause rollout, collect telemetry, propose rollback; create incident/design learning loop |

Every rerun records:

```yaml
rerun:
  triggered_by: "review_comment:comment-123"
  source_artifact: "HLD-DEMO-001@v3"
  invalidated_artifacts: ["LLD-DEMO-001@v1", "PLAN-DEMO-001@v1"]
  requested_scope: ["failure-behavior", "rollback"]
  run_id: "run-456"
  context_hash: "sha256:..."
  agent_profile: "solution-architect"
  model_provider: "provider-adapter-id"
```

## Gate design

### Gate contract

Each gate has the same shape:

```yaml
gate:
  id: "architecture"
  subject: "HLD-DEMO-001"
  required_role: "solution-architect"
  required_evidence:
    - requirements_coverage
    - options_and_tradeoffs
    - threat_model
    - migration_and_rollback
    - context_provenance
  automated_checks:
    - das-schema-valid
    - no-blocking-comments
    - all-required-sections
    - traceability-complete
  human_decision: "required"
  valid_for: "artifact_content_hash"
  on_approve: "unlock:lld"
  on_reject: "return:hld_review"
```

### Approval sequence

1. Automated checks run.
2. If checks fail, the workflow enters `NEEDS_REWORK`; no human approval request is created until the artifact is reviewable.
3. If checks pass, the system requests the required human reviewer.
4. The reviewer sees the artifact diff, context evidence, automated findings, open questions, and proposed downstream impact.
5. The reviewer approves, requests changes, rejects, or asks a blocking question.
6. The policy service validates the identity and hash, appends an immutable approval, and emits the next event.
7. Any later content change invalidates that approval automatically.

The system should distinguish **blocking** comments from **non-blocking** comments. A non-blocking comment remains visible and traceable but does not stop the workflow. A blocking comment must be resolved by the reviewer who raised it or explicitly reclassified by an authorized human.

## Automation patterns to use

### Pattern 1: Event-driven workflow

Use webhooks from Jira, Git, CI/CD, security, and observability to an event gateway. Normalize them into events such as:

```text
initiative.created
context.ready
requirements.approved
hld.review_requested
hld.comment_added
architecture.approved
lld.generated
pr.created
checks.failed
pr.human_approved
deployment.health_regressed
```

Use idempotency keys such as `source_system + source_event_id` so retries do not create duplicate agents, branches, or Jira issues.

### Pattern 2: Durable workflow with human waits

Use a durable workflow runtime for multi-day design reviews and cross-repository work. Human approval is represented as a signal/input to the workflow. The runtime can retry context retrieval and agent calls, but it must not retry a human decision as if it were an activity.

### Pattern 3: Policy-as-code

Keep gate rules in versioned policy files and evaluate them in the orchestrator and CI. Example:

```yaml
rules:
  - name: implementation-requires-approved-hld
    when: artifact.type in ["lld", "plan", "implementation"]
    require:
      - parent.hld.status == "approved"
      - parent.hld.approval.gate == "architecture"
      - parent.hld.approval.content_sha256 == parent_hash
  - name: public-api-requires-architecture-review
    when: change.paths intersects ["openapi/**", "api/**"]
    require:
      - human_role("solution-architect")
      - contract_compatibility_passed
```

### Pattern 4: Bounded agent loops

Each agent loop has a maximum number of retries, maximum time/cost, allowed tools, and stop conditions. A coding loop may fix a failing unit test three times; it must then create an escalation rather than endlessly changing code. A design loop may regenerate a section after feedback; it must not silently alter the approved decision.

### Pattern 5: Fan-out and fan-in

After LLD approval, fan out to repository workstreams. Fan in only after all required contracts, tests, security checks, and PR approvals are complete. One failed dependency pauses only dependent workstreams where possible.

## Repository-first implementation choices

The choices below describe the current repository-first implementation and
future extension points. The framework is an evolving standard, not limited to
the initial pilot.

Start with the tools already present in the organization:

- **Triggers:** Jira automation, Git provider webhooks, CI webhooks, and a small event gateway.
- **Workflow:** a simple database-backed state machine for the first pilot; adopt Temporal or an equivalent durable workflow engine when approvals span days and fan-out becomes real.
- **Agent execution:** existing coding agent behind a model/provider adapter; record prompt, model, tools, context hash, and output.
- **Policy:** YAML/JSON policy plus a validator in CI and the orchestrator.
- **Artifacts:** Git repository, Markdown, YAML, JSON Schema, Mermaid/PlantUML.
- **Review:** GitHub/GitLab PRs, CODEOWNERS, required checks, and protected branches.
- **Context:** repository metadata, Jira, API specs, ADRs, and a small search index before adding vector search.
- **Evidence:** object storage or Git evidence directory plus a traceability database.

Do not make Jira automation the entire orchestrator. It is useful for work-item triggers and notifications, but the artifact hash, gate, context provenance, fan-out, retry, and audit semantics belong in the AI-SDLC control plane.

## Example end-to-end automation

```text
Jira: issue created
  -> webhook -> Initiative API
  -> create design branch and initiative.yaml
  -> build context-pack.yaml
  -> run risk classifier
  -> invoke requirements agent
  -> open requirements PR
  -> request Product Owner

Product Owner approves
  -> policy service verifies role + hash
  -> emit requirements.approved
  -> invoke HLD agent with context pack
  -> open HLD PR + request Solution Architect

Architect requests changes
  -> classify comment
  -> rerun affected HLD sections
  -> update PR, invalidate previous draft hash

Architect approves HLD
  -> policy service records approval
  -> emit architecture.approved
  -> generate LLD and workstreams
  -> request Senior Engineer

Engineer approves LLD
  -> create branches and Jira stories
  -> invoke bounded implementation workers
  -> open linked PRs
  -> CI/security/contract checks run

Check fails
  -> send logs to worker
  -> bounded repair loop
  -> rerun checks
  -> escalate after retry budget

Human PR approvals + checks pass
  -> merge queue
  -> deploy to test
  -> collect health evidence
  -> request Release Owner

Release Owner approves
  -> protected environment deployment
  -> monitor SLOs
  -> close traceability links
```

## What humans should see at each gate

Do not make reviewers search through agent logs. Present a gate packet:

- artifact diff and current version/hash;
- one-page summary;
- requirements and NFR coverage;
- context sources and freshness;
- automated checks and unresolved findings;
- AI-generated options and recommendation;
- risk classification and affected repositories;
- changes since the last review;
- downstream artifacts that will be unlocked or invalidated;
- explicit decision buttons: approve, request changes, reject, ask question.

The reviewer is deciding on evidence, not on the model's confidence.

## Minimum automation backlog

Build these first:

1. `das-validate` — schema, IDs, links, required sections, hashes.
2. `architecture-gate` — approved HLD status, role, current hash, no blocking comments.
3. `context-build` — source discovery and provenance bundle.
4. `trace-check` — no orphaned requirements, PRs, deployments, or approvals.
5. `jira-sync` — status, links, assignees, and comments.
6. `pr-evidence` — tests, security, contracts, and design references.
7. `approval-service` — append-only human approval records and invalidation.
8. `rerun-router` — maps feedback type to affected artifacts and jobs.
9. `notification-service` — reviewer requests, escalations, failures, and reminders.
10. `initiative-approval-sync` — process a merged initiative PR, expand its
    boilerplate, and record valid human requirements approval in one automation PR.
11. `initiative-approval-backfill` — repair older initiatives with manual
    workflow dispatch through the same post-merge processor.
12. `audit-export` — complete initiative evidence for governance and release review.

## Automation maturity levels

| Level | Description | Human role |
|---|---|---|
| 0 | Manual documents and PRs | Humans run every step |
| 1 | Templates, validation, notifications, trace links | Humans trigger and approve |
| 2 | AI drafts requirements/HLD/LLD; automation assembles context and opens reviews | Humans decide at every gate |
| 3 | Approved HLD automatically unlocks LLD and cross-repository workstreams; bounded coding loops | Humans own architecture, PR merge, and release |
| 4 | Risk-based automatic routing, test repairs, deployment evidence, canary analysis | Humans approve higher-risk changes and exceptions |
| 5 | Limited autonomy for low-risk changes only | Humans govern policy, sampling, incidents, and all high-risk gates |

The enterprise should target Level 2 for the first pilot, Level 3 after the gate is proven, and Level 4 only after evidence shows that the controls and evaluations are reliable.
