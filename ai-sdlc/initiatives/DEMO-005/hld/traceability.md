# HLD traceability

| Requirement | HLD response | Evidence required before LLD |
|---|---|---|
| REQ-DEMO-005-01 | One authenticated client-facing PayAPI collection using existing Gateway/Auth0/IMS. | Exact route/version and authorization matrix |
| REQ-DEMO-005-02 | Existing PayCore `t_core`; `wallet = APPLE_PAY`; approved token reference; inclusive date range. | Verified columns, token policy, masked query |
| REQ-DEMO-005-03 | Existing bounded pagination/error/stable-ordering contract; reject unbounded work. | Current API standard, max bounds, cursor and SLO |
| REQ-DEMO-005-04 | Existing IMS client/region enforcement and server-side predicates. | Existing helper/package and isolation tests |
| REQ-DEMO-005-05 | Allow-listed response and redacted logs/traces/audit; no sensitive token/card data. | Data-flow, retention/access and automated redaction tests |

Source traceability remains in [`traceability.yaml`](../../traceability.yaml).
