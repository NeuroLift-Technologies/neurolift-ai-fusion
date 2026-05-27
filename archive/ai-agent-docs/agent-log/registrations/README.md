# Agent Registration Records

This directory stores agent registration JSON files created at the start of each
agent session.

## Intent

Registration records make active ownership explicit before any implementation
work begins. They support thread coordination in `docs/active-threads.md` and
prevent overlapping work by multiple agents.

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

## Minimal example

```json
{
  "agent_name": "CODEX",
  "session_id": "automation-158b2152-7214-45b1-9efe-a458133e75b6",
  "session_start": "2026-04-24T15:30:00Z",
  "task_scope": "Update runtime and runbook documentation after merged PR review",
  "branch": "cursor/codebase-documentation-alignment-f6f9",
  "thread_id": null,
  "otoi_version": "ORG-DEV-OTOI-1.0.0",
  "trigger_context": {
    "event_type": "pull_request",
    "action": "closed",
    "pr_number": 22
  },
  "related_pr": "https://github.com/NeuroLift-Technologies/neurolift-ai-fusion/pull/22"
}
```

Use this as a baseline payload, then add any runtime-specific metadata required by
your automation environment.

## Workflow

1. Read required governance docs:
   - `NLT-DEV-OTOI.md` from the repository root (synced copy)
   - `AGENTS.md`
   - `CLAUDE.md`
   - `docs/active-threads.md`
2. If root `NLT-DEV-OTOI.md` is missing, record that blocker in your
   registration and request/trigger the **Sync Governance (Public)** workflow
   (`.github/workflows/sync-governance-public.yml`) to refresh the synced copy
   from `NeuroLift-Technologies/.github-private`.
3. Create registration JSON in this directory.
4. Add/update an entry in `docs/active-threads.md`.
5. Continue implementation work.

## Governance

Governed by ORG-DEV-OTOI-1.0.0 Section 3.
