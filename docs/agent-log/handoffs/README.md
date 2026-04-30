# Agent Handoff Records (`docs/agent-log/handoffs/`)

This directory is the **current** location for session-end handoff artifacts under SOP-NLT-001.

Use this folder for handoffs that summarize what an agent completed, what remains, and what the next agent needs to continue safely.

## When to write a handoff

Write a handoff JSON file whenever an agent session ends, including:

- normal completion
- partial completion with remaining work
- blocked work that requires escalation or new access

## File naming

Use a date-first filename so records sort chronologically.

Recommended pattern:

```text
{AGENT}-{YYYY-MM-DD}-{short-task-name}-handoff.json
```

Example from this repository:

```text
CLAUDE-2026-04-05-pull-fusion-files-handoff.json
```

## Minimum content checklist

The authoritative schema is defined in SOP-NLT-001 Step 8 (`handoff-record.json`).  
At minimum, include fields that let another contributor resume work without guesswork:

- `agent_name`, `session_id`, `session_end`
- `task_scope`
- `work_completed` (what is done)
- `work_not_completed` (what still needs work)
- `blockers` (if any)
- `next_steps` (ordered, executable)
- `files_changed`
- `branch`, `pr_url` (or `null` if none)

## Common pitfalls

- **Writing to the wrong directory:** new handoffs belong in `docs/agent-log/handoffs/`; `docs/ai-agent-docs/handoffs/` is the legacy archive.
- **Missing resumability details:** include exact file paths, command hints, and branch names in `next_steps`.
- **Silent blockers:** if access, policy, or scope prevents completion, record it explicitly in `blockers`.

## Related docs

- `docs/agent-log/registrations/README.md` (session start records)
- `docs/ai-agent-docs/handoffs/README.md` (legacy handoff archive guidance)
- `docs/active-threads.md` (current thread ownership and status)
