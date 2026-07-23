# Governed AI-SDLC Initiative Template

Copy this directory into the design repository and replace `DEMO-001` with the Jira epic or initiative key.

## Required sequence

1. Complete `initiative.yaml` and `requirement.md`.
2. Obtain Product Owner approval and record it in `approvals.yaml`.
3. Generate or complete `hld/hld.md` and review it through a design PR.
4. Record the Solution Architect approval with the exact HLD content hash.
5. Only then create `lld/lld.md` and repository workstreams.
6. Link stories, PRs, CI runs, and deployments in `traceability.yaml`.

The HLD approval is a hard gate. An LLD, implementation plan, or implementation PR that does not reference an approved HLD version and hash must fail validation.

## Suggested commands for the future POC

```text
ai-sdlc validate templates/ai-sdlc-initiative
ai-sdlc context build --initiative DEMO-001
ai-sdlc requirements draft --initiative DEMO-001
ai-sdlc hld generate --initiative DEMO-001
ai-sdlc hld approve --initiative DEMO-001 --principal user@example.com
ai-sdlc lld generate --initiative DEMO-001
ai-sdlc plan generate --initiative DEMO-001
ai-sdlc workspaces create --initiative DEMO-001
ai-sdlc trace show --initiative DEMO-001
```

These commands are the target UX; the first POC may implement them as scripts or a small service.
