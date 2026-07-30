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
last_message="$target/evidence/agent-last-message.md"

test -d "$target" || { echo "Unknown initiative: $initiative_id" >&2; exit 1; }
command -v codex >/dev/null 2>&1 || { echo "Codex CLI was not found on PATH." >&2; exit 30; }
prompt="$(python3 "$root/tooling/render_prompt.py" --name hld-generation --initiative-id "$initiative_id" --model "$model" --profile "${AI_SDLC_HLD_PROFILE:-auto}")"

if [ "${AI_SDLC_AGENT_DRY_RUN:-0}" = "1" ]; then
  printf '%s\n' "codex --ask-for-approval never exec --cd $target --model $model --sandbox workspace-write --output-last-message $last_message - < rendered-prompt"
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

test -s "$target/hld/hld.md" || { echo "Codex did not produce $target/hld/hld.md" >&2; exit 31; }
echo "Codex HLD proposal generated under: $target/hld"
