---
das_version: "0.1"
artifact:
  id: "HLD-{{ initiative.id }}"
  type: hld
  version: 1
  status: draft
  title: "{{ initiative.title }}"
  initiative: "{{ initiative.id }}"
  owner: "{{ roles.solution_architect }}"
  profile: "{{ hld.profile }}"
  change_size: ""
traceability:
  parents: ["REQ-{{ initiative.id }}"]
  satisfies: []
  impacts: []
design_baseline: "../evidence/design-baseline.yaml"
approvals:
  required: [architecture]
  records: []
policy:
  implementation_locked_until: architecture.approved
---

# Solution Design: {{ initiative.title }}

<!--
This is a section menu, not a checklist. Keep the final HLD short enough for a
human architecture review. Retain the required decision sections, add only
sections that affect this initiative, and remove unused guidance and empty
tables. Put substantial detail in a linked HLD part or LLD when needed.
-->

## 1. Motivation

<!-- REQUIRED: explain why the change is needed. -->

<!-- State the business or technical reason for the change and the intended outcome. -->

## 2. Authors & Approvals

<!-- Approval status is evidence only; architecture approval is human-owned. -->

| Role | Person or team | Status |
|---|---|---|
| Business Owner | | |
| Solution Architect / ARB | | Pending |
| Engineering Lead | | |
| Security | | |

## 3. Solution Overview

<!-- REQUIRED: summarise the recommended direction. -->

<!-- Summarise the recommended solution in one or two short paragraphs. -->

**Change size:** small / medium / large
**Impact summary:** affected services, repositories, integrations, data,
security, deployment, and migration impact in one concise line.

### Goals

<!-- Include when useful. -->

### Non-Goals

<!-- Include when useful. -->

## 4. High Level Business Requirements

<!-- Include the requirements that drive the architecture decision. Do not copy the full requirement. -->

| ID | Requirement | Acceptance signal |
|---|---|---|

## 5. Architecture Principles Applied

<!-- Reference approved principles and patterns only where they constrain this design. -->

| ID | Architecture Principle | Application to this design |
|---|---|---|

## 6. Non-Functional Requirements

<!-- Keep only applicable subsections and measurable targets. Do not invent values. -->

### Availability and Reliability

### Performance and Scalability

### Maintainability

### Observability

### Security and Compliance

### Data Quality

### Disaster Recovery

## 7. Assumptions

| ID | Assumption | Owner |
|---|---|---|

## 8. Risks

<!-- REQUIRED: state material risks, or explicitly state that none are known. -->

| ID | Risk | Impact | Mitigation / Owner |
|---|---|---|---|

## 9. Solution Design

<!-- REQUIRED: include only the design views needed to explain the decision. -->

<!--
Select only the views needed to explain the decision. Typical choices are
Context, High Level Architecture Diagram, Logical View, Information/Data View,
Physical/Deployment View, API and Integration Design, Event and Message Flow,
Component Model, Security Design, Networking Considerations, and Migration and
Rollout. Do not include every view by default.
-->

### Context

<!-- C4 Level 1: actors, system boundary, and major external interactions. -->

### High Level Architecture Diagram

<!-- Add a Mermaid diagram only when it clarifies a material decision. -->

## Context gaps

<!-- Keep one canonical register. Do not repeat these gaps elsewhere. -->

| Gap ID | Missing fact | Owner | Retrieval action | Blocks decision? |
|---|---|---|---|---|

### Logical View

### Information/Data View

<!-- Add ERD, data ownership, segregation, or lifecycle only when material. -->

### Physical/Deployment View

<!-- Include regions, environments, workload zones, and platform boundaries only when changed or relevant. -->

### Component Model

### API and Integration Design

### Event and Message Flow

### Security Design

### Networking Considerations

### Migration and Rollout

<!-- Remove unused subsections from the generated document. -->

## 10. Security Considerations

<!-- Include only initiative-specific security decisions and required review. -->

## 11. Testing Considerations

<!-- Summarise design-specific testing; detailed test cases belong in the LLD. -->

## 12. Operations Considerations

### Observability and Alerting

### Runbooks and Support

### Disaster Recovery

### RTO and RPO Requirements

### DR Strategy

## 13. Commercial View

<!-- Include only when cost, licensing, data volume, or capacity materially affects the decision. -->

### Data Volumes

### Cost Estimation

### Final Cost Estimation

## 14. Key Design Decisions

| ID | Design Aspect | Decision | Rationale | Status |
|---|---|---|---|---|

## 15. Open Items & Decisions Required

<!-- Include unresolved questions that do not belong in the context-gap register. -->

| ID | Item | Owner | Status |
|---|---|---|---|

## 16. Pending Items from ARB

<!-- Include only when ARB review is required or has outstanding items. -->

| ID | Item | Owner | Status |
|---|---|---|---|

## 17. Traceability

<!-- Link the requirement, context baseline, affected services, repositories, ADRs, and follow-on LLDs. -->

## Architecture Approval

Solution Architect / ARB: Pending
