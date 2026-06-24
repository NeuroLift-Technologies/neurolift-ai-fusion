---
name: nlt-commit-format
description: 'Format NLT agent commit messages correctly (OTOI Section 4.2). Use when writing a commit message, when asked about the NLT commit format, when a commit is flagged as non-compliant, or when preparing to commit changes in any NeuroLift Technologies repository.'
nlt-otoi-version: ORG-DEV-OTOI-1.0.2
nlt-solidarity-framework: true
nlt-haief: true
nlt-authority: Joshua W. Dorsey, Sr.
---

# NLT Commit Message Format (OTOI Section 4.2)

Validated by `.github/workflows/agent-commit-format.yml`.

## Commit Format

```
[AGENT_NAME] type(scope): description
```

## Fields

| Field | Description | Example |
|-------|-------------|---------|
| `AGENT_NAME` | Your agent name (no spaces; hyphens OK) | `Claude`, `Copilot`, `Codex` |
| `type` | Change type | `feat` |
| `scope` | Area affected | `handoff-template` |
| `description` | Imperative-mood; no trailing period | `add session end protocol fields` |

## Allowed Types

| Type | When to use |
|------|------------|
| `feat` | New feature or file |
| `fix` | Bug fix |
| `docs` | Documentation-only |
| `refactor` | Refactor without behavior change |
| `chore` | Maintenance, cleanup, config |
| `test` | Adding or updating tests |
| `ci` | CI workflow changes |

## Valid Examples

```
[Claude] feat(claude-template): add .claude/ canonical template
[Claude] fix(validate-governance): correct workflow path in required-files list
[Codex] docs(sop-001): clarify step 7 commit format requirements
[Copilot] chore(governance): add repo governance stubs (ORG-DEV-OTOI-1.0.2)
```

## Common Mistakes

| Wrong | Right | Why |
|-------|-------|-----|
| `feat: add template` | `[Claude] feat(scope): add template` | Missing `[AGENT_NAME]` |
| `[Claude] added template` | `[Claude] feat(templates): add template` | Missing type and scope |
| `[Claude] feat(templates): Added template.` | `[Claude] feat(templates): add template` | Past tense; trailing period |
| `[Claude] update(templates): ...` | `[Claude] chore(templates): ...` | `update` is not an allowed type |
| `[My Agent Name] feat(x): y` | `[My-Agent-Name] feat(x): y` | No spaces in AGENT_NAME |

## Fork Repository Exception

The commit format requirement does **not** apply to pull requests from forked repositories. The `agent-commit-format` check skips fork PRs automatically.

## References

- `templates/commit-message.md` — Full guide
- `NLT-DEV-OTOI.md` Section 4.2 — Commit format spec
- `SOPs/new-agent-onboarding.md` — SOP-NLT-001 Step 7
