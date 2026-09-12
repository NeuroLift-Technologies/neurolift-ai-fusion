## PR Review Hermes Bot — Requirements

This section defines the standard that must be met for every Pull Request across all NeuroLift Technologies repositories. The PR Review Hermes Bot enforces these requirements automatically.

### Merge Gate — All Must Be True

For any Pull Request to be merged in a NeuroLift Technologies repository, **all** of the following must be true:

1. **All status checks must pass (green)** — No failing checks permitted
2. **At least 1 human approval required** — Automated or bot approvals do not count
3. **No unresolved review comments** — All review comments must be addressed
4. **PR description must be complete** — Filled using `PULL_REQUEST_TEMPLATE/agent-contribution.md` (or the repo equivalent)
5. **Commit messages follow NLT format** — `[AGENT_NAME] type(scope): description`
6. **Branch is up to date with target branch** — Behind branches cannot be merged
7. **Scope declaration documented** — Any new top-level directories added must be explicitly called out in the PR description

### Bot Enforcement

The **PR Review Hermes Bot** enforces these rules via GitHub Actions:

- Posts a status summary on every PR (open, synchronize, reopened)
- Verifies all required status checks are green
- Posts a blocking commit status (`hermes-bot/merge-gate`) when checks fail or are missing
- Re-checks on every new commit pushed to the PR
- Posts a reminder if a PR sits without review activity for an extended period

### Required Status Checks

Each repository should configure branch protection to require these checks (or the repo-equivalent):

- `OSSAR-Scan` (security vulnerabilities)
- `Check Contact Email Compliance`
- `Scan PR for Credential Exposure (SOP-NLT-003)`
- `Scan for Governance Incidents (SOP-NLT-003)`
- `validate` (governance compliance)
- `Validate Agent Commit Format (SOP-NLT-001)`
- `Check Agent Handoff Record (SOP-NLT-001)`
- `hermes-bot/merge-gate` (the bot's own gate)

### Branch Protection

Each repository's default branch should have:

- Require PR before merging: **yes**
- Required approving reviewers: **1**
- Dismiss stale approvals on new commits: **yes**
- Require status checks to pass: **yes** (all of the above)
- Require branches to be up to date: **yes**
- Allow force pushes: **no**
- Allow deletions: **no**

### When the Bot Blocks a Merge

If the bot blocks a merge:

1. Read the bot's PR comment to identify the failing/missing check
2. Fix the issue or wait for the check to complete if it is still running
3. Push the fix — the bot re-verifies automatically
4. Once all checks pass and a human approves, merge is permitted

### Agent Session Start Checklist (with PR requirements)

```
1. Read NLT-DEV-OTOI.md (this repo)
2. Read repo-level CLAUDE.md (working repo)
3. Read docs/active-threads.md (working repo)
4. Self-register per OTOI Section 3
5. Confirm task scope before beginning
6. Work from a feature branch and open a Pull Request — never push directly to main or protected branches
7. After opening the PR, confirm the PR Review Hermes Bot has posted its status summary
8. Before merging, verify all status checks are green and at least 1 human approval exists
```

### Handoff Note

When handing off a PR:
- Include the PR number in the handoff record
- Note which checks are still pending (if any)
- Note whether a human approval has been granted
- If the PR is waiting on a human review, flag that explicitly

---

*PR Review Hermes Bot — NeuroLift Technologies | ORG-DEV-OTOI-1.0.3*
