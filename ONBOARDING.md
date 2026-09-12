# 🚀 3-Minute Onboarding: neurolift-ai-fusion

> Read this first. Understand this repo in 3 minutes. Then go deeper with README.md or QUICKSTART.md.

---

## What Is This?

**NeuroLift AI Fusion** is the **intelligence + platform** layer of the Avatar-Aide-Advocate system. It owns everything about how Avatars *think*, how Aides *coach*, and how humans *interact* with the training system.

The **environment** — the world, rooms, objects, NPCs, and the authoritative deterministic simulation runtime — lives in [`nlt-world-engine`](https://github.com/NeuroLift-Technologies/nlt-world-engine), now driven by the **UE 5.8 Unreal WorldEngine**. This repo owns the brains that plug into that world.

If `nlt-world-engine` is the **Sims game**, this repo is the **AI mod + the web/mobile app wrapper**.

---

## The 4 Stacks

This repo has **four runnable surfaces**. Know which one you're in.

### 🐍 `src/` — Python Simulation Engine (The Intelligence)

```
What:     Python AI simulation — ADHD trait models, Aide coaching, training loop, fusion.
Why:      The brains. This is where Avatars learn and Aides coach.
Run:      python3 -m compileall src scripts   # syntax check
Tests:    pytest tests/test_simulation/test_session_orchestrator.py
```

**Core modules:**

| Module | What it does |
|--------|--------------|
| `src/avatars/` | ADHD trait models (BaseAvatar, StayAlertAvatar, TaskKickstartAvatar, etc.) — eachAvatar's `get_adhd_trait_impact()` defines how its trait affects task performance |
| `src/aides/` | Aide coaching logic (BaseAide) — `get_expertise_strategies()`, `get_real_world_insights()` |
| src/fusion/` | Fusion engine — combines Avatar's lived experience + Aide's expertise → Advocate |
| `src/simulation/session_orchestrator.py` | **Active API** — `SessionOrchestrator`, `SessionConfig`, `SessionResult` |
| `src/simulation/environment/scenarios.py` | Scenario library (workplace, personal, social, academic) |
| `src/core/events.py` | EventBus — the message bus between Avatars, Aides, and the engine |
| `src/database/supabase_client.py` | Supabase persistence (optional; works without it) |

**Key classes you'll hit first:**

```python
# The seam — plug a custom Avatar/Aide into the orchestrator:
orchestrator = SessionOrchestrator(avatar, aide, SessionConfig(...))
result = orchestrator.run_session(scenarios)
```

> **Known issue:** `scripts/test_training_loop.py` fails at `CoachingContext` signature mismatch. Use `SessionOrchestrator` directly as the stable API. See `QUICKSTART.md` for the verified smoke test.

---

### 🌐 `apps/web/` — Next.js Frontend

```
What:     Next.js web surface. Pair directory, dashboards, simulation-lab.
Why:      Humans interact with the training system through this.
Run:      cd apps/web && pnpm install --frozen-lockfile && pnpm dev
→          http://localhost:3000
```

**JS dependency boundaries:**
| Path | Lockfile | Use for |
|------|----------|---------|
| `apps/web/` | `pnpm-lock.yaml` | Next.js web + `/simulation-lab` |
| `apps/mobile/` | `package-lock.json` | Expo mobile starter |
| `cloudflare-engine/` | `package-lock.json` | World Engine Worker + local Wrangler |

---

### 📱 `apps/mobile/` — Expo (React Native)

```
What:     Expo mobile app. Same training system on iOS & Android.
Run:      cd apps/mobile && npm install && npx expo start
```

---

### ⚡ `apps/api/` — FastAPI Backend

```
What:     Python FastAPI. REST API that wraps the simulation engine.
Run:      cd apps/api && pip install -r requirements.txt && uvicorn main:app --reload
→          http://localhost:8000/docs
```

---

### ☁️ `cloudflare-engine/` — Cloudflare Workers

```
What:     Cloudflare Worker backend. Durable Objects for per-pair state, WebSocket fan-out.
Why:      Scales to 19+ pairs at ~$34/month. Real-time observer streaming.
Run:      cd cloudflare-engine && npm ci && npx wrangler dev
```

> **Note:** The Cloudflare Durable Objects here are the **web/observer + pair-state layer**, not the authoritative simulation runtime. The simulation world itself (rooms, objects, NPCs, tick loop) is now the **UE 5.8 WorldEngine** in [`nlt-world-engine`](https://github.com/NeuroLift-Technologies/nlt-world-engine). See [`WorldEngine/docs/architecture/`](https://github.com/NeuroLift-Technologies/nlt-world-engine/tree/main/WorldEngine/docs/architecture) for the authoritative architecture (Fusion owns semantic reality, Unreal owns physical reality).

See `ARCHITECTURE.md` in `nlt-world-engine` for the MMO topology (one Durable Object per pair, WebSocket observers, Vercel + Cloudflare split).

---

## How Training Works

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        TRAINING LOOP                                    │
│                                                                         │
│   ┌──────────────┐  attempt     ┌──────────────────────────────────┐   │
│   │   Avatar     │ ──────────► │         SCENARIO                  │   │
│   │ (ADHD trait) │             │  (from nlt-world-engine — UE WorldEngine)  │   │
│   └──────┬───────┘             └───────────────┬──────────────────┘   │
│          │                                      │ result                │
│          │ observes                             ▼                       │
│          │                             ┌──────────────────┐            │
│          │                             │   Aide evaluates  │            │
│          │                             │   struggle, picks │            │
│          │                             │   coaching strat  │            │
│          │                             └────────┬─────────┘            │
│          │                                      │ coaching              │
│          ◄──────────────────────────────────────┘                       │
│          │                                                              │
│          ▼                                                              │
│   Independence ↑  →  Bond ↑  →  Fusion Ready  →  Advocate             │
└─────────────────────────────────────────────────────────────────────────┘
```

**The 19 pairs** (16 executive function + 3 non-executive):

| Trait | Avatar | Aide Expertise |
|-------|--------|----------------|
| StayAlert | Sustained attention deficit | Attention coaching (Pomodoro, chunking) |
| ImpulseGuard | Impulsivity control | Impulse regulation strategies |
| FocusFlow | Hyperfocus management | Focus modulation |
| Timely | Time blindness | Time awareness training |
| MemoryMate | Working memory deficits | Memory scaffolding |
| MoodEase | Emotional regulation | Emotional coaching |
| TaskKickstart | Task initiation difficulty | Activation strategies |
| CalmCore | Low frustration tolerance | Frustration tolerance building |
| Planner Pro | Prioritization and planning | Planning systems |
| SmoothSwitch | Transition difficulties | Transition rituals |
| AwareMate | Self-monitoring challenges | Metacognitive strategies |
| SteadyMind | Poor impulse control | Impulse regulation |
| FocusRecharge | Effortful focus fatigue | Energy management |
| EffortAlign | Effort vs. productivity perception | Effort calibration |
| StressShield | Stress sensitivity | Stress management |
| SensoryBalance | Sensory sensitivity | Sensory modulation |
| SensorySeeker | Sensory seeking behavior | Sensory engagement |
| SocialSync | Social challenges | Social skills coaching |
| ConfidenceCoach | Self-esteem and identity | Identity building |

---

## Where to Contribute

| I want to work on... | Go to... |
|----------------------|----------|
| **ADHD trait modeling** (how an Avatar's trait affects performance) | `src/avatars/` — subclass `BaseAvatar`, implement `get_adhd_trait_impact()` and `simulate_struggle()` |
| **Aide coaching logic** (strategies, expertise, real-world insights) | `src/aides/` — subclass `BaseAide`, implement `get_expertise_strategies()` and `get_real_world_insights()` |
| **Fusion engine** (Avatar + Aide → Advocate) | `src/fusion/` |
| **Training loop / session orchestration** | `src/simulation/session_orchestrator.py` |
| **Scenario definitions** (what tasks/challenges exist) | `src/simulation/environment/scenarios.py` |
| **Web UI** (Next.js pages, dashboards, simulation-lab) | `apps/web/` |
| **Mobile app** (Expo) | `apps/mobile/` |
| **API endpoints** (FastAPI) | `apps/api/` |
| **Cloudflare Worker** (Durable Objects, WebSocket fan-out, pair state) | `cloudflare-engine/` |
| **Persistence / database** (Supabase) | `src/database/` |
| **Shared types / SDK** | `packages/simulation-sdk/` |
| **Governance / onboarding / agent protocol** | `NLT-DEV-OTOI.md`, `AGENTS.md`, `agents/`, `SOPs/` |

---

## Key Files at a Glance

```
README.md                              ← Full project docs (831 lines, read after this)
QUICKSTART.md                          ← 5-min setup, entrypoint status matrix, smoke tests
IMPLEMENTATION-COMPLETE.md             ← Detailed implementation record
file-structure.md                      ← Governance architecture & file map
NLT-DEV-OTOI.md                        ← Canonical governance contract (read FIRST)
AGENTS.md                              ← Internal coordination gateway

src/                                   ← Python simulation engine (the intelligence)
├── avatars/                           ← ADHD trait models (19 pairs)
├── aides/                             ← Aide coaching logic
├── fusion/                            ← Fusion engine
├── simulation/
│   ├── session_orchestrator.py        ← ★ ACTIVE API — SessionOrchestrator, SessionConfig
│   ├── training_session.py            ← (legacy, known CoachingContext mismatch)
│   └── environment/scenarios.py       ← Scenario library (13 scenarios)
├── core/events.py                     ← EventBus
├── database/supabase_client.py        ← Supabase persistence (optional)
└── __init__.py

apps/
├── web/                               ← Next.js frontend (pnpm)
├── mobile/                            ← Expo React Native (npm)
└── api/                               ← FastAPI backend (pip)

cloudflare-engine/                     ← Cloudflare Worker + Durable Objects (npm/wrangler)
packages/simulation-sdk/               ← Shared TypeScript types
services/api/                          ← Additional API services
data/                                  ← Training data, datasets
docs/                                  ← Architecture, research, active threads
scripts/                               ← Setup, training loop, test scripts
tests/                                 ← pytest test suite
world3d/                               ← 3D world assets
supabase/                              ← Supabase migrations, edge functions
```

---

## Quick Start (4 Paths)

```bash
# Path A: Python simulation engine (compile + test)
python3 -m compileall src scripts
pytest tests/test_simulation/test_session_orchestrator.py

# Path B: Verified orchestrator smoke test (Python heredoc)
python3 - <<'PY'
from src.core.events import EventBus
from src.avatars.base_avatar import BaseAvatar
from src.aides.base_aide import BaseAide
from src.simulation.session_orchestrator import SessionOrchestrator, SessionConfig

class DemoAvatar(BaseAvatar):
    def get_adhd_trait_impact(self, tc):
        return {"difficulty_modifier": 1.1, "quality_modifier": 0.05, "time_modifier": 1.0, "cognitive_load_modifier": 0.1}
    def simulate_struggle(self, tc):
        return ["mild_struggle"]

class DemoAide(BaseAide):
    def get_expertise_strategies(self, ctx):
        return [{"strategy": "Chunk tasks", "techniques": ["break into chunks"], "expected_outcomes": ["higher completion"], "effectiveness": 0.7, "context_match": 0.7}]
    def get_real_world_insights(self, ctx):
        return [{"source": "real_world", "strategy": "Accountability", "techniques": ["pair work"], "expected_outcomes": ["more consistency"], "effectiveness": 0.8, "context_match": 0.8}]

bus = EventBus()
avatar = DemoAvatar("demo", {"trait_name": "demo"}, event_bus=bus)
aide = DemoAide("demo_aide", {"expertise_area": "demo"}, event_bus=bus)
orch = SessionOrchestrator(avatar, aide, SessionConfig(max_attempts_per_scenario=2, max_coaching_per_attempt=1, check_fusion_readiness=False))
result = orch.run_session([{"name": "Focus Task", "task_type": "focus", "base_success_rate": 0.8, "cognitive_demand": 0.4}])
print(result.phase.name, result.total_attempts, len(result.scenario_results))
PY

# Path C: Next.js web app
cd apps/web && pnpm install --frozen-lockfile && pnpm dev
# → http://localhost:3000

# Path D: FastAPI
cd apps/api && pip install -r requirements.txt && uvicorn main:app --reload
# → http://localhost:8000/docs

# Path E: Cloudflare Worker
cd cloudflare-engine && npm ci && npx wrangler dev
```

---

## The Boundary: What This Repo Is NOT

| This repo IS | This repo is NOT |
|--------------|------------------|
| Avatar/Aide ML models and trait logic | The deterministic world engine (rooms, objects, tick loop) |
| The training loop (session orchestration) | The authoritative simulation runtime |
| Aide coaching expertise and RRT | The UE 5.8 physical substrate |
| Fusion logic (Avatar + Aide → Advocate) | — |
| Web, mobile, API, Cloudflare Worker surfaces | — |
| Scenarios as *tasks* an Avatar attempts | Scenarios as *environments* the Avatar lives in (that's `nlt-world-engine`) |

**Rule of thumb:** If it changes how the Avatar *thinks, learns, or is coached*, it's here. If it changes the *world the Avatar lives in*, it's in `nlt-world-engine`.

---

## Reading Order for Deeper Understanding

1. **This file** ← you are here
2. `QUICKSTART.md` — setup, entrypoint status matrix, verified smoke tests, troubleshooting
3. `README.md` — full project docs (vision, architecture, CI, maintenance)
4. `IMPLEMENTATION-COMPLETE.md` — detailed implementation record
5. `file-structure.md` — governance architecture & `.github-private` file map
6. `NLT-DEV-OTOI.md` — governance, guardrails, escalation protocol (non-negotiable)
7. `docs/` — architecture docs, active threads, research notes

---

## Known Issues (Read Before Starting)

| Issue | Workaround |
|-------|------------|
| `scripts/test_training_loop.py` fails at `CoachingContext` mismatch | Use `SessionOrchestrator` directly — it's the stable API |
| `scripts/run_training_session.py` has import path errors | Pending import-path reconciliation |
| `scripts/setup_environment.py` overwrites `.gitignore` and `LICENSE` | Run only in fresh clone/sandbox |
| Legacy scripts have outdated coaching context shape | `src/simulation/session_orchestrator.py` is the source of truth |

---

## Non-Negotiable

> **Joshua W. Dorsey, Sr. is final authority on all architectural, deployment, UX, and strategic decisions. Escalate. Do not guess.**

- Commit format: `[AGENT_NAME] type(scope): description`
- End every session with a handoff record
- No credentials in code or VCS
- No LLM provider lock-in
- No production deployments without explicit human approval

---

*Part of the [NeuroLift Technologies](https://github.com/NeuroLift-Technologies) ecosystem. OTOI v1.0.3.*
