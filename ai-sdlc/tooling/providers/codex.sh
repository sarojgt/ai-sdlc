#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <initiative-id> [model]" >&2
  exit 2
fi

initiative_id="$1"
model="${2:-gpt-5.6-luna}"
root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$root/initiatives/$initiative_id"
request_file="$target/evidence/agent-request.yaml"
last_message="$target/evidence/agent-last-message.md"

test -f "$request_file" || { echo "Missing agent request: $request_file" >&2; exit 1; }
command -v codex >/dev/null 2>&1 || {
  echo "Codex CLI was not found on PATH." >&2
  echo "Install/authenticate Codex, then rerun this command." >&2
  exit 30
}

prompt="Act as a senior enterprise Solution Architect. Read the request, approved requirement, repository-local shared context, initiative-relative context, and prior feedback. Start with an impact assessment before designing: classify the change as small, medium, large, or program-level; classify complexity/risk as low, moderate, high, or critical; count and name affected services, repositories, APIs, data stores or tables, events, jobs, infrastructure components, and user or client channels; identify internal and external integration points; assess data/security, runtime/deployment, migration/compatibility, and operational impact; and select the required governance path. Apply a context-first rule: discover whether the capability belongs in existing components or requires a new component. Reuse an existing service, API, database, table, event, platform capability, security control, deployment pattern, and approved architecture pattern when supported by the context, but do not assume a reuse path merely because one sounds plausible. Base the recommendation on applicable enterprise architecture principles, guardrails, security policies, technology standards, and previously approved patterns. Prefer the smallest compliant design. Provide alternatives only when there is a material trade-off, a pattern mismatch, or a meaningful constraint, and explain why each alternative is or is not recommended. Do not invent an alternate source, projection, event pipeline, BFF, token flow, database, or service to compensate for missing evidence. Trace the requirement to the relevant business domain, existing architecture, repositories, APIs, schemas, tables, events, integrations, security boundaries, deployment environments, and operational capabilities. If a material fact is missing, add a concise CONTEXT GAP with the missing artifact, why it matters, owner/source, and retrieval action; do not replace the gap with a generic architecture. Keep confirmed facts fixed, and leave only unsupported details as gated context work. Produce one concise human-readable HLD in hld/hld.md. Keep the key decisions, scope, impacted components, applicable standards, recommended pattern, alternatives, trade-offs, risks, context gaps, approvals, and traceability in that document. Embed only useful Mermaid diagrams directly in hld.md; do not make separate diagram files the primary human review artifact. Supporting adr.md, risks.md, and traceability.md may be generated, but avoid long duplicated prose. Do not generate LLD detail such as executable SQL, class/package structure, detailed test cases, or migration scripts. Do not modify protected artifacts, approve architecture, implement, merge, or deploy. End with context gaps, open questions, and summary."

prompt="$prompt Write the primary HLD to hld/hld.md. Use these assessment labels exactly: change size = small, medium, large, or program-level; complexity/risk = low, moderate, high, or critical. Do not use simple as a size category."
prompt="$prompt Read evidence/design-baseline.yaml as the immutable input snapshot. Preserve its path and exact requirement/context references in the HLD. Do not invent or silently replace version tags or hashes."

if [ "${AI_SDLC_AGENT_DRY_RUN:-0}" = "1" ]; then
  printf '%s\n' "codex --ask-for-approval never exec --cd $target --model $model --sandbox workspace-write --output-last-message $last_message - < prompt" 
  exit 0
fi

"$root/tooling/providers/run_codex_with_progress.sh" "$target" "$model" "$last_message" "$prompt"

cat > "$target/evidence/agent-response.yaml" <<EOF
agent_response:
  run_id: "RUN-$initiative_id-HLD-1"
  status: completed
  provider: codex
  model: "$model"
  skill_id: hld-generation
  generated_directory: hld/
  human_approval_required: true
EOF

echo "Codex HLD proposal generated under: $target/hld"
echo "Human gate: review the generated proposal and approve through the architecture PR."
