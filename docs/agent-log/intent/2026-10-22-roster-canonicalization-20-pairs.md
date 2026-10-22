# Intent Log Entry

**Date:** 2026-10-22T13:00:00Z  
**Agent:** Claude (Claude Code, Sonnet 5.5)  
**Session:** agent/claude-roster-canonicalization-20  
**OTOI Version:** ORG-DEV-OTOI-1.0.0  
**Working repo:** NeuroLift-Technologies/neurolift-ai-fusion (plus sibling repo `nlt-fusion`, same branch name)

---

### Action

Make the README roster canonical across both repos: 20 Avatar-Aide-Advocate pairs, 14 Executive Function and 6 Non-Executive Function, with the README names.

1. `prototypes/world-engine/data.js`: replace the 19-avatar roster with the 20 README entries. Rebuild `AVATARS`, `AIDES`, and `STRATEGIES` (keyed by `flavor`). Keep the contract: every `avatar.id` has an `AIDES` entry, every `avatar.flavor` is a `STRATEGIES` key, every `scenario.room` is a `ROOMS` id.
2. Count and name fixes (19 -> 20): `prototypes/world-engine/README.md`, `docs/architecture.md`, `docs/game-engine-vertical-slice.md`, `IMPLEMENTATION-COMPLETE.md`, and the directly coupled `prototypes/world-engine/hud.jsx` ("AVATAR FLEET") and `docs/specs/world-engine-prototype-schema.md` (roster table).
3. In `nlt-fusion`: `ONBOARDING.md`, `web/index.html`, `web/nlt-world-engine.html`, `world-engine-godot/RENDERER-PLAN.md`, `ART-PIPELINE.md`, `assets/characters/PIPELINE-PROBE.md`, `ARCHITECTURE.md`, `DEPLOYMENT.md`.

Not touched: `docs/agent-log/**` (other than adding this entry and a handoff), `archive/`, `_archive/`, `docs/active-threads.md` TH-016, `chatgpt-init-review.md`, `nlt-fusion/docs/escalations/**`, `.claude/`, `mcp-config.yaml`, any Vercel or production setting.

---

### Rationale

Joshua W. Dorsey, Sr. decided on 2026-10-22 that the README roster is canonical and every other source changes to match (Pair Roster Canonicalization Brief, 2026-10-22). This entry cites that decision as the approval. It is a broad-scope change across many files plus a data rebuild, so OTOI section 7 requires logging intent first.

Work is done on a fresh branch from `origin/main`, in separate worktrees, because `pr-125` is behind `main` and still carries the stale 19-pair web UI strings.

---

### Risks

- `data.js` is consumed by `sim.jsx`, `app.jsx` and `hud.jsx`. A broken cross-reference would break the prototype at load. Mitigation: load `data.js` in Node and check the contract before committing.
- The 18 non-Python avatars are design proposals. Traits, blurbs and aide pairings are authored here from the README descriptions and are open to Josh's review.
- Edits to deployed `nlt-fusion/web/*.html` pages. Mitigation: check deployment status first and keep edits to text only.

---

### Alternatives Considered

1. **Fix only the count (19 -> 20) in `data.js`** — Not chosen: 14 of the 19 names are not in the README, so a count fix would leave the wrong roster.
2. **Work on `pr-125` directly** — Not chosen: it is behind `main` and would mix this change into an unrelated PR.

---

### Escalation Needed

**no**

No change to Avatar or Aide base class interfaces, no new integration, schema, RLS, or provider change. Nothing here touches production. Any Vercel production change still needs Josh's explicit go-ahead and is out of scope.

---

### Outcome

**Date completed:** 2026-10-22  
**Result:** Roster rebuilt and counts fixed in both repos as planned; `data.js` contract verified in Node. Committed locally on `agent/claude-roster-canonicalization-20` in both repos; nothing pushed.  
**Deviations from plan:** Also fixed `BUILD-SUMMARY.md`, `DEPLOYMENT.md` line 297, and `RENDERER-PLAN.md` line 226 (same stale count, not listed in the brief). Worked from `origin/main` because `pr-125` is behind it. See `docs/agent-log/handoffs/CLAUDE-2026-10-22-roster-canonicalization-handoff.json`.
