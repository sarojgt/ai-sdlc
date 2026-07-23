---
context_id: api-standards
context_type: consistent
authority: architecture-and-api-governance
status: imported-snapshot
owner: architecture-and-engineering
review_cadence: verify-against-confluence-before-material-design
source: https://paymentology.atlassian.net/wiki/spaces/pa/pages/10114367527/API+Standards
retrieved: 2026-07-22
---

# API Standards

This is a repository snapshot of the Paymentology API standards. Confluence is
the upstream source of truth until this content is formally migrated. Confirm
the current Confluence page before making a material API decision.

## Design position

- Design the contract before implementation.
- Design from the client perspective.
- Keep APIs aligned to business domains rather than internal system names.
- Prefer consistent enterprise conventions over local convenience.
- Review APIs during design, before code is complete.
- Publish usable documentation and examples.
- Version and deprecate breaking changes deliberately.

## Authentication and request context

- APIs must authenticate and authorize requests.
- Bearer-token authentication using JWT is the default company standard.
- Authorization must use scopes, roles, or claims.
- Tenant and security context must be propagated through an approved gateway or
  equivalent trusted mechanism.
- Common headers include `Authorization` and `X-Request-Id`.
- Use `X-Idempotency-Key` for mutating requests that require safe retries.

## URI and payload conventions

Preferred public shape:

```text
https://{host}/api/{routingNamespace}/v{major}/{resource}/{resourceId}/{subresource}
```

- Use HTTPS only.
- Use plural nouns for collections and kebab-case path segments.
- Do not expose internal microservice names unless they are part of the public
  contract.
- Use JSON camelCase field names.
- Use `{resourceType}Id` identifiers.
- Use `isX` or `hasX` for booleans where appropriate.
- Use SCREAMING_SNAKE_CASE for enum values.
- Use ISO 8601 UTC timestamps.
- Use ISO 4217 currency codes.

## Reliability and errors

- Side-effecting operations must be repeat-safe.
- Validate idempotency keys before processing mutating requests.
- Use semantic HTTP status codes consistently.
- Use a shared error envelope and distinguish transport errors from domain
  errors.
- API designs must document timeout, retry, pagination, rate limiting,
  observability, and deprecation behavior where relevant.

## HLD implications

An HLD proposing a new API should include the contract boundary, authentication
model, tenant context, idempotency behavior, versioning strategy, error model,
observability, and compatibility plan. An API design is not implementation-ready
until these decisions are reviewed by the relevant human owners.

## Source

[API Standards](https://paymentology.atlassian.net/wiki/spaces/pa/pages/10114367527/API+Standards)
