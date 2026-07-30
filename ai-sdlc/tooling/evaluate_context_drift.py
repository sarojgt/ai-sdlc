#!/usr/bin/env python3
"""Compare an HLD's immutable context baseline with current main-reachable tags."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from context_versions import latest_tag, tag_commit  # noqa: E402


def baseline_packages(text: str) -> list[tuple[str, str]]:
    return re.findall(r'(?ms)^    - id: "([^"]+)"\s*$.*?^      version_tag: "([^"]+)"\s*$', text)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: evaluate_context_drift.py <initiative-dir>", file=sys.stderr)
        return 2
    initiative = Path(sys.argv[1]).resolve()
    baseline = initiative / "evidence" / "design-baseline.yaml"
    if not baseline.is_file():
        print(f"Missing HLD design baseline: {baseline}", file=sys.stderr)
        return 1
    records = baseline_packages(baseline.read_text(encoding="utf-8"))
    output = initiative / "evidence" / "context-drift.yaml"
    lines = ["context_drift:", f'  initiative: "{initiative.name}"', "  action: human_decision_required", "  auto_regeneration: false", "  packages:"]
    for package, baseline_tag in records:
        current_tag = latest_tag(package)
        classification = "none" if baseline_tag == current_tag else ("reassessment_required" if baseline_tag == "unreleased" or current_tag == "unreleased" else "review_recommended")
        lines.extend([f'    - id: "{package}"', f'      baseline_version: "{baseline_tag}"', f'      current_version: "{current_tag}"', f'      current_commit: "{tag_commit(current_tag)}"', f'      classification: "{classification}"'])
    lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Context drift evidence written: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
