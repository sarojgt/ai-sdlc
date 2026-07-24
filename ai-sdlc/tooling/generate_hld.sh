#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <initiative-id> <agent-provider> [model] [sequence]" >&2
  exit 2
fi

initiative_id="$1"
agent_provider="$2"
agent_model="${3:-gpt-5.6-luna}"
sequence="${4:-1}"
root="$(cd "$(dirname "$0")/.." && pwd)"
target="$root/initiatives/$initiative_id"

test -d "$target" || { echo "Unknown initiative: $initiative_id" >&2; exit 1; }

if ! grep -q 'status: approved' "$target/requirement.md"; then
  echo "Requirement is not approved. Review it before generating HLD." >&2
  echo "Run: just ai-sdlc-review-requirement $initiative_id" >&2
  exit 10
fi

mkdir -p "$target/evidence" "$target/generated"
python3 "$root/tooling/build_design_baseline.py" "$initiative_id" > "$target/evidence/design-baseline.yaml"
cp "$root/templates/agent-request.yaml" "$target/evidence/agent-request.yaml"
cp "$root/templates/agent-run.yaml" "$target/evidence/agent-run.yaml"

for file in "$target/evidence/agent-request.yaml" "$target/evidence/agent-run.yaml"; do
  sed -i '' \
    -e "s/{{ initiative.id }}/$initiative_id/g" \
    -e "s/{{ task.type }}/hld/g" \
    -e "s/{{ task.sequence }}/$sequence/g" \
    -e "s/{{ task.skill }}/hld-generation/g" \
    -e "s/{{ requirement.version }}/1/g" \
    -e "s/{{ requirement.hash }}/REQUIRED_HASH/g" \
    -e "s/{{ context.version }}/1/g" \
    -e "s/{{ context.hash }}/REQUIRED_CONTEXT_HASH/g" \
    -e "s/{{ policy.risk_tier }}/medium/g" \
    -e "s/{{ task.output_schema }}/hld.v0.1/g" \
    -e "s/{{ agent.provider }}/$agent_provider/g" \
    -e "s/{{ agent.model }}/$agent_model/g" \
    "$file"
done

echo "HLD request prepared: $target/evidence/agent-request.yaml"
echo "Agent provider: $agent_provider"
echo "Agent model: $agent_model"

"$root/tooling/run_agent.sh" "$initiative_id" "$agent_provider" "$agent_model"
