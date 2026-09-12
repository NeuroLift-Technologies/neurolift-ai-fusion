# AGENTS.md — NeuroLift Technologies Organization-Wide Internal Gateway

> **Internal use only.** This is the private governance gateway for all coding agents operating within NeuroLift Technologies repositories. For public-facing principles, see the public [`NeuroLift-Technologies/.github`](https://github.com/NeuroLift-Technologies/.github) repository.

---

## You Are Here

You are a coding agent operating within the **NeuroLift Technologies** organization. This document is your internal coordination gateway.

**Mandatory reading order:**
1. `NLT-DEV-OTOI.md` — Full org-level coding agent contract (this repo, root level)
2. `REVIEW.md` — Canonical agent review format (see §4.5)
3. Repo-level `CLAUDE.md` — Project-specific context (in the repo you are working in)
4. `docs/active-threads.md` — Current work state (in the repo you are working in)
5. **PR Review Hermes Bot** — Confirm the bot is active and all PR checks have passed before merging (see PR Requirements section below)

> **Can't access `.github-private`?** If links to this repository return 404, key governance
> docs are mirrored publicly:
> - NLT-DEV-OTOI.md → https://github.com/NeuroLift-Technologies/.github/blob/main/governance/NLT-DEV-OTOI.md
> - AGENTS.md → https://github.com/NeuroLift-Technologies/.github/blob/main/governance/AGENTS.md
>
> Ask your org admin to grant the GitHub App access to `.github-private`. See
> `docs/troubleshooting/github-app-access.md` in this repo for instructions.

**Final authority:** Joshua W. Dorsey, Sr. Escalate. Do not guess.

---

## Solidarity Framework Principles (Public)

The ethical foundation of all NLT work is publicly documented in the **Solidarity Framework** and **HAIEF** (Human-AI Ethical Integration Framework):

- Public governance principles: [`NeuroLift-Technologies/.github`](https://github.com/NeuroLift-Technologies/.github)
- HAIEF reference: https://elevaitionfoundation.org

The principles are public. The operational machinery is in this private repository.

---

## Coordination Protocol

### Session Start (Every Session)

```
1. Read NLT-DEV-OTOI.md (this repo)
2. Read REVIEW.md (this repo) — canonical review format
3. Read repo-level `CLAUDE.md` (working repo)
4. Read `docs/active-threads.md` (working repo)
5. Self-register per OTOI Section 3
6. Confirm task scope before beginning
7. Work from a feature branch and open a Pull Request — never push directly to `main` or protected branches
```

### Commit Format

All agent commits must follow:

```
[AGENT_NAME] type(scope): description
```

Types: `feat`, `fix`, `docs`, `refactor`, `chore`, `test`, `ci`

All agent-authored changes must go through a Pull Request opened from a feature branch. Do not push directly to `main` or other protected branches.

### Escalation Triggers

Escalate to Joshua immediately when:
- Task scope is unclear or conflicts with existing work
- An architectural or deployment decision is required
- A blocker cannot be resolved by the agent
- An ethical concern arises
- LLM provider or external service selection is needed
- PR checks are failing but should be passing
- Hermes bot misconfiguration detected

Use the escalation template: `templates/escalation.md`

---

## Guardrails

These are **non-negotiable**. No exceptions without explicit Joshua approval:

| Guardrail | Details |
|---|---|
| No LLM provider lock-in | Do not hardcode or commit to a specific LLM provider |
| No architecture decisions | Database, deployment, framework choices require human sign-off |
| No production deployments | Human must explicitly approve all production actions |
| No credential storage | Never store secrets, tokens, or credentials in code or VCS |
| No external integrations | Third-party service connections require Joshua's approval |
| PR-only workflow | Create changes on feature branches and deliver them through Pull Requests; never push directly to `main` or other protected branches |
| No OTOI self-amendment | This governance doc cannot be changed by agents |

---

## PR Review Requirements

### Merge Gate Requirements

For any Pull Request to be merged in a NeuroLift Technologies repository:

**All of the following must be true:**

1. **All status checks must pass (green)** — No failing checks allowed
   - OSSAR-Scan (security vulnerabilities)
   - Check Contact Email Compliance
   - Scan PR for Credential Exposure (SOP-NLT-003)
   - Scan for Governance Incidents (SOP-NLT-003)
   - Validate (governance compliance)
   - Validate Agent Commit Format (SOP-NLT-001)
   - Check Agent Handoff Record (SOP-NLT-001)
   - Any repository-specific required checks

2. **At least 1 human approval required** — Automated approvals do not count

3. **No unresolved review comments** — All review comments must be addressed

4. **PR description must be complete and accurate** — Using PULL_REQUEST_TEMPLATE/agent-contribution.md

5. **Commit messages follow NLT format** — `[AGENT_NAME] type(scope): description`

6. **Branch is up to date with target branch** — Before merging

7. **Scope declaration documented** — If new top-level directories added (via pr-scope-check.yml)

### Hermes Bot Enforcement

The **PR Review Hermes Bot** enforces these requirements automatically:

- Monitors all PRs in configured repositories
- Verifies all required status checks have passed
- Posts review comments on PRs with issues found
- Blocks merge if any requirement is not met
- Requires human approval (automated approvals do not count)

### Bot Configuration

To enable the Hermes bot on a repository, add `.github/workflows/pr-review-hermes.yml`:

```yaml
name: PR Review Hermes Bot
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

permissions:
  contents: read
  pull-requests: write
  checks: read
  statuses: read

jobs:
  hermes-review:
    name: PR Review Hermes
    runs-on: ubuntu-latest
    steps:
      - name: Check status
        uses: actions/github-script@v7
        with:
          script: |
            // Verify all required checks pass
            // Post review comments
            // Block merge if checks incomplete
```

### Branch Protection Rules

Each repository's default branch must have these branch protection rules:

```
- Require pull request reviews before merging: 1 approving review
- Dismiss stale pull request approvals when new commits are pushed: true
- Require status checks to pass before merging: all required checks
- Require branches to be up to date before merging: true
- Do not allow bypassing the above settings: true
- Restrict who can push to matching branches: maintainers only
```

---

## Internal File Map

All files below live in this repository (`NeuroLift-Technologies/.github-private`):

```
NLT-DEV-OTOI.md                        ← Canonical org-level agent contract
AGENTS.md                               ← This file (updated with PR requirements)
REVIEW.md                               ← Canonical agent review format
nltotoi.json                            ← Discovery manifest

.nltotoi/
├── README.md                           ← Namespace overview
├── index/governance-files.md          ← File registry
├── contracts/README.md                ← Contract namespace
├── proposals/validation-roadmap.md    ← Validation roadmap
└── scripts/validate-governance.sh     ← Governance validation

templates/
├── agent-registration.json            ← OTOI Section 3 registration format
├── handoff-record.json                ← OTOI Section 5 handoff format
├── escalation.md                      ← OTOI Section 4.3 escalation format
├── intent-log.md                      ← Intent logging template
└── review-record.md                   ← Fillable review record template

ISSUE_TEMPLATE/
├── agent-escalation.md                ← GitHub escalation issue form
└── governance-proposal.md             ← OTOI amendment proposal form

PULL_REQUEST_TEMPLATE/
└── agent-contribution.md              ← Agent PR checklist

workflows/
├── pr-review-hermes.yml               ← PR Review Hermes Bot (NEW)
├── validate-governance.yml            ← CI: runs validate-governance.sh
└── other workflow files...

SOPs/
├── new-agent-onboarding.md            ← How to onboard a new coding agent
├── repo-governance-setup.md           ← How to add governance to a new NLT repo
└── incident-response.md               ← What to do when an agent goes off-rails
```

---

## Multi-Agent Coordination

When multiple agents may be active:

1. **Check active-threads.md first** — do not begin work already in progress
2. **Claim your thread** — update active-threads.md when starting a task
3. **Write handoff records** — never leave a session without a handoff document
4. **Do not overwrite peer work** — if conflict is detected, escalate

---

## Handoff Protocol

Before ending any significant session:

1. Update `docs/active-threads.md` in the working repo
2. Write a handoff record to `docs/agent-log/handoffs/` using `templates/handoff-record.json`
3. Document any open escalations in `docs/escalations/`
4. Summarize decisions made and decisions pending

---

*Internal governance document — NeuroLift Technologies | ORG-DEV-OTOI-1.0.3*
