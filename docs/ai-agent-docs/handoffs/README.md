# Legacy Handoff Archive (`docs/ai-agent-docs/handoffs/`)

This directory stores **legacy handoff artifacts** created before the SOP-NLT-001
`docs/agent-log/*` structure was adopted.

## Status of this directory

- Keep existing files for historical traceability.
- Do not use this folder for new standard session-end handoffs.
- Write new session handoffs to `docs/agent-log/handoffs/`.
- Treat planning artifacts in this archive as historical context unless they
  explicitly cite current source paths verified in the active branch.

## Recently archived planning artifacts

PR #44 moved two February 2026 AI-to-agent planning artifacts into this archive:

| File | Purpose | Current-use guidance |
| --- | --- | --- |
| `chatgpt-init-review.md` | Initial repository review and Codex-ready planning notes | Use as strategic context only; branch names and recommended paths predate the current monorepo layout. |
| `codex-v0-execution-plan.md` | V0 simulation vertical-slice task plan | Verify against `src/avatars/base_avatar.py`, `src/aides/base_aide.py`, and `src/simulation/session_orchestrator.py` before implementation. |

As of 2026-05-02, no `src/metrics/` package or `configs/scenarios/` DSL exists in
this branch. The current source-verified runtime contracts remain documented in
`docs/architecture.md`.

## Why this folder still receives files occasionally

Some automation flows and older prompts still reference `docs/handoffs/`.
For example, PR #18 added:

- `docs/ai-agent-docs/handoffs/handoff_copilot_repo_access_confirmed.json`

That file is valid as a historical record, but new handoff work should follow
the current SOP path in `docs/agent-log/handoffs/`.

## Migration guidance for maintainers

When you touch legacy automation or prompts:

1. Update path references from `docs/ai-agent-docs/handoffs/` to `docs/agent-log/handoffs/`.
2. Keep old files in place unless there is an explicit archival/migration plan.
3. Ensure `docs/active-threads.md` and agent docs point to the same target path.

## Related docs

- `docs/agent-log/handoffs/README.md` (current handoff runbook)
- `docs/agent-log/registrations/README.md` (session start records)
- `AGENTS.md` (coordination and onboarding requirements)
