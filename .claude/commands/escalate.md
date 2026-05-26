---
description: File an escalation record and GitHub issue per OTOI §4.3
argument-hint: "<brief topic, e.g. 'database choice'>"
---

Create a complete escalation record per ORG-DEV-OTOI-1.0.0 Section 4.3 and file a GitHub issue.

**Topic:** $ARGUMENTS

## When to Escalate

1. Task scope is unclear or conflicts with existing work
2. An architectural or deployment decision is required
3. A blocker cannot be resolved
4. An ethical concern arises
5. An LLM provider selection or external service integration is needed
6. A production deployment is being considered
7. A governance document amendment is proposed

**When in doubt, escalate. Do not guess.**

## Steps

1. Use the format in `templates/escalation.md` (or `.claude/skills/nlt-escalation/SKILL.md`).

2. Determine priority:
   - `critical`: Active incident, credentials exposed, production system affected
   - `high`: Architectural decision blocking significant work
   - `medium`: Design or integration choice needed to proceed
   - `low`: Informational — flagging for Joshua's awareness

3. Fill in the record: Date, Agent, Session, OTOI Version (ORG-DEV-OTOI-1.0.0), Target (Joshua W. Dorsey, Sr.), Priority, Trigger, Situation, Decision Required, Options Considered, Recommendation, Blockers.

4. Write the record to:
   ```
   docs/escalations/<YYYY-MM-DD>-<topic-slug>.md
   ```

5. File a GitHub issue using `mcp__github__issue_write` (or `ISSUE_TEMPLATE/agent-escalation.md`).

6. Commit with:
   ```
   [Claude] docs(escalation): file <topic> escalation (ORG-DEV-OTOI-1.0.0)
   ```

## Escalation Target

- **Joshua W. Dorsey, Sr.**
- Email: `info@neuroliftsolutions.com`
