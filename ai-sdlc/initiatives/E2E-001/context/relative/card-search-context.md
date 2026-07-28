# Card Search — Initiative-Relative Context

This requirement is intended to extend the existing card-search capability for
authorized users who need to find cards using a customer name.

The HLD context-discovery step must confirm the concrete existing API/service,
authoritative data source, searchable fields and indexes, matching semantics,
authorization and masking controls, client/tenant/region boundaries,
pagination/error conventions, deployment reuse, and observability/audit
capabilities.

No new service, database, authorization path, or external integration is
assumed at intake. Any missing material fact must be recorded as a `CONTEXT
GAP` with an owner and retrieval action during HLD generation.
