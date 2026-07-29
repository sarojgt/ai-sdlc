#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <initiative-id> <model>" >&2
  exit 2
fi

initiative_id="$1"
model="$2"
root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$root/initiatives/$initiative_id"
assessment="$target/evidence/hld-assessment.yaml"

test -d "$target" || { echo "Unknown initiative: $initiative_id" >&2; exit 1; }
command -v copilot >/dev/null 2>&1 || { echo "GitHub Copilot CLI was not found on PATH." >&2; exit 30; }

prompt="Act as an HLD impact-assessment agent for initiative $initiative_id. Read the approved requirement, all relevant shared and initiative-relative context, guardrails, existing HLD if present, and evidence/design-baseline.yaml. Before full HLD generation, determine the delivery profile from evidence: small, medium, or large. Assess scope, complexity/risk, affected services and repositories, APIs, data stores, events, jobs, infrastructure, channels, internal and external integrations, security, deployment, migration, operations, and governance. Prefer the smallest profile that is adequate; do not use simple as a category. If facts are missing, record concise context gaps and retrieval actions, but do not invent facts. Write only $assessment as YAML with these exact fields: change_size, complexity, recommended_profile, rationale, affected_services, affected_repositories, integration_points, context_gaps. Use scalar strings for the first four fields and integer counts for affected_services, affected_repositories, and integration_points. recommended_profile must be small, medium, or large. Do not modify hld/hld.md, requirements, approvals, LLDs, code, or any protected artifact. Do not approve architecture, merge, or deploy."

echo "[AI-SDLC] Assessing HLD scope and selecting profile with Copilot: $model" >&2
python3 "$root/tooling/with_timeout.py" "${AI_SDLC_ASSESSMENT_TIMEOUT_SECONDS:-300}" \
  copilot --model "$model" --yolo --allow-tool=write --allow-tool='shell(git:*)' --no-ask-user -p "$prompt"

test -s "$assessment" || { echo "Copilot did not produce $assessment" >&2; exit 31; }
echo "[AI-SDLC] HLD assessment written: $assessment" >&2
