#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <initiative-id> <model> <iteration>" >&2
  exit 2
fi

initiative_id="$1"
model="$2"
iteration="$3"
root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$root/initiatives/$initiative_id"
review_file="$target/feedback/ai-review.md"

test -d "$target" || { echo "Unknown initiative: $initiative_id" >&2; exit 1; }
test -f "$target/hld/hld.md" || { echo "Missing HLD: $target/hld/hld.md" >&2; exit 1; }
command -v copilot >/dev/null 2>&1 || { echo "GitHub Copilot CLI was not found on PATH." >&2; exit 30; }

prompt="Act as an independent senior architecture reviewer for initiative $initiative_id. Review hld/hld.md against the approved requirement, evidence/design-baseline.yaml, hld-assessment.yaml, repository-local context and guardrails, initiative-relative context, and prior feedback. Check that the HLD contains a valid change_size classification of small, medium, or large and that its decisions, options, risks, diagrams, and linked supporting documents are proportionate to that classification. Check impact assessment, affected services and repositories, APIs, data stores, events, integrations, security, deployment, migration, operations, governance, standards, approved patterns, traceability, and Mermaid rendering. Reject unsupported claims presented as facts, contradictions, unnecessary implementation detail, duplicated prose, and non-rendering diagrams. Require the smallest compliant HLD decision document; report missing facts as owned context gaps. Do not use a line-count threshold as a substitute for judgment. Do not modify hld/hld.md or protected artifacts. Write only feedback/ai-review.md with YAML front matter: reviewer: github-copilot, model: $model, iteration: $iteration, decision: pass|changes_requested|escalate. Use pass only when evidence-based, specific, standards-aligned, traceable, concise for the selected profile, and ready for human Solution Architect review. Use changes_requested for fixable issues. Use escalate only for unsafe requirements or serious security/governance contradictions. Do not approve architecture, create an LLD, implement, merge, or deploy."

echo "[AI-SDLC] Starting GitHub Copilot reviewer: $model" >&2
python3 "$root/tooling/with_timeout.py" "${AI_SDLC_AGENT_TIMEOUT_SECONDS:-480}" \
  copilot --model "$model" --yolo --allow-tool=write --allow-tool='shell(git:*)' --no-ask-user -p "$prompt"

test -f "$review_file" || { echo "Copilot reviewer did not create $review_file" >&2; exit 31; }
echo "[AI-SDLC] Copilot review written: $review_file" >&2
