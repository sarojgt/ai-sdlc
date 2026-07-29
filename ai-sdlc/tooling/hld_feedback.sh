#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <initiative-id> [agent-provider] [model]" >&2
  exit 2
fi

initiative_id="$1"
agent_provider="${2:-codex}"
agent_model="${3:-gpt-5.6-luna}"
root="$(cd "$(dirname "$0")/.." && pwd)"
target="$root/initiatives/$initiative_id"

test -d "$target" || { echo "Unknown initiative: $initiative_id" >&2; exit 1; }

scope=""
comment=""
read -r -p "Sections to revise, for example risks, rollback: " scope
read -r -p "Architect feedback: " comment

mkdir -p "$target/feedback"
feedback_file="$target/feedback/human-review.md"
{
  echo "# Architecture feedback"
  echo ""
  echo "Initiative: $initiative_id"
  echo "Agent for rerun: $agent_provider"
  echo "Model for rerun: $agent_model"
  echo "Scope: $scope"
  echo ""
  echo "$comment"
} > "$feedback_file"

echo "Saved feedback: $feedback_file"
echo "Rerun the bounded HLD generation with:"
echo "  AI_SDLC_HLD_RESUME=1 just ai-sdlc-hld $initiative_id $agent_provider $agent_model"
