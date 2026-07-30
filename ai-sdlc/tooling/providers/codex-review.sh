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
prompt="$(python3 "$root/tooling/render_prompt.py" --name hld-review --initiative-id "$initiative_id" --provider codex --model "$model" --iteration "$iteration" --profile "${AI_SDLC_HLD_PROFILE:-auto}" --feedback-file "${AI_SDLC_HLD_FEEDBACK_FILE:-}")"

if [ "${AI_SDLC_AGENT_DRY_RUN:-0}" = "1" ]; then
  printf '%s\n' "codex --ask-for-approval never exec --cd $target --model $model --sandbox workspace-write --output-last-message $last_message < rendered-review-prompt"
  exit 0
fi

python3 "$root/tooling/with_timeout.py" "${AI_SDLC_AGENT_TIMEOUT_SECONDS:-480}" \
  "$root/tooling/providers/run_codex_with_progress.sh" "$target" "$model" "$last_message" "$prompt"
test -f "$review_file" || { echo "Codex reviewer did not create: $review_file" >&2; exit 30; }
echo "AI HLD review written: $review_file"
