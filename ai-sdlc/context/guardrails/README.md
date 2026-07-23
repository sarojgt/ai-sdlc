# AI Guardrails

Guardrails constrain AI proposals and actions. They are separate from
ordinary context and must be enforced by validators, workflow gates, and CI.

Add Markdown policies here, for example:

- Security and data-classification rules
- Prohibited architecture patterns
- Mandatory enterprise patterns
- Coding and testing standards
- Approval and deployment restrictions

Current imported guardrails include secure logging/data classification and
architecture review governance. Confluence remains the upstream authority;
repository changes are the reviewed AI working set.

Agents must never approve requirements, approve architecture, merge protected
branches, or deploy production.
