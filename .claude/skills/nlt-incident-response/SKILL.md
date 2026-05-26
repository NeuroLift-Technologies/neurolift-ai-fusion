---
name: nlt-incident-response
description: 'Respond to a coding agent that has gone off-rails or violated NLT governance (SOP-NLT-003). Use when an agent has made unauthorized changes, committed credentials, exceeded scope, or taken irreversible actions.'
nlt-otoi-version: ORG-DEV-OTOI-1.0.0
nlt-solidarity-framework: true
nlt-haief: true
nlt-authority: Joshua W. Dorsey, Sr.
---

# NLT Incident Response — Agent Off-Rails (SOP-NLT-003)

Use this skill immediately when an incident is detected.

## When to Use

- A coding agent has made unauthorized architectural decisions
- An agent committed secrets, credentials, or sensitive data
- An agent exceeded authorized scope
- An agent took irreversible actions without approval
- Behavior is inconsistent with ORG-DEV-OTOI-1.0.0

## Severity Classification

| Severity | Examples |
|----------|---------|
| **Critical** | Secrets committed, production systems modified, external systems accessed without approval |
| **High** | Unauthorized architecture decisions, scope significantly exceeded, data integrity affected |
| **Medium** | Commit format violations, missing handoff records, active-threads.md not updated |
| **Low** | Minor protocol deviations with no functional impact |

## Immediate Response (Critical / High)

### Step 1: Stop the Agent

Terminate the agent session immediately. Do not allow further commits.

### Step 2: Assess the Damage

1. What unauthorized actions were taken?
2. Are secrets or credentials exposed? → If yes, treat as security incident immediately
3. Were production systems affected?
4. What is the current state of the working branch/repo?
5. Is any data at risk?

### Step 3: Secure (If Credentials Exposed)

1. **Immediately revoke** all exposed credentials — treat as compromised
2. Rotate all secrets referenced in or near the affected commits
3. Remove secrets from git history (`git filter-branch` or BFG)
4. Force-push the cleaned branch
5. Audit all systems that used the exposed credentials

**This must happen within minutes, not hours.**

### Step 4: Revert Unauthorized Changes

```bash
git revert [commit-sha]
# OR
git reset --hard [last-good-sha] && git push --force-with-lease origin [branch]
```

### Step 5: Document the Incident

Create an incident record at `docs/escalations/incident-[date]-[brief-description].md`.

### Step 6: Escalate

File GitHub issue using `ISSUE_TEMPLATE/agent-escalation.md` (or `/escalate`). Priority: **critical**. Contact: `info@neuroliftsolutions.com`

## Standard Response (Medium / Low)

1. Document the deviation in `docs/escalations/`
2. Fix commit messages, add missing handoff records, update `docs/active-threads.md`
3. Bring the deviation to Joshua's attention for protocol review

## References

- `SOPs/incident-response.md` — Full SOP
- `NLT-DEV-OTOI.md` — Canonical org-level contract
- `ISSUE_TEMPLATE/agent-escalation.md` — Escalation issue form
