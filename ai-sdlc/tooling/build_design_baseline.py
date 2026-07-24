#!/usr/bin/env python3
"""Create the immutable version/hash input snapshot for HLD generation."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


SEMVER = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def run(*args: str) -> str:
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout.strip()


def latest_tag(track: str) -> str:
    candidates = []
    pattern = "v*" if not track else f"{track}/v*"
    for tag in run("git", "tag", "--list", pattern).splitlines():
        version = tag.rsplit("/", 1)[-1]
        if SEMVER.match(version):
            candidates.append((tuple(int(part) for part in SEMVER.match(version).groups()), tag))
    return max(candidates)[1] if candidates else "unreleased"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "missing"


def directory_hash(path: Path) -> str:
    digest = hashlib.sha256()
    if not path.is_dir():
        return "missing"
    for file in sorted(item for item in path.rglob("*") if item.is_file()):
        digest.update(str(file.relative_to(path)).encode())
        digest.update(file.read_bytes())
    return digest.hexdigest()


def value(item: object) -> str:
    return json.dumps(item, ensure_ascii=False)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: build_design_baseline.py <initiative-id>", file=sys.stderr)
        return 2
    initiative_id = sys.argv[1]
    root = Path(__file__).resolve().parent.parent
    target = root / "initiatives" / initiative_id
    if not target.is_dir():
        print(f"Unknown initiative: {initiative_id}", file=sys.stderr)
        return 1

    print('baseline_version: "0.1"')
    print(f"repository_commit: {value(run('git', 'rev-parse', 'HEAD'))}")
    print(f"framework_tag: {value(latest_tag(''))}")
    print("initiative:")
    print(f"  id: {value(initiative_id)}")
    print(f"  tag: {value(latest_tag(f'initiative/{initiative_id}'))}")
    print("requirement:")
    print(f"  artifact: {value(f'REQ-{initiative_id}')}")
    print(f"  version_tag: {value(latest_tag(f'initiative/{initiative_id}'))}")
    print(f"  content_sha256: {value(file_hash(target / 'requirement.md'))}")
    print("context:")
    print(f"  manifest_sha256: {value(file_hash(target / 'context-manifest.yaml'))}")
    print(f"  consistent_tag: {value(latest_tag('context/consistent'))}")
    print(f"  guardrails_tag: {value(latest_tag('context/guardrails'))}")
    print(f"  relative_tag: {value(latest_tag(f'initiative/{initiative_id}/context'))}")
    print(f"  relative_content_sha256: {value(directory_hash(target / 'context' / 'relative'))}")
    print("design:")
    print(f"  hld_tag: {value(latest_tag(f'initiative/{initiative_id}/hld'))}")
    print(f"  lld_tag: {value(latest_tag(f'initiative/{initiative_id}/lld'))}")
    print("generation:")
    print("  hld_uses_this_baseline: true")
    print("  architecture_approval_required: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
