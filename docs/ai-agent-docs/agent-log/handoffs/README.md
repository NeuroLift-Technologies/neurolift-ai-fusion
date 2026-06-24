# Archived Agent Handoff Records

This directory stores historical handoff JSON files that were imported with
older AI-agent documentation.

For current work, write new session-end handoffs to:

```text
docs/agent-log/handoffs/
```

Do not add new files here unless you are preserving or migrating a legacy
artifact.

## Purpose

Handoff records preserve session continuity for the next agent by capturing:

- what was completed,
- what remains,
- blockers/escalations,
- and the exact branch/context needed to continue.

In this archive path, use existing records as historical context only. Verify any
branch, PR, or workflow details against the current `docs/agent-log/` record set
before treating them as active state.

## File Naming Convention (Repository Usage)

```
{AGENT_NAME}-{YYYY-MM-DD}-{scope}-handoff.json
```

## Example

```
CLAUDE-2026-04-05-pull-fusion-files-handoff.json
```

If your automation runtime imposes a different filename format, follow that runtime
requirement; otherwise use the repository convention above for discoverability.

## Record Structure (handoff-record.json)

See SOP-NLT-001 Step 8 for the full `handoff-record.json` schema. Current records
in this repository include these top-level fields:

- `agent_name`
- `session_id`
- `session_end`
- `task_scope`
- `work_completed`
- `work_not_completed`
- `blockers`
- `next_steps`
- `files_changed`
- `branch`
- `pr_url`
- `escalations_filed`
- `otoi_version`

## Writing Guidance

1. Keep `work_completed` and `work_not_completed` actionable and specific.
2. Record blockers as concrete constraints (tool scope, missing access, failing interface, etc.).
3. Include reproducible `next_steps` commands where possible.
4. List every changed file path in `files_changed`.
5. Use UTC timestamps (`YYYY-MM-DDTHH:MM:SSZ`) for consistency across agents.

## Governance

Governed by ORG-DEV-OTOI-1.0.2 Section 5. No session ends without a handoff record.
