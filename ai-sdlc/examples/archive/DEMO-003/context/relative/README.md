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

The AI context builder will combine this directory with shared context and
guardrails before invoking an agent.

## Initiative context

### Impacted capabilities

- Payment status processing
- Partner webhook delivery
- Operations and delivery observability

### Candidate repositories

- `payment-service`
- `partner-webhook-service`
- `platform-observability`

### Known constraints

- Webhook delivery must be idempotent.
- Retries must be bounded and recoverable through a dead-letter process.
- Payment credentials and sensitive authentication data must not be included in
  webhook payloads, logs, or operational evidence.
