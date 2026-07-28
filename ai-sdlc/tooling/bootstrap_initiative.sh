#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 4 ]; then
  echo "Usage: $0 <initiative-id> <title> <business-outcome> <problem-statement> [owner] [work-item-id] [risk-tier] [data-classification] [profile]" >&2
  exit 2
fi

initiative_id="$1"
title="$2"
business_outcome="$3"
problem_statement="$4"
owner="${5:-team.example}"
work_item_id="${6:-$initiative_id}"
provider="github"
risk_tier="${7:-medium}"
data_classification="${8:-internal}"
profile="${9:-intake}"

case "$initiative_id" in
  *[!A-Za-z0-9_-]*) echo "Initiative ID contains unsupported characters" >&2; exit 2 ;;
esac

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

root="$(cd "$(dirname "$0")/.." && pwd)"
target="$root/initiatives/$initiative_id"
template="$root/templates/initiative"

if [ -e "$target" ]; then
  echo "Initiative already exists: $target" >&2
  exit 1
fi

mkdir -p "$target"

copy_files() {
  for relative in "$@"; do
    src="$template/$relative"
    dst="$target/$relative"
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
  done
}

if [ "$profile" = "full" ]; then
  cp -R "$template/." "$target/"
else
  # Keep the Product Owner intake PR human-sized. Metadata, approvals,
  # traceability, and reusable design scaffolding are created after merge by
  # expand_initiative.py.
  copy_files "requirement.md"
fi

find "$target" -type f -print0 | while IFS= read -r -d '' file; do
  # Use a backup suffix so this works with BSD sed on macOS and GNU sed
  # on GitHub-hosted Ubuntu runners.
  sed -i.bak \
    -e "s/{{ initiative.id }}/$initiative_id/g" \
    -e "s/{{ initiative.title }}/$title/g" \
    -e "s/{{ initiative.owner }}/$owner/g" \
    -e "s/{{ source.provider }}/$provider/g" \
    -e "s/{{ source.work_item_id }}/$work_item_id/g" \
    -e "s/{{ policy.risk_tier }}/$risk_tier/g" \
    -e "s/{{ policy.data_classification }}/$data_classification/g" \
    -e "s/{{ roles.solution_architect }}/team.solution-architecture/g" \
    -e "s/{{ roles.senior_engineer }}/team.engineering/g" \
    -e "s/{{ requirement.business_outcome }}/$business_outcome/g" \
    -e "s/{{ requirement.problem_statement }}/$problem_statement/g" \
    "$file"
  rm -f "$file.bak"
done

echo "Created initiative: $target"
echo "Next: complete requirement.md, build context, and request business review."
