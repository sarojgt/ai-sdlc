Created the implementation-oriented HLD package:

- [hld.md](../hld/hld.md)
- [risks.md](../hld/risks.md)
- [adr.md](../hld/adr.md)
- [traceability.md](../hld/traceability.md)
- Updated both implementation options and linked Mermaid diagrams.

The design remains strictly PayAPI → PayCore `t_core`, using `wallet = APPLE_PAY`, approved token/date filters, existing IMS authorization, query bounds, BL/Lume deployment reuse, and no new service, database, projection, event pipeline, token flow, or BFF.

Key context gaps are the exact route/package, `t_core` columns/token representation, existing indexes/query plan, API contract values, SLOs, and BL/Lume deployment classification. Architecture approval remains pending.
