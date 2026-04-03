# NeuroLift Technologies - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Installation

```bash
# Navigate to project directory
cd /path/to/neurolift

# Install dependencies
pip install -r requirements.txt
```

### Run a Training Session

```bash
# Execute the complete training demonstration
python3 scripts/test_training_loop.py
```

That's it! The system will:
1. Create a StayAlert Avatar (experiences attention deficit)
2. Create a StayAlertAide (provides attention coaching)
3. Run an Email Processing scenario
4. Display comprehensive results

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
from src.simulation.training_session import TrainingSession

avatar = StayAlertAvatar("avatar1", config)
aide = StayAlertAide("aide1", config)

for i in range(5):
    scenario = ScenarioLibrary.get_scenario_by_id(f"wp_{i % 5 + 1}")
    session = TrainingSession(avatar, aide, scenario)
    results = session.run()
    print(f"Session {i+1} complete")
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
python3 scripts/test_training_loop.py
```

### Check System Status

```python
from src.database.supabase_client import SupabaseClient
db = SupabaseClient()
print(db._is_available())  # True if connected, False otherwise
```

---

## 📊 Next Steps

1. **Run the test** - Execute `test_training_loop.py`
2. **Explore results** - Examine the output metrics
3. **Try other scenarios** - Modify the script to use different scenarios
4. **Create custom Avatars** - Implement your own Avatar trait
5. **Build an interface** - Create a web UI for visualization

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

---

## 📞 Support

- **Documentation**: See `IMPLEMENTATION-COMPLETE.md` for full details
- **Architecture**: See `docs/architecture.md`
- **Code**: All code is well-commented with docstrings

---

## 🎉 Success!

You've successfully:
- ✓ Installed NeuroLift Technologies
- ✓ Run a complete Avatar-Aide training session
- ✓ Observed authentic ADHD trait simulation
- ✓ Seen evidence-based coaching in action

Congratulations! You're now running an advanced AI experiential learning system.

---

**Ready to explore? Run: `python3 scripts/test_training_loop.py`**
