#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <initiative-id> <model>" >&2
  exit 2
fi

initiative_id="$1"
model="$2"
root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$root/initiatives/$initiative_id"

test -d "$target" || { echo "Unknown initiative: $initiative_id" >&2; exit 1; }
command -v copilot >/dev/null 2>&1 || { echo "GitHub Copilot CLI was not found on PATH." >&2; exit 30; }

prompt="Act as the Solution Architect HLD generation agent for initiative $initiative_id. Read the approved requirement.md, context-manifest.yaml, all relevant files under context/relative/, shared context under ../context/consistent/, guardrails under ../context/guardrails/, AGENTS.md, and evidence/design-baseline.yaml. Generate a concise, enterprise-quality HLD proposal in hld/hld.md and supporting HLD Markdown artifacts required by the repository templates. Assess change size, complexity/risk, affected services and repositories, APIs, data stores, events, jobs, infrastructure, channels, integrations, security, deployment, migration, operational impact, and governance. Use confirmed standards and approved patterns. Recommend the smallest compliant design. Include only meaningful alternatives and trade-offs. Include useful Mermaid diagrams directly in hld/hld.md when applicable, including context, C4, deployment, sequence, component, or ERD views. Record missing facts as explicit CONTEXT GAPs with owners and retrieval actions; do not invent enterprise components or silently treat assumptions as facts. Keep implementation details for the LLD. Preserve the exact design-baseline reference. Modify only HLD artifacts and generated evidence for this initiative. Do not approve architecture, create implementation code, create an LLD, merge, or deploy."

echo "[AI-SDLC] Starting GitHub Copilot generator: $model" >&2
echo "[AI-SDLC] Context loading and HLD analysis in progress..." >&2
copilot --model "$model" --yolo --allow-tool=write --allow-tool='shell(git:*)' --no-ask-user -p "$prompt"

test -s "$target/hld/hld.md" || { echo "Copilot did not produce $target/hld/hld.md" >&2; exit 31; }
echo "[AI-SDLC] Copilot HLD generation completed." >&2
