---
description: Log intent BEFORE a significant or irreversible action per OTOI §7
argument-hint: "<brief topic, e.g. 'refactor auth module'>"
---

Write an intent log entry per ORG-DEV-OTOI-1.0.0 Section 7 **BEFORE** taking the action.

**Topic:** $ARGUMENTS

## When to Log Intent

A significant action is one that is:

- **Broad scope** — affects many files, services, or people
- **Irreversible** — difficult or impossible to undo (deletes, migrations, force-pushes)
- **Architectural** — changes how systems are structured or interact
- **Sensitive** — involves credentials, access controls, or PII

When in doubt, log it.

## Steps

1. Use the format in `templates/intent-log.md` (or `.claude/skills/nlt-intent-log/SKILL.md`).

2. Fill in: Date, Agent, Session, OTOI Version, Working repo, Action, Rationale, Risks, Alternatives Considered, Escalation Needed (yes/no).

3. **If Escalation Needed is `yes`:** STOP. Use `/escalate <topic>` before proceeding.

4. If `no`: write the entry to:
   ```
   docs/agent-log/intent/<YYYY-MM-DD>-<topic-slug>.md
   ```

5. Commit the intent log:
   ```
   [Claude] docs(intent): log <topic> intent (ORG-DEV-OTOI-1.0.0)
   ```

6. Proceed with the action.

7. After completion, return and fill the **Outcome** section.

8. Commit the outcome:
   ```
   [Claude] docs(intent): record outcome of <topic> (ORG-DEV-OTOI-1.0.0)
   ```
