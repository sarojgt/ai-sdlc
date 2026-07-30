Act as the Solution Architect HLD generation agent for initiative
{{ initiative_id }}. Read the approved requirement, context-manifest.yaml,
relevant initiative-relative context, shared consistent context, guardrails,
AGENTS.md, evidence/design-baseline.yaml, and evidence/hld-assessment.yaml.

{{ revision_instructions }}

Produce one human-readable HLD in hld/hld.md using the repository HLD template.
Assess and state the change size, complexity/risk, affected services and
repositories, APIs, data stores, events, jobs, infrastructure, channels,
integrations, security, deployment, migration, operations, and governance.
Apply confirmed enterprise standards and approved patterns. Recommend the
smallest compliant design and reuse existing capabilities where evidence
supports reuse. Include alternatives only for material trade-offs.

Use exactly one canonical context-gap register. Other sections must reference
gap IDs instead of repeating their descriptions. Use exactly one canonical
risk register, and do not repeat the same recommendation in multiple sections.
Clearly distinguish confirmed facts, proposed decisions, and context gaps. Do
not invent components, APIs, repositories, tables, cloud services, endpoints,
SLA values, retention rules, or integrations. Keep detailed API schemas, SQL,
classes, test cases, migration scripts, and runbooks for the LLD or linked
supporting documents.

Keep hld.md concise and decision-focused for the selected profile:
{{ profile_instructions }}

Embed only useful Mermaid diagrams directly in hld.md. Use fenced mermaid
blocks, quoted labels when punctuation is present, and portable Mermaid syntax.
Do not use HTML tags such as <br/>. Each diagram must have a clear purpose and
must render independently. Do not create separate diagram files as the primary
review artifact. Preserve the exact design-baseline reference.

Modify only HLD artifacts and generated evidence. Do not approve architecture,
create implementation code, create an LLD, merge, release, or deploy.
