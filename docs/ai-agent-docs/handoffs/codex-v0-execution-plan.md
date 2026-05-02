# Codex Handoff — NeuroLift AI Fusion Simulation Environment (V0 Execution Plan)
**Repository:** NeuroLift-Technologies/neurolift-ai-fusion  
**Date:** 2026-02-11  
**From:** ChatGPT (GPT-5.2 Thinking)  
**To:** Codex (Dev Team)  
**Mode:** Planning + execution validation (instrumentation-first)

> **Archive note (2026-05-02):** This is a historical planning handoff imported by PR #44.
> It predates the current full-stack repository structure and should not be treated as an
> implemented API contract. Source-verified current runtime entrypoints are documented in
> `docs/architecture.md`: `src/avatars/base_avatar.py`, `src/aides/base_aide.py`, and
> `src/simulation/session_orchestrator.py`. As of this import, `src/metrics/*` and
> `configs/scenarios/workplace.meeting_dynamics.yaml` do not exist in the repository.

---

## 1) What I noticed (repo + branch reality)

### A) Branch landscape (current active lines)
- `master` (default)
- `cursor/create-simulation-environment-repository-structure-b820` (simulation environment branch)
- `cursor/ai-agent-business-repository-structure-setup-73af`
- `claude/cloudflare-connector-access-018QZhQp8Kg9uucUAvLJB6Jf`

### B) Root README problem: two narratives fused without an index
The current root `README.md` blends:
1) “AI agent business operations” (CFO/CTO/CMO + dashboards + orchestration)
2) “Simulation environment” (Avatar → Aide → Advocate experiential training)

This is strategically fine, but operationally confusing for contributors and agents. It increases mis-scoped PRs and slows execution.

### C) The real technical risk isn’t the concept — it’s **measurable learning**
The simulation vision is strong, but it can degrade into a “story engine” if we don’t ship:
- consequence persistence
- impairment mechanics
- scenario authoring
- telemetry/metrics

So the execution plan must be **telemetry-first**.

---

## 2) The ask (what you’re expected to do)

You are being asked to implement the **minimum runnable vertical slice** of the simulation environment so the team can prove:
- the loop runs end-to-end
- consequences persist
- Aide interventions are integrated
- learning/progress is measurable (even if primitive at first)

The target is:
- **Avatar:** StayAlert
- **Scenario:** workplace.meeting_dynamics
- **Outputs:** JSONL telemetry + per-episode summary + FRI V0

---

## 3) Expected outcome (Definition of Done)

### V0 must demonstrate:
1) A deterministic simulation loop (seeded)
2) Persistent state mutation from failure/success (stress/reputation/backlog)
3) A configurable impairment modifier system (ADHD trait → mechanics)
4) Scenario defined in data (YAML/JSON), not hardcoded
5) NPC interactions including baseline + biased behavior affecting consequences
6) Telemetry artifacts for every run (JSONL + episode summary)
7) A placeholder **Fusion Readiness Index (FRI V0)** computed from telemetry

If you ship that, the project transitions from “vision” to “training system.”

---

## 4) Implementation plan (ordered tasks with acceptance criteria)

### TASK 1 — Core interfaces (base classes)
Create minimal abstract interfaces:
- `src/avatars/base.py`
- `src/aides/base.py`
- `src/simulation/base.py`
- `src/metrics/base.py`

Acceptance:
- `Avatar.observe(state) -> obs`
- `Avatar.act(obs) -> action`
- `Aide.recommend(state, avatar_trace) -> intervention`
- `Simulation.reset(config)`
- `Simulation.step(avatar_action, aide_action)`
- `Metrics.record(step_context)`, `flush()`

---

### TASK 2 — Time + consequence engine
Implement:
- `src/simulation/time.py` (tick scheduler / event queue)
- `src/simulation/consequence.py` (state mutations)

Acceptance:
- Consequences persist across ticks/episodes (e.g., `stress`, `reputation`, `task_backlog`)
- Tick-based loop is deterministic under a seed

---

### TASK 3 — Impairment modifier system (trait → mechanics)
Implement:
- `src/avatars/impairments.py`

Mechanic baseline for StayAlert:
- Attention slip: probabilistic action delay / increased mistake probability / missed cues

Acceptance:
- Configurable via YAML/JSON
- Seeded randomness → reproducible runs

---

### TASK 4 — Scenario authoring DSL (thin YAML)
Create:
- `configs/scenarios/workplace.meeting_dynamics.yaml`

Include:
- actors (avatar, aide, NPCs)
- objectives
- triggers/events
- success/failure conditions

Acceptance:
- Scenario loads and runs without code changes

---

### TASK 5 — NPC baseline + bias behaviors
Implement:
- `src/simulation/npcs.py`

Include:
- Neurotypical NPC baseline (fast completion / fewer errors)
- Biased NPC (unfair evaluation / microaggression events that increase stress or reduce reputation)

Acceptance:
- NPC actions affect consequences in state

---

### TASK 6 — Telemetry + FRI V0
Implement:
- `src/metrics/telemetry.py` (JSONL logging)
- `src/metrics/fri.py` (FRI V0 computation)

FRI V0 (minimum):
- independence rate (tasks completed without aide intervention)
- error recurrence rate
- stress recovery time

Acceptance:
- Each episode writes:
  - step-by-step JSONL
  - episode summary JSON incl. FRI V0

---

### TASK 7 — CLI runner + run artifacts
Implement:
- `scripts/run_training_session.py`

Acceptance:
- Command works:
  - `python scripts/run_training_session.py --avatar stay_alert --scenario workplace.meeting_dynamics --seed 123`
- Writes artifacts to:
  - `data/runs/<timestamp>/`

---

## 5) Repo hygiene changes (do after V0, not before)

**Strong recommendation:** Don’t do a big re-org before V0 runs.

After V0 is working:
- Convert root README into an index
- Move narratives into:
  - `docs/business-agents/README.md`
  - `docs/simulation/README.md`
- Add:
  - `LICENSE`
  - `CODE_OF_CONDUCT.md`
  - `CONTRIBUTING.md`

---

## 6) Branch + PR guidance

A “planning PR” is fine, but the key is to avoid PRs that only move text around.

Preferred flow:
1) Create Issue: “Simulation V0 vertical slice (StayAlert + meeting_dynamics)”
2) Implement Tasks 1–7 on a feature branch (or use the already-created review branch if desired)
3) Open PR with:
   - minimal code + telemetry artifacts
   - brief architecture notes
   - how to run
   - what success looks like

---

## 7) World models note (Fei-Fei Li / “world models” direction)
Josh flagged a parallel path: pursuing “world models” as a broader long-term avenue.

Action for Codex now:
- **Do not** pivot into world-model architecture work in this sprint.
- Design V0 so it’s compatible later:
  - explicit state representation
  - deterministic step transitions
  - clean observation/action interfaces

That makes a future “world model / learned simulator” layer a drop-in replacement for the handcrafted simulation engine.

---

## 8) Final expected deliverable (what success looks like to the team)
When you’re done, Josh should be able to run one command and see:
- a complete simulation run
- consequences changing the state
- an Aide intervening at least once
- JSONL telemetry proving what happened
- an episode summary with FRI V0

That’s the unlock point for expanding scenarios, adding dysfunction injection, and scaling beyond StayAlert.

---

**Signature:** ChatGPT (GPT-5.2 Thinking)  
**Timestamp:** 2026-02-11