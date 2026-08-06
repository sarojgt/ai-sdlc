#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 5 ]; then
  echo "Usage: $0 <initiative-id> <generator-provider> <generator-model> <reviewer-provider> <reviewer-model> [auto|small|medium|large]" >&2
  exit 2
fi

initiative_id="$1"
generator_provider="$2"
generator_model="$3"
reviewer_provider="$4"
reviewer_model="$5"
profile="${6:-${AI_SDLC_HLD_PROFILE:-auto}}"
root="$(cd "$(dirname "$0")/.." && pwd)"
target="$root/initiatives/$initiative_id"
profile_file="$root/config/hld-profiles.yaml"

profile_value() {
  awk -v profile="$profile" -v key="$1" '
    $0 ~ "^  " profile ":" { inside=1; next }
    inside && $0 ~ /^  [A-Za-z0-9_-]+:/ { inside=0 }
    inside && $0 ~ "^    " key ":" { sub("^    " key ": *", ""); print; exit }
  ' "$profile_file"
}

case "$profile" in
  auto|small|medium|large) ;;
  *) echo "Unsupported HLD profile: $profile (expected auto, small, medium, or large)" >&2; exit 2 ;;
esac

max_iterations="${AI_SDLC_HLD_LOOP_MAX_ITERATIONS:-$(profile_value max_iterations)}"
max_elapsed_minutes="${AI_SDLC_HLD_MAX_ELAPSED_MINUTES:-$(profile_value max_elapsed_minutes)}"
configured_agent_timeout_seconds="${AI_SDLC_AGENT_TIMEOUT_SECONDS:-}"
agent_timeout_seconds="${configured_agent_timeout_seconds:-$(( $(profile_value agent_timeout_minutes) * 60 ))}"
export AI_SDLC_HLD_PROFILE="$profile" AI_SDLC_AGENT_TIMEOUT_SECONDS="$agent_timeout_seconds"

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
python3 "$root/tooling/approval_gate.py" requirements "$target"

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
if [ "$max_elapsed_minutes" -lt 1 ]; then
  echo "max_elapsed_minutes must be at least one minute" >&2
  exit 2
fi

started_at="$(date +%s)"
checkpoint_file="$target/evidence/hld-loop.yaml"
resume="${AI_SDLC_HLD_RESUME:-0}"
case "$resume" in
  1|true|TRUE|yes) resume=1 ;;
  *) resume=0 ;;
