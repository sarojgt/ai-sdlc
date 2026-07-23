---
context_id: observability-principles
context_type: consistent
authority: platform-engineering-and-security
status: imported-snapshot
owner: platform-engineering
review_cadence: verify-against-observability-platform-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/PRO/pages/8878555246/Observability+Use+Case+How+do+we+integrate+Datadog+with+AWS
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/10152149027/Dispute+Portal+Monitoring+Observability
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/9979297796/Webhook+Observability
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/10107486292/DRAFT+Paymentology+Observability+Migration+Programme
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/10071408699/Grafana+Design+Doc+aws+gcp+observability
retrieved: 2026-07-22
---

# Observability Principles

Observability is a shared platform concern. New services should use the
approved telemetry libraries, collectors, tags, dashboards, monitors, and
retention policies rather than inventing a local monitoring stack.

## Minimum service standard

Every service should provide, as applicable:

- structured stdout logs with severity, service, environment, region, client
  or tenant-safe identifier, and correlation identifiers;
- metrics for traffic, errors, latency, saturation, dependency health, queue
  depth/lag, and business-critical outcomes;
- distributed traces using OpenTelemetry-compatible propagation;
- health/readiness endpoints and dependency health signals;
- dashboards and alerts mapped to an owner and an operational runbook;
- SLOs, alert thresholds, escalation, and rollback signals.

## Correlation and transaction traceability

Use the approved request and transaction identifiers consistently across API,
service, Kafka, webhook, database, and partner boundaries. Trace and span IDs
must correlate logs to APM traces. Payment processing flows should preserve the
approved transaction/RID identifiers without exposing sensitive card data.

## Platform direction

- Datadog and CloudWatch are established platform capabilities in the current
  technology context.
- OpenTelemetry-compatible tracing, Micrometer metrics, stdout logs, and
  Actuator health endpoints are reusable backend patterns.
- Observability migration work is moving toward a shared OpenTelemetry/Grafana
  Cloud model; designs must verify the current target before committing to a
  vendor-specific integration.
- Avoid duplicating the same logs and metrics across platforms without a clear
  investigation or compliance reason.

## Security and CHD guardrails

- Never send PAN, SAD, authentication headers, tokens, private keys, or raw
  production payloads to logs, traces, dashboards, or AI context.
- Apply field redaction and client/region-safe tagging before telemetry leaves
  a CHD boundary.
- HLDs must state what telemetry is generated in CHD, what is exported to
  common observability platforms, and what transformations occur.
- Alert and audit data must have an owner, retention policy, and access model.

## HLD requirements

Every HLD must define:

- golden signals and service-specific business metrics;
- trace propagation across synchronous and asynchronous boundaries;
- log schema and sensitive-field redaction;
- dashboards, alerts, SLOs, and runbooks;
- data retention and cost controls;
- CHD/common-zone telemetry flow;
- deployment health, rollback, and release verification signals.

## Sources

- [Observability with AWS and Datadog](https://paymentology.atlassian.net/wiki/spaces/PRO/pages/8878555246/Observability+Use+Case+How+do+we+integrate+Datadog+with+AWS)
- [Dispute Portal Observability](https://paymentology.atlassian.net/wiki/spaces/TS/pages/10152149027/Dispute+Portal+Monitoring+Observability)
- [Webhook Observability](https://paymentology.atlassian.net/wiki/spaces/TS/pages/9979297796/Webhook+Observability)
- [Observability Migration Programme](https://paymentology.atlassian.net/wiki/spaces/TS/pages/10107486292/DRAFT+Paymentology+Observability+Migration+Programme)
- [AWS/GCP Observability Design](https://paymentology.atlassian.net/wiki/spaces/TS/pages/10071408699/Grafana+Design+Doc+aws+gcp+observability)
