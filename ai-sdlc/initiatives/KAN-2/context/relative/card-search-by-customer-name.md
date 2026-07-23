# KAN-2 relative context: card search by customer name

Source work item: <https://randomtry.atlassian.net/browse/KAN-2>

## Confirmed from Jira intake

- Business users need a read-only API to search card records by customer name.
- Consumers are support and internal users.
- The endpoint must live in the relevant card service/API layer.
- Results must be filtered by the provided customer name and paginated.
- Responses must include only the minimum required card details.
- Existing authorization, standard error handling, observability, audit logging,
  secure logging, and API documentation standards must be reused.
- Card creation/update, customer profile changes, and new search UI are out of
  scope.

## Context gaps to resolve during HLD

- Exact card service/API repository, route, version, and owner.
- Exact role or permission model for authorized support and internal users.
- Existing customer name matching standard and normalization requirements.
- Approved minimum card response fields and masking rules.
- Customer-card data source, query path, and index/performance characteristics.
- Existing pagination, error envelope, audit event, metric, trace, and log
  redaction conventions for support APIs.
