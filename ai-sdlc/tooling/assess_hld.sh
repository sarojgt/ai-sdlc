#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <initiative-id> <provider> <model>" >&2
  exit 2
fi

initiative_id="$1"
provider="$2"
model="$3"
root="$(cd "$(dirname "$0")/.." && pwd)"

case "$provider" in
  codex)
    "$root/tooling/providers/codex-assess.sh" "$initiative_id" "$model"
    ;;
  github-copilot)
    "$root/tooling/providers/github-copilot-assess.sh" "$initiative_id" "$model"
    ;;
  *)
    echo "No HLD assessment adapter is installed for provider '$provider'." >&2
    exit 20
    ;;
esac
