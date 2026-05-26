---
name: nlt-escalation
description: 'Write a complete NLT escalation record (OTOI Section 4.3). Use when an agent hits a guardrail, needs a human decision, encounters a blocker, faces an unclear task scope, or must escalate an architectural, deployment, ethical, or strategic question to Joshua W. Dorsey, Sr.'
nlt-otoi-version: ORG-DEV-OTOI-1.0.0
nlt-solidarity-framework: true
nlt-haief: true
nlt-authority: Joshua W. Dorsey, Sr.
---

# NLT Escalation Record (OTOI Section 4.3)

This skill guides agents through creating a complete **escalation record** as defined in ORG-DEV-OTOI-1.0.0 Section 4.3. Escalation is not failure — it is correct protocol.

The `/escalate <topic>` slash command automates this workflow.

## When to Use This Skill

- Task scope is unclear or conflicts with existing work
- An architectural or deployment decision is required
- A blocker cannot be resolved by the agent
- An ethical concern has arisen
- An LLM provider selection or external service integration is needed
- A production deployment is being considered
- A governance document amendment is proposed

**When in doubt, escalate. Do not guess.**

## Escalation Target

**Joshua W. Dorsey, Sr.**
Email: info@neuroliftsolutions.com
GitHub: File via `ISSUE_TEMPLATE/agent-escalation.md`

## Where to Store the Record

```
docs/escalations/[date]-[topic].md
```

## Priority Levels

| Priority | When to use |
|----------|------------|
| `critical` | Active incident, credentials exposed, production system affected |
| `high` | Architectural decision blocking significant work |
| `medium` | Design or integration choice needed to proceed |
| `low` | Informational — flagging for Joshua's awareness |

## References

- `templates/escalation.md` — Blank escalation template
- `NLT-DEV-OTOI.md` Section 4.3 — Escalation format spec
- `ISSUE_TEMPLATE/agent-escalation.md` — GitHub escalation issue form
