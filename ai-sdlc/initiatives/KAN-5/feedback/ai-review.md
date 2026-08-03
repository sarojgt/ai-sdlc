---
reviewer: github-copilot
model: claude-haiku-4.5
iteration: 1
decision: pass
---

# Independent architecture review: KAN-5 HLD

## Review summary

The High-Level Design for KAN-5 (`hld/hld.md`) is a standards-compliant, concise architecture proposal that correctly addresses the approved requirement to add a temporary card-blocking API. The HLD is correctly classified as **Medium** change size with **High** complexity/risk, proportionate to extending an existing card-management API with time-bounded state and automatic restoration.

The design appropriately:
- Rejects creating a new service (Option C) and recommends extending existing capabilities (Option A)
- Identifies all missing enterprise facts as explicit, owned context gaps (CG-01 through CG-07)
- Provides complete requirement traceability without inventing implementation detail
- Includes comprehensive security, reliability, and operational guidance
- Preserves the HLD as a concise decision document, deferring schema, routes, and detailed procedures to the LLD phase

The HLD is ready for human Solution Architect or ARB review and approval before LLD generation.

## Findings

### Requirement coverage and traceability

The HLD provides complete coverage of all 8 functional requirements:

| Requirement | Coverage |
|---|---|
| **REQ-KAN-5-01** (API endpoint) | Section 6, Target approach: extends existing card-management API |
| **REQ-KAN-5-02** (Accept card ID and duration) | Section 6: domain validation occurs at authoritative state boundary |
| **REQ-KAN-5-03** (Validate authorization) | Section 6, diagram: gateway enforces authorization; BFF/service enforce client/region |
| **REQ-KAN-5-04** (Reject invalid/duplicate) | Section 6: validates duration, idempotency, and active-block absence |
| **REQ-KAN-5-05** (Reuse patterns) | Section 5, Option A recommendation: extend existing capability; no new service |
| **REQ-KAN-5-06** (Record metadata) | Section 6: retains requester, timestamps, correlation, expiry, restoration condition |
| **REQ-KAN-5-07** (Automatic expiry) | Section 6, expiry diagram: uses existing time-based mechanism with conditional restoration |
| **REQ-KAN-5-08** (Audit/observability) | Section 8: structured logging, telemetry, traces; PAN/SAD/secrets excluded |

### Classification and proportionality

- **Change size: Medium** ✓ Correct. One bounded API mutation plus time-lifecycle extension, reusing existing patterns; not a small isolated change, not a program-level or multi-service initiative.
- **Complexity/Risk: High** ✓ Correct. Incorrect restoration can affect card usability and customer experience; high security and compliance implications.
- **Profile fit (medium)** ✓ Appropriate. Sections 1-11 provide impact assessment, problem, scope, context gaps, reuse analysis, options, security/NFRs, delivery, risks, and traceability without excessive implementation detail.

### Context gaps and ownership

Seven context gaps are explicitly identified with owners and retrieval actions:

- **CG-01** (Card-state service and API owner): service catalog, repository, state-machine evidence
- **CG-02** (Product, Risk, Card, Identity owners): duration bounds, requester roles, policy evidence
- **CG-03** (Card platform and SRE owners): existing expiry capability and recovery runbook
- **CG-04** (Card platform owner): state-transition precedence and conflict rules
- **CG-05** (Card data, Security, Platform owners): CHD classification, zone, persistence, deployment evidence
- **CG-06** (Operations/SRE, Security owners): audit contract, telemetry, dashboards, SLOs, retention
- **CG-07** (Product, Card owners): notifications and external-integration requirements

Each gap is actionable and blocks specific LLD or release decisions. The HLD does not invent missing facts or assume deployment details.

### Impact assessment

Section 1 correctly assesses:

| Dimension | Assessment | Valid |
|---|---|---|
| Services/repositories | 2 logical capabilities; exact names unconfirmed (CG-01) | ✓ Honest |
| Integrations | 6 logical integration points (gateway, authz, card-state, audit, observability, API doc) | ✓ Comprehensive |
| Data/security | High impact; confidential card references, requester identity, client/region context; PCI/CHD classification unknown (CG-05) | ✓ High-risk |
| Runtime/deployment | Medium impact; reuses existing service deployment; expiry mechanism reliability unconfirmed (CG-03) | ✓ Appropriate |
| Migration | Low to medium; backward-compatible API addition; state-persistence impact unconfirmed (CG-05) | ✓ Reasonable |

### Options and trade-offs

Section 7 presents three options:

| Option | Decision | Rationale |
|---|---|---|
| **A: Extend existing capability with existing expiry** | **Recommended** | Minimizes surface, aligns with requirement, subject to CG-01–CG-06 |
| **B: Use enterprise event/scheduling fallback** | Conditional | Only if CG-03 confirms no supported expiry path; adds async complexity |
| **C: Create standalone card-control service** | Rejected | Violates reuse constraint; duplicates ownership and risk |

