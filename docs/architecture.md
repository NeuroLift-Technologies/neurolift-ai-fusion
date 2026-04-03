# NeuroLift Simulation Architecture (Code-Verified)

This document describes the current runtime architecture as implemented in `src/`.
It intentionally reflects real interfaces and constraints in the codebase.

## 1) Intent

NeuroLift models **experiential learning** by pairing:

- an `Avatar` that attempts tasks while expressing ADHD-related struggle patterns
- an `Aide` that observes and intervenes with coaching
- a `FusionEngine` that evaluates whether the pair is ready to become an `Advocate`

The core idea is not "train on static data", but "accumulate structured lived experience" through repeated attempt/coaching loops.

---

## 2) Implemented subsystems and codepaths

### Core infrastructure

- `src/core/events.py`
  - `EventBus`, `Signal`, `SignalType`
  - decoupled pub/sub between Avatar, Aide, session orchestration, and fusion
- `src/core/state_machine.py`
  - `StateMachine`, `InvalidTransitionError`
  - validated lifecycle transitions with enter/exit callbacks
- `src/core/protocols.py`
  - `InteractionChannel` for Avatar<->Aide messages
  - `ExperienceMemory` / `ExperienceRecord` for experiential history
  - `ObservationReport` / `CoachingIntervention` payload types

### Avatar and Aide runtime

- `src/avatars/base_avatar.py`
  - Avatar lifecycle states (`IDLE`, `ATTEMPTING_TASK`, `STRUGGLING`, etc.)
  - task attempts, emotional/cognitive updates, burnout assessment
  - learning progress + independence tracking
  - Experience memory recording on every attempt
- `src/aides/base_aide.py`
  - binds to avatar and subscribes to avatar signals
  - observe->coach loop and crisis escalation
  - strategy effectiveness tracking over time

### Training orchestration

- `src/simulation/session_orchestrator.py`
  - `SessionOrchestrator` is the current game-loop style orchestrator
  - runs per-scenario attempt/coaching retries with abort thresholds
  - optional fusion-readiness assessment at session end
- `src/simulation/training_session.py`
  - legacy/alternate training session manager with optional Supabase writes
  - used by `scripts/test_training_loop.py`

### Fusion

- `src/fusion/readiness_assessor.py`
  - multidimensional readiness scoring:
    - experiential depth
    - coaching effectiveness
    - independence level
    - emotional resilience
    - strategy internalization
    - burnout management
- `src/fusion/fusion_engine.py`
  - readiness check + fusion report generation
  - emits fusion lifecycle signals (`FUSION_STARTED`, `FUSION_COMPLETED`, etc.)
- `src/advocates/base_advocate.py`
  - target base class for fused advocate behavior and support response modes

---

## 3) Runtime interaction model

### Event-driven contract

1. Avatar emits signals (task started, struggling, completed, burnout warning)
2. Aide subscribes with optional source filtering (paired avatar only)
3. Aide may deliver coaching through:
   - direct avatar method call (`receive_coaching`)
   - channel message (`MessageType.COACHING_INTERVENTION`)
4. Session orchestrator aggregates outcomes and can trigger readiness assessment

### State guarantees

- Avatar transitions are validated through `StateMachine`
- invalid transitions raise `InvalidTransitionError`, with defensive fallback in `BaseAvatar`
- transition history is retained for diagnostics

### Experiential memory

`ExperienceMemory` stores `ExperienceRecord` entries that include:

- task context
- struggles experienced
- emotional journey
- coaching received
- success/failure outcome
- independence delta

This is later consumed by readiness scoring and intended Advocate behavior.

---

## 4) Session orchestration workflow

`SessionOrchestrator.run_session()` expects a list of scenario dicts with keys such as:

- `name`
- `task_type`
- `base_success_rate`
- `cognitive_demand`

The orchestrator loop:

1. Avatar attempts scenario task
2. on failure, Aide may provide up to `max_coaching_per_attempt` interventions
3. retries are counted toward global `max_attempts_per_scenario`
4. scenario aborts if burnout risk exceeds threshold
5. session computes final independence and optional fusion readiness

### Minimal example

```python
from src.avatars.adhd_traits.stay_alert_avatar import StayAlertAvatar
from src.aides.coaching.stay_alert_aide import StayAlertAide
from src.simulation.session_orchestrator import SessionOrchestrator, SessionConfig

avatar = StayAlertAvatar("avatar_1", {"attention_duration": 15})
aide = StayAlertAide("aide_1", {"expertise_area": "sustained_attention"})

config = SessionConfig(
    max_attempts_per_scenario=5,
    max_coaching_per_attempt=2,
    success_rate_target=0.7,
)

scenarios = [
    {
        "name": "Focused reading",
        "task_type": "reading",
        "base_success_rate": 0.65,
        "cognitive_demand": 0.7,
    }
]

result = SessionOrchestrator(avatar, aide, config).run_session(scenarios)
print(result.to_dict())
```

---

## 5) Fusion workflow

`FusionEngine.fuse(avatar, aide, force=False)`:

1. runs readiness assessment
2. blocks if any required dimension fails (unless forced)
3. extracts:
   - avatar experiential summary
   - aide coaching effectiveness summary
4. derives `AdvocateCapabilities`
5. validates fusion output and returns `FusionReport`

Use `force=True` only for controlled experiments/tests when readiness gates are expected to fail.

---

## 6) Persistence and operational constraints

### Optional Supabase persistence

`src/database/supabase_client.py` is optional:

- if `supabase` package is unavailable, client becomes no-op
- if env vars are missing, client also becomes no-op

Required env vars for live writes:

- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_SUPABASE_ANON_KEY`

### Practical implication

Training flows still run locally even when database connectivity is absent; writes are skipped gracefully.

---

## 7) Testing coverage (current)

- `tests/test_core/test_events.py` covers event bus subscription/filter/history/error handling
- `tests/test_core/test_state_machine.py` covers transitions, guards, callbacks, reset/history
- `tests/test_simulation/test_session_orchestrator.py` covers attempt/retry caps, burnout abort, readiness checks
- `tests/test_fusion/test_exports.py` validates fusion package exports

---

## 8) Known architecture gaps

1. **Dual event systems**
   - `src/core/events.py` (`SignalType`) is used by avatar/aide/orchestrator/fusion
   - `src/simulation/environment/world_engine.py` contains a separate `EventType`
   - these are not yet unified
2. **SimulationEnvironment alias**
   - `src/simulation/__init__.py` currently aliases `SimulationEnvironment` to `WorldEngine`
   - useful for compatibility, but not yet a fully integrated environment facade
3. **Script path divergence**
   - `scripts/run_training_session.py` and `scripts/test_training_loop.py` exercise different training stacks
   - both are useful, but maintainers should keep them aligned as APIs evolve

---

## 9) Extension guidance

When adding a new Avatar/Aide pair:

1. implement trait class inheriting `BaseAvatar`
2. implement aide class inheriting `BaseAide`
3. define scenario inputs that match orchestrator contract
4. add tests for:
   - trait impact/struggle behavior
   - coaching strategy selection
   - session outcomes and readiness scoring

Keep interfaces event-driven and prefer extending existing docs instead of creating parallel architecture pages.