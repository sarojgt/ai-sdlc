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
prompt="$(python3 "$root/tooling/render_prompt.py" --name hld-review --initiative-id "$initiative_id" --provider github-copilot --model "$model" --iteration "$iteration" --profile "${AI_SDLC_HLD_PROFILE:-auto}" --feedback-file "${AI_SDLC_HLD_FEEDBACK_FILE:-}")"

echo "[AI-SDLC] Starting GitHub Copilot reviewer: $model" >&2
python3 "$root/tooling/with_timeout.py" "${AI_SDLC_AGENT_TIMEOUT_SECONDS:-480}" \
  copilot --model "$model" --yolo --allow-tool=write --allow-tool='shell(git:*)' --no-ask-user -p "$prompt"

test -f "$review_file" || { echo "Copilot reviewer did not create $review_file" >&2; exit 31; }
echo "[AI-SDLC] Copilot HLD review written: $review_file" >&2
