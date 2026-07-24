#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <initiative-id> <agent-provider> [model]" >&2
  exit 2
fi

initiative_id="$1"
agent_provider="$2"
agent_model="${3:-gpt-5.6-luna}"
root="$(cd "$(dirname "$0")/.." && pwd)"
target="$root/initiatives/$initiative_id"

test -d "$target" || { echo "Unknown initiative: $initiative_id" >&2; exit 1; }

case "$agent_provider" in
  codex)
    "$root/tooling/providers/codex.sh" "$initiative_id" "$agent_model"
    ;;
  github-copilot)
    "$root/tooling/providers/github-copilot.sh" "$initiative_id" "$agent_model"
    ;;
  *)
    echo "No local adapter is installed for provider '$agent_provider'." >&2
    echo "Add ai-sdlc/tooling/providers/$agent_provider.sh without changing the lifecycle contract." >&2
    exit 20
    ;;
esac
