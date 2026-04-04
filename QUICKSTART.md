# NeuroLift Technologies - Quick Start Guide

> **Current status (Apr 2026):** script entrypoints are in transition. Use this guide for validated setup checks, and treat the training script runs as reproducible diagnostics rather than guaranteed successful end-to-end sessions.

## 🚀 Get Started in 5 Minutes

### Installation

```bash
# Navigate to project directory
cd /path/to/neurolift-ai-fusion

# Install dependencies
pip install -r requirements.txt
```

### Run a Training Session

```bash
# Syntax smoke check first
python3 -m compileall src scripts

# Execute the current interactive training demonstration
python3 scripts/test_training_loop.py
```

> `scripts/test_training_loop.py` currently executes setup + scenario selection, then fails at coaching context construction with `TypeError: CoachingContext.__init__() got an unexpected keyword argument 'avatar'`. Keep using it as a reproducible integration checkpoint until script/runtime interfaces are reconciled.

### Minimal Orchestrator API Smoke Test (Verified)

This example mirrors the current `SessionOrchestrator` contract used in tests:

```bash
python3 - <<'PY'
from src.core.events import EventBus
from src.avatars.base_avatar import BaseAvatar
from src.aides.base_aide import BaseAide
from src.simulation.session_orchestrator import SessionOrchestrator, SessionConfig

class DemoAvatar(BaseAvatar):
    def get_adhd_trait_impact(self, task_context):
        return {"difficulty_modifier": 1.1, "quality_modifier": 0.05, "time_modifier": 1.0, "cognitive_load_modifier": 0.1}
    def simulate_struggle(self, task_context):
        return ["mild_struggle"]

class DemoAide(BaseAide):
    def get_expertise_strategies(self, context):
        return [{"strategy": "Chunk tasks", "techniques": ["break work into chunks"], "expected_outcomes": ["higher completion"], "effectiveness": 0.7, "context_match": 0.7}]
    def get_real_world_insights(self, context):
        return [{"source": "real_world", "strategy": "Use accountability", "techniques": ["pair work"], "expected_outcomes": ["more consistency"], "effectiveness": 0.8, "context_match": 0.8}]

bus = EventBus()
avatar = DemoAvatar("avatar_demo", {"trait_name": "demo"}, event_bus=bus)
aide = DemoAide("aide_demo", {"expertise_area": "demo_coaching"}, event_bus=bus)
orchestrator = SessionOrchestrator(
    avatar,
    aide,
    SessionConfig(max_attempts_per_scenario=2, max_coaching_per_attempt=1, check_fusion_readiness=False),
)
result = orchestrator.run_session([
    {"name": "Focus Task", "task_type": "focus", "base_success_rate": 0.8, "cognitive_demand": 0.4}
])
print(result.phase.name, result.total_attempts, len(result.scenario_results))
PY
```

Current demo behavior:
1. Creates a StayAlert Avatar and StayAlertAide
2. Enumerates workplace scenarios and selects one
3. Runs the first attempt of a training session
4. Then currently fails at a known `CoachingContext` signature mismatch

---

## 📊 Understanding the Output

### Session Results
```
Status: ✓ SUCCESS
Attempts: 1/1
Average Quality Score: 0.35
```

- **Status**: Did the Avatar complete the task?
- **Attempts**: How many tries did it take?
- **Quality Score**: 0-1 scale, higher is better

### Avatar Final State
```
Current State: learning
Emotional State: relieved
Overall Independence: 0.10
Success Rate: 1.00
```

- **State**: Avatar's current cognitive state (idle, struggling, learning, independent)
- **Emotional State**: How the Avatar feels
- **Independence**: 0-1 scale of mastery (1.0 = complete independence)
- **Success Rate**: Percentage of tasks completed successfully

### Aide Metrics
```
Total Interventions: 0
Successful Interventions: 0
Success Rate: 0.00
```

- **Interventions**: How many times the Aide coached
- **Success Rate**: How often coaching led to success

---

## 🧠 What's Happening?

### Avatar-Aide-Advocate Process

```
Avatar                      Aide
  |                          |
  └─ Attempts Task ─────────→ Observes Struggle
                             │
                             └─ Provides Coaching
                             │
  ←─ Receives Coaching ──────┘
  │
  └─ Tries Again
```

### Training Loop

1. **Avatar Attempts Task** - Tries to complete scenario with authentic ADHD struggle
2. **Task Succeeds or Fails** - Result recorded
3. **Aide Evaluates Performance** - Analyzes struggle indicators
4. **Coaching Provided** (if needed) - Evidence-based strategies applied
5. **Avatar Learns** - Progress tracked toward independence

