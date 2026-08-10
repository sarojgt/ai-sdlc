# Banking.Live Service Context

This directory is the human-readable service and repository catalogue for the
Banking.Live estate. It complements `banking-live-estate.md`; it does not
replace repository discovery, deployment manifests, or service-owner
confirmation.

Each page records confirmed repository mappings, service responsibility,
important boundaries, deployment context, and unresolved discovery gaps. A
repository listed here is a context starting point, not permission to change
that repository.

The catalogue is intentionally conservative. When Confluence and GitHub use
different names, both names are retained and the mapping is marked for
confirmation where necessary.

## Minimum service context contract

Before an initiative uses a service page, it should be able to answer, from
this catalogue and its linked evidence:

| Area | Required information |
| --- | --- |
| Ownership | Service owner, repository, deployable unit, and source authority |
| Interface | API/route or message boundary, protocol, authentication, and consumers |
| Data | Database, schema/table or function families, classification, and ownership |
| Runtime | Ports, pools, queues, jobs, dependencies, and failure/retry behavior |
| Deployment | BL2/Lume target, region, client model, zone, and deployment repository |
| Evidence | Source links, retrieval date, confidence, and explicit context gaps |

HLD generation must use the assembled repository context only. If a required
field is missing, the agent records a `CONTEXT GAP` with an owner and retrieval
action; it must not silently search external systems or invent a service,
database, table, or integration.

The current local scan inventory is in
[repository-scan-inventory.md](repository-scan-inventory.md). It records the
repository commit used as evidence; the service pages remain the curated
business and technical context.
