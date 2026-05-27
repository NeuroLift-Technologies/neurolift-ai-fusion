# `.claude/hooks/` — Session Lifecycle Hooks

**Governed by:** ORG-DEV-OTOI-1.0.0

| File | Lifecycle event | Purpose |
|---|---|---|
| `session-start.sh` | `SessionStart` (startup, resume, clear, compact) | Prints OTOI mandatory reading order and verifies governance file presence. Always exits 0. |

Hooks are wired in `.claude/settings.json` under `hooks.SessionStart`. The matcher `"*"` runs the hook on every session-start event.

**Do not edit this hook here** — it is synced from `.github-private/.claude/hooks/`. For repo-specific additions, use `.claude/settings.local.json`.
