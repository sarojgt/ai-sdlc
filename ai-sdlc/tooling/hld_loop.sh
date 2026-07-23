#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 5 ]; then
  echo "Usage: $0 <initiative-id> <generator-provider> <generator-model> <reviewer-provider> <reviewer-model>" >&2
  exit 2
fi

initiative_id="$1"
generator_provider="$2"
generator_model="$3"
reviewer_provider="$4"
reviewer_model="$5"
root="$(cd "$(dirname "$0")/.." && pwd)"
target="$root/initiatives/$initiative_id"
policy_file="$root/config/hld-loop-policy.yaml"

policy_value() {
  sed -n "s/^  $1: *//p" "$policy_file" | head -1 | tr -d '\r'
}

max_iterations="${AI_SDLC_HLD_LOOP_MAX_ITERATIONS:-$(policy_value max_iterations)}"
max_elapsed_minutes="$(policy_value max_elapsed_minutes)"

test -d "$target" || { echo "Unknown initiative: $initiative_id" >&2; exit 1; }
grep -q 'status: approved' "$target/requirement.md" || {
  echo "Requirement is not approved. HLD loop cannot start." >&2
  exit 10
}

case "$max_iterations" in
  ''|*[!0-9]*) echo "max-iterations must be a positive integer" >&2; exit 2 ;;
esac

if [ "$max_iterations" -lt 1 ] || [ "$max_iterations" -gt 5 ]; then
  echo "max-iterations must be between 1 and 5" >&2
  exit 2
fi

case "$max_elapsed_minutes" in
  ''|*[!0-9]*) echo "max_elapsed_minutes must be a positive integer" >&2; exit 2 ;;
esac

started_at="$(date +%s)"

hld_hash() {
  find "$target/hld" -type f -print | sort | while IFS= read -r file; do
    shasum -a 256 "$file"
  done | shasum -a 256 | awk '{print $1}'
}

mkdir -p "$target/feedback" "$target/evidence"
mkdir -p "$target/hld"
previous_feedback_hash=""

for iteration in $(seq 1 "$max_iterations"); do
  echo "HLD AI loop iteration $iteration/$max_iterations"
  echo "Safety policy: max $max_iterations iterations, max $max_elapsed_minutes minutes"
  echo "Generator: $generator_provider / $generator_model"
  echo "Reviewer: $reviewer_provider / $reviewer_model"

  if [ "${AI_SDLC_HLD_LOOP_DRY_RUN:-0}" = "1" ]; then
    echo "DRY RUN: ./ai-sdlc/tooling/generate_hld.sh $initiative_id $generator_provider $generator_model $iteration"
    echo "DRY RUN: ./ai-sdlc/tooling/review_hld.sh $initiative_id $reviewer_provider $reviewer_model $iteration"
    continue
  fi

  before_hld_hash="$(hld_hash)"
  "$root/tooling/generate_hld.sh" "$initiative_id" "$generator_provider" "$generator_model" "$iteration"
  after_hld_hash="$(hld_hash)"

  if [ "$iteration" -gt 1 ] && [ "$before_hld_hash" = "$after_hld_hash" ]; then
    echo "HLD did not change after requested revisions; escalating to human Solution Architect." >&2
    exit 10
  fi

  "$root/tooling/review_hld.sh" "$initiative_id" "$reviewer_provider" "$reviewer_model" "$iteration"

  review_file="$target/feedback/ai-review-$iteration.md"
  test -f "$review_file" || {
    echo "AI reviewer did not produce: $review_file" >&2
    exit 30
  }

  feedback_hash="$(sed -e '/^reviewer:/d' -e '/^model:/d' -e '/^iteration:/d' "$review_file" | shasum -a 256 | awk '{print $1}')"
  if [ -n "$previous_feedback_hash" ] && [ "$feedback_hash" = "$previous_feedback_hash" ]; then
    echo "Repeated AI feedback detected; escalating to human Solution Architect." >&2
    exit 10
  fi
  previous_feedback_hash="$feedback_hash"

  elapsed_seconds=$(( $(date +%s) - started_at ))
  if [ "$elapsed_seconds" -ge $(( max_elapsed_minutes * 60 )) ]; then
    echo "HLD AI loop time limit reached; escalating to human Solution Architect." >&2
    exit 10
  fi

  decision="$(sed -n 's/^decision: *//p' "$review_file" | head -1 | tr -d '\r' | tr '[:upper:]' '[:lower:]')"
  case "$decision" in
    pass)
      cat > "$target/evidence/hld-loop.yaml" <<EOF
hld_loop:
  status: ai_review_passed
  initiative: "$initiative_id"
  iterations: $iteration
  generator_provider: "$generator_provider"
  generator_model: "$generator_model"
  reviewer_provider: "$reviewer_provider"
  reviewer_model: "$reviewer_model"
  human_architecture_approval_required: true
EOF
      echo "AI review passed after $iteration iteration(s)."
      echo "Next gate: human Solution Architect review and approval."
      exit 0
      ;;
    changes_requested)
      if [ "$iteration" -eq "$max_iterations" ]; then
        echo "AI review still requests changes after $max_iterations iteration(s)." >&2
        echo "Escalate to the human Solution Architect: $review_file" >&2
        exit 10
      fi
      echo "AI review requested changes; continuing with bounded regeneration."
      ;;
    escalate|*)
      echo "AI reviewer returned decision '$decision'; escalating to human review." >&2
      exit 10
      ;;
  esac
done

if [ "${AI_SDLC_HLD_LOOP_DRY_RUN:-0}" = "1" ]; then
  echo "Dry run complete; no agents were invoked and no artifacts were changed."
  exit 0
fi

echo "AI HLD loop completed without a review decision." >&2
exit 10
