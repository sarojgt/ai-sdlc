#!/usr/bin/env python3
"""Resolve a safe HLD profile from assessment metadata or an existing HLD."""
import re
import sys
from pathlib import Path

VALID = {"small", "medium", "large"}

def value(text: str, key: str):
    match = re.search(rf"^\s*{re.escape(key)}\s*:\s*[\"']?([^\"'\n#]+)", text, re.I | re.M)
    return match.group(1).strip().lower() if match else None

def existing_hld_profile(text: str):
    patterns = (
        r"^\s*change_size\s*:\s*[\"']?(small|medium|large)\b",
        r"^\s*recommended_profile\s*:\s*[\"']?(small|medium|large)\b",
        r"change\s*size\s*[:|]\s*[\"']?(small|medium|large)\b",
        r"\*\*change\s+size\*\*\s*[:|]\s*[\"']?(small|medium|large)\b",
    )
    for pattern in patterns:
        match = re.search(pattern, text, re.I | re.M)
        if match:
            return match.group(1).lower()
    return None

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: resolve_hld_profile.py <initiative-directory>")
    target = Path(sys.argv[1])
    assessment = target / "evidence" / "hld-assessment.yaml"
    hld = target / "hld" / "hld.md"
    profile = None
    if assessment.exists():
        text = assessment.read_text(encoding="utf-8")
        profile = value(text, "recommended_profile") or value(text, "change_size")
    if profile not in VALID and hld.exists():
        profile = existing_hld_profile(hld.read_text(encoding="utf-8"))
    if profile not in VALID:
        raise SystemExit("assessment did not contain recommended_profile: small, medium, or large")
    print(profile)

if __name__ == "__main__":
    main()
