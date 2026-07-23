---
das_version: "0.1"
artifact:
  id: "HLD-DEMO-004"
  type: hld
  version: 3
  status: draft
  title: "Client-scoped Banking.Live transaction status webhooks"
  initiative: "DEMO-004"
  owner: "team.solution-architecture"
traceability:
  parents: ["REQ-DEMO-004"]
  satisfies: ["REQ-DEMO-004-01", "REQ-DEMO-004-02", "REQ-DEMO-004-03", "REQ-DEMO-004-04"]
approvals:
  required: [architecture]
  records: []
policy:
  implementation_locked_until: architecture.approved
---

# HLD proposal: client-scoped Banking.Live transaction status webhooks

## Status, scope, and authority

This is a reviewable HLD proposal, not an approval. The human Solution
Architect owns the decision. It authorizes no LLD, implementation, merge, or
deployment.

The design covers status-event production, CHD sanitization, subscription
authorization, handoff to the shared Webhook Platform, delivery semantics,
observability, and BL2/Lume coexistence. It deliberately does not define
detailed API/event schemas, database schemas, IaC, code, or test cases.

## Evidence and confidence

Confirmed from `requirement.md`: the requirement is approved; eligible,
client-scoped status events must reach the shared Webhook Platform; subscription
management uses API Gateway, Auth0, and IMS; payloads exclude PAN, SAD, private
keys, tokens, and unrestricted production payloads; delivery is idempotent with
bounded recovery and shared observability.

Confirmed from the prepared context pack: enterprise event streaming and
webhooks are reuse-first capabilities; Auth0 authenticates, API Gateway
validates JWTs, and IMS authorizes client/region access; CHD and Common
Workload require an explicit, controlled flow; Lume is strategic while BL2
remains supported; environments and tiers may be shared or dedicated.

The context is an imported snapshot retrieved 2026-07-22 and must be checked
against platform owners before material design. No initiative-specific estate,
repository, runtime, rate, incident, dashboard, or runbook evidence is present.
Feedback contains only its README; no AI or human review was supplied.

Proposal assumptions: an authoritative BL2 or Lume boundary can expose a
durable status change; a governed event ingress and Webhook Platform exist;
event identity can be created at the authoritative boundary; and the client
endpoint supports the platform signing contract. These are gates, not facts.

## Proposed architecture

Use a minimal, schema-versioned, allow-listed status event. The authoritative
producer publishes it through the governed event boundary, or through an
approved durable outbox/adapter where direct BL2 publication is unavailable.
The shared Webhook Platform owns subscription lifecycle, tenant routing,
signing, delivery, timeout, bounded retries, DLQ, delivery history, and
authorized replay. Producers do not call client endpoints directly.

Subscription requests enter through the approved API Gateway route. Auth0
validates the principal and token; IMS resolves the client hierarchy, grant,
permission, and region. The request fails closed when the region or client
context cannot be authorized. For machine clients, use an approved Auth0
M2M/service identity and scoped audience; exact registration is open.

At-least-once delivery is the default. `event_id` is immutable and stable for
the domain event; each attempt has a separate attempt identity. The client
deduplicates by `event_id`. Ordering, correction events, retention, quotas,
latency SLO, and exact fields remain unresolved.

## Reuse and platform fit

| Capability | Searched context | Decision and owner |
|---|---|---|
| Event streaming | enterprise capabilities; event-streaming principles | Reuse governed Kafka/MSK pattern; producer owns topic/schema, Platform Engineering owns cluster |
| Webhooks | enterprise capabilities; webhook principles | Reuse shared subscriptions/orchestrator/delivery; Webhook Platform owns operation |
| API and identity | authentication/authorization; IMS/API Gateway | Reuse API Gateway, Auth0, IMS; identity/platform owners approve route and grants |
| Observability | observability principles | Reuse shared telemetry, dashboards, monitors, and runbooks; Platform Engineering owns standard |
| Persistence | BL estate and CHD/CW zones | No new store selected; any existing PayCore/outbox remains source-owned and requires classification |
| Client connectivity | Lume strategic/deployment context | Use the platform’s approved HTTPS/signing and, where applicable, mTLS direction; verify endpoint contract |

No local Kafka cluster, webhook engine, identity flow, or monitoring stack is
proposed. Option 2 is an adapter exception only when a BL2 capability gap is
confirmed, with a retirement owner and milestone.

## Boundaries and responsibilities

| Boundary | Responsibility | Data posture |
|---|---|---|
| BL2/Lume CHD source | Status semantics, eligible transitions, source identity, durable handoff | May contain CHD; keep in source zone |
| Sanitization boundary | Allow-list, token/reference mapping, redaction, safe correlation IDs | Only approved non-sensitive data crosses |
| Common Workload event/platform | Transport, schema governance, subscription, delivery, retry, DLQ, replay | No PAN/SAD/secrets/tokens/raw payloads |
| API/identity | Gateway exposure, Auth0 JWT validation, IMS client/region authorization | Audit without sensitive token/payload logging |
| Observability | Redacted logs, metrics, traces, alerts and runbooks | Transform before leaving CHD; retention/access to confirm |