---

## 📚 Available Scenarios

### Workplace (5)
- Email Processing
- Report Writing
- Meeting Participation
- Code Review
- Deadline Crunch

### Personal Life (4)
- Household Cleaning
- Grocery Shopping & Cooking
- Bill Paying
- Morning Routine

### Social (2)
- Phone Conversations
- Social Events

### Academic (2)
- Study Sessions
- Project Work

---

## 🔧 Customization

### Modify Avatar Traits

```python
avatar_config = {
    "attention_duration": 15,        # Minutes before attention drift
    "drift_probability": 0.3,        # 30% chance of losing focus
    "hyperfocus_tendency": 0.2,      # 20% chance of hyperfocus
}

avatar = StayAlertAvatar("my_avatar", avatar_config)
```

### Change Scenario

In `scripts/test_training_loop.py`, modify the scenario selection:

```python
# Instead of scenarios[0], try scenarios[1], scenarios[2], etc.
choice = scenarios[1]  # Select Report Writing instead
```

### Run Multiple Sessions

```python
from src.core.events import EventBus
from src.avatars.base_avatar import BaseAvatar
from src.aides.base_aide import BaseAide
from src.simulation.session_orchestrator import SessionOrchestrator, SessionConfig

class DemoAvatar(BaseAvatar):
    def get_adhd_trait_impact(self, task_context):
        return {"difficulty_modifier": 1.1, "quality_modifier": 0.05, "time_modifier": 1.0, "cognitive_load_modifier": 0.1}
    def simulate_struggle(self, task_context):
        return ["mild_struggle"]

class DemoAide(BaseAide):
    def get_expertise_strategies(self, context):
        return [{"strategy": "Chunk tasks", "techniques": ["break work into chunks"], "expected_outcomes": ["higher completion"], "effectiveness": 0.7, "context_match": 0.7}]
    def get_real_world_insights(self, context):
        return [{"source": "real_world", "strategy": "Use accountability", "techniques": ["pair work"], "expected_outcomes": ["more consistency"], "effectiveness": 0.8, "context_match": 0.8}]

bus = EventBus()
avatar = DemoAvatar("avatar_demo", {"trait_name": "demo"}, event_bus=bus)
aide = DemoAide("aide_demo", {"expertise_area": "demo_coaching"}, event_bus=bus)
orchestrator = SessionOrchestrator(
    avatar,
    aide,
    SessionConfig(max_attempts_per_scenario=2, max_coaching_per_attempt=1, check_fusion_readiness=False),
)

for i in range(3):
    result = orchestrator.run_session([
        {"name": f"Focus Task {i+1}", "task_type": "focus", "base_success_rate": 0.8, "cognitive_demand": 0.4}
    ])
    print(result.phase.name, result.total_attempts, len(result.scenario_results))
```

---

## 📖 Key Concepts

### ADHD Traits
**StayAlert**: Sustained attention deficit
- Struggles to focus for extended periods
- Experiences attention drift
- Vulnerable to hyperfocus on irrelevant tasks

**TaskKickstart**: Task initiation difficulty
- Hard to start tasks (even easy ones)
- Procrastination patterns
- Performance improves after starting

### Coaching Strategies

**Attention Expert** provides:
- Pomodoro Technique adaptations
- Environmental optimization
- Task chunking methods
- Body doubling support
- Transition rituals
- External accountability systems

### Progress Tracking

**Independence Level**: 0.0 to 1.0
- 0.0 = Needs constant coaching
- 0.5 = Can succeed with occasional support
- 1.0 = Complete independence

---

## 🔄 Database Integration (Optional)

### Enable Supabase Persistence

1. Get Supabase credentials from `https://supabase.com`
2. Set environment variables:

```bash
export VITE_SUPABASE_URL="your_url"
export VITE_SUPABASE_SUPABASE_ANON_KEY="your_key"
```

3. Run training - data automatically saves to database

### Without Supabase

Training runs locally without database - no setup required!

---

## 🧪 Testing

### Run All Verifications

```bash
# 1) Syntax smoke check
python3 -m compileall src scripts

# 2) Current orchestration contract (stable test target)
pytest tests/test_simulation/test_session_orchestrator.py

# 3) Optional integration diagnostic (expected known failure point)
python3 scripts/test_training_loop.py
```

### Check System Status

