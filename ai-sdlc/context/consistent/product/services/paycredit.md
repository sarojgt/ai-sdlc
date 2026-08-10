---
context_id: service-paycredit
context_type: consistent
authority: service-catalog-and-repository-discovery
status: imported-snapshot
owner: paycredit-product-and-engineering
review_cadence: verify-against-repository-and-service-catalog-before-material-design
sources:
  - https://github.com/Paymentology/paycredit
  - https://github.com/Paymentology/paycredit-ui
  - https://github.com/Paymentology/paycredit-test-automation
retrieved: 2026-08-10
repository_commit: d7bde9c
scan_scope: readme-build-source-service-database-messaging-deployment
---

# PayCredit

## Service role

PayCredit product capability and its client-facing application surfaces. The
existing PayCredit product context remains the domain source; this page adds
repository discovery metadata.

## Business capability

PayCredit provides credit-product capabilities including revolving credit,
instalment loans, delinquency, rewards, hardship, monitoring, reports, taxes,
and Banking.Live integration. It is a multi-service product estate; an
initiative must identify the bounded service, BFF, data store, and client
surface rather than changing the root repository by default.

## Repository map

| Repository | Status | Use |
| --- | --- | --- |
| [Paymentology/paycredit](https://github.com/Paymentology/paycredit) | confirmed | Primary PayCredit service/application |
| [Paymentology/paycredit-ui](https://github.com/Paymentology/paycredit-ui) | confirmed | PayCredit UI |
| [Paymentology/paycredit-test-automation](https://github.com/Paymentology/paycredit-test-automation) | confirmed | Test automation |
| [Paymentology/paycredit-team-shared-resources](https://github.com/Paymentology/paycredit-team-shared-resources) | confirmed | Team-shared resources |

## Dependencies and boundaries

Confirm client-facing exposure, identity, APIs, data classification, and
integration with Banking.Live or Atlas before selecting a repository.

## Technical profile

| Area | Confirmed context |
| --- | --- |
| Runtime | Java 21+, Maven, Spring Boot microservices with DevTools |
| Data stores | PostgreSQL databases for credit, delinquency, instalment loans, monitoring, rewards, and taxes |
| Database connectivity/pool | Spring datasource configuration; exact pool values require service configuration discovery |
| Communication | Feign HTTP clients between services; Kafka messaging; actuator and Swagger HTTP endpoints |
| Internal dependencies | Revolving Credit, Fast Orchestration, Lidia, BFF, BL Integration, Instalment Loan, Monitoring, Reward, Delinquency, Reports, Taxes, and Hardship services |
| External/platform dependencies | Valkey/Redis cache, LocalStack/S3-compatible storage, Kafka, and Banking.Live integration |
| Security/observability | Service authentication, credentials, health/info endpoints, logs, metrics, traces, and data classification require environment confirmation |

## Deployment context

Confirm whether the initiative targets a public portal, internal portal, Lume,
or a dedicated/shared client deployment.

## HLD implications

Identify product boundary, UI/API repositories, client context, data stores,
security, deployment, and test ownership.

## Scan-confirmed delivery profile

The local scan confirms a Java 21/Spring Boot multi-module build, separate
service health endpoints, PostgreSQL data domains, Feign HTTP clients, Kafka,
Valkey/Redis, S3-compatible storage, and Helm routes/timeouts. Exact
service-to-database ownership is feature-specific.

## Context gaps

- Confirm which PayCredit repositories are production-owned versus supporting
  or experimental.
