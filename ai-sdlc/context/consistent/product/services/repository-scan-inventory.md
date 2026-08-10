---
context_id: service-repository-scan-inventory
context_type: consistent
authority: local-repository-scan
status: scanned-snapshot
owner: engineering-architecture
review_cadence: refresh-before-material-design
retrieved: 2026-08-10
---

# Service Repository Scan Inventory

This inventory records local, read-only scans of repositories referenced by the
Banking.Live service catalogue. It is evidence for context refresh, not a
substitute for service-owner confirmation.

## Scan policy

- Source: local SSH clones under the ignored `.local-repository-cache/`.
- Scan date: 2026-08-10.
- Scope: repository documentation, build/runtime files, API definitions,
  migrations, deployment manifests, and observable integration/configuration
  metadata.
- Sensitive content: secrets, credentials, tokens, PAN, key material, and
  production values are excluded from curated context.
- Use: consult the linked service page first; refresh the page when the pinned
  repository commit is stale.

## Repository commits

| Repository | Scanned commit | Context page |
| --- | --- | --- |
| [atlas-auth-transaction-insights](https://github.com/Paymentology/atlas-auth-transaction-insights) | `057d4f6` | [Atlas](atlas.md) |
| [atlas-config-hub](https://github.com/Paymentology/atlas-config-hub) | `eb8e9b3` | [Atlas](atlas.md) |
| [atlas-environments](https://github.com/Paymentology/atlas-environments) | `ab40fb8` | [Atlas](atlas.md) |
| [atlas-identity-management](https://github.com/Paymentology/atlas-identity-management) | `084048b` | [Atlas](atlas.md) |
| [atlas-payportal](https://github.com/Paymentology/atlas-payportal) | `baac0b2` | [Atlas](atlas.md) |
| [atlas-priv-client-directory](https://github.com/Paymentology/atlas-priv-client-directory) | `e606153` | [Atlas](atlas.md) |
| [atlas-pub-user-management](https://github.com/Paymentology/atlas-pub-user-management) | `d9bc6e5` | [Atlas](atlas.md) |
| [atlas-transaction-insights](https://github.com/Paymentology/atlas-transaction-insights) | `947be6e` | [Atlas](atlas.md) |
| [atlas-ui-kit](https://github.com/Paymentology/atlas-ui-kit) | `3f21945` | [Atlas](atlas.md) |
| [bl-environments](https://github.com/Paymentology/bl-environments) | `2ec927d` | [BL environments](bl-environments.md) |
| [decision-engine](https://github.com/Paymentology/decision-engine) | `b7976e1` | [Decision Engine](decision-engine.md) |
| [decision-engine-atlas](https://github.com/Paymentology/decision-engine-atlas) | `4e03d31` | [Decision Engine](decision-engine.md) |
| [decision-engine-dsl](https://github.com/Paymentology/decision-engine-dsl) | `c6c28e3` | [Decision Engine](decision-engine.md) |
| [payapi](https://github.com/Paymentology/payapi) | `bbcc4ef` | [PayAPI](payapi.md) |
| [paycontrol](https://github.com/Paymentology/paycontrol) | `fde0aac` | [PayControl](paycontrol.md) |
| [paycoredb](https://github.com/Paymentology/paycoredb) | `fc5ead8` | [PayCore DB](paycoredb.md) |
| [paycredit](https://github.com/Paymentology/paycredit) | `d7bde9c` | [PayCredit](paycredit.md) |
| [paycredit-team-shared-resources](https://github.com/Paymentology/paycredit-team-shared-resources) | `0c267a7` | [PayCredit](paycredit.md) |
| [paycredit-test-automation](https://github.com/Paymentology/paycredit-test-automation) | `6c7b261` | [PayCredit](paycredit.md) |
| [paycredit-ui](https://github.com/Paymentology/paycredit-ui) | `4754b12` | [PayCredit](paycredit.md) |
| [paykeydb](https://github.com/Paymentology/paykeydb) | `5c86b3e` | [PayKey DB](paykeydb.md) |
| [paykeyserv](https://github.com/Paymentology/paykeyserv) | `10ffe67` | [PayKeyService](paykeyservice.md) |
| [paylogdb](https://github.com/Paymentology/paylogdb) | `4b37d71` | [PayLog DB](paylogdb.md) |
| [paypower](https://github.com/Paymentology/paypower) | `2e89209` | [PayPower](paypower.md) |
| [payroute](https://github.com/Paymentology/payroute) | `baa6db1` | [PayRoute](payroute.md) |
| [payscheduler](https://github.com/Paymentology/payscheduler) | `95e7ff4` | [PayScheduler](payscheduler.md) |
| [payswitch-context](https://github.com/Paymentology/payswitch-context) | `bf43157` | [PaySwitch](payswitch.md) |
| [payswitch-iso8583-core](https://github.com/Paymentology/payswitch-iso8583-core) | `d67c7b5` | [PaySwitch](payswitch.md) |
| [payswitch-keymanager](https://github.com/Paymentology/payswitch-keymanager) | `62ac7bd` | [PaySwitch](payswitch.md) |
| [payswitch-orchestration](https://github.com/Paymentology/payswitch-orchestration) | `9bb8159` | [PaySwitch](payswitch.md) |
| [payswitch-paypower-adaptor](https://github.com/Paymentology/payswitch-paypower-adaptor) | `772a69e` | [PaySwitch](payswitch.md) |
| [payswitch-pks-adaptor](https://github.com/Paymentology/payswitch-pks-adaptor) | `b0f5dfc` | [PaySwitch](payswitch.md) |
| [payswitch-scheme-parser](https://github.com/Paymentology/payswitch-scheme-parser) | `fcfb756` | [PaySwitch](payswitch.md) |
| [paytokdb](https://github.com/Paymentology/paytokdb) | `841df85` | [PayTok DB](paytokdb.md) |
| [rule-engine-v1-load-test](https://github.com/Paymentology/rule-engine-v1-load-test) | `e404386` | [Rule Engine](rule-engine.md) |

## Remaining discovery rule

The rule-engine implementation repository is not represented by the available
load-test repository. Do not infer service behavior from that auxiliary scan;
the primary implementation and deployment repository still require owner
confirmation.
