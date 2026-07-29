# AI Agent Runner and CLI Adapter Design

## Purpose

Allow the same AI-SDLC workflow to use Codex, Claude, GitHub Copilot, local models, or another coding agent without changing the lifecycle, context model, DAS artifacts, or human gates.

## User-facing command

The engineer uses one stable command:

```text
just ai-sdlc-hld PAY-4567 codex gpt-5.6-luna
```

Provider and model are separate inputs. The provider selects the adapter; the
model is passed through the common request contract and translated by that
adapter. A different provider can therefore use a different model naming
scheme without changing the lifecycle command or DAS artifacts.

The orchestrator performs the same steps regardless of the selected provider:

```text
preconditions
  → context assembly
  → request creation
  → agent adapter invocation
  → output validation
  → artifact hashing
  → design PR creation
  → human Solution Architect review
```

## Skill command boundary

Skills have stable repository entry points. The provider and model are runtime
parameters, not part of the skill identity:

```text
just ai-sdlc-skill hld-generation PAY-4567 codex gpt-5.6-luna
just ai-sdlc-skill hld-review PAY-4567 codex gpt-5.6-terra
```

The convenience commands `ai-sdlc-hld`, `ai-sdlc-hld-loop`, and
`ai-sdlc-hld-feedback` call the same skill runners with lifecycle-specific
guards. Registered skills that do not yet have an executable adapter stop
explicitly rather than silently performing an incomplete task.

## Adapter boundary

The orchestrator does not call a vendor CLI directly. It calls an adapter command:

```text
ai-sdlc-agent-codex
ai-sdlc-agent-claude
ai-sdlc-agent-github-copilot
ai-sdlc-agent-custom
```

Each adapter accepts the same input and produces the same output:

```text
stdin:  hld-run.yaml
stdout: progress and structured run events
files:  generated artifacts in generated/
output: agent-response.yaml
exit 0: task completed and response is valid
exit 10: task needs human input
exit 20: policy/tool authorization failure
exit 30: agent execution failure
```

This avoids coupling the standard flow to unstable or provider-specific CLI flags. Each adapter can translate the common request into the provider's native invocation.

## Request contract

```yaml
agent_request:
  run_id: "RUN-{{ initiative.id }}-HLD-001"
  initiative_id: "{{ initiative.id }}"
  task_type: "hld"
  skill_id: "hld-generation"
  agent:
    provider: "codex"
    model: "gpt-5.6-luna"
  requirement:
    artifact_id: "REQ-{{ initiative.id }}"
    version: 2
    content_sha256: "sha256:..."
  context:
    pack_id: "CTX-{{ initiative.id }}-v3"
    pack_version: 3
    content_sha256: "sha256:..."
    manifest: "context-manifest.yaml"
  policy:
    version: "2026-07-21"
    risk_tier: "medium"
    allowed_tools: [read_context, read_repository, render_diagram]
    denied_tools: [approve_architecture, merge, deploy_production]
  output:
    schema: "hld.v0.1"
    directory: "hld/"
    required_files: ["hld.md", "agent-response.yaml"]
```

## Response contract

```yaml
agent_response:
  run_id: "RUN-{{ initiative.id }}-HLD-001"
  status: "completed"       # completed | needs_human_input | failed
  provider: "codex"
  model: "gpt-5.6-luna"
  skill_id: "hld-generation"
  generated_files:
    - "hld/hld.md"
  requirements_covered: []
  open_questions: []
  warnings: []
  tool_calls: []
  context_pack_hash: "sha256:..."
  output_hash: "sha256:..."
```

## HLD command behavior

```text
just ai-sdlc-hld PAY-4567 codex gpt-5.6-luna
```

The command should:

1. Resolve `ai-sdlc/initiatives/PAY-4567`.
2. Verify the requirement is approved.
3. Build or refresh the relative context pack.
4. Load consistent context, guardrails, and the `hld-generation` skill.
5. Write `evidence/hld-run.yaml`.
6. Run the selected adapter.
7. Validate the response and generated HLD.
8. Run secret and policy checks.
9. Hash the generated artifacts.
10. Create or update a draft design PR.
11. Assign the Solution Architect.
12. Stop and wait for human feedback.

