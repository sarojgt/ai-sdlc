---
context_id: paymentology-tech-radar
context_type: consistent
authority: engineering-and-platform-governance
status: imported-snapshot
owner: engineering-platform-and-architecture
review_cadence: refresh-before-material-technology-decision
source: https://github.com/Paymentology/tech-radar/blob/main/data.json
source_commit: ea130ee129a5c5bfb50d16d7afa82c7733f80fc2
retrieved: 2026-07-22
---

# Paymentology Technology Radar

This is a curated snapshot of `Paymentology/tech-radar/data.json`. Use the
ring as a technology-selection signal, not as a substitute for architecture,
security, platform, or product approval.

## Ring meanings

| Ring | Meaning for HLD generation |
| --- | --- |
| Adopt | Preferred default when it satisfies the requirement and platform constraints. |
| Trial | Suitable for a bounded experiment or limited production use with an owner and success criteria. |
| Assess | Requires investigation, evidence, and human review before material adoption. |
| Hold | Avoid for new work; use only for existing systems or an explicitly documented exception. |

## Adopt: languages and frameworks

- Java 21 with Spring Boot 4.0.1 for backend services.
- JavaScript, TypeScript 5.8.3, and React 19.1.0 for web applications.
- Erlang 27 for approved or existing concurrency-oriented use cases.
- SQL for structured data access.

Java 17, Java 14, Rust, C++, ColdFusion, legacy Java/Maven combinations,
WildFly, and related legacy application-server choices are marked Hold or
limited to existing use cases. Kotlin 1.9.20, Elixir 1.15, Python, and Apache
Spark are marked Assess, with Python and Spark limited to data-engineering
contexts.

## Adopt: cloud and runtime platforms

- AWS and GCP are adopted cloud platforms.
- Kubernetes and AWS EKS are adopted container-orchestration choices.
- AWS RDS Aurora PostgreSQL is the adopted relational database platform.
- AWS ElastiCache, AWS IAM, AWS S3, AWS API Gateway, AWS Lambda, AWS WAF, and
  Datadog are adopted platform capabilities where their scope fits.
- Auth0 and ZeroTouch PKI are adopted identity and certificate-management
  capabilities.
- NGINX is the adopted web-server choice.

Google GKE and Google Cloud Managed Service for Apache Kafka are marked
Assess. Azure and OCI are marked Hold in the radar, although other platform
context may permit regional, legacy, or contractual exceptions. Such an
exception must be explicit in the HLD.

Standalone PostgreSQL 16.6 is marked Hold while AWS RDS Aurora PostgreSQL is
marked Adopt. Designs must therefore distinguish the approved managed
platform choice from an existing or exceptional standalone database use case.

## Adopt: messaging, data, and integration

- Kafka for streaming and asynchronous messaging.
- AWS MSK for Kafka management in AWS.
- HTTPS/JSON for real-time HTTP messaging.
- Liquibase for database schema versioning and change management.
- Terraform for infrastructure and application configuration.
- Helm for Kubernetes packaging.

Google Cloud Managed Kafka is Assess. AWS SNS is Hold for new portable or
multi-cloud workloads because the radar identifies limited portability; use it
only when an AWS-specific decision is justified.

## Adopt: engineering and delivery tools

- GitHub and GitHub Actions with GitHub Runners.
- Gradle 9.3.1; Maven is Hold for new work.
- JFrog Platform, including Artifactory and Xray.
- SonarQube Cloud, Checkov, Checkstyle, JUnit 5, and Mockito.
- Renovate for automated dependency updates.
- IntelliJ as an adopted IDE.

## Adopt: operations and security

- Datadog and AWS CloudWatch for monitoring and observability.
- AWS IAM for identity and access management.
- Auth0 for identity-provider capability.
- ZeroTouch PKI for certificate and PKI services.
- AWS WAF and Palo Alto for network/application protection.
- HashiCorp Vault for identity-based secrets and encryption management.

Grafana and Grafana Loki are Trial. PagerDuty, PRTG, and FusionReactor are
Hold or limited to existing use cases.

## Adopt and evaluate: AI tooling

- OpenAI, Codex, GitHub Copilot, ChatGPT, Microsoft Copilot Chat, AWS Bedrock,
  PayAI, and Inkeep are marked Adopt in the source radar for their listed use
  cases.
- Cursor is Trial.
- Windsurf is Hold pending security review.

The radar status does not remove the AI SDLC governance requirements. AI tools
must still use approved context, follow guardrails, produce evidence, and stop
at human approval gates.

## Adopt: architecture techniques

The radar lists the following techniques as Adopt:

- Cloud Strategy principles.
- Event Streaming principles.
- Adapter Pattern principles.
- Core Database principles.
- Reference Data definition and architecture.
- Microfrontend architecture principles.

The corresponding Confluence or architecture-space documents should be added
to the context pack when an initiative is affected by the technique.

## HLD decision rules

Every technology choice in an HLD should include:

1. The Tech Radar ring at the time of design.
2. Why the technology fits the requirement and target platform.
3. Alternatives considered, especially when the choice is Trial or Assess.
4. A documented exception and owner when the choice is Hold.
5. Portability, regional, security, operational, and cost implications.
6. The evidence needed before LLD or implementation.

The HLD agent must not upgrade an Assess, Trial, or Hold technology to Adopt by
itself.

## Source and refresh

[Paymentology Tech Radar data.json](https://github.com/Paymentology/tech-radar/blob/main/data.json)

This snapshot was retrieved from the `main` branch at commit
`ea130ee129a5c5bfb50d16d7afa82c7733f80fc2`. Refresh it before a material
technology decision or when the source repository changes.
