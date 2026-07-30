#!/usr/bin/env python3
"""Create the immutable version/hash input snapshot for HLD generation."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


SEMVER = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def run(*args: str) -> str:
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout.strip()


def latest_framework_tag(track: str) -> str:
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


def selected_context_packages(manifest: Path) -> list[tuple[str, str, str]]:
    """Return unique package/version/commit records from the assembled pack."""
    if not manifest.is_file():
        return []
    values: dict[str, dict[str, str]] = {}
    current: dict[str, str] | None = None
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if re.match(r"^    - id:", line):
            current = {}
        elif current is not None:
            match = re.match(r'^      (package|version_tag|version_commit): "(.*)"$', line)
            if match:
                current[match.group(1)] = match.group(2)
                if len(current) == 3:
                    values[current["package"]] = current
    return [(package, details["version_tag"], details["version_commit"]) for package, details in sorted(values.items())]


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
    print(f"framework_tag: {value(latest_framework_tag(''))}")
    print("initiative:")
    print(f"  id: {value(initiative_id)}")
    print(f"  tag: {value(latest_framework_tag(f'initiative/{initiative_id}'))}")
    print("requirement:")
    print(f"  artifact: {value(f'REQ-{initiative_id}')}")
    print(f"  version_tag: {value(latest_framework_tag(f'initiative/{initiative_id}'))}")
    print(f"  content_sha256: {value(file_hash(target / 'requirement.md'))}")
    print("context:")
    print(f"  manifest_sha256: {value(file_hash(target / 'context-manifest.yaml'))}")
    print(f"  relative_tag: {value(latest_framework_tag(f'initiative/{initiative_id}/context'))}")
    print(f"  relative_content_sha256: {value(directory_hash(target / 'context' / 'relative'))}")
    print("  selected_packages:")
    for package, tag, commit in selected_context_packages(target / "context-manifest.yaml"):
        print(f"    - id: {value(package)}")
        print(f"      version_tag: {value(tag)}")
        print(f"      version_commit: {value(commit)}")
    print("design:")
    print(f"  hld_tag: {value(latest_framework_tag(f'initiative/{initiative_id}/hld'))}")
    print(f"  lld_tag: {value(latest_framework_tag(f'initiative/{initiative_id}/lld'))}")
    print("generation:")
    print("  hld_uses_this_baseline: true")
    print("  architecture_approval_required: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