The command must not create LLDs or implementation branches. Those are separate commands and require the HLD gate.

## Codex adapter

The initial real adapter invokes the non-interactive Codex command:

```text
codex exec \
  --cd <initiative-workspace> \
  --model <requested-model> \
  --sandbox workspace-write \
  --ask-for-approval never \
  --output-last-message <evidence-file> \
  "<governed HLD prompt>"
```

The adapter writes proposal files only beneath `hld/`. It never
changes the approved requirement, records an architecture approval, merges a
branch, or deploys. A future Claude, Copilot, or local-model adapter receives
the same request and must produce the same response contract.

`codex exec` is non-interactive, so the adapter uses `never` for in-session
command approval. This is safe only for the bounded HLD workspace-write policy:
the prompt, output-directory restriction, external validators, and human
architecture gate remain mandatory. Implementation and deployment adapters
must use stricter isolated runners and independent policy enforcement.

## Feedback and rerun commands

```text
just ai-sdlc-feedback PAY-4567 \
  --artifact HLD-PAY-4567 \
  --comment-id 12345
```

The system classifies the comment and reruns only the affected skill scope.

## AI review loop

HLD generation may use an independent reviewer model before human review:

```text
just ai-sdlc-hld-loop PAY-4567 codex gpt-5.6-luna codex gpt-5.6-terra
```

The reviewer writes the latest decision to `feedback/ai-review.md` with one of
these decisions:

```text
pass
changes_requested
escalate
```

The orchestrator continues while the reviewer requests useful changes, but
enforces a configured safety policy: maximum iterations, maximum elapsed time,
repeated-feedback detection, and unchanged-HLD detection. It escalates when
the loop does not converge. A `pass` unlocks only the human Solution Architect
review; it never unlocks LLD or implementation by itself.

```text
just ai-sdlc-hld PAY-4567 claude

# The orchestrator reads the feedback scope from the saved review event.
# Example event: evidence/review-comment-12345.yaml
```

## Hooks are enforcement points

Hooks should be attached to the orchestrator lifecycle, not only to a particular CLI:

```text
before_agent_run
  verify permissions and context

after_agent_run
  validate artifacts and collect evidence

before_human_gate
  verify review packet is complete

on_human_approval
  record hash and unlock next state

on_human_feedback
  invalidate affected downstream work and rerun

on_agent_failure
  retry within budget or escalate
```

An agent CLI may have its own local hooks, but those are supplementary. The enterprise gate must be enforced outside the agent because the agent cannot be trusted to enforce its own permissions.

## Provider-specific adapter responsibilities

Each adapter owns only the translation to its provider:

| Adapter | Owns | Must not own |
|---|---|---|
| Codex | Local Codex invocation, session setup, output capture | HLD approval, lifecycle state, enterprise policy |
| Claude | Claude CLI invocation, output capture | HLD approval, lifecycle state, enterprise policy |
| GitHub Copilot | Copilot/repository agent invocation, output capture | HLD approval, lifecycle state, enterprise policy |
| Local model | Local runtime invocation and output capture | HLD approval, lifecycle state, enterprise policy |

## Security requirements

- Run each agent in an isolated workspace.
- Pass only the context pack allowed for the role and risk tier.
- Use short-lived credentials.
- Do not expose production credentials.
- Allow-list tools and repositories.
- Log provider, model, prompt/skill version, context hash, tool calls, and output hash.
- Enforce human approval outside the agent process.
- Apply retry and cost limits.

## Recommended implementation order

1. Implement the common request/response files.
2. Implement a fake adapter that returns a deterministic HLD fixture.
3. Implement validation and PR creation around the fake adapter.
4. Add one real provider adapter.
5. Add a second provider adapter and verify identical artifact output contracts.
6. Add feedback/rerun hooks.
7. Add Jira and Confluence adapters later.

Starting with a fake adapter is valuable because it proves orchestration and governance independently of model quality or vendor CLI behavior.
