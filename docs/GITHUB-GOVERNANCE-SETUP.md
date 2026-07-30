# GitHub governance setup

Repository files can validate approved reviewers; GitHub administrators must
enforce the same policy at merge time.

For this POC, `ai-sdlc/config/github-governance.yaml` lists `sarojgt` for the
three human roles. Replace those entries with enterprise GitHub teams before
production use.

Configure `main` branch protection to require pull-request reviews, dismissal
on new commits, CODEOWNERS review for requirement/HLD/LLD paths, the
`das-gate` and Conventional Commit checks, and squash merges only.

Do not grant Actions permission to bypass these rules. Automation PRs may use
auto-merge only after the same required checks pass.
