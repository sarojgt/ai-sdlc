---
context_id: service-payapi
context_type: consistent
authority: service-catalog-and-repository-discovery
status: imported-snapshot
owner: banking-live-api-owners
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/7400423715/Teams+vs+BL+Services
  - https://paymentology.atlassian.net/wiki/spaces/TS/pages/10010918939/PECA-1056+-+Migrate+PayAPI+PayScheduler+Integration+from+DB+Socket+to+REST+API
  - https://github.com/Paymentology/payapi
retrieved: 2026-08-10
repository_commit: bbcc4ef
scan_scope: readme-build-source-database-deployment-observability
---

# PayAPI

## Service role

Banking.Live API/application boundary and integration surface. The service is
owned in the Confluence catalogue by Admin APIs & Portals.

## Business capability

PayAPI exposes Banking.Live business capabilities to portal, operations, and
integrating-service consumers. It translates approved API contracts into
domain actions, validates client and requester context, invokes the relevant
PayCore/PayTok/PayLog or partner path, and returns governed responses and
errors.

Typical business changes include new or changed client-facing endpoints,
card/account/payment operations, rule or decisioning actions, tokenization
flows, reporting/integration APIs, and API documentation. PayAPI is an
application boundary, not automatically the owner of every business record:
the HLD must identify the authoritative domain service, database, stored
procedure, event, or downstream API for each change.

Primary consumers include Atlas/portal BFFs, internal Banking.Live operations,
PayScheduler, PayControl, and other approved service integrations. Public and
internal access paths, client/region scope, authentication, authorization, and
data classification must be identified per capability.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/payapi](https://github.com/Paymentology/payapi) | confirmed | Primary service repository |

## Dependencies and boundaries

- Exposes and consumes approved APIs and platform integrations.
- Existing PayScheduler integration has been moving from direct PayCore writes
  and sockets to PayScheduler REST APIs.
- Reuse approved IMS/API Gateway, authentication, client-context, and
  observability patterns.

## Confirmed implementation map

Repository evidence identifies the existing card-status surface as a likely
extension point for card-state operations:

| Area | Confirmed evidence |
| --- | --- |
| Route family | `CardController` contains `/pws/pws_set_card_status/` and `/pcjs/pcjs_card_status_edit/` routes |
| Processing | `SetCardStatusProcessor` and `EditCardStatusProcessor` validate and authorize card-status changes |
| Data access | `CardDb` owns the card-status database calls and records API timing/log information |
| Database paths | Existing status changes call PayCore and PayTok stored procedures through separate connection pools |
| Authorization | Existing paths use client/session authorization or auth-code validation; exact actor/scopes remain feature-specific |
| Audit | `ApiLogDB` is used for request/response and outcome logging; safe-field policy remains mandatory |

## Rules and decisioning boundary

PayAPI is the API/action boundary for rule-related setup and integration. It
does not own transaction-time evaluation: PayPower performs evaluation during
authorization, while PayCore DB remains the persisted rule/procedure surface.
PayControl is the setup and operational configuration surface. Identify the
rule family and API action before selecting a repository or database change.

This is evidence for reuse, not a decision that every new card capability must
use an existing route.

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | Java 21 runtime image, Spring Boot, Apache Camel routes, Maven `uber-jar`, and Kubernetes Helm chart |
| Data stores | Separate PayCore, PayTok, PayLog, and PaySim PostgreSQL data sources are configured; read-select pools exist for Core, Tok, and Log |
| Database connectivity/pool | Hikari pools use tenant-aware/IAM-capable datasource construction; the scanned defaults use minimum idle 5, 10-minute idle timeout, 30-minute max lifetime, and 20-second leak detection; PayLog has a 5-second connection timeout and other pools use 10 seconds |
| Communication | Camel HTTP/API routes, REST integrations, JDBC/stored procedures, legacy socket-pool/ISO8583 support, HTTP clients, S3/GCS storage, and OpenAPI-generated API documentation |
| Internal dependencies | PayScheduler, PayCore, PayTok, PayLog, PaySim, IMS/API Gateway, client identity authorization, rule actions, Decision Engine admin client, and observability libraries |
| External dependencies | Feature-specific partner integrations require discovery |
| Security/observability | Spring Security, client identity verification, TLS/JKS secrets, NetworkPolicy, Actuator probes, OpenTelemetry, Datadog Java tracing, metrics, and structured API logs |

## Deployment and interface profile

| Area | Confirmed context |
| --- | --- |
| Container | Production image runs `/bl/app.jar`; local/prod targets expose application port 8080, health/Actuator port 8082, and telemetry/debug-related ports by deployment target |
| Health | Docker liveness uses `/actuator/health/liveness`; the chart provides Kubernetes probes and Gateway API/Ingress options |
| API documentation | Camel OpenAPI support is enabled; chart configuration uses an HTTPS API documentation host and `/ppws` base path pattern; environment values must be confirmed per deployment |
| Client identity | `X-Client-Id` is verified against request body/client context on configured paths; malformed or mismatched identity requests are rejected or handled according to the configured verification mode |
| Tenant routing | Core, Tok, Log, and PaySim datasource builders support IAM, region, multi-tenancy environment/workload, and tenant configuration |
| Deployment configuration | Helm controls image, service, Gateway API/Ingress, secrets, NetworkPolicy, probes, storage, and cloud-specific AWS/GCP database or object-storage settings |

## Repository scan evidence

The local scan covered README, Maven dependencies, Dockerfile, application
configuration, Helm values, Hikari datasource classes, API controllers, and
database-access classes. It confirms capability families but does not expose
environment secrets or production configuration values. The scan was pinned to
`bbcc4ef` on 2026-08-10.

## Scan-confirmed implementation anchors

- API ownership is split across general PayAPI controllers and feature areas
  such as transaction, card, PayCredit, tokenization, and 3DS integrations.
- Database access is represented by DAO/repository layers and stored-procedure
  calls rather than a single ORM-owned schema. A new data feature must identify
  the PayCore, PayTok, PayLog, or PaySim access path before design approval.
- The Helm chart is the deployment contract for service, Gateway API/Ingress,
  probes, NetworkPolicy, secrets, and database configuration.
- Scheduler-facing functionality has a REST integration path in addition to
  legacy integration code; new work should prefer the approved REST boundary
  after confirming the current contract.

These anchors were derived from the `bbcc4ef` source, configuration, and chart
scan. They guide repository selection but do not replace endpoint or schema
owner confirmation.

## Deployment context

Runs as part of the Banking.Live estate and is also a target service for Lume
and Kubernetes deployments. Confirm the active deployment model for each
initiative.

## HLD implications

Identify API contracts, authorization, client/tenant context, data access,
downstream services, deployment target, and backward compatibility.

## Context gaps

- Confirm the owning team and target branch for the affected feature.
- Confirm the exact route/version, actor permissions, request/response/error
  contract, idempotency, and gateway exposure.
- Confirm whether the feature uses PayCore, PayTok, both, or another store; name
  the stored procedure/table/function and read/write path.
- Confirm the effective pool, timeout, downstream integration, port, chart, and
  deployment repository from the affected branch/environment.
- Confirm whether the scanned `bbcc4ef` commit remains current before a
  material design; refresh this page when the service or chart changes.
