# Use Bash so recipes work on macOS, Linux, and GitHub-hosted Ubuntu runners.
set shell := ["bash", "-cu"]

default:
    @just --list

# Create a new initiative instance from the reusable templates.
ai-sdlc-init id title business_outcome problem_statement owner="team.example" work_item="" risk_tier="medium" data_classification="internal" profile="intake":
    ./ai-sdlc/tooling/bootstrap_initiative.sh "{{id}}" "{{title}}" "{{business_outcome}}" "{{problem_statement}}" "{{owner}}" "{{work_item}}" "{{risk_tier}}" "{{data_classification}}" "{{profile}}"

# Interactively collect a requirement and create a new initiative instance.
ai-sdlc-new:
    ./ai-sdlc/tooling/new_initiative.sh

# Expand an approved intake into the reusable boilerplate scaffold.
ai-sdlc-expand initiative:
    python3 ./ai-sdlc/tooling/expand_initiative.py "ai-sdlc/initiatives/{{initiative}}"

# Show the latest framework, initiative, design, and context versions.
ai-sdlc-version-view:
    python3 ./ai-sdlc/tooling/version_matrix.py

# Show the requirement for human Product Owner review.
ai-sdlc-review-requirement initiative:
    @echo "Review requirement: ai-sdlc/initiatives/{{initiative}}/requirement.md"
    @echo "A human Product Owner must set the artifact status to approved and record approval before HLD generation."

# Run one registered skill through its provider adapter.
ai-sdlc-skill skill initiative provider="codex" model="gpt-5.6-luna":
    ./ai-sdlc/tooling/run_skill.sh "{{skill}}" "{{initiative}}" "{{provider}}" "{{model}}"

# Generate an HLD and run the bounded AI review loop.
# The generator and reviewer remain independently selectable.
ai-sdlc-hld initiative generator_provider="codex" generator_model="gpt-5.6-luna" reviewer_provider="codex" reviewer_model="gpt-5.6-terra":
    ./ai-sdlc/tooling/hld_loop.sh "{{initiative}}" "{{generator_provider}}" "{{generator_model}}" "{{reviewer_provider}}" "{{reviewer_model}}"

# Explicit name for the bounded HLD review loop.
ai-sdlc-hld-loop initiative generator_provider="codex" generator_model="gpt-5.6-luna" reviewer_provider="codex" reviewer_model="gpt-5.6-terra":
    ./ai-sdlc/tooling/hld_loop.sh "{{initiative}}" "{{generator_provider}}" "{{generator_model}}" "{{reviewer_provider}}" "{{reviewer_model}}"

# Capture architect feedback and prepare a bounded HLD rerun.
ai-sdlc-hld-feedback initiative agent="codex" model="gpt-5.6-luna":
    ./ai-sdlc/tooling/hld_feedback.sh "{{initiative}}" "{{agent}}" "{{model}}"

# Validate one initiative instance.
ai-sdlc-validate initiative:
    ./ai-sdlc/tooling/validate_structure.sh "{{initiative}}"

# Validate every generated initiative instance.
ai-sdlc-validate-all:
    for initiative in ai-sdlc/initiatives/*; do \
        if [ -d "$initiative" ]; then \
            ./ai-sdlc/tooling/validate_structure.sh "$initiative"; \
        fi; \
    done

# Show the reusable AI-SDLC framework structure.
ai-sdlc-tree:
    find ai-sdlc -type f | awk -F/ 'NF <= 4' | sort

# Show the current initiative lifecycle documentation.
ai-sdlc-docs:
    @echo "Research: docs/ai-native-sdlc-research.md"
    @echo "Adoption: docs/adoption-and-poc-plan.md"
    @echo "Automation: docs/automation-and-gates.md"
    @echo "Reusable model: ai-sdlc/design/reusable-template-model.md"
    @echo "HLD runbook: ai-sdlc/design/hld-generation-runbook.md"
