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

test -d "$target" || { echo "Unknown initiative: $initiative_id" >&2; exit 1; }
command -v copilot >/dev/null 2>&1 || { echo "GitHub Copilot CLI was not found on PATH." >&2; exit 30; }
prompt="$(python3 "$root/tooling/render_prompt.py" --name hld-generation --initiative-id "$initiative_id" --model "$model" --profile "${AI_SDLC_HLD_PROFILE:-auto}")"

echo "[AI-SDLC] Starting GitHub Copilot generator: $model" >&2
echo "[AI-SDLC] Context loading and HLD analysis in progress..." >&2
python3 "$root/tooling/with_timeout.py" "${AI_SDLC_AGENT_TIMEOUT_SECONDS:-480}" \
  copilot --model "$model" --yolo --allow-tool=write --allow-tool='shell(git:*)' --no-ask-user -p "$prompt"

test -s "$target/hld/hld.md" || { echo "Copilot did not produce $target/hld/hld.md" >&2; exit 31; }
echo "[AI-SDLC] Copilot HLD generation completed." >&2
