# Initiative Instances

This directory contains generated instances of the reusable initiative
templates. Each initiative is self-contained and keeps its requirement at the
root, separate from initiative-specific relative context.

`DEMO-001` is only a fixture. New requirements should be created with the
interactive command:

```text
just ai-sdlc-new
```

For scripted creation:

```text
just ai-sdlc-init PAY-4567 "Payment status notification" "Allow clients to receive timely payment status updates" "Clients cannot reliably see payment status changes" team.payments PAY-4567 medium internal intake
```

Use the `intake` profile for a small business-review PR. After merge, the
post-merge automation adds the reusable boilerplate and synchronizes valid
human approval metadata in a follow-up PR.

The generated structure after scaffold expansion is:

```text
<initiative-id>/
  initiative.md
  requirement.md
  initiative.yaml
  traceability.yaml
  approvals.yaml
  context-manifest.yaml
  context/relative/
  hld/
  lld/
  feedback/
  approvals/
  evidence/
```

The intake PR is intentionally smaller; it stops at the core files needed for
business review and traceability.

Do not edit the reusable templates to customize a single initiative. Change
the instance or improve the shared template deliberately.