The permitted flow is CHD source → authenticated sanitization/egress → Common
Workload platform. Bidirectional or direct source-to-client connectivity is not
assumed.

## Deployment and migration posture

The initiative spans `coexistence`: BL2 remains supported and Lume is the
target for new capability work. The current environment, cloud, region, tier,
version, and shared/dedicated model are unknown and must come from the current
environment catalog.

| Concern | Working boundary | Must be confirmed |
|---|---|---|
| BL2 Professional/shared | Shared source runtime/data may require client isolation and noisy-neighbor controls | Client cohort, region, source topology, release coordination |
| BL2 Enterprise/dedicated | Dedicated source resources may remain client-specific | Which compute, DB, network, HSM, DR are dedicated |
| Lume Professional | Shared compute/platform with dedicated logical client DB is the default direction | Regional hub, database isolation, event access |
| Lume Enterprise/Plus | Dedicated workload/data/middleware, with more shared or dedicated network/DR by tier | Commercial/compliance isolation and failover needs |
| Common platform | Shared event, Webhook, identity, telemetry with tenant isolation | Regional deployment, residency, quotas, platform SLO |

Migration is cohort-based: shadow/non-delivering validation, one client/region
cohort, evidence gates, then expansion. BL2 adapter use is time-bounded and
must have a retirement signal. Rollback disables new activation/consumption for
the affected cohort, preserves delivery state/DLQ for audit and recovery, and
does not alter the underlying transaction path. Re-enable a legacy sender only
after duplicate and identity behavior is proven.

## Quality attributes and trade-offs

| Dimension | HLD response |
|---|---|
| Security | Least-privilege service identities, JWT validation, IMS client/region checks, tenant isolation, encryption, managed signing rotation, fail-closed authorization, and redacted logs/DLQs |
| Performance | Asynchronous handoff isolates transactions; measure source-to-acceptance, queue age, and platform-to-client latency |
| Scalability | Independent event consumers and delivery workers; partition/order deliberately; per-client quotas and back-pressure prevent noisy neighbors |
| Cost | Reuse minimizes bespoke capability; event, delivery-history, DLQ, replay, and telemetry volume need a budget; adapter adds source capacity and lifecycle cost |
| Operations | Shared dashboards/alerts for throughput, errors, latency, lag, retries, DLQ age, replay, and reconciliation; named owners and runbooks required |
| Migration | One event contract supports BL2 and Lume cohorts; adapter is a compatibility bridge, not the target architecture |

Detailed option narratives and the comparison are in [Option 1](options/option-01.md)
and [Option 2](options/option-02.md). Risks and mitigations are in [risks.md](risks.md).

## Diagrams

- [Context: actors, trust boundaries, and CHD/Common Workload](diagrams/context.mmd)
- [C4 Level 1: system context](diagrams/c4-l1-context.mmd)
- [C4 Level 2: containers](diagrams/c4-l2-containers.mmd)
- [Deployment: environment, region, shared/dedicated, and runtime boundaries](diagrams/deployment.mmd)
- [Sequence: subscription and principal event flow](diagrams/sequence.mmd)

An ERD is intentionally omitted: no new database, durable store, or data
ownership boundary is selected by this HLD. If Option 2 uses an outbox or
journal, its schema and ownership must be designed and reviewed in the LLD.

## Review gates before LLD

1. Confirm authoritative producers, eligible statuses, ordering, correction
   semantics, event identity, rates, fan-out, and SLOs.
2. Confirm event schema, topic/ACL, retention, replay, DLQ, signing, quotas,
   regional routing, residency, and Webhook Platform onboarding contract.
3. Confirm API Gateway route, Auth0 issuer/audience/scopes and M2M identity,
   IMS permissions, cache/rate limits, audit, and failure behavior.
4. Classify every source, event, store, backup, cache, DLQ, log, trace, and
   support artifact as CHD/CW/unknown; obtain security approval for unknowns.
5. Inventory BL2/Lume cohorts, environment, region, tier, cloud, shared/
   dedicated resources, versions, owners, dashboards, runbooks, and rollback evidence.

## Open questions

1. Which BL component is authoritative for each eligible status, and can it publish durably?
2. What are status, ordering, correction, identity, retention, rate, fan-out, and latency requirements?
3. What are the platform contracts for ingress, signing, retry, DLQ, replay, regional routing, quotas, and SLOs?
4. Which API Gateway route, Auth0 application/audience/scopes, M2M identity, and IMS permissions apply per region?
5. Which fields and telemetry are approved, and what are residency, deletion, audit, and retention periods?
6. Which BL2/Lume cohorts, clouds, regions, tiers, versions, deployment repositories, and support owners are in scope?
7. Does BL2 require an outbox/adapter, and what is its retirement milestone?

## Concise summary

The conditional working direction is a sanitized, stable-identity status event
into the shared Webhook Platform, with API Gateway/Auth0/IMS authorization,
bounded recovery, and redacted observability. Option 1 is strategic; Option 2
is a controlled BL2 bridge. Estate and platform evidence plus Solution
Architect review are required before any LLD or implementation.

**Architecture approval: pending — human Solution Architect**
