# Initiative Intake Agent Guide

Use this guide when a Jira requirement is being turned into the first GitHub
initiative PR.

## Objective

Create the smallest useful initiative PR for human business review.

The intake PR should capture only the requirement and the minimum metadata
needed to keep traceability intact. Do not create the full boilerplate in the
initial PR.

## Allowed files in the intake PR

- `initiative.md`
- `requirement.md`
- `initiative.yaml`
- `traceability.yaml`
- `approvals.yaml`
- `context-manifest.yaml`

## Do not add in the intake PR

- `context/relative/README.md`
- `hld/README.md`
- `hld/hld.md`
- `lld/README.md`
- `lld/lld.md`
- `feedback/**`
- `approvals/README.md`
- `evidence/**`
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

After the intake PR is merged, the post-merge workflow creates a follow-up PR
to add the reusable folder structure and README guides.
