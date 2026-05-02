# Open Items Review — neurolift-ai-fusion

**Reviewer:** GitHub Copilot (Task Agent)  
**Session ID:** 502b28d2-4d11-478a-8db5-0ddb6d3e66a5  
**Date:** 2026-05-02  
**Task:** [Open Items for the Next Agent](https://github.com/NeuroLift-Technologies/neurolift-ai-fusion/tasks/68bab7f6-c773-48b4-80e3-b08a63ff36c8?session_id=502b28d2-4d11-478a-8db5-0ddb6d3e66a5)  
**Branch reviewed:** `main` (as of commit `ebead55`)  
**Thread:** TH-007

---

## Purpose

This report captures all open items discovered during the session-start review of `docs/active-threads.md`, the last handoff record, all open PRs, all open GitHub Issues, and all unresolved code-review comments. It is intended as a ready reference for the next agent or human contributor.

---

## 🔴 Blockers (Known, Unresolved)

### B-1 — Root `npm install` broken (mobile peer dependency conflict)

**Source:** TH-006 handoff (`docs/agent-log/handoffs/2026-05-01-codex-main-sync-simulation-lab-handoff.json`)

The root-level `npm install` fails due to a peer dependency conflict between `victory-native`, `@shopify/react-native-skia`, and the expected React version in the mobile workspace. Web-only installs (`npm install --prefix apps/web`) work correctly.

**Impact:** CI cannot run root-level install; full monorepo integration testing is blocked.  
**Suggested action:** Either pin `victory-native` and `@shopify/react-native-skia` to versions compatible with the current React Native version, or split CI into independent web and mobile install flows.

---

### B-2 — `apps/web` npm audit findings (8 vulnerabilities, Next.js 14 security warning)

**Source:** TH-006 handoff

`npm install --prefix apps/web` reports 8 audit findings and a `next@14.2.3` security warning. Dependabot PR #42 proposes upgrading Next.js to 15.5.15.

**Impact:** Known security exposure in the web app dependency tree.  
**Suggested action:** Review and merge PR #42, or manually upgrade `next` and address the remaining findings.

---

## 🟡 Decisions Pending (from TH-006 Handoff)

| ID | Decision | Notes |
|----|----------|-------|
| D-1 | Whether to upgrade Next.js and address npm audit findings | PR #42 (Dependabot) is open and ready to review |
| D-2 | Whether to resolve the mobile peer dependency conflict or split web/mobile CI install flows | No blocker to making the split now |
| D-3 | Whether to push `codex-cli/local-simulation-lab-before-main-sync` to remote for archival, or delete as superseded | Currently local-only |

---

## 🟠 Open Pull Requests (13 total as of 2026-05-02)

| # | Title | State | Priority | Recommended Action |
|---|-------|-------|----------|--------------------|
| **#43** | Add neurolift-ai-fusion workspace file | Draft | High | Fix Cloudflare build failure; mark non-draft once resolved |
| **#42** | Bump next 14→15 (Dependabot) | Open | High | Review and merge (resolves B-2 above) |
| **#41** | [CURSOR] docs: align PR #37 monorepo runbooks | Draft | Medium | Review, consolidate with #38, merge or close |
| **#38** | docs: document full-stack monorepo workflow | Draft | Medium | May overlap with #41 — consolidate and merge or close |
| **#36** | [CURSOR] docs: align agent log + Cloudflare runbooks | Draft | Medium | Review and merge or close |
| **#34** | [CURSOR] docs: Cloudflare API probe workflow | Draft | Low | May overlap with #27/#26 — consolidate and close duplicates |
| **#32** | feat: full-stack web + mobile app | Open | High | 9 unresolved review comments (see section below); needs rebase onto current `main` |
| **#29** | [CURSOR] docs: agent onboarding registration | Draft | Low | Review and merge or close |
| **#28** | [GPT] docs: fusion runtime contracts | Draft | Low | Review and merge or close |
| **#27** | [GPT] docs: Cloudflare API probe workflow | Draft | Low | Likely duplicate of #26/#34 — close |
| **#26** | [CODEX] docs: Cloudflare API access probe | Draft | Low | Likely duplicate of #27/#34 — close |
| **#25** | docs: governance sync workflow reference | Draft | Low | Review and merge or close |
| **#23** | [CODEX] docs: runtime examples + agent-log samples | Open | Medium | Review and merge or close |

> **Note on doc PRs #23–#29, #34, #36, #38, #41:** These are all documentation-only draft PRs opened by bot agents. A cleanup pass to merge the substantive ones and close duplicates would reduce noise significantly.

---

## 🔵 Unresolved Code-Review Comments on PR #32

All 9 comments are from **Gemini Code Assist**, dated 2026-04-25. None are resolved or outdated.

### 🔴 High Priority (will cause installation failures)

| # | File | Line | Issue | Suggested Fix |
|---|------|------|-------|---------------|
| C-1 | `apps/web/package.json` | 16 | Hallucinated versions for `axios`, `react`, `react-dom`, `react-router-dom` | `axios@^1.7.8`, `react@^19.0.0`, `react-dom@^19.0.0`, `react-router-dom@^7.1.3` |
| C-2 | `apps/web/package.json` | 32 | Invalid `typescript` (8.x) and `vite` (7.x) versions | `typescript@~5.7.2`, `vite@^6.0.0` |
| C-3 | `apps/mobile/package.json` | 18 | Non-existent Expo SDK 54, Router 6, React Native 0.81 | `expo@~52.0.0`, `expo-router@~4.0.0`, `react-native@0.76.0`, `react@18.3.1` |

> **Note:** C-1 through C-3 are in the `feat/fullstack-web-mobile-app` branch (PR #32), **not** in `main`. The current `main` web app (`apps/web/`) was rebuilt from scratch by TH-003/TH-004 with correct dependency versions. These comments apply only to the `feat/fullstack-web-mobile-app` branch.

### 🔴 High Priority (security)

| # | File | Line | Issue | Suggested Fix |
|---|------|------|-------|---------------|
| C-4 | `backend/app/main.py` | 27 | CORS `allow_origins=["*"]` — wildcard allows any origin | Restrict to `["http://localhost:5173", "http://localhost:8081"]` for dev; use env var for prod origins |

### 🟡 Medium Priority (code quality / Python 3.12 compatibility)

| # | File | Line | Issue | Suggested Fix |
|---|------|------|-------|---------------|
| C-5 | `backend/app/routers/fusion.py` | 9 | `import random` inside function; missing `timezone` import | Move `import random` to top level; add `from datetime import datetime, timezone` |
| C-6 | `backend/app/routers/fusion.py` | 58 | Second `import random` inside function (PEP 8 violation) | Remove; already imported at top after C-5 fix |
| C-7 | `backend/app/routers/fusion.py` | 72 | `datetime.utcnow()` deprecated in Python 3.12+ | Replace with `datetime.now(timezone.utc)` |
| C-8 | `backend/app/routers/scenarios.py` | 6 | Missing `Optional` in `typing` import | Add `Optional` to existing import |
| C-9 | `backend/app/routers/scenarios.py` | 108 | `category` parameter missing `Optional[str]` type hint | Change to `async def list_scenarios(category: Optional[str] = None)` |

---

## 📋 Open GitHub Issues

| # | Title | Recommended Action |
|---|-------|-------------------|
| **#40** | "milestone achieved" (auto-created by bot) | Safe to close — documents a prior agent's failed merge conflict attempt that is now superseded |
| **#39** | Code Review (auto-created by bot) | Safe to close — duplicates the Gemini review comments on PR #32; address at PR level |

---

## 📊 Prioritised Work Queue for Next Agent

Recommended order of attack:

1. **Merge PR #42** (Dependabot Next.js bump) — resolves B-2, low risk, automated.
2. **Fix mobile peer dependency conflict** (B-1) — unblocks root CI; investigate `victory-native` + `@shopify/react-native-skia` version alignment.
3. **Address PR #32 review comments** (C-1 through C-9) — fix the `feat/fullstack-web-mobile-app` branch so it can be merged.
4. **Close open GitHub Issues #39 and #40** — housekeeping.
5. **Consolidate doc draft PRs** (#23–#29, #34, #36, #38, #41) — merge substantive ones, close duplicates.
6. **Decide on D-3** (backup branch archival) — low effort, keeps remote clean.

---

## 📌 Agent Conventions Reminder

- **Next thread ID:** TH-007 (this session) → next = **TH-008**
- **Commit format:** `[AGENT_NAME] type(scope): description`
- **Register** at session start in `docs/agent-log/registrations/`
- **Handoff** at session end in `docs/agent-log/handoffs/`
- Escalate any architectural or deployment decisions to Joshua W. Dorsey, Sr. before proceeding
