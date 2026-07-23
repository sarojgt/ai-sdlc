# Risks and mitigations

| ID | Risk | Mitigation / owner | Exit evidence |
|---|---|---|---|
| R-01 | Wrong `t_core` columns or Apple Pay semantics | PayCore owner confirms schema and `wallet = APPLE_PAY`; Payments confirms meaning. | Schema/data contract and masked query |
| R-02 | Card-token reference is sensitive or mismatched | Tokenization/Security approve only a non-sensitive, non-reversible lookup representation; otherwise remove the filter. | Token policy, retention/access and redaction tests |
| R-03 | Cross-client or cross-region leakage | Reuse IMS and server-side predicates; never trust caller tenancy; fail closed. | Authorization/isolation matrix |
| R-04 | Unbounded or poorly indexed query harms PayCore | Enforce range/page/cursor bounds; inspect existing indexes and plans; load test before LLD. | `EXPLAIN`/plan and capacity evidence |
| R-05 | API contract drift | Reuse existing route/version, pagination, error and response conventions. | API catalogue and contract tests |
| R-06 | IMS or PayCore dependency failure | Reuse existing timeouts, safe errors, rate limits and fail-closed authorization. | Failure-mode tests and runbook |
| R-07 | Sensitive data in response or telemetry | Allow-list fields; redact token/PAN/SAD/auth material and raw payloads. | Automated redaction/data-flow tests |
| R-08 | BL/Lume deployment mismatch | Reuse each environment's existing PayAPI release and gateway registration. | BL and Lume smoke/deployment evidence |
| R-09 | Undefined SLO, retention, or operator access | Product/SRE/Security/FinOps approve NFR and telemetry matrix before release. | NFR, retention/access and cost review |

Release blockers are R-01 through R-05 and the NFR/region/runtime decisions.
They are evidence gates, not a reason to introduce a new architecture.
