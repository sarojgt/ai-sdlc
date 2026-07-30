#!/usr/bin/env python3
"""Validate the approval evidence required to enter a lifecycle stage."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path


def front_matter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, flags=re.S)
    if not match:
        raise ValueError(f"Missing YAML front matter: {path}")
    return match.group(1)


def value(text: str, name: str) -> str:
    match = re.search(rf"^\s*{re.escape(name)}:\s*[\"']?([^\"'\n#]+)", text, re.M)
    return match.group(1).strip() if match else ""


def approval_block(text: str, gate: str) -> str:
    match = re.search(rf"(?ms)^\s*- gate:\s*{re.escape(gate)}\s*$.*?(?=^\s*- gate:|\Z)", text)
    if not match:
        raise ValueError(f"Missing {gate} approval record")
    return match.group(0)


def requirement_hash(initiative: Path) -> str:
    digest = hashlib.sha256()
    requirement = initiative / "requirement.md"
    digest.update(b"requirement.md\0")
    digest.update(requirement.read_bytes())
    relative = initiative / "context" / "relative"
    if relative.is_dir():
        for path in sorted(item for item in relative.rglob("*") if item.is_file()):
            digest.update(b"\0")
            digest.update(str(path.relative_to(initiative)).encode())
            digest.update(b"\0")
            digest.update(path.read_bytes())
    return digest.hexdigest()


def hld_hash(initiative: Path) -> str:
    return hashlib.sha256((initiative / "hld" / "hld.md").read_bytes()).hexdigest()


def require_gate(initiative: Path, gate: str) -> None:
    approvals = initiative / "approvals.yaml"
    artifact = initiative / ("requirement.md" if gate == "requirements" else "hld/hld.md")
    if not approvals.exists() or not artifact.exists():
        raise ValueError(f"{gate} gate requires {approvals.name} and {artifact.relative_to(initiative)}")

    if value(front_matter(artifact), "status") != "approved":
        raise ValueError(f"{gate} artifact is not approved")

    record = approval_block(approvals.read_text(encoding="utf-8"), gate)
    if value(record, "decision") != "approved":
        raise ValueError(f"{gate} approval decision is not approved")
    if not value(record, "principal") or not value(record, "review_commit"):
        raise ValueError(f"{gate} approval record is incomplete")

    expected_hash = requirement_hash(initiative) if gate == "requirements" else hld_hash(initiative)
    if value(record, "content_sha256") != expected_hash:
        raise ValueError(f"{gate} approval content hash does not match the current artifact")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("gate", choices=["requirements", "hld"])
    parser.add_argument("initiative_dir", type=Path)
    args = parser.parse_args()
    try:
        require_gate(args.initiative_dir.resolve(), args.gate)
    except (OSError, ValueError) as error:
        print(f"Lifecycle gate blocked: {error}", file=sys.stderr)
        return 10
    print(f"Lifecycle gate passed: {args.gate}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
