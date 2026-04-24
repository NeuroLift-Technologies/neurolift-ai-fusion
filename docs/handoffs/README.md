# Legacy Handoff Archive (`docs/handoffs/`)

This directory stores **legacy handoff artifacts** created before the SOP-NLT-001
`docs/agent-log/*` structure was adopted.

## Status of this directory

- Keep existing files for historical traceability.
- Do not use this folder for new standard session-end handoffs.
- Write new session handoffs to `docs/agent-log/handoffs/`.

## Why this folder still receives files occasionally

Some automation flows and older prompts still reference `docs/handoffs/`.
For example, PR #18 added:

- `docs/handoffs/handoff_copilot_repo_access_confirmed.json`

That file is valid as a historical record, but new handoff work should follow
the current SOP path in `docs/agent-log/handoffs/`.

## Migration guidance for maintainers

When you touch legacy automation or prompts:

1. Update path references from `docs/handoffs/` to `docs/agent-log/handoffs/`.
2. Keep old files in place unless there is an explicit archival/migration plan.
3. Ensure `docs/active-threads.md` and agent docs point to the same target path.

## Related docs

- `docs/agent-log/handoffs/README.md` (current handoff runbook)
- `docs/agent-log/registrations/README.md` (session start records)
- `AGENTS.md` (coordination and onboarding requirements)