The decision is evidence-based and subject to appropriate gates.

### Security and compliance

Section 8 provides comprehensive guidance:

- **Authentication/Authorization**: HTTPS + existing Auth0/API Gateway/IMS path; no new roles (CG-02)
- **Data classification**: CHD/Common Workload classification deferred to CG-05; requires Security input
- **Safe logging**: Explicitly prohibits PAN, SAD, secrets, headers, full payloads; requires redaction policy confirmation
- **Retention and access**: Reuse existing card-data and audit-retention policies; no new privacy policy
- **Isolation**: Propagate and validate established client/region context; zone placement unknown (CG-05)

Guidance is specific and defers dangerous decisions to pre-LLD context gates, not to implementation.

### Diagrams and rendering

Three Mermaid diagrams are included:

1. **Sequence diagram (lines 139–157)**: Authorized actor → Gateway → Authorization → CardAPI → State → Audit path. Syntax valid; flow is accurate.
2. **Expiry flowchart (lines 159–168)**: Temporal block reaches expiry → existing mechanism → state check → conditional restoration → telemetry. Syntax valid; conditional restoration is critical.
3. **Security zone flowchart (lines 190–199)**: Portal → Gateway → Service → State → Persistence/Audit, with zone/region boundaries marked as unknown. Syntax valid; appropriately highlights missing data-flow evidence.

All diagrams are syntactically correct, render logically, and accurately depict the design without overconstaining implementation.

### Delivery and gates

Section 9 appropriately specifies:

- **Preconditions**: Resolve CG-01–CG-06; obtain Solution Architect approval before LLD
- **Contract**: Backward-compatible API addition; exact route/version deferred to LLD (CG-01)
- **Rollout**: Use existing service pipeline and release controls; no feature-flag platform proposed
- **Verification**: Confirm authorized creation, denial, expiry, preservation, auditability, telemetry, recovery
- **Rollback**: Disable new requests; do not bulk-remove active blocks without Risk/Operations authorization

Guidance is complete and acknowledges the high-risk nature of card-state rollback.

### Absence of over-specification

The HLD appropriately excludes:

- Specific API routes, versions, or JSON schemas (deferred to LLD)
- Database schema details or persistence implementation (deferred to CG-05 and LLD)
- Detailed scheduling implementation or retry algorithms (deferred to CG-03 and LLD)
- Test cases, runbooks, or migration scripts (LLD-phase work)
- Specific SLO values, thresholds, or on-call routing (Operations ownership; referenced in CG-06)

This restraint maintains the HLD as a decision document, not an LLD.

## Minor observations

1. **Duplication review**: Section 5 ("Reuse and platform fit") and Section 6 ("Target approach") have some overlapping prose about extending existing capability. This is appropriate for clarity given the high-risk nature, not duplication.

2. **Jira reference**: The traceability correctly links to the approved requirement at Section 11. The Jira URL in the requirement ("https://randomtry.atlassian.net/browse/KAN-5") is a placeholder; this is expected and not a defect.

3. **Context pack status**: The context manifest shows the context pack in draft with zero selected items and no relative context. This is flagged in the HLD (Section 5) as a CONTEXT GAP. Appropriate guidance for context assembly before LLD is present.

4. **Design baseline reference**: The HLD correctly preserves the exact design baseline at `../evidence/design-baseline.yaml` (line 98). Requirement approval hash matches current `requirement.md` SHA256.

## Conclusion

**Decision: PASS**

The HLD is standards-aligned, concise, traceable, and ready for human Solution Architect or ARB review and formal approval. It correctly:

- Classifies the change as Medium/High and applies proportional detail
- Addresses all 8 functional requirements without over-specification
- Identifies missing enterprise facts as explicit, owned context gaps that must be resolved before LLD
- Recommends reusing existing patterns in compliance with the requirement and reuse guardrails
- Provides complete security, reliability, and operational guidance with appropriate risk acknowledgment
- Maintains the HLD as a decision document, not an implementation blueprint
- Defers all implementation detail and dangerous decisions to pre-LLD context gates and the LLD phase

**Required next steps:**
1. Solution Architect or ARB reviews and formally approves (or provides feedback) on this HLD
2. Before LLD generation: resolve CG-01 through CG-07 with respective owners
3. If feedback is provided: bound any AI rerun to the specific feedback; do not regenerate the entire HLD

**Important note**: This is an independent AI architecture review, not a human approval. The HLD must receive formal approval from the designated Solution Architect or ARB before LLD generation, implementation, or deployment can proceed.
