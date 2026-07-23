---
context_id: banking-live
context_type: consistent
authority: product-and-platform-architecture
status: imported-snapshot
owner: banking-live-and-lume-platform
review_cadence: verify-against-confluence-before-material-design
source: https://paymentology.atlassian.net/wiki/spaces/LUME/pages/8977547536/00.01+What+is+Lume+ex.+BL3
retrieved: 2026-07-22
---

# Banking.Live and Lume

Banking.Live is Paymentology's issuer-processing platform. Banking.Live 3.0,
also referred to in the Lume material, is the modern cloud-based platform
direction for new clients and clients migrated from legacy environments.

## Capability context

- Existing Banking.Live functionality remains part of the product contract
  while the infrastructure and platform capabilities evolve.
- Lume enables capabilities that depend on modern cloud-native infrastructure.
- New clients and migrated clients are expected to use the modern platform
  path, while legacy or back-book clients may remain on older infrastructure
  during transition.
- A design must distinguish product compatibility from infrastructure
  compatibility; the same business capability may have different deployment,
  integration, and operational constraints across generations.

## HLD implications

Banking.Live-related HLDs must identify whether the change targets legacy BL,
BL3/Lume, or both; whether backward compatibility is required; which APIs or
events are shared; and what migration or coexistence behavior is needed.

## Source

[What is Lume / BL3](https://paymentology.atlassian.net/wiki/spaces/LUME/pages/8977547536/00.01+What+is+Lume+ex.+BL3)
