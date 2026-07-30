#!/usr/bin/env python3
"""Render versioned provider-neutral lifecycle prompts."""

from __future__ import annotations

import argparse
from pathlib import Path


PROFILE_INSTRUCTIONS = {
    "auto": "Use the profile selected by the preflight assessment and keep the main document proportionate; link substantial detail.",
    "small": "Include only material decisions, impact, context gaps, recommendation, risks, approval conditions, traceability, and at most two useful diagrams. Link deeper detail only when needed.",
    "medium": "Include material options, trade-offs, security, operations, rollout, and useful diagrams. Keep the main document reviewable and link substantial detail.",
    "large": "Keep hld.md as a decision summary and create linked supporting documents for security, deployment, migration, options, or other depth that would make the main review difficult.",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", choices=["hld-assessment", "hld-generation", "hld-review"])
    parser.add_argument("--initiative-id", required=True)
    parser.add_argument("--model", default="")
    parser.add_argument("--provider", default="")
    parser.add_argument("--iteration", default="1")
    parser.add_argument("--profile", default="auto")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    prompt_name = {"hld-assessment": "assessment", "hld-generation": "generation", "hld-review": "review"}[args.name]
    path = root / "prompts" / "hld" / f"{prompt_name}.md"
    text = path.read_text(encoding="utf-8")
    values = {
        "initiative_id": args.initiative_id,
        "model": args.model,
        "provider": args.provider,
        "iteration": args.iteration,
        "profile_instructions": PROFILE_INSTRUCTIONS.get(args.profile, PROFILE_INSTRUCTIONS["auto"]),
    }
    for key, value in values.items():
        text = text.replace("{{ " + key + " }}", value)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
