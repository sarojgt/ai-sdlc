---
reviewer: codex
model: gpt-5.6-terra
iteration: 1
decision: escalate
---

# Independent HLD review — DEMO-004

## Blocking findings

1. **The architecture's essential source and event decisions are not evidenced.** The HLD makes the authoritative producer, eligible status transitions, durable handoff, stable event identity, ordering/correction semantics, and event fields explicit open questions. Those choices determine whether REQ-DEMO-004-01 and the idempotency acceptance criterion can be met; they cannot be selected safely from the available context.  
   **Affected sections:** `hld.md` — Evidence and confidence, Proposed architecture, Review gates before LLD, Open questions; `adr.md`; `risks.md` R-01 and R-05.  
   **Required change:** Banking.Live domain owners must provide the authoritative component(s), approved status catalogue, atomic/durable publication mechanism, event-identity rule, and correction/ordering semantics. Regenerate the HLD with those decisions traced to REQ-DEMO-004-01 and the idempotency acceptance criterion.

2. **The proposed CHD-to-Common Workload crossing is not sufficiently specified or approved.** The HLD introduces a sanitizer and an egress into the shared event platform, but does not identify the account/project, concrete ingress/egress control, protocol and allow-list, classification of the event and all persistence/telemetry surfaces, or the security evidence approving the crossing. The CHD/CW guardrail requires these details and security review when classification is unknown. This blocks validation of REQ-DEMO-004-04.  
   **Affected sections:** `hld.md` — Boundaries and responsibilities, Deployment and migration posture, Review gates before LLD; `diagrams/context.mmd`, `diagrams/c4-l2-containers.mmd`, and `diagrams/deployment.mmd`; `risks.md` R-02 and R-10.  
   **Required change:** Security and platform owners must confirm the zone/account-project mapping, data classification, allowed fields and safe correlation attributes, egress path and identity, and retention/access controls for the event, topic, DLQ, replay, logs, traces, caches, backups, and support artifacts. Regenerate the boundaries and diagrams from that evidence; retain only approved non-sensitive data outside CHD.

3. **The subscription authorization design lacks the required identity facts and downstream enforcement boundary.** It names API Gateway, Auth0, and IMS, but leaves the Auth0 tenant/application/organization, issuer, audience, scopes, principal types, regional IMS endpoint, permissions, service identity lifecycle, and the protected service's independent authorization enforcement undefined. The diagrams show the gateway storing a subscription in the platform without showing the latter enforcement. This leaves REQ-DEMO-004-03 and cross-client isolation unverified.  
   **Affected sections:** `hld.md` — Proposed architecture and Review gates before LLD; `diagrams/sequence.mmd`; `diagrams/c4-l1-context.mmd`; `diagrams/c4-l2-containers.mmd`; `risks.md` R-03 and R-04.  
   **Required change:** Identity and Webhook Platform owners must supply the approved public/client or service-to-service flow, concrete route, Auth0 and IMS registrations/permissions, regional resolution, token/secret/certificate lifecycle, audit/rate-limit/cache rules, and the Webhook subscription service's enforcement responsibility. Regenerate the authorization flow and failure behaviour accordingly.

4. **The review gate records conflict on whether the requirement was formally approved.** `requirement.md` states `status: approved` and records product-owner approval, while `approvals.yaml` records the requirements gate as `pending` with no principal, hash, or timestamp. This breaks approval traceability for the HLD parent artifact and requires a human record correction; an AI review must not choose which record governs.  
   **Affected sections:** approval and traceability metadata for `REQ-DEMO-004` and `HLD-DEMO-004`.  
   **Required change:** The authorized Product Owner/workflow owner must reconcile the requirements-gate record, including the reviewed artifact hash and timestamp, before progressing the HLD gate.

## Non-blocking findings

- The HLD appropriately reuses the shared Webhook Platform and governed event-streaming direction, keeps delivery at-least-once, avoids direct producer-to-client delivery, and preserves human architecture approval as pending.
- The reuse table names context sources and high-level owners, but does not identify the actual platform interfaces, repositories searched, or onboarding contacts. Add these once discovery evidence is available.
- Run evidence is internally inconsistent: `evidence/agent-response.yaml` reports the HLD run completed while `evidence/agent-run.yaml` remains `request-prepared`. Reconcile this for auditability.

## Recommendation

**Escalate to the Banking.Live domain, Security/Platform, Identity, Webhook Platform, and Product Owner/workflow owners.** Obtain and record the missing source-of-truth, cross-zone, authorization, and approval facts first; then regenerate the HLD for a bounded follow-up review. This review does not approve the architecture or unlock LLD work.
