#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import hashlib
import re
import sys
from pathlib import Path


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def replace_first(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        fail(f"Could not update {label}")
    return updated


def main() -> int:
    if len(sys.argv) < 8:
        fail(
            "Usage: sync_initiative_approval.py <initiative-dir> <reviewer> <review-id> <submitted-at> <approved> <review-commit> <head-commit>"
        )

    initiative_dir = Path(sys.argv[1]).resolve()
    reviewer = sys.argv[2].strip() or "unknown"
    review_id = sys.argv[3].strip()
    submitted_at = sys.argv[4].strip() or dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    approved = sys.argv[5].strip().lower() == "true"
    review_commit = sys.argv[6].strip()
    head_commit = sys.argv[7].strip()

    initiative_yaml = initiative_dir / "initiative.yaml"
    initiative_md = initiative_dir / "initiative.md"
    requirement_md = initiative_dir / "requirement.md"
    approvals_yaml = initiative_dir / "approvals.yaml"

    for path in (initiative_yaml, initiative_md, requirement_md, approvals_yaml):
        if not path.exists():
            fail(f"Missing required file: {path}")

    def requirement_hash() -> str:
        digest = hashlib.sha256()
        digest.update(b"requirement.md\0")
        digest.update(requirement_md.read_bytes())
        relative = initiative_dir / "context" / "relative"
        if relative.is_dir():
            for path in sorted(item for item in relative.rglob("*") if item.is_file()):
                digest.update(b"\0")
                digest.update(str(path.relative_to(initiative_dir)).encode())
                digest.update(b"\0")
                digest.update(path.read_bytes())
        return digest.hexdigest()

    approvals_text = approvals_yaml.read_text()
    current_hash = requirement_hash()
    stored_hash_match = re.search(
        r"(?ms)^\s*- gate:\s*requirements\s*$.*?^\s+content_sha256:\s*\"?([^\"\n]+)",
        approvals_text,
    )
    stored_hash = stored_hash_match.group(1).strip() if stored_hash_match else ""
    requirements_approved = re.search(
        r"(?ms)^\s*- gate:\s*requirements\s*$.*?^\s+decision:\s*approved\s*$",
        approvals_text,
    )
    if requirements_approved and approved and review_commit and review_commit == head_commit and stored_hash == current_hash:
        print(f"Initiative {initiative_dir.name} is already approved; no sync needed")
        return 0

    if not approved or review_commit != head_commit:
        if not requirements_approved:
            print(f"Initiative {initiative_dir.name} remains pending; no valid current-head approval found")
            return 0
        yaml_text = initiative_yaml.read_text()
        yaml_text = replace_first(yaml_text, r"^(\s*status:\s*)[^\n]+$", r"\1draft", "initiative artifact status")
        initiative_yaml.write_text(yaml_text)
        md_text = initiative_md.read_text()
        md_text = replace_first(md_text, r"^(\s*-\s*Status:\s*)[^\n]+$", r"\1intake", "initiative markdown status")
        initiative_md.write_text(md_text)
        requirement_text = requirement_md.read_text()
        requirement_text = replace_first(requirement_text, r"^(\s*status:\s*)[^\n]+$", r"\1draft", "requirement artifact status")
        requirement_md.write_text(requirement_text)
        approvals_text = re.sub(
            r"(?ms)(^\s*- gate:\s*requirements\s*$.*?^\s+decision:\s*)approved(\s*$)",
            r"\1pending\2",
            approvals_text,
            count=1,
        )
        approvals_text = re.sub(
            r"(?ms)(^\s*- gate:\s*requirements\s*$.*?^\s+principal:\s*)[^\n]*",
            r'\1""', approvals_text, count=1,
        )
        approvals_text = re.sub(
            r"(?ms)(^\s*- gate:\s*requirements\s*$.*?^\s+content_sha256:\s*)[^\n]*",
            r'\1""', approvals_text, count=1,
        )
        approvals_text = re.sub(
            r"(?ms)(^\s*- gate:\s*requirements\s*$.*?^\s+timestamp:\s*)[^\n]*",
            r'\1""', approvals_text, count=1,
        )
        approvals_text = re.sub(
            r"(?ms)(^\s*- gate:\s*requirements\s*$.*?^\s+review_commit:\s*)[^\n]*",
            r'\1""', approvals_text, count=1,
        )
        approvals_yaml.write_text(approvals_text)
        print(f"Invalidated requirements approval for {initiative_dir.name}; a current-head human review is required")
        return 0

    yaml_text = initiative_yaml.read_text()
    yaml_text = replace_first(
        yaml_text,
        r"^(\s*status:\s*)[^\n]+$",
        r"\1approved",
        "initiative artifact status",
    )
    yaml_text = replace_first(
        yaml_text,
        r"^(\s*state:\s*)[^\n]+$",
        r"\1approved",
        "initiative workflow state",
    )
    initiative_yaml.write_text(yaml_text)

    md_text = initiative_md.read_text()
    md_text = replace_first(
        md_text,
        r"^(\s*-\s*Status:\s*)[^\n]+$",
        r"\1approved",
        "initiative markdown status",
    )
    initiative_md.write_text(md_text)

    requirement_text = requirement_md.read_text()
    requirement_text = replace_first(
        requirement_text,
        r"^(\s*status:\s*)[^\n]+$",
        r"\1approved",
        "requirement artifact status",
    )
    requirement_md.write_text(requirement_text)

    # The approved hash must represent the final approved requirement,
    # including its status metadata, not the draft bytes that existed before
    # this synchronization step.
    content_hash = requirement_hash()

    approvals_text = replace_first(
        approvals_text,
        r"^(\s*decision:\s*)pending$",
        r"\1approved",
        "approval decision",
    )
    approvals_text = replace_first(
        approvals_text,
        r"^(\s*principal:\s*).*$",
        f'\\1"{reviewer}"',
        "approval principal",
    )
    approvals_text = replace_first(
        approvals_text,
        r"^(\s*content_sha256:\s*).*$",
        f'\\1"{content_hash}"',
        "approval content hash",
    )
    approvals_text = replace_first(
        approvals_text,
        r"^(\s*timestamp:\s*).*$",
        f'\\1"{submitted_at}"',
        "approval timestamp",
    )
    if "review_commit:" in approvals_text:
        approvals_text = replace_first(
            approvals_text,
            r"^(\s*review_commit:\s*).*$",
            f'\\1"{review_commit}"',
            "review commit",
        )
    else:
        approvals_text = approvals_text.replace(
            f'    timestamp: "{submitted_at}"',
            f'    timestamp: "{submitted_at}"\n    review_commit: "{review_commit}"',
            1,
        )
    approvals_yaml.write_text(approvals_text)

    print(f"Updated approval state for {initiative_dir.name} -> approved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
