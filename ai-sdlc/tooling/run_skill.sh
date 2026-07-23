#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 4 ]; then
  echo "Usage: $0 <skill-id> <initiative-id> <provider> <model>" >&2
  exit 2
fi

skill_id="$1"
initiative_id="$2"
provider="$3"
model="$4"
root="$(cd "$(dirname "$0")/.." && pwd)"

case "$skill_id" in
  hld-generation)
    "$root/tooling/generate_hld.sh" "$initiative_id" "$provider" "$model"
    ;;
  hld-review)
    "$root/tooling/review_hld.sh" "$initiative_id" "$provider" "$model" 1
    ;;
  requirements-analysis|lld-generation|implementation)
    echo "Skill '$skill_id' is registered but its executable adapter is not implemented yet." >&2
    echo "This command intentionally stops before invoking an agent." >&2
    exit 20
    ;;
  *)
    echo "Unknown skill: $skill_id" >&2
    echo "Registered skills are defined in ai-sdlc/config/skills.yaml." >&2
    exit 2
    ;;
esac
