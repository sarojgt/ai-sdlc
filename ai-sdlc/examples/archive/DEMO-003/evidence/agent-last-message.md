Revised the reviewable HLD under `generated/hld/`:

- [hld.md](.../generated/hld/hld.md)
- [option-01.md](.../generated/hld/options/option-01.md)
- [option-02.md](.../generated/hld/options/option-02.md)
- [context.mmd](.../generated/hld/diagrams/context.mmd)
- [risks.md](.../generated/hld/risks.md)
- [adr.md](.../generated/hld/adr.md)

Addressed the review blocker by defining stable `event_id` / `X-Payment-Event-Id` identity across retries, replay, and migration, and added a lifecycle sequence diagram. Protected artifacts were not modified. Architecture approval remains pending.

Open questions: event identity composition, signing standard, volumes/SLA, retention/residency, platform availability, ownership, and migration path.

Summary: Option 1, durable asynchronous delivery, remains the proposed direction; all unresolved decisions are explicitly visible for Solution Architect review.