# Governance Restoration Audit Log — 2026-05-28

**Agent:** Claude Code
**Session ID:** CLAUDE-2026-05-28-governance-docs-restore
**Branch:** `claude/governance-docs-restore-yB5sI`
**Thread:** TH-014
**OTOI Version:** ORG-DEV-OTOI-1.0.0
**Repo:** NeuroLift-Technologies/neurolift-ai-fusion

---

## Summary

This change **supersedes PR #75** (Copilot's governance cleanup) and restores
org-level framing that PR #75 over-trimmed via a global find/replace from
`.github-private` to `neurolift-ai-fusion`. It is part of a coordinated
11-repo cleanup tracked in `NeuroLift-Technologies/nlt-agent-1#4`.

This change **does not** touch PR #74 (Antigravity stubs), which is out of
scope for this restoration.

---

## What changed

### Universal matrix — kept from PR #75

- README.md — added the `ai_assistant_directive` YAML block.
- `.nltotoi/README.md`, `.nltotoi/index/governance-files.md`,
  `.nltotoi/proposals/validation-roadmap.md` — scoped from `.github-private`
  to `neurolift-ai-fusion` (local scope only).
- `.nltotoi/scripts/validate-governance.sh` — updated repo name string only.
- `nltotoi.json` — `repository.name` flipped to local repo. Preserved
  `public_governance` URL (canonical `.github`), `visibility: private`, and
  `purpose` string.
- `docs/agent-log/README.md`, registrations, handoffs — preserved audit
  files added by PR #75 (Antigravity, Codex TH-012).
- `docs/active-threads.md` — added TH-012, TH-013, TH-014 rows; bumped
  Last updated to 2026-05-28.
- `.gitignore` — added `output/playwright/` ignore.
- `prototypes/world-engine/index.html` — kept the inline favicon improvement.

### Universal matrix — preserved against PR #75 over-trimming

- `NLT-DEV-OTOI.md` — kept the org-wide framing intact. PR #75 rewrote
  the scope and repository headers; that change is **rejected**.
- `AGENTS.md` — PR #75 added a new repo-scoped version. We instead restored
  the canonical version from `archive/ai-agent-docs/AGENTS.md` (see below).
- `CLAUDE.md` — same: restored the canonical archive version, not PR #75's
  new minimal version.
- All other org-wide files (`file-structure.md`, `SOPs/*`, `agents/*`,
  `templates/*`, `docs/escalations/README.md`) are unchanged.

### Per-repo extra — archive recovery

The canonical governance files `CLAUDE.md` and `AGENTS.md` had been
incorrectly moved to `archive/ai-agent-docs/` and were missing from the
repo root. Since no root copies existed, this change moves them back:

- `git mv archive/ai-agent-docs/CLAUDE.md CLAUDE.md`
- `git mv archive/ai-agent-docs/AGENTS.md AGENTS.md`

The archive directory still contains `agent-log/`, `ai-guidance/`, and
`reviews/` — those are intentionally left in place.

### SOP upgrade

- `SOPs/repo-governance-setup.md` upgraded from v1.0.0 to v1.1.0 from
  the canonical source at `NeuroLift-Technologies/.github-private`.

---

## What is out of scope

- PR #74 (Antigravity stubs) — explicitly untouched.
- Any code, app, or infrastructure change beyond governance/audit files.

---

## Validation

The repo-local validator at `.nltotoi/scripts/validate-governance.sh`
was run in `--strict` mode after edits. See PR description for results.

---

## Files changed (high level)

- Restored from archive: `CLAUDE.md`, `AGENTS.md`
- Modified: `README.md`, `nltotoi.json`, `.nltotoi/README.md`,
  `.nltotoi/index/governance-files.md`,
  `.nltotoi/proposals/validation-roadmap.md`,
  `.nltotoi/scripts/validate-governance.sh`,
  `SOPs/repo-governance-setup.md`, `docs/active-threads.md`,
  `.gitignore`, `prototypes/world-engine/index.html`
- New: `docs/agent-log/README.md`,
  `docs/agent-log/handoffs/.gitkeep`,
  `docs/agent-log/registrations/.gitkeep`,
  `docs/agent-log/registrations/ANTIGRAVITY-2026-05-27-governance-alignment.json`,
  `docs/agent-log/registrations/CODEX-2026-05-27-world-engine-working-prototype.json`,
  `docs/agent-log/handoffs/2026-05-27-ANTIGRAVITY-governance-alignment.json`,
  `docs/agent-log/handoffs/CODEX-2026-05-27-world-engine-working-prototype-handoff.json`,
  `docs/agent-log/2026-05-28-claude-governance-restoration.md` (this file)
