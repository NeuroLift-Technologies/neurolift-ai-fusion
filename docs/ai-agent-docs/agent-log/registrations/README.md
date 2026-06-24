# Archived Agent Registration Records

This directory stores historical agent registration JSON files that were imported
with older AI-agent documentation.

For current work, write new session-start records to:

```text
docs/agent-log/registrations/
```

Do not add new files here unless you are preserving or migrating a legacy
artifact.

## Intent

Registration records make active ownership explicit before any implementation
work begins. They support thread coordination in `docs/active-threads.md` and
prevent overlapping work by multiple agents.

In this archive path, use existing records as historical context only. Verify any
branch, PR, or workflow details against the current `docs/agent-log/` record set
before treating them as active state.

## File naming convention

Use:

```
{AGENT_NAME}-{YYYY-MM-DD}-{short-session-scope}.json
```

Example:

```
CODEX-2026-04-24-docs-sync-session.json
```

## Minimum record fields

Until the formal schema file is added to this repository, include at least:

- `agent_name`
- `session_id`
- `session_start` (ISO timestamp)
- `task_scope`
- `branch`
- `thread_id` (or `null` if not yet assigned)
- `otoi_version`

If available in your runtime, also include:

- `trigger_context` (automation/webhook metadata)
- `related_pr` (URL or PR number)

## Workflow

1. Read required governance docs (`.github-private/NLT-DEV-OTOI.md`,
   `AGENTS.md`, `CLAUDE.md`, `docs/active-threads.md`).
2. Create registration JSON in `docs/agent-log/registrations/`.
3. Add/update an entry in `docs/active-threads.md`.
4. Continue implementation work.

## Governance

Governed by ORG-DEV-OTOI-1.0.2 Section 3.
