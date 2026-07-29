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
review_file="$target/feedback/ai-review.md"
last_message="$target/evidence/ai-review-$iteration-last-message.md"

test -d "$target" || { echo "Unknown initiative: $initiative_id" >&2; exit 1; }
test -f "$target/hld/hld.md" || { echo "Missing HLD: $target/hld/hld.md" >&2; exit 1; }
command -v codex >/dev/null 2>&1 || { echo "Codex CLI was not found on PATH." >&2; exit 30; }

prompt="Act as an independent senior architecture reviewer. Review hld/hld.md against the approved requirement, shared and relative context, guardrails, approved standards and patterns, and prior feedback. Verify that the HLD contains a valid change_size classification of small, medium, or large and that its depth, options, risks, and diagrams are proportionate to that classification. Verify affected services/repositories, APIs, data stores, events, integrations, security boundaries, environments, deployment, migration, operations, governance, traceability, and Mermaid rendering. Confirm that existing facts, proposed changes, and unresolved context gaps are clearly distinguished; do not invent components to fill gaps. Require the smallest compliant HLD decision document, with detailed implementation reserved for the LLD. Write feedback/ai-review.md with YAML front matter reviewer: codex, model: $model, iteration: $iteration, decision: pass|changes_requested|escalate. Use pass only for a concise, evidence-based, standards-aligned HLD ready for human Solution Architect review; changes_requested for fixable issues; escalate only for unsafe requirements or serious security/governance contradictions. Do not modify HLD or protected artifacts, approve architecture, create LLD, implement, merge, or deploy."

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