esac
commit_checkpoints="${AI_SDLC_HLD_COMMIT_CHECKPOINTS:-0}"
checkpoint_branch="${AI_SDLC_HLD_BRANCH:-}"
file_hash() {
  if [ -f "$1" ]; then
    sha256 "$1" | awk '{print $1}'
  fi
}
requirement_hash="$(file_hash "$target/requirement.md")"
context_manifest_hash="$(file_hash "$target/context-manifest.yaml")"
# A human-review batch is an explicit input to a revision.  Keep the internal
# name generic so AI reviewer feedback can become the next revision input too.
feedback_file="${AI_SDLC_HLD_REVISION_FEEDBACK_FILE:-${AI_SDLC_HLD_FEEDBACK_FILE:-}}"
if [ -n "$feedback_file" ]; then
  case "$feedback_file" in
    /*|*".."*) echo "Feedback file must be a relative initiative path" >&2; exit 2 ;;
  esac
  test -f "$target/$feedback_file" || { echo "Feedback file not found: $feedback_file" >&2; exit 1; }
fi
start_iteration=1
if [ -z "$feedback_file" ] && [ "$resume" = "1" ] && [ -f "$checkpoint_file" ]; then
  stored_requirement_hash="$(sed -n 's/^  requirement_sha256: *"\{0,1\}\([^" ]*\).*/\1/p' "$checkpoint_file" | head -1)"
  stored_context_manifest_hash="$(sed -n 's/^  context_manifest_sha256: *"\{0,1\}\([^" ]*\).*/\1/p' "$checkpoint_file" | head -1)"
  if [ -n "$stored_requirement_hash" ] && [ "$stored_requirement_hash" != "$requirement_hash" ]; then
    echo "Cannot resume: requirement.md changed since the checkpoint." >&2
    exit 12
  fi
  if [ -n "$stored_context_manifest_hash" ] && [ "$stored_context_manifest_hash" != "$context_manifest_hash" ]; then
    echo "Cannot resume: context-manifest.yaml changed since the checkpoint." >&2
    exit 12
  fi
  start_iteration="$(sed -n 's/^  iteration: *//p' "$checkpoint_file" | head -1)"
  start_iteration="${start_iteration:-1}"
fi
phase="initializing"
latest_decision=""
latest_review_file=""
loop_finished=0
write_checkpoint() {
  status="$1"
  iteration="$2"
  mkdir -p "$(dirname "$checkpoint_file")"
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
  latest_review_file: "$latest_review_file"
  latest_decision: "$latest_decision"
  review_file: "$latest_review_file"
  requirement_sha256: "$requirement_hash"
  context_manifest_sha256: "$context_manifest_hash"
  repository_commit: "$(git rev-parse HEAD)"
  feedback_file: "$feedback_file"
  prompt_set: "hld-prompts-v1"
  agent_timeout_seconds: $agent_timeout_seconds
  human_architecture_approval_required: true
EOF
}
checkpoint_commit() {
  checkpoint_phase="$1"
  [ "$commit_checkpoints" = "1" ] || return 0
  git config user.name "${AI_SDLC_GIT_USER_NAME:-github-actions[bot]}"
  git config user.email "${AI_SDLC_GIT_USER_EMAIL:-41898282+github-actions[bot]@users.noreply.github.com}"
  # Keep the human-facing PR focused while retaining every review under the
  # immutable feedback/reviews and feedback/batches evidence paths.
  git add "$target/hld" "$target/evidence"
  for evidence_dir in "$target/feedback/reviews" "$target/feedback/batches"; do
    [ -e "$evidence_dir" ] && git add "$evidence_dir"
  done
  if git diff --cached --quiet; then
    return 0
  fi
  git commit -m "chore(hld): checkpoint iteration-${iteration:-$start_iteration}-$checkpoint_phase"
  if [ -n "$checkpoint_branch" ]; then
    git push origin "HEAD:$checkpoint_branch"
  fi
}
on_exit() {
  result=$?
  if [ "$loop_finished" -eq 0 ]; then
    write_checkpoint "interrupted_or_failed" "${iteration:-$start_iteration}"
    checkpoint_commit "failure"
  fi
  exit "$result"
}
trap on_exit EXIT

hld_hash() {
  find "$target/hld" -type f -print | sort | while IFS= read -r file; do
    sha256 "$file"
  done | sha256 | awk '{print $1}'
}

remaining_timeout_seconds() {
  elapsed=$(( $(date +%s) - started_at ))
  remaining=$(( max_elapsed_minutes * 60 - elapsed ))
  if [ "$remaining" -le 0 ]; then
    echo "HLD AI loop time limit reached; escalating to human Solution Architect." >&2
    exit 10
  fi
  if [ "$remaining" -lt "$agent_timeout_seconds" ]; then
    echo "$remaining"
  else
    echo "$agent_timeout_seconds"
  fi
}

run_agent_within_budget() {
  timeout_seconds="$(remaining_timeout_seconds)"
  AI_SDLC_AGENT_TIMEOUT_SECONDS="$timeout_seconds" "$@"
}

record_profile() {
  python3 - "$target/hld/hld.md" "$profile" <<'PY'
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
profile = sys.argv[2]
text = path.read_text(encoding="utf-8")
if re.search(r"^\s*change_size\s*:", text, flags=re.MULTILINE):
    text = re.sub(r"^(\s*change_size\s*:\s*).*$", rf"\1{profile}", text, count=1, flags=re.MULTILINE)
elif text.startswith("---\n"):
    text = text.replace("---\n", f"---\nchange_size: {profile}\n", 1)
else:
    text = f"---\nchange_size: {profile}\n---\n\n" + text
path.write_text(text, encoding="utf-8")
PY
}

previous_feedback_hash=""

if [ "${AI_SDLC_HLD_LOOP_DRY_RUN:-0}" = "1" ]; then
  echo "DRY RUN: profile=$profile, max_iterations=$max_iterations, max_elapsed_minutes=$max_elapsed_minutes, agent_timeout_seconds=$agent_timeout_seconds"
  echo "DRY RUN: ./ai-sdlc/tooling/generate_hld.sh $initiative_id $generator_provider $generator_model 1"
  echo "DRY RUN: ./ai-sdlc/tooling/review_hld.sh $initiative_id $reviewer_provider $reviewer_model 1"
  loop_finished=1
  exit 0
fi

mkdir -p "$target/feedback" "$target/evidence"
python3 "$root/tooling/run_lifecycle_hooks.py" before_hld "$target"
python3 "$root/tooling/initialize_design_artifacts.py" "$target" hld
python3 "$root/tooling/build_context_pack.py" "$target"

if [ "$profile" = "auto" ]; then
  assessment_file="$target/evidence/hld-assessment.yaml"
  if [ ! -s "$assessment_file" ]; then
    echo "[AI-SDLC] Running preflight HLD impact assessment before generation..."
    AI_SDLC_ASSESSMENT_TIMEOUT_SECONDS="${AI_SDLC_ASSESSMENT_TIMEOUT_SECONDS:-300}" \
      "$root/tooling/assess_hld.sh" "$initiative_id" "$generator_provider" "$generator_model"
  else
    echo "[AI-SDLC] Reusing existing HLD impact assessment."
  fi
  profile="$(python3 "$root/tooling/resolve_hld_profile.py" "$target")" || {
    echo "HLD profile assessment is invalid; expected small, medium, or large." >&2
    exit 10
  }
  echo "AI-selected HLD profile: $profile"
fi

if [ ! -s "$target/evidence/hld-assessment.yaml" ]; then
  echo "[AI-SDLC] Creating the required HLD impact assessment before generation..."
  AI_SDLC_ASSESSMENT_TIMEOUT_SECONDS="${AI_SDLC_ASSESSMENT_TIMEOUT_SECONDS:-300}" \
    "$root/tooling/assess_hld.sh" "$initiative_id" "$generator_provider" "$generator_model"
fi
python3 "$root/tooling/sync_hld_evidence.py" "$target"

max_iterations="${AI_SDLC_HLD_LOOP_MAX_ITERATIONS:-$(profile_value max_iterations)}"
max_elapsed_minutes="${AI_SDLC_HLD_MAX_ELAPSED_MINUTES:-$(profile_value max_elapsed_minutes)}"
agent_timeout_seconds="${configured_agent_timeout_seconds:-$(( $(profile_value agent_timeout_minutes) * 60 ))}"
export AI_SDLC_HLD_PROFILE="$profile" AI_SDLC_AGENT_TIMEOUT_SECONDS="$agent_timeout_seconds"

reuse_existing_hld=0
if [ -z "$feedback_file" ] && [ "$resume" = "1" ] && [ -s "$target/hld/hld.md" ]; then
  reuse_existing_hld=1
  echo "[AI-SDLC] Resume mode: existing HLD will be retained for review."
fi

for iteration in $(seq "$start_iteration" "$max_iterations"); do
  echo "HLD AI loop iteration $iteration/$max_iterations (profile: $profile)"
  echo "Safety policy: max $max_iterations iterations, max $max_elapsed_minutes minutes"
  echo "Generator: $generator_provider / $generator_model"
  echo "Reviewer: $reviewer_provider / $reviewer_model"

  phase="generator"
  write_checkpoint "running" "$iteration"
  before_hld_hash="$(hld_hash)"
  if [ "$reuse_existing_hld" -eq 1 ] && [ "$iteration" -eq "$start_iteration" ]; then
    echo "[AI-SDLC] Skipping generator; resuming with existing HLD."
  else
    if [ -n "$feedback_file" ]; then
      export AI_SDLC_HLD_MODE=revision
      export AI_SDLC_HLD_FEEDBACK_FILE="$feedback_file"
    else
      export AI_SDLC_HLD_MODE=initial
      unset AI_SDLC_HLD_FEEDBACK_FILE
    fi
    run_agent_within_budget "$root/tooling/generate_hld.sh" "$initiative_id" "$generator_provider" "$generator_model" "$iteration"
  fi
  after_hld_hash="$(hld_hash)"
  record_profile
  python3 "$root/tooling/resolve_hld_profile.py" "$target" >/dev/null || {
    echo "Generated HLD does not contain a valid change_size classification." >&2
    exit 10
  }
  echo "[AI-SDLC] Validating generated HLD structure and Mermaid diagrams before AI review..."
  python3 "$root/tooling/validate_hld_artifacts.py" "$target"
  python3 "$root/tooling/run_lifecycle_hooks.py" after_hld "$target"
  checkpoint_commit "generator"
  reuse_existing_hld=0

  if [ "$iteration" -gt 1 ] && [ "$before_hld_hash" = "$after_hld_hash" ]; then
    echo "HLD did not change after requested revisions; escalating to human Solution Architect." >&2
    exit 10
  fi

  phase="reviewer"
  write_checkpoint "running" "$iteration"
  run_agent_within_budget "$root/tooling/review_hld.sh" "$initiative_id" "$reviewer_provider" "$reviewer_model" "$iteration"

  review_file_relative="feedback/reviews/ai-review-iteration-$iteration.md"
  export AI_SDLC_HLD_REVIEW_FILE="$review_file_relative"
  review_file="$target/$review_file_relative"
  test -f "$review_file" || {
    echo "AI reviewer did not produce: $review_file" >&2
    exit 30
  }
  python3 "$root/tooling/validate_ai_review.py" "$review_file"
  latest_review_file="$review_file_relative"
  latest_decision="$(sed -n 's/^decision: *//p' "$review_file" | head -1 | tr -d '\r' | tr '[:upper:]' '[:lower:]')"
  write_checkpoint "reviewed" "$iteration"
  checkpoint_commit "reviewer"

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

  decision="$latest_decision"
  case "$decision" in
    ready_for_human_review|pass)
      if ! python3 "$root/tooling/validate_hld_readiness.py" "$target"; then
        write_checkpoint "discovery_required" "$iteration"
        checkpoint_commit "discovery"
        loop_finished=1
        echo "AI review passed, but unresolved foundational context gaps require a discovery gate." >&2
        exit 10
      fi
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
  latest_review_file: "$latest_review_file"
  latest_decision: "$latest_decision"
  requirement_sha256: "$requirement_hash"
  context_manifest_sha256: "$context_manifest_hash"
  repository_commit: "$(git rev-parse HEAD)"
  feedback_file: "$feedback_file"
  prompt_set: "hld-prompts-v1"
  human_architecture_approval_required: true
EOF
      checkpoint_commit "complete"
      loop_finished=1
      echo "AI review completed after $iteration iteration(s)."
      echo "Next gate: human Solution Architect review and approval."
      exit 0
      ;;
    changes_requested)
      if [ "$iteration" -eq "$max_iterations" ]; then
        write_checkpoint "changes_requested" "$iteration"
        checkpoint_commit "blocked"
        loop_finished=1
        echo "AI review still requests changes after $max_iterations iteration(s)." >&2
        echo "Escalate to the human Solution Architect: $review_file" >&2
        exit 10
      fi
      feedback_file="$review_file_relative"
      write_checkpoint "changes_requested" "$iteration"
      export AI_SDLC_HLD_MODE=revision AI_SDLC_HLD_FEEDBACK_FILE="$feedback_file"
      echo "AI review requested changes; continuing with bounded regeneration."
      ;;
    escalate|*)
      write_checkpoint "escalated" "$iteration"
      checkpoint_commit "escalated"
      loop_finished=1
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
