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
just ai-sdlc-init PAY-4567 "Payment status notification" team.payments PAY-4567
```

The generated structure is:

```text
<initiative-id>/
  initiative.md
  requirement.md
  context/relative/
  hld/
  lld/
  feedback/
  approvals/
  evidence/
```

Add Markdown files only where the initiative needs them. The framework creates
README files in the directories so their purpose is visible in GitHub.

Do not edit the reusable templates to customize a single initiative. Change
the instance or improve the shared template deliberately.
