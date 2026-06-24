# Agent Log

This directory stores current agent coordination records per
ORG-DEV-OTOI-1.0.2.

PR #76 restored this current `docs/agent-log/` tree alongside root
`AGENTS.md` and `CLAUDE.md`. Use it for active work in this repository.
Archived AI-agent notes remain under `docs/ai-agent-docs/` and
`archive/ai-agent-docs/`; treat those as historical context only unless current
source files confirm the same behavior.

## Directory contract

| Path | Purpose | Source schema |
| --- | --- | --- |
| `registrations/` | Session-start self-registration records | `templates/agent-registration.json`, OTOI Section 3 |
| `handoffs/` | Session-end handoff records | `templates/handoff-record.json`, OTOI Section 5 |

Recommended file names are date/agent scoped so records sort and remain easy to
trace:

```text
docs/agent-log/registrations/{AGENT}-{YYYY-MM-DD}-{short-scope}.json
docs/agent-log/handoffs/{AGENT}-{YYYY-MM-DD}-{short-scope}-handoff.json
```

Repository examples:

```text
docs/agent-log/registrations/CODEX-2026-05-27-world-engine-working-prototype.json
docs/agent-log/handoffs/CODEX-2026-05-27-world-engine-working-prototype-handoff.json
```

## Session workflow

1. Read `NLT-DEV-OTOI.md`, `AGENTS.md`, `CLAUDE.md`, and
   `docs/active-threads.md`.
2. Create one registration JSON file in `registrations/` before making changes.
3. Add or update the relevant row in `docs/active-threads.md` with owner,
   branch, status, and thread ID.
4. During work, keep active-thread status accurate when scope or blockers change.
5. Before ending the session, create one handoff JSON file in `handoffs/`, move
   the thread to the Completed Threads table when complete, and link the handoff.

## Registration checklist

Each registration should follow `templates/agent-registration.json` and include:

- `agent_name`, `platform`, `version`, and `session_id`
- `entry_date`, `entry_point`, `working_repo`, and `working_branch`
- `acknowledged_otoi: true` and `otoi_version: "ORG-DEV-OTOI-1.0.2"`
- capabilities, limitations, and preferred handoff format

## Handoff checklist

Each handoff should follow `templates/handoff-record.json` and include:

- completed work and any remaining work
- blockers, decisions made, decisions pending, and escalations
- exact files modified
- validation commands in `tests_run`
- `tests_passing` that reflects the validation actually run
- `pr_url` when a pull request exists

Use empty arrays for fields with no entries. Do not omit required fields.

## Common pitfalls

- Do not write new records to `docs/ai-agent-docs/agent-log/`,
  `docs/ai-agent-docs/handoffs/`, `archive/ai-agent-docs/`, or legacy
  `docs/handoffs/` paths.
- Do not mark `tests_passing` true when no validation ran or when validation was
  skipped; explain skipped validation in `tests_run` or `next_agent_notes`.
- Do not leave `docs/active-threads.md` showing active ownership after the
  session is complete.
- Do not modify `NLT-DEV-OTOI.md` or governance authority language without the
  formal escalation/amendment process.
