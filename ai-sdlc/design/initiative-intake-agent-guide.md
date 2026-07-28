# Initiative Intake Agent Guide

Use this guide when a Jira requirement is being turned into the first GitHub
initiative PR.

## Objective

Create the smallest useful initiative PR for human business review.

The intake PR should capture only the requirement. Traceability metadata is
created by post-merge automation from the requirement front matter. Do not
create the full boilerplate in the initial PR.

## Allowed files in the intake PR

- `requirement.md`
- Optional initiative-specific files under `context/relative/`

## Do not add in the intake PR

- `hld/README.md`
- `hld/hld.md`
- `lld/README.md`
- `lld/lld.md`
- `feedback/**`
- `approvals/README.md`
- `evidence/**`
- Initiative metadata such as `initiative.md`, `initiative.yaml`,
  `traceability.yaml`, `approvals.yaml`, or `context-manifest.yaml`
- Any implementation code or workflow changes

## Required behavior

- Keep the wording human readable.
- Keep the requirement generic enough for the initiative, not tied to one
  implementation detail unless the Jira item explicitly requires it.
- Preserve traceability back to the Jira work item.
- Use the `intake` bootstrap profile.
- Stop after creating the intake PR.
- Let the post-merge automation add the reusable boilerplate and synchronize
  valid human approval metadata.

## Example command shape

```text
just ai-sdlc-init \
  PAY-4567 \
  "Temporary card blocking API" \
  "Allow a card to be blocked for a defined duration and automatically restored when the block expires" \
  "Clients and operations need a temporary block without manual follow-up" \
  team.payments \
  PAY-4567 \
  medium \
  internal \
  intake
```

## Handoff

After the intake PR is approved or merged, the post-merge workflow creates a
follow-up PR to add initiative metadata and the context manifest. The HLD
workflow creates HLD, evidence, and feedback artifacts when it starts; the LLD
workflow creates LLD artifacts only after HLD approval. The workflow may also
synchronize valid human requirement approval metadata. Do not add these files
manually to the intake PR.
