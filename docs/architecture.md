# NeuroLift Technologies Simulation Environment - Architecture Overview

**Date:** Apr 4, 2026  
**Version:** 1.1  
**Author:** Cursor AI (Initial Implementation)

## System Architecture

The NeuroLift Technologies Simulation Environment implements a novel approach to AI training through experiential learning. Unlike traditional machine learning approaches that train on datasets, this system creates realistic simulation environments where AI agents (Avatars) experience authentic challenges and learn through doing.

## Current Runtime Contracts (Source-Verified, Apr 2026)

The sections below include conceptual architecture. For day-to-day engineering work,
use the following codepaths as the current contract surface:

- `src/avatars/base_avatar.py`
- `src/aides/base_aide.py`
- `src/simulation/session_orchestrator.py`

### Public constructors and orchestration entrypoints

```python
# src/avatars/base_avatar.py
BaseAvatar(avatar_id: str, trait_config: Dict[str, Any], event_bus: Optional[EventBus] = None)

# src/aides/base_aide.py
BaseAide(aide_id: str, expertise_config: Dict[str, Any], event_bus: Optional[EventBus] = None)

# src/simulation/session_orchestrator.py
SessionOrchestrator(
    avatar: BaseAvatar,
    aide: BaseAide,
    config: Optional[SessionConfig] = None,
    event_bus: Optional[EventBus] = None,
)
result = orchestrator.run_session(scenarios: List[Dict[str, Any]])
```

Scenario dictionaries are expected to include at least:
`name`, `task_type`, `base_success_rate`, and `cognitive_demand`.

### Runtime workflow (current path)

1. Create Avatar + Aide with shared or compatible `EventBus`.
2. `SessionOrchestrator` binds the pair via `aide.bind_to_avatar(avatar)`.
3. Avatar attempts tasks (`attempt_task`), Aide observes/coaches (`observe_and_coach`).
4. Session tracks attempts/coaching/independence and (optionally) fusion readiness.

### Constraints and known pitfalls

- `src/simulation/training_session.py` uses an older `CoachingContext` shape
  and is currently not the canonical orchestration path.
- `scripts/test_training_loop.py` routes through `TrainingSession`, so it is
  useful as a reproducible diagnostic, not as a stable "green path."
- The stable verification target for orchestration behavior is:
  `tests/test_simulation/test_session_orchestrator.py`.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    NeuroLift Technologies Simulation Environment           │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Avatars   │  │    Aides    │  │  Advocates  │        │
