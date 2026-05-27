# `.claude/` — Claude Code Session Governance

**Synced from:** `NeuroLift-Technologies/.github-private` (canonical)
**Governed by:** ORG-DEV-OTOI-1.0.0 | Solidarity Framework | HAIEF
**Authority:** Joshua W. Dorsey, Sr.

---

## DO NOT EDIT FILES HERE

This directory is a **synced copy** of the canonical template in `NeuroLift-Technologies/.github-private/.claude/`. The `governance-auto-propagate.yml` workflow overwrites this directory whenever upstream changes.

**To change session governance:** open a PR against `.github-private/.claude/`. Once merged, the next propagation run will open a sync PR here.

**For repo-specific overrides:** create `.claude/settings.local.json` in this repo. The propagation workflow never touches that file.

---

## What This Directory Provides

When a Claude Code session starts in this repo:

1. **SessionStart hook** (`hooks/session-start.sh`, wired via `settings.json`) prints the OTOI mandatory reading order and validates that `NLT-DEV-OTOI.md`, `AGENTS.md`, `CLAUDE.md`, and `nltotoi.json` exist.
2. **Subagents** (`agents/`) are available via subagent dispatch: `nlt-governance-steward`, `nlt-code-reviewer`, `swe-agent`.
3. **Skills** (`skills/`) are loadable on demand: `nlt-otoi`, `nlt-agent-registration`, `nlt-handoff-record`, `nlt-escalation`, `nlt-intent-log`, `nlt-commit-format`, `nlt-incident-response`.
4. **Slash commands** (`commands/`):
   - `/register-session` — file agent self-registration (OTOI §3)
   - `/handoff` — write session handoff (OTOI §5)
   - `/escalate <topic>` — file an escalation (OTOI §4.3)
   - `/intent-log <topic>` — log intent before significant action (OTOI §7)
   - `/governance-check` — run `validate-governance.sh`

---

*Synced from `NeuroLift-Technologies/.github-private` | ORG-DEV-OTOI-1.0.0*
