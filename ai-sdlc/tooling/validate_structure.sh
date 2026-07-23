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

required_files=(
  "$root/schemas/das.schema.yaml"
  "$root/config/gates.yaml"
  "$root/config/roles.yaml"
  "$root/config/context-sources.yaml"
  "$initiative/initiative.yaml"
  "$initiative/context-manifest.yaml"
  "$initiative/requirement.md"
  "$initiative/hld/hld.md"
  "$initiative/lld/lld.md"
  "$initiative/approvals.yaml"
  "$initiative/traceability.yaml"
)

for file in "${required_files[@]}"; do
  test -f "$file" || { echo "Missing required file: $file" >&2; exit 1; }
done

grep -q 'implementation_locked_until: architecture.approved' "$initiative/initiative.yaml"
grep -q 'type: hld' "$initiative/hld/hld.md"
grep -q 'type: lld' "$initiative/lld/lld.md"
grep -q 'decision: pending' "$initiative/approvals.yaml"

echo "AI-SDLC framework structure is valid."
echo "Next implementation step: replace placeholder checks with DAS/hash/approval validation."
