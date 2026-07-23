#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 4 ]; then
  echo "Usage: $0 <target-directory> <model> <last-message-file> <prompt>" >&2
  exit 2
fi

target="$1"
model="$2"
last_message="$3"
prompt="$4"
started_at="$(date +%s)"

echo "[AI-SDLC] Starting Codex model: $model" >&2
echo "[AI-SDLC] Workspace: $target" >&2
echo "[AI-SDLC] Context loading and architecture analysis in progress..." >&2

codex \
  --ask-for-approval never \
  exec \
  --cd "$target" \
  --model "$model" \
  --sandbox workspace-write \
  --output-last-message "$last_message" \
  "$prompt" &
codex_pid=$!

while kill -0 "$codex_pid" 2>/dev/null; do
  sleep 15
  if kill -0 "$codex_pid" 2>/dev/null; then
    elapsed=$(( $(date +%s) - started_at ))
    echo "[AI-SDLC] Still processing: context discovery / HLD analysis (${elapsed}s elapsed)..." >&2
  fi
done

wait "$codex_pid"
echo "[AI-SDLC] Codex processing completed." >&2