│  │             │  │             │  │             │        │
│  │ • ADHD      │  │ • RRT Core  │  │ • Fusion    │        │
│  │   Traits    │  │ • PhD       │  │   Engine    │        │
│  │ • Struggle  │  │   Expertise │  │ • Combined  │        │
│  │   Simulation│  │ • Real      │  │   Experience│        │
│  │             │  │   Feedback  │  │   +         │        │
│  └─────────────┘  └─────────────┘  │   Expertise │        │
│           │               │        └─────────────┘        │
│           └───────┬───────┘                               │
│                   │                                       │
│  ┌─────────────────────────────────────────────────────────┤
│  │              Simulation Environment                    │
│  │                                                       │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  │   Scenarios │  │     NPCs    │  │  Challenges │   │
│  │  │             │  │             │  │             │   │
│  │  │ • Workplace │  │ • Neurotyp. │  │ • Random    │   │
│  │  │ • Personal  │  │ • Biased    │  │   Dysfunc.  │   │
│  │  │ • Social    │  │ • Supportive│  │ • Burnout   │   │
│  │  └─────────────┘  └─────────────┘  │   Sim.      │   │
│  │                                   └─────────────┘   │
│  │                                                       │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  │ World Engine│  │ Time System │  │ Consequence │   │
│  │  │             │  │             │  │   System    │   │
│  │  │ • Physics   │  │ • Scheduling│  │ • Real      │   │
│  │  │ • Events    │  │ • Passage   │  │   Results   │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │
│  └─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────────────────────────────────────────┤
│  │              Training & Metrics                        │
│  │                                                       │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  │ Session     │  │ Progress    │  │ Fusion      │   │
│  │  │ Manager     │  │ Tracker     │  │ Readiness   │   │
│  │  │             │  │             │  │             │   │
│  │  │ • Training  │  │ • Independence│  │ • Criteria  │   │
│  │  │   Loop      │  │ • Milestones │  │ • Assessment│   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │
│  └─────────────────────────────────────────────────────────┤
└─────────────────────────────────────────────────────────────┘
```

## Source-Verified Runtime Contracts (Apr 2026)

The sections below provide conceptual architecture. For implementation-facing work,
use this contract map first so docs and code stay aligned.

### Canonical orchestration path

| Contract | Source |
| --- | --- |
| Main runtime loop is `SessionOrchestrator.run_session(scenarios)` | `src/simulation/session_orchestrator.py` |
| Stable interface verification tests | `tests/test_simulation/test_session_orchestrator.py` |
| Scenario input keys expected by orchestrator loop | `name`, `task_type`, `base_success_rate`, `cognitive_demand` |
| Session tuning knobs | `SessionConfig` (`max_attempts_per_scenario`, `max_coaching_per_attempt`, `min_attempts_for_success_check`, `success_rate_target`, `burnout_abort_threshold`, `check_fusion_readiness`) |

### Avatar-Aide runtime interaction (current implementation)

1. `SessionOrchestrator` binds `BaseAide` to `BaseAvatar` via `bind_to_avatar(...)`.
2. Avatar and Aide share one `EventBus` (`src/core/events.py`) for signal-driven coordination.
3. Per attempt, Avatar executes `attempt_task(...)`; on failures, Aide runs `observe_and_coach(...)`.
4. Coaching effectiveness is always tracked after retries (including failed retries) through `track_intervention_effectiveness(...)`.
5. Session completion emits `SESSION_COMPLETED` and serializes results through `SessionResult.to_dict()`.

### Legacy/diagnostic path (not canonical)

`src/simulation/training_session.py` is a legacy manager that still drives database-oriented
session flow. It currently builds `CoachingContext` with an older shape (`avatar=...`,
`current_struggle=...`), while `src/aides/base_aide.py` now defines `CoachingContext`
as `avatar_id + observation + task_context (+ optional summary/timestamp)`.

Use `SessionOrchestrator` for current integration work and treat `TrainingSession` as a
diagnostic compatibility path until that interface mismatch is reconciled.

### Persistence behavior constraints

- Supabase is optional at runtime.
- `SupabaseClient` only initializes a live client when both `VITE_SUPABASE_URL` and
  `VITE_SUPABASE_SUPABASE_ANON_KEY` are present and the `supabase` package is installed.
- When unavailable, DB methods return `None`/`[]` and simulation components continue in local mode.

## Core Components

### 1. Avatar System

**Purpose:** Simulate authentic ADHD experiences and struggles

**Key Characteristics:**
- Embodies specific ADHD traits (attention deficit, impulsivity, working memory issues, etc.)
- Experiences realistic stress, frustration, and failure patterns
- Makes decisions with real consequences in simulated environments
- Learns through repeated attempts and gradual improvement

**Architecture:**
```python
class BaseAvatar:
    """Base class for all ADHD trait Avatars"""
    
    def __init__(self, trait_config: Dict[str, Any]):
        self.trait_config = trait_config
        self.current_state = AvatarState()
        self.struggle_patterns = []
        self.learning_progress = {}
    
    def attempt_task(self, scenario: Scenario) -> TaskResult:
        """Attempt a task with ADHD trait affecting performance"""
        pass
    
    def experience_consequence(self, result: TaskResult) -> None:
        """Process the result and update internal state"""
        pass
    
    def get_independence_level(self) -> float:
        """Return current independence level (0.0 to 1.0)"""
        pass
```

### 2. Aide System

**Purpose:** Provide expert coaching and support during Avatar struggles

**Foundation Components:**
1. **RRT Core:** Rapid Response Team foundation with burnout detection
2. **PhD Expertise:** Deep academic knowledge of specific executive functions
3. **Real-World Feedback:** Community wisdom from successful ADHD individuals

**Architecture:**
```python
class BaseAide:
    """Base class for all coaching Aides"""
    
    def __init__(self, expertise_config: Dict[str, Any]):
        self.rrt_core = RRTFoundation()
        self.phd_expertise = ExecutiveFunctionExpertise()
        self.real_world_feedback = CommunityWisdom()
        self.coaching_strategies = []
    
    def observe_avatar_struggle(self, avatar: BaseAvatar, scenario: Scenario) -> None:
        """Monitor Avatar's current challenges"""
        pass
    
    def provide_coaching(self, avatar: BaseAvatar, context: CoachingContext) -> CoachingAction:
        """Provide real-time coaching intervention"""
        pass
    
    def assess_burnout_risk(self, avatar: BaseAvatar) -> BurnoutRisk:
        """Evaluate if Avatar is approaching burnout"""
        pass
```

### 3. Simulation Environment

**Purpose:** Create realistic scenarios with meaningful consequences

**Key Features:**
- **World Engine:** Manages simulation state, physics, and events
- **Time System:** Handles scheduling, deadlines, and time passage
- **Consequence System:** Ensures actions have realistic results
- **NPCs:** Create social dynamics and comparison scenarios
- **Random Challenges:** Inject unexpected difficulties to test resilience

**Architecture:**
```python
class SimulationEnvironment:
    """Core simulation environment"""
    
    def __init__(self, config: EnvironmentConfig):
        self.world_engine = WorldEngine()
        self.time_system = TimeSystem()
        self.consequence_system = ConsequenceSystem()
        self.npc_manager = NPCManager()
        self.challenge_injector = ChallengeInjector()
    
    def run_scenario(self, scenario: Scenario, avatar: BaseAvatar, aide: BaseAide) -> ScenarioResult:
        """Execute a complete scenario with Avatar-Aide interaction"""
        pass
    
    def inject_random_challenge(self, avatar: BaseAvatar) -> Challenge:
        """Randomly introduce new executive function challenges"""
        pass