```python
from src.database.supabase_client import SupabaseClient
db = SupabaseClient()
print(db._is_available())  # True if connected, False otherwise
```

---

## 🧹 Repository Maintenance Automation (PR Cleanup)

Use this when you need to reproduce or validate pull-request hygiene behavior in GitHub Actions.

### What the workflow does

- Workflow file: `.github/workflows/pr-cleanup.yml`
- Actions UI name: **PR Cleanup**
- Runs daily at `06:00 UTC` (`cron: 0 6 * * *`) and supports manual dispatch
- Marks inactive PRs as `stale` after 30 days, then auto-closes after 7 more days (`auto-closed` label)
- Deletes branches for merged PRs when the branch belongs to this repository
- Reads up to 100 closed PRs per run when scanning for merged branch deletion candidates

### Safety constraints (from workflow logic)

- Draft PRs are exempt from stale marking (`exempt-draft-pr: true`)
- Issues are never marked stale/closed by this workflow
- Branch cleanup skips protected branches and common default branch names
- Branches from fork-based PRs are not deleted by the cleanup job
- Workflow permissions must include `contents: write`, `pull-requests: write`, and `issues: write`

### Manual run (Actions UI)

1. Go to **Actions** -> **PR Cleanup** -> **Run workflow**
2. Select the branch/ref
3. Optionally override:
   - `days_before_stale` (default `30`)
   - `days_before_close` (default `7`)
4. Review logs from:
   - `stale-prs` (stale/close decisions)
   - `delete-merged-branches` (branch cleanup actions)

### Quick verification checklist

After each manual run, confirm:

1. The run used the intended `days_before_stale` and `days_before_close` values.
2. Draft PRs were skipped and issue staleness was not applied.
3. Branch cleanup outcomes are expected (`deleted`, `skipped protected`, `fork source`, or `already deleted`).
4. Any remaining merged branches are not just outside the current 100-PR scan window.

### Common pitfalls

- **Merged branch not deleted:** branch may already be removed, protected, or from a fork PR.
- **Unexpected stale label:** any new activity (comment/commit/review) keeps an active PR from closure.

---

## 📊 Next Steps

1. **Run the baseline checks** - `compileall` + `test_session_orchestrator.py`
2. **Use `test_training_loop.py` as a diagnostic** - Reproduce and inspect current integration mismatch
3. **Try other scenarios** - Modify scenario selection in `scripts/test_training_loop.py`
4. **Create custom Avatars/Aides** - Prototype against `SessionOrchestrator` contracts
5. **Build an interface** - Add a UI layer once script/runtime interfaces are reconciled

---

## 🆘 Troubleshooting

### ImportError: No module named 'supabase'

This is fine! The system works without Supabase. Data stays local.

To enable Supabase: `pip install supabase`

### Training session takes a while

This is normal - each attempt involves complex calculations. Sessions typically complete in 1-5 seconds per attempt.

### "No scenarios found"

Verify `src/simulation/environment/scenarios.py` exists and contains ScenarioLibrary class.

### Database warnings

Warnings about database are informational only - training continues successfully without database.

### `ImportError` in `scripts/run_training_session.py`

If you see `ImportError: attempted relative import beyond top-level package`, this is due to an import path mismatch between script imports and package-relative imports inside `src/avatars`.

### `CoachingContext` TypeError in `scripts/test_training_loop.py`

If you see `TypeError: CoachingContext.__init__() got an unexpected keyword argument 'avatar'`, the script is using an outdated coaching context shape compared to `src/aides/base_aide.py`.

### `CoachingContext` TypeError in `src/simulation/training_session.py`

If `TrainingSession.run()` fails at coaching construction, the same mismatch exists in
`src/simulation/training_session.py` (`CoachingContext` is instantiated with legacy fields).
Prefer `src/simulation/session_orchestrator.py` for current interface validation.

---

## 📞 Support

- **Documentation**: See `IMPLEMENTATION-COMPLETE.md` for full details
- **Architecture**: See `docs/architecture.md`
- **Code**: All code is well-commented with docstrings

---

## ✅ Validation Complete (Current Baseline)

You have successfully:
- ✓ Installed NeuroLift Technologies
- ✓ Verified code syntax across `src/` and `scripts/`
- ✓ Confirmed the current orchestrator contract via targeted tests
- ✓ Reproduced known script-level integration mismatches for debugging

You now have a reliable baseline for local development and troubleshooting.

---

**Ready to explore? Start with: `pytest tests/test_simulation/test_session_orchestrator.py`**
