# Initiative: Temporary card blocking API

## Summary

- Initiative ID: `KAN-4`
- Owner: `team.cards`
- Source work item: `KAN-4`
- Status: intake

## Business outcome

Allow authorized clients or operations users to temporarily block a card for a
defined period, with automatic expiry that restores the card to its previous
usable state without manual intervention.

## Scope

### In scope

- Authenticated temporary card-blocking API capability.
- Explicit expiry duration and automatic restoration after expiry.
- Requester, creation, expiry, audit, logging, metrics, and tracing requirements.
- Existing authentication, authorization, tenant isolation, and card-management
  platform patterns.

### Out of scope

- New standalone card-control platform.
- Card issuance or tokenization changes unless required by the HLD.
- Manual unblocking as the only restoration mechanism.
- Redesign of existing auth, observability, or deployment standards.

## Known stakeholders

- Product owner: pending
- Solution architect: pending
- Engineering owner: card service/API owner to confirm
- Security and operations owners: pending

## Links

- Source work item: https://randomtry.atlassian.net/browse/KAN-4
- Design PR:
- Implementation PR(s):
