# Relative Context

This directory contains information specific to this initiative. Add only
context needed to understand and design the change.

Examples:

- Current-state architecture
- Impacted services and repositories
- Existing APIs and events
- Relevant ADRs
- Runtime or deployment evidence
- Initiative-specific constraints
- Business or regional details not covered by shared context

The requirement remains at the initiative root:

```text
../requirement.md
```

## Initial initiative context

### Impacted capabilities

- Payment status processing
- Customer notification delivery

### Candidate repositories

- `payment-service`
- `notification-service`

### Known design constraint

The notification path must be idempotent and must not expose payment
credentials or sensitive authentication data.

### Context status

This is a small demonstration context. In a real initiative, the team would
add current-state diagrams, API contracts, relevant ADRs, and repository links
before requesting HLD generation.

The AI context builder will combine this directory with shared context and
guardrails before invoking an agent.
