## AI-SDLC change

Use a Conventional Commit title, for example:

```text
feat(ai-sdlc): add a new initiative workflow
fix(ai-sdlc): prevent approval sync loops
docs(ai-sdlc): clarify intake instructions
```

Valid types include `feat`, `fix`, `perf`, `refactor`, `revert`, `docs`,
`test`, `chore`, `ci`, `build`, and `style`. Add `!` or a `BREAKING CHANGE:`
footer for a breaking change.

- Initiative: `DEMO-001`
- Artifact type: `design | implementation | release`
- Requirement IDs:
- HLD reference and content hash:
- LLD reference and content hash:
- Impacted repositories:

## Gate checklist

- [ ] DAS metadata is valid.
- [ ] Context manifest is present and versioned.
- [ ] Parent design artifacts are approved where required.
- [ ] Automated checks passed.
- [ ] Security impact was assessed.
- [ ] Migration and rollback were considered.
- [ ] Human reviewer/CodeOwner is assigned.

## AI disclosure

- Agent/model used:
- Context pack ID/version:
- Human owner:
- AI-generated changes reviewed by a human: yes/no

## Scope changes

Does this change modify the approved architecture? If yes, stop implementation and create a new HLD/ADR revision.
