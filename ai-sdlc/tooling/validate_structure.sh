#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
target="${1:?Usage: $0 <initiative-directory>}"

if [ -d "$target" ]; then
  initiative="$(cd "$target" && pwd)"
elif [ -d "$root/$target" ]; then
  initiative="$(cd "$root/$target" && pwd)"
else
  echo "Initiative directory not found: $target" >&2
  exit 1
fi

# A Product Owner intake is intentionally requirement-only. The post-merge
# expansion step creates initiative metadata, approvals, traceability, context
# manifest, and the reusable design scaffold.
if [ ! -f "$initiative/initiative.yaml" ]; then
  test -f "$initiative/requirement.md" || {
    echo "Requirement-only intake is missing requirement.md: $initiative" >&2
    exit 1
  }
  while IFS= read -r -d '' file; do
    relative="${file#"$initiative"/}"
    case "$relative" in
      requirement.md|context/relative/*)
        ;;
      *)
        echo "Invalid intake file: $relative" >&2
        echo "Allowed intake files are requirement.md and optional context/relative/**." >&2
        exit 1
        ;;
    esac
  done < <(find "$initiative" -type f -print0)
  echo "AI-SDLC intake structure is valid."
  echo "Next step: merge after Product Owner review so post-merge expansion can create the scaffold."
  exit 0
fi

state="$(awk '
  /^workflow:/ { in_workflow=1; next }
  in_workflow && /^[[:space:]]*state:/ {
    print $2
    exit
  }
' "$initiative/initiative.yaml")"

core_files=(
  "$root/schemas/das.schema.yaml"
  "$root/config/gates.yaml"
  "$root/config/roles.yaml"
  "$root/config/context-sources.yaml"
  "$initiative/initiative.yaml"
  "$initiative/context-manifest.yaml"
  "$initiative/requirement.md"
  "$initiative/initiative.md"
  "$initiative/approvals.yaml"
  "$initiative/traceability.yaml"
)

for file in "${core_files[@]}"; do
  test -f "$file" || { echo "Missing required file: $file" >&2; exit 1; }
done

grep -q 'implementation_locked_until: architecture.approved' "$initiative/initiative.yaml"

# Requirements approval may be synchronized by the post-merge workflow. The
# HLD and LLD gates must remain pending until their separate human gates pass.
approval_decisions="$(awk '
  /^  - gate:/ { gate=$3 }
  /^[[:space:]]+decision:/ { print gate ":" $2 }
' "$initiative/approvals.yaml")"
case "$state" in
  hld_approved|lld_draft|lld_review|lld_approved|implementation_ready|implementing|pr_review|release_ready|deployed|learning)
    grep -q '^hld:approved$' <<< "$approval_decisions"
    ;;
  *)
    grep -q '^hld:pending$' <<< "$approval_decisions"
    ;;
esac
grep -q '^lld:pending$' <<< "$approval_decisions"

case "$state" in
  intake)
    ;;
  scaffolded|approved)
    # Design, feedback, evidence, and relative-context directories are created
    # lazily by their lifecycle workflows.
    ;;
  hld_draft|hld_review|hld_approved|lld_draft|lld_review|lld_approved|implementation_ready|implementing|pr_review|release_ready|deployed|learning)
    scaffold_files=("$initiative/hld/hld.md")
    case "$state" in
      lld_draft|lld_review|lld_approved|implementation_ready|implementing|pr_review|release_ready|deployed|learning)
        scaffold_files+=("$initiative/lld/lld.md")
        ;;
    esac
    for file in "${scaffold_files[@]}"; do
      test -f "$file" || { echo "Missing lifecycle file: $file" >&2; exit 1; }
    done
    ;;
esac

echo "AI-SDLC framework structure is valid."
echo "Next implementation step: replace placeholder checks with DAS/hash/approval validation."
