#!/usr/bin/env bash
set -euo pipefail

ask() {
  local label="$1"
  local value
  read -r -p "$label: " value
  printf '%s' "$value"
}

echo "Create a new AI-SDLC initiative"
echo ""

initiative_id="$(ask 'Initiative ID, for example PAY-4567')"
title="$(ask 'Requirement title')"
owner="$(ask 'Owning team')"
work_item_id="$(ask 'Source work-item ID, or press Enter to reuse initiative ID')"
work_item_id="${work_item_id:-$initiative_id}"
business_outcome="$(ask 'Business outcome')"
problem_statement="$(ask 'Problem statement')"
risk_tier="$(ask 'Risk tier [low|medium|high|critical]')"
risk_tier="${risk_tier:-medium}"
data_classification="$(ask 'Data classification [public|internal|confidential|restricted]')"
data_classification="${data_classification:-internal}"
profile="$(ask 'Bootstrap profile [intake|full]')"
profile="${profile:-intake}"

case "$risk_tier" in
  low|medium|high|critical) ;;
  *) echo "Invalid risk tier: $risk_tier" >&2; exit 2 ;;
esac

case "$data_classification" in
  public|internal|confidential|restricted) ;;
  *) echo "Invalid data classification: $data_classification" >&2; exit 2 ;;
esac

case "$profile" in
  intake|full) ;;
  *) echo "Invalid profile: $profile" >&2; exit 2 ;;
esac

script_dir="$(cd "$(dirname "$0")" && pwd)"
"$script_dir/bootstrap_initiative.sh" "$initiative_id" "$title" "$business_outcome" "$problem_statement" "$owner" "$work_item_id" "$risk_tier" "$data_classification" "$profile"
target="$script_dir/../initiatives/$initiative_id"

export AI_SDLC_BUSINESS_OUTCOME="$business_outcome"
export AI_SDLC_PROBLEM_STATEMENT="$problem_statement"
export AI_SDLC_RISK_TIER="$risk_tier"
export AI_SDLC_DATA_CLASSIFICATION="$data_classification"

TARGET="$target" perl -0pi -e 's/\{\{ requirement\.business_outcome \}\}/$ENV{AI_SDLC_BUSINESS_OUTCOME}/g; s/\{\{ requirement\.problem_statement \}\}/$ENV{AI_SDLC_PROBLEM_STATEMENT}/g' "$target/requirement.md"
TARGET="$target" perl -0pi -e 's/medium/$ENV{AI_SDLC_RISK_TIER}/g; s/internal/$ENV{AI_SDLC_DATA_CLASSIFICATION}/g' "$target/initiative.yaml" "$target/requirement.md"

echo ""
echo "Created: $target"
echo "Next step: Product Owner review"
echo "  just ai-sdlc-review-requirement $initiative_id"
