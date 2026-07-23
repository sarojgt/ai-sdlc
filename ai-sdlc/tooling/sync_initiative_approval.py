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
    if len(sys.argv) < 5:
        fail(
            "Usage: sync_initiative_approval.py <initiative-dir> <reviewer> <review-id> <submitted-at>"
        )

    initiative_dir = Path(sys.argv[1]).resolve()
    reviewer = sys.argv[2].strip() or "unknown"
    review_id = sys.argv[3].strip()
    submitted_at = sys.argv[4].strip() or dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    initiative_yaml = initiative_dir / "initiative.yaml"
    initiative_md = initiative_dir / "initiative.md"
    approvals_yaml = initiative_dir / "approvals.yaml"

    for path in (initiative_yaml, initiative_md, approvals_yaml):
        if not path.exists():
            fail(f"Missing required file: {path}")

    content_hash = hashlib.sha256(initiative_yaml.read_bytes()).hexdigest()

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

    approvals_text = approvals_yaml.read_text()
    decision = re.search(r"^\s*decision:\s*([^\s]+)\s*$", approvals_text, flags=re.MULTILINE)
    if decision and decision.group(1) == "approved":
        print(f"Approval state for {initiative_dir.name} is already approved")
        return 0

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
    approvals_yaml.write_text(approvals_text)

    print(f"Updated approval state for {initiative_dir.name} -> approved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
