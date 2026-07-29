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

prompt="Act as the Solution Architect HLD generation agent for initiative $initiative_id. Read the approved requirement.md, context-manifest.yaml, all relevant files under context/relative/, shared context under ../context/consistent/, guardrails under ../context/guardrails/, AGENTS.md, and evidence/design-baseline.yaml. Generate one concise, enterprise-quality HLD proposal in hld/hld.md. Assess change size, complexity/risk, affected services and repositories, APIs, data stores, events, jobs, infrastructure, channels, integrations, security, deployment, migration, operational impact, and governance. Use confirmed standards and approved patterns. Recommend the smallest compliant design. Include alternatives only for material trade-offs. Record missing facts as explicit CONTEXT GAPs with owners and retrieval actions; never present an unknown service, repository, table, cloud component, endpoint, SLA, retention rule, or integration as confirmed. Keep detailed API schemas, SQL, classes, test cases, migration scripts, and runbooks for the LLD. Preserve the exact design-baseline reference. Modify only HLD artifacts and generated evidence for this initiative. Do not approve architecture, create implementation code, create an LLD, merge, or deploy."
case "${AI_SDLC_HLD_PROFILE:-auto}" in
  auto) prompt="$prompt Use the auto profile: first classify the change as small, medium, or large. Set change_size in the HLD front matter to exactly one of those values, then apply that profile's level of detail. Allow enough detail for the actual impact; do not force a small design into a small document." ;;
  small) prompt="$prompt Use the small profile: keep hld.md concise and decision-focused. Include only material impact, confirmed context and gaps, recommendation, key risks, approval conditions, traceability, and at most two useful Mermaid diagrams. Omit obvious implementation detail and place any necessary deeper explanation in a linked supporting document." ;;
  medium) prompt="$prompt Use the medium profile: include material options, trade-offs, security, operations, rollout, and up to four useful Mermaid diagrams. Keep hld.md reviewable and move substantial detail into linked supporting documents." ;;
  large) prompt="$prompt Use the large profile: keep hld.md as a decision summary with useful diagrams and create linked detail documents for security, deployment, migration, options, or other depth that would make the main review difficult." ;;
esac

echo "[AI-SDLC] Starting GitHub Copilot generator: $model" >&2
echo "[AI-SDLC] Context loading and HLD analysis in progress..." >&2
python3 "$root/tooling/with_timeout.py" "${AI_SDLC_AGENT_TIMEOUT_SECONDS:-480}" \
  copilot --model "$model" --yolo --allow-tool=write --allow-tool='shell(git:*)' --no-ask-user -p "$prompt"

test -s "$target/hld/hld.md" || { echo "Copilot did not produce $target/hld/hld.md" >&2; exit 31; }
echo "[AI-SDLC] Copilot HLD generation completed." >&2
