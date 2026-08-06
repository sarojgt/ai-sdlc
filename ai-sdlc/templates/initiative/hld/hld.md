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
This file contains only the mandatory human-review core. Select relevant
optional sections from templates/initiative/hld/section-catalog.md, then remove
all template comments and empty placeholders. Put substantial detail in a
focused linked artifact or the LLD when needed.
-->

## 1. Motivation

<!-- REQUIRED: explain why the change is needed. -->

<!-- State the business or technical reason for the change and the intended outcome. -->

## 2. Solution Overview

<!-- REQUIRED: summarise the recommended direction. -->

<!-- Summarise the recommended solution in one or two short paragraphs. -->

**Change size:** small / medium / large
**Impact summary:** affected services, repositories, integrations, data,
security, deployment, and migration impact in one concise line.

## 3. Solution Design

<!-- REQUIRED: explain the recommended architecture at the level needed for the assessed impact. -->

<!-- Name evidenced services, repositories, APIs, data, integrations, and deployment boundaries. -->

## 4. Risks

<!-- REQUIRED: state material risks, or explicitly state that none are known. -->

| ID | Risk | Impact | Mitigation / Owner |
|---|---|---|---|

## 5. Context Gaps

<!-- Keep one canonical register. Do not repeat these gaps elsewhere. -->

| Gap ID | Missing fact | Owner | Retrieval action | Blocks decision? |
|---|---|---|---|---|

## Architecture Approval

Solution Architect / ARB: Pending
