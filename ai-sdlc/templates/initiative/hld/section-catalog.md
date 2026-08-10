# HLD optional section catalog

This is a section menu for the HLD agent, not content to copy into every HLD.
The assessment selects only sections that help a human make the architecture
decision. Keep the reference names below when selected; omit empty sections.

| Section | Include when it answers |
|---|---|
| Authors & Approvals | Who owns a required review not already represented by the architecture gate? |
| High Level Business Requirements | Which few requirements directly constrain the architecture? |
| Architecture Principles Applied | Which approved principle materially shapes the recommendation? |
| Non-Functional Requirements | Which measurable NFR changes or constrains the design? |
| Availability and Reliability | Does failure handling or availability change? |
| Performance and Scalability | Is there a material volume, latency, throughput, or capacity decision? |
| Maintainability | Is operability or ownership a design trade-off? |
| Observability | Does the initiative introduce a new signal, SLO, or monitoring boundary? |
| Security and Compliance | Is there initiative-specific identity, authorization, data, or regulatory impact? |
| Data Quality | Does correctness, lineage, reconciliation, or stewardship affect the decision? |
| Disaster Recovery | Do RTO, RPO, failover, or recovery arrangements change? |
| Assumptions | Does the recommendation depend on a testable, owned assumption? |
| Context | Do actors, system boundary, or external interactions need clarification? |
| High Level Architecture Diagram | Would one diagram clarify a material boundary better than prose? |
| Logical View | Are responsibilities or component boundaries changing? |
| Information/Data View | Are ownership, storage, segregation, lineage, or lifecycle changing? |
| Physical/Deployment View | Are regions, environments, zones, platforms, or topology changing? |
| Component Model | Are several components and their responsibilities material to the decision? |
| API and Integration Design | Is an API or integration boundary being introduced or changed? |
| Event and Message Flow | Is asynchronous behaviour or ordering material? |
| Security Design | Does the security model require a focused design view? |
| Networking Considerations | Are trust zones, connectivity, ingress, egress, or mTLS changing? |
| Migration and Rollout | Is compatibility, phasing, rollback, or migration material? |
| Testing Considerations | Is there a design-specific test concern beyond normal engineering practice? |
| Operations Considerations | Does support, runbook, ownership, or incident response change? |
| Commercial View | Do cost, licensing, volume, or capacity affect the decision? |
| Key Design Decisions | Are several decisions easier to review as a compact decision table? |
| Open Items & Decisions Required | Is a non-context question still awaiting an owner or decision? |
| Pending Items from ARB | Has ARB explicitly raised or requested an item? |
| Traceability | Would human-readable links add value beyond the machine baseline? |

Do not use optional sections to repeat the requirement, recommendation, risks,
context gaps, or unchanged platform standards. Detailed contracts, schemas,
classes, SQL, test cases, scripts, and runbooks belong in an LLD or a focused
supporting artifact.
