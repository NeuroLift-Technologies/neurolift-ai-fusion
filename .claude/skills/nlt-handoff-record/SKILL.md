---
name: nlt-handoff-record
description: 'Write a complete NLT session handoff record (OTOI Section 5). Use when ending a coding session, when asked to write a handoff, create a handoff record, document session end, or prepare work for the next agent.'
nlt-otoi-version: ORG-DEV-OTOI-1.0.0
nlt-solidarity-framework: true
nlt-haief: true
nlt-authority: Joshua W. Dorsey, Sr.
---

# NLT Session Handoff Record (OTOI Section 5)

This skill guides agents through writing a complete **session handoff record** as required by ORG-DEV-OTOI-1.0.0 Section 5. A handoff record must be written at the end of every significant session.

The `/handoff` slash command automates this workflow.

## Where to Store the Handoff

Save the completed handoff to:
```
docs/agent-log/handoffs/[date]-[session-id].json
```

## Handoff Record Template

```json
{
  "handoff_record": {
    "session_id":         "[Branch or unique identifier]",
    "agent_name":         "Claude Code",
    "date":               "[YYYY-MM-DD]",
    "otoi_version":       "ORG-DEV-OTOI-1.0.0",
    "repo":               "NeuroLift-Technologies/neurolift-ai-fusion",
    "branch":             "[branch]",
    "work_completed":     [],
    "work_in_progress":   [],
    "blockers":           [],
    "decisions_made":     [],
    "decisions_pending":  [],
    "escalations":        [],
    "next_agent_notes":   "[What the next agent needs to know]",
    "files_modified":     [],
    "tests_run":          [],
    "tests_passing":      true,
    "pr_url":             "[URL if applicable]"
  }
}
```

## Field Guidance

All fields required; use empty arrays where there is no content.

- `otoi_version`: Must be `"ORG-DEV-OTOI-1.0.0"`
- `work_completed`: Specific, concrete list (not aspirational)
- `tests_passing`: Boolean — do not assert `true` if tests were not run
- `files_modified`: Match the actual diff

## Session-End Checklist

Before writing the handoff record:

- [ ] Update `docs/active-threads.md` with current thread state
- [ ] Document any open escalations in `docs/escalations/`
- [ ] Ensure all changes are committed and pushed
- [ ] Record the PR URL if one was created

## References

- `templates/handoff-record.json` — Blank template
- `NLT-DEV-OTOI.md` Section 5 — Canonical spec
