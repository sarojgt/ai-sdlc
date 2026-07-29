#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 5 ]; then
  echo "Usage: $0 <initiative-id> <generator-provider> <generator-model> <reviewer-provider> <reviewer-model> [small|medium|large]" >&2
  exit 2
fi

initiative_id="$1"
generator_provider="$2"
generator_model="$3"
reviewer_provider="$4"
reviewer_model="$5"
profile="${6:-${AI_SDLC_HLD_PROFILE:-small}}"
root="$(cd "$(dirname "$0")/.." && pwd)"
target="$root/initiatives/$initiative_id"
policy_file="$root/config/hld-loop-policy.yaml"
profile_file="$root/config/hld-profiles.yaml"

policy_value() {
  sed -n "s/^  $1: *//p" "$policy_file" | head -1 | tr -d '\r'
}

profile_value() {
  awk -v profile="$profile" -v key="$1" '
    $0 ~ "^  " profile ":" { inside=1; next }
    inside && $0 ~ /^  [A-Za-z0-9_-]+:/ { inside=0 }
    inside && $0 ~ "^    " key ":" { sub("^    " key ": *", ""); print; exit }
  ' "$profile_file"
}

case "$profile" in
  small|medium|large) ;;
  *) echo "Unsupported HLD profile: $profile (expected small, medium, or large)" >&2; exit 2 ;;
esac

max_iterations="${AI_SDLC_HLD_LOOP_MAX_ITERATIONS:-$(profile_value max_iterations)}"
max_elapsed_minutes="${AI_SDLC_HLD_MAX_ELAPSED_MINUTES:-$(profile_value max_elapsed_minutes)}"
agent_timeout_seconds="${AI_SDLC_AGENT_TIMEOUT_SECONDS:-$(( $(profile_value agent_timeout_minutes) * 60 ))}"
max_hld_lines="$(profile_value max_hld_lines)"
export AI_SDLC_HLD_PROFILE="$profile" AI_SDLC_AGENT_TIMEOUT_SECONDS="$agent_timeout_seconds"

case "$max_hld_lines" in
  ''|*[!0-9]*) echo "max_hld_lines must be a positive integer" >&2; exit 2 ;;
esac

sha256() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$@"
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$@"
  else
    echo "No SHA-256 command found (expected sha256sum or shasum)." >&2
    return 1
  fi
}

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
checkpoint_file="$target/evidence/hld-loop.yaml"
resume="${AI_SDLC_HLD_RESUME:-0}"
start_iteration=1
if [ "$resume" = "1" ] && [ -f "$checkpoint_file" ]; then
  start_iteration="$(sed -n 's/^  iteration: *//p' "$checkpoint_file" | head -1)"
  start_iteration="${start_iteration:-1}"
fi
phase="initializing"
loop_finished=0
write_checkpoint() {
  status="$1"
  iteration="$2"
  cat > "$checkpoint_file" <<EOF
hld_loop:
  status: $status
  initiative: "$initiative_id"
  profile: "$profile"
  iteration: $iteration
  phase: "$phase"
  generator_provider: "$generator_provider"
  generator_model: "$generator_model"
  reviewer_provider: "$reviewer_provider"
  reviewer_model: "$reviewer_model"
  agent_timeout_seconds: $agent_timeout_seconds
  human_architecture_approval_required: true
EOF
}
on_exit() {
  result=$?
  if [ "$loop_finished" -eq 0 ]; then
    write_checkpoint "interrupted_or_failed" "${iteration:-$start_iteration}"
  fi
  exit "$result"
}
trap on_exit EXIT

hld_hash() {
  find "$target/hld" -type f -print | sort | while IFS= read -r file; do
    sha256 "$file"
  done | sha256 | awk '{print $1}'
}

previous_feedback_hash=""

if [ "${AI_SDLC_HLD_LOOP_DRY_RUN:-0}" = "1" ]; then
  echo "DRY RUN: profile=$profile, max_iterations=$max_iterations, max_elapsed_minutes=$max_elapsed_minutes, agent_timeout_seconds=$agent_timeout_seconds, max_hld_lines=$max_hld_lines"
  echo "DRY RUN: ./ai-sdlc/tooling/generate_hld.sh $initiative_id $generator_provider $generator_model 1"
  echo "DRY RUN: ./ai-sdlc/tooling/review_hld.sh $initiative_id $reviewer_provider $reviewer_model 1"
  loop_finished=1
  exit 0
fi

mkdir -p "$target/feedback" "$target/evidence"
python3 "$root/tooling/initialize_design_artifacts.py" "$target" hld

for iteration in $(seq "$start_iteration" "$max_iterations"); do
  echo "HLD AI loop iteration $iteration/$max_iterations (profile: $profile)"
  echo "Safety policy: max $max_iterations iterations, max $max_elapsed_minutes minutes"
  echo "Generator: $generator_provider / $generator_model"
  echo "Reviewer: $reviewer_provider / $reviewer_model"

  phase="generator"
  write_checkpoint "running" "$iteration"
  before_hld_hash="$(hld_hash)"
  "$root/tooling/generate_hld.sh" "$initiative_id" "$generator_provider" "$generator_model" "$iteration"
  after_hld_hash="$(hld_hash)"
  hld_lines="$(wc -l < "$target/hld/hld.md" | tr -d ' ')"
  if [ "$hld_lines" -gt "$max_hld_lines" ]; then
    echo "HLD exceeds $profile profile limit: $hld_lines lines (maximum $max_hld_lines)." >&2
    echo "Regenerate a concise decision document or select a larger profile." >&2
    exit 10
  fi

  if [ "$iteration" -gt 1 ] && [ "$before_hld_hash" = "$after_hld_hash" ]; then
    echo "HLD did not change after requested revisions; escalating to human Solution Architect." >&2
    exit 10
  fi

  phase="reviewer"
  write_checkpoint "running" "$iteration"
  "$root/tooling/review_hld.sh" "$initiative_id" "$reviewer_provider" "$reviewer_model" "$iteration"

  review_file="$target/feedback/ai-review.md"
  test -f "$review_file" || {
    echo "AI reviewer did not produce: $review_file" >&2
    exit 30
  }

  feedback_hash="$(sed -e '/^reviewer:/d' -e '/^model:/d' -e '/^iteration:/d' "$review_file" | sha256 | awk '{print $1}')"
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
  profile: "$profile"
  generator_provider: "$generator_provider"
  generator_model: "$generator_model"
  reviewer_provider: "$reviewer_provider"
  reviewer_model: "$reviewer_model"
  human_architecture_approval_required: true
EOF
      loop_finished=1
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