```

### 4. Advocate Fusion System

**Purpose:** Combine trained Avatar experience with Aide expertise

**Fusion Criteria:**
- Avatar demonstrates consistent independence across scenarios
- Aide has proven effective coaching strategies
- Both systems have sufficient training data
- Fusion readiness assessment passes

**Architecture:**
```python
class FusionEngine:
    """Manages Avatar-Aide fusion into Advocates"""
    
    def assess_fusion_readiness(self, avatar: BaseAvatar, aide: BaseAide) -> FusionReadiness:
        """Evaluate if Avatar-Aide pair is ready for fusion"""
        pass
    
    def fuse_into_advocate(self, avatar: BaseAvatar, aide: BaseAide) -> BaseAdvocate:
        """Combine Avatar and Aide into fused Advocate"""
        pass
    
    def validate_advocate(self, advocate: BaseAdvocate) -> ValidationResult:
        """Test fused Advocate's capabilities"""
        pass
```

## Data Flow Architecture

### Training Loop Flow

```
1. Scenario Selection
   ↓
2. Avatar Attempts Task
   ↓
3. ADHD Trait Affects Performance
   ↓
4. Aide Observes Struggle
   ↓
5. Aide Provides Coaching
   ↓
6. Avatar Tries Again (with support)
   ↓
7. Consequence System Evaluates Result
   ↓
8. Progress Tracking Updates
   ↓
9. Independence Assessment
   ↓
10. [Repeat until mastery OR fusion readiness]
```

### Fusion Process Flow

```
1. Avatar Independence Check
   ↓
2. Aide Effectiveness Assessment
   ↓
3. Fusion Readiness Evaluation
   ↓
4. Experience + Expertise Combination
   ↓
5. Advocate Validation Testing
   ↓
6. RRT Burnout Response Integration
   ↓
7. Final Advocate Deployment
```

## Design Patterns

### 1. Component-Based Architecture
- Each Avatar trait is a separate component
- Aide expertise modules are independent components
- Scenarios are modular and composable
- Easy to add new traits, strategies, or scenarios

### 2. Observer Pattern
- Progress tracking observes Avatar-Aide interactions
- Metrics system monitors training progress
- Fusion readiness assessment watches independence levels

### 3. Strategy Pattern
- Different coaching strategies for different situations
- Multiple intervention approaches per executive function
- Adaptive strategy selection based on context

### 4. Factory Pattern
- Scenario generation from templates
- Avatar-Aide pair creation
- NPC behavior instantiation

### 5. State Machine Pattern
- Avatar state transitions (struggling → learning → independent)
- Aide coaching state management
- Simulation environment state tracking

## Privacy and Security Architecture

### Local Processing Design
- All simulation runs locally
- No external data transmission
- User data stored locally only
- No cloud dependencies

### Data Privacy Principles
- Minimal data collection
- Explicit consent for any data sharing
- Transparent data handling
- No monetization of user data

### Security Considerations
- Input validation for all user data
- Secure configuration management
- Local storage encryption
- No external API dependencies

## Performance Considerations

### Simulation Performance
- Efficient state management for long training sessions
- Parallel execution of multiple Avatar-Aide pairs
- Optimized event processing
- Memory management for extended runs

### Scalability Design
- Support for running all 19 Avatar-Aide pairs simultaneously
- Efficient resource allocation
- Horizontal scaling capabilities
- Performance monitoring and optimization

## Testing Architecture

### Unit Testing
- Individual component testing
- Avatar trait behavior validation
- Aide coaching strategy testing
- Scenario execution testing

### Integration Testing
- Avatar-Aide interaction testing
- End-to-end scenario testing
- Fusion process validation
- Performance benchmarking

### Validation Testing
- Real-world scenario accuracy
- ADHD trait authenticity
- Coaching effectiveness
- Advocate capability validation

## Future Extensibility

### Adding New Traits
- New Avatar trait components
- Corresponding Aide expertise modules
- Relevant scenario additions
- Updated fusion criteria

### New Scenario Types
- Additional workplace scenarios
- Personal life situation expansion
- Social dynamic variations
- Educational environment scenarios

### Enhanced AI Capabilities
- More sophisticated NPC behaviors
- Advanced coaching strategies
- Improved fusion algorithms
- Better burnout detection

---

**This architecture supports the core innovation of experiential AI learning while maintaining flexibility for future enhancements and community contributions.**