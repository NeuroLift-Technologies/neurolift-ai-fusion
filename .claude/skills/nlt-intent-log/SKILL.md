---
name: nlt-intent-log
description: 'Write an NLT intent log entry before taking a significant action (OTOI Section 7). Use when about to make a broad-scope change, an irreversible action, an architectural modification, or any action that warrants transparency before execution.'
nlt-otoi-version: ORG-DEV-OTOI-1.0.3
nlt-solidarity-framework: true
nlt-haief: true
nlt-authority: Joshua W. Dorsey, Sr.
---

# NLT Intent Log (OTOI Section 7)

This skill guides agents through creating an **intent log entry** as required by ORG-DEV-OTOI-1.0.3 Section 7. Log your intent before acting, then record the outcome afterward.

The `/intent-log <topic>` slash command automates this workflow.

## When to Use

- Before any action with broad scope or architectural impact
- Before any irreversible action (deletes, force-pushes, schema changes)
- Before touching files outside your immediate task scope
- When you are unsure whether an action requires escalation

## Where to Store

```
docs/agent-log/intent/[date]-[topic].md
```

## What Qualifies as "Significant"?

- **Broad scope** — affects many files, services, or people
- **Irreversible** — difficult or impossible to undo
- **Architectural** — changes how systems are structured or interact
- **Sensitive** — involves credentials, access controls, or PII

When in doubt, log it. Intent logging costs little and protects everyone.

## Decision Flowchart

```
Significant action identified?
        |
        v
Write intent log entry
        |
        v
Escalation needed? --yes--> Stop; /escalate <topic>
        |
       no
        |
        v
Proceed with action
        |
        v
Fill in Outcome section
```

## References

- `templates/intent-log.md` — Blank template
- `NLT-DEV-OTOI.md` Section 7 — Intent logging spec
- `templates/escalation.md` — Escalation template
