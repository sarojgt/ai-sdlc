#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <initiative-id> [model] [iteration]" >&2
  exit 2
fi

initiative_id="$1"
model="${2:-gpt-5.6-terra}"
iteration="${3:-1}"
root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$root/initiatives/$initiative_id"
review_file="$target/feedback/ai-review-$iteration.md"
last_message="$target/evidence/ai-review-$iteration-last-message.md"

test -d "$target" || { echo "Unknown initiative: $initiative_id" >&2; exit 1; }
test -f "$target/hld/hld.md" || { echo "Missing HLD: $target/hld/hld.md" >&2; exit 1; }
command -v codex >/dev/null 2>&1 || { echo "Codex CLI was not found on PATH." >&2; exit 30; }

prompt="Act as an independent senior architecture reviewer. Review the HLD against the approved requirement, repository-local shared context, initiative-relative context, guardrails, and prior feedback. First verify the impact assessment: change size, affected services, repositories, APIs, data stores/tables, events, jobs, infrastructure, user or client channels, internal/external integrations, data/security, deployment, migration, operations, and governance path. Verify that the HLD correctly distinguishes confirmed existing components, proposed new components, and unresolved context. Check that reuse decisions are supported by evidence and that the recommendation explicitly applies the relevant enterprise architecture principles, guardrails, security policies, technology standards, and approved patterns. The recommended option should be the smallest compliant design. Alternatives should appear only for a material trade-off, pattern mismatch, or meaningful constraint, with clear reasons for rejecting or retaining them. Check that the design has not invented an alternate source, projection, event pipeline, BFF, token flow, database, or service merely because context is incomplete. Confirm that the requirement is traced to relevant APIs, schemas/tables, events, integrations, security boundaries, environments, and operational capabilities where applicable. Require missing facts to be reported as concise context gaps with owners and retrieval actions. Require the HLD to be a short decision document with useful diagrams embedded in hld.md; detailed SQL, classes, packages, test cases, and migration scripts belong in the LLD. Write feedback/ai-review-$iteration.md with YAML front matter reviewer: codex, model: $model, iteration: $iteration, decision: pass|changes_requested|escalate. Use pass for a concise, evidence-based HLD with an explicit standards-based recommendation and context gaps; changes_requested for vague, overly detailed, unsupported, or inconsistent content; escalate only for unsafe requirements or serious security/governance contradictions. Do not modify HLD or protected artifacts, approve architecture, create LLD, implement, merge, or deploy."

if [ "${AI_SDLC_AGENT_DRY_RUN:-0}" = "1" ]; then
  printf '%s\n' "codex --ask-for-approval never exec --cd $target --model $model --sandbox workspace-write --output-last-message $last_message < review-prompt"
  exit 0
fi

"$root/tooling/providers/run_codex_with_progress.sh" "$target" "$model" "$last_message" "$prompt"

test -f "$review_file" || {
  echo "Codex reviewer did not create: $review_file" >&2
  exit 30
}

echo "AI HLD review written: $review_file"
