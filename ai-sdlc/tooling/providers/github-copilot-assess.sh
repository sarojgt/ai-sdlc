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
prompt="$(python3 "$root/tooling/render_prompt.py" --name hld-assessment --initiative-id "$initiative_id" --model "$model")"

echo "[AI-SDLC] Assessing HLD scope and selecting profile with Copilot: $model" >&2
python3 "$root/tooling/with_timeout.py" "${AI_SDLC_ASSESSMENT_TIMEOUT_SECONDS:-300}" \
  copilot --model "$model" --yolo --allow-tool=write --allow-tool='shell(git:*)' --no-ask-user -p "$prompt"

test -s "$assessment" || { echo "Copilot did not produce $assessment" >&2; exit 31; }
echo "[AI-SDLC] HLD assessment written: $assessment" >&2
