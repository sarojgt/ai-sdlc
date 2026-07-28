#!/usr/bin/env python3
from __future__ import annotations

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


def hld_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def update_gate(text: str, decision: str, principal: str, content_hash: str, timestamp: str, review_commit: str) -> str:
    block = r"(?ms)(^\s*- gate:\s*hld\s*$.*?)(?=^\s*- gate:|\Z)"
    match = re.search(block, text)
    if not match:
        fail("HLD approval record is missing")
    current = match.group(1)
    current = replace_first(current, r"^(\s*decision:\s*)[^\n]+$", rf"\1{decision}", "HLD decision")
    current = replace_first(current, r"^(\s*principal:\s*).*$", f'\\1"{principal}"', "HLD principal")
    current = replace_first(current, r"^(\s*content_sha256:\s*).*$", f'\\1"{content_hash}"', "HLD content hash")
    current = replace_first(current, r"^(\s*timestamp:\s*).*$", f'\\1"{timestamp}"', "HLD timestamp")
    if "review_commit:" in current:
        current = replace_first(current, r"^(\s*review_commit:\s*).*$", f'\\1"{review_commit}"', "HLD review commit")
    else:
        current = current.rstrip("\n") + f'\n    review_commit: "{review_commit}"\n'
    return text[: match.start(1)] + current + text[match.end(1) :]


def main() -> int:
    if len(sys.argv) != 8:
        fail(
            "Usage: sync_hld_approval.py <initiative-dir> <reviewer> <review-id> "
            "<submitted-at> <approved> <review-commit> <head-commit>"
        )

    initiative_dir = Path(sys.argv[1]).resolve()
    reviewer = sys.argv[2].strip()
    submitted_at = sys.argv[4].strip()
    approved = sys.argv[5].strip().lower() == "true"
    review_commit = sys.argv[6].strip()
    head_commit = sys.argv[7].strip()

    initiative_yaml = initiative_dir / "initiative.yaml"
    approvals_yaml = initiative_dir / "approvals.yaml"
    hld_md = initiative_dir / "hld" / "hld.md"
    for path in (initiative_yaml, approvals_yaml, hld_md):
        if not path.exists():
            fail(f"Missing required HLD approval file: {path}")

    approvals_text = approvals_yaml.read_text()
    hld_approved = re.search(
        r"(?ms)^\s*- gate:\s*hld\s*$.*?^\s+decision:\s*approved\s*$", approvals_text
    )
    valid = approved and review_commit and review_commit == head_commit
    if not valid:
        if not hld_approved:
            print(f"Initiative {initiative_dir.name} HLD remains pending; no current-head architect approval found")
            return 0
        approvals_yaml.write_text(update_gate(approvals_text, "pending", "", "", "", ""))
        hld_text = hld_md.read_text()
        hld_text = replace_first(hld_text, r"^(\s*status:\s*)[^\n]+$", r"\1draft", "HLD status")
        hld_text = replace_first(hld_text, r"^(Solution Architect / ARB:\s*).*$", r"\1pending", "HLD approval text")
        hld_md.write_text(hld_text)
        yaml_text = initiative_yaml.read_text()
        yaml_text = replace_first(yaml_text, r"^(\s*state:\s*)[^\n]+$", r"\1hld_review", "initiative workflow state")
        initiative_yaml.write_text(yaml_text)
        print(f"Invalidated HLD approval for {initiative_dir.name}; a current-head architect review is required")
        return 0

    content_hash = hld_hash(hld_md)
    approvals_yaml.write_text(update_gate(approvals_text, "approved", reviewer, content_hash, submitted_at, review_commit))
    hld_text = hld_md.read_text()
    hld_text = replace_first(hld_text, r"^(\s*status:\s*)[^\n]+$", r"\1approved", "HLD status")
    hld_text = replace_first(hld_text, r"^(Solution Architect / ARB:\s*).*$", rf"\1{reviewer}", "HLD approval text")
    hld_md.write_text(hld_text)
    yaml_text = initiative_yaml.read_text()
    yaml_text = replace_first(yaml_text, r"^(\s*state:\s*)[^\n]+$", r"\1hld_approved", "initiative workflow state")
    initiative_yaml.write_text(yaml_text)
    print(f"Updated HLD approval state for {initiative_dir.name} -> approved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
