#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <initiative-id> <reviewer-provider> [model] [iteration]" >&2
  exit 2
fi

initiative_id="$1"
reviewer_provider="$2"
reviewer_model="${3:-gpt-5.6-terra}"
iteration="${4:-1}"
root="$(cd "$(dirname "$0")/.." && pwd)"

case "$reviewer_provider" in
  codex)
    "$root/tooling/providers/codex-review.sh" "$initiative_id" "$reviewer_model" "$iteration"
    ;;
  github-copilot)
    "$root/tooling/providers/github-copilot-review.sh" "$initiative_id" "$reviewer_model" "$iteration"
    ;;
  *)
    echo "No HLD reviewer adapter is installed for provider '$reviewer_provider'." >&2
    exit 20
    ;;
esac
