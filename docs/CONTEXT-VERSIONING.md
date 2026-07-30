# Context versioning

`main` is the context authority. A merged `feat(context)`, `fix(context)`, or
breaking context PR creates scoped semantic tags for changed packages:

| Path | Tag track |
|---|---|
| `consistent/architecture/**`, `guardrails/architecture/**` | `context/architecture/vX.Y.Z` |
| security context or guardrails | `context/security/vX.Y.Z` |
| `consistent/technology/**` | `context/technology/vX.Y.Z` |
| `consistent/platform/**` | `context/platform/vX.Y.Z` |
| `consistent/business/**` | `context/domain/vX.Y.Z` |
| `consistent/product/**` | `context/product/vX.Y.Z` |

The context builder records only selected packages and their exact tag, tag
commit, source paths, and hashes. An HLD therefore remains reproducible even
after `main` changes.

Run `just ai-sdlc-context-drift <ID>` to compare an existing HLD baseline with
current reachable package tags. It writes evidence only; a human decides
whether to review, revise, or supersede the HLD. It never regenerates a design.

Packages without a historical tag are recorded as `unreleased` until their
first context release. Bootstrap initial package tags on `main` once through a
controlled release operation before relying on version-only governance.
