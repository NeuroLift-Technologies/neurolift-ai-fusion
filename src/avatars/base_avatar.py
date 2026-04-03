"""
Base Avatar Class

The foundation for all ADHD trait Avatars. Implements core behavior patterns,
state management, and learning progression tracking.

Each Avatar embodies a specific ADHD trait and experiences authentic struggles
in simulation environments, learning through repeated attempts and gradual
improvement with Aide support.

Architecture notes
------------------
* A formal StateMachine governs Avatar lifecycle transitions.
* An EventBus Signal is emitted on every state change so that Aides,
  the WorldEngine, and the SessionOrchestrator can react without
  tight coupling.
* An ExperienceMemory stores every attempt as an ExperienceRecord,
  giving the Avatar (and later the fused Advocate) a structured
  autobiography to draw on — the heart of experiential learning.
* An InteractionChannel is the dedicated pipe to the paired Aide;
  all coaching flows through it.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import random
import uuid
from datetime import datetime, timedelta

from ..core.events import EventBus, Signal, SignalType
from ..core.state_machine import StateMachine, InvalidTransitionError
from ..core.protocols import (
    ExperienceMemory,
    ExperienceRecord,
    InteractionChannel,
    Message,
    MessageType,
    ObservationReport,
    CoachingIntervention,
)


# ---------------------------------------------------------------------------
# Enums and data classes
# ---------------------------------------------------------------------------

class AvatarState(Enum):
    """Current state of the Avatar in the simulation."""
    IDLE = "idle"
    ATTEMPTING_TASK = "attempting_task"
    STRUGGLING = "struggling"
    RECEIVING_COACHING = "receiving_coaching"
    APPLYING_STRATEGY = "applying_strategy"
    LEARNING = "learning"
    INDEPENDENT = "independent"
    BURNOUT_RISK = "burnout_risk"
    BURNOUT = "burnout"
    RECOVERING = "recovering"


class TaskDifficulty(Enum):
    """Difficulty levels for tasks."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXTREME = "extreme"


@dataclass
class TaskResult:
    """Result of an Avatar's task attempt."""
    success: bool
    completion_time: Optional[timedelta]
    quality_score: float  # 0.0 to 1.0
    struggle_indicators: List[str]
    aide_interventions: List[str]
    emotional_state: str
    cognitive_load: float  # 0.0 to 1.0
    strategies_used: List[str] = field(default_factory=list)
    independent: bool = False  # True if no coaching was needed
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "completion_time_seconds": (
                self.completion_time.total_seconds() if self.completion_time else None
            ),
            "quality_score": self.quality_score,
            "struggle_indicators": self.struggle_indicators,
            "aide_interventions": self.aide_interventions,
            "emotional_state": self.emotional_state,
            "cognitive_load": self.cognitive_load,
            "strategies_used": self.strategies_used,
            "independent": self.independent,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class LearningProgress:
    """Track Avatar's learning progression for one task type."""
    task_type: str
    attempts: int = 0
    successes: int = 0
    independent_successes: int = 0
    total_coaching_sessions: int = 0
    independence_milestones: List[datetime] = field(default_factory=list)
    current_independence_level: float = 0.0  # 0.0 to 1.0
    last_improvement: Optional[datetime] = None
    consecutive_successes: int = 0
    consecutive_failures: int = 0

    @property
    def success_rate(self) -> float:
        if self.attempts == 0:
            return 0.0
        return self.successes / self.attempts

    @property
    def independent_success_rate(self) -> float:
        if self.attempts == 0:
            return 0.0
        return self.independent_successes / self.attempts

    @property
    def is_independent(self) -> bool:
        """Avatar has achieved independence when level >= 0.8."""
        return self.current_independence_level >= 0.8


# ---------------------------------------------------------------------------
# Learning/independence tuning constants
# ---------------------------------------------------------------------------

INDEPENDENCE_GAIN_INDEPENDENT_SUCCESS = 0.1
INDEPENDENCE_GAIN_COACHED_SUCCESS = 0.05
INDEPENDENCE_LOSS_ON_FAILURE = 0.02
INDEPENDENCE_COACHING_LOOKBACK_SECONDS = 60


# ---------------------------------------------------------------------------
# Helper: build the Avatar state machine with valid transitions
# ---------------------------------------------------------------------------

def _build_avatar_state_machine() -> StateMachine:
    """Create a StateMachine with the legal Avatar lifecycle transitions."""
    sm = StateMachine(AvatarState, AvatarState.IDLE)

    # From IDLE
    sm.add_transitions(AvatarState.IDLE, [
        AvatarState.ATTEMPTING_TASK,
    ])

    # From ATTEMPTING_TASK
    sm.add_transitions(AvatarState.ATTEMPTING_TASK, [
        AvatarState.STRUGGLING,
        AvatarState.LEARNING,
        AvatarState.INDEPENDENT,
        AvatarState.BURNOUT_RISK,
    ])

    # From STRUGGLING
    sm.add_transitions(AvatarState.STRUGGLING, [
        AvatarState.RECEIVING_COACHING,
        AvatarState.ATTEMPTING_TASK,   # retry without help
        AvatarState.BURNOUT_RISK,
        AvatarState.IDLE,              # give up on task
    ])

    # From RECEIVING_COACHING
    sm.add_transitions(AvatarState.RECEIVING_COACHING, [
        AvatarState.APPLYING_STRATEGY,
        AvatarState.ATTEMPTING_TASK,
        AvatarState.RECOVERING,
    ])

    # From APPLYING_STRATEGY
    sm.add_transitions(AvatarState.APPLYING_STRATEGY, [
        AvatarState.ATTEMPTING_TASK,
        AvatarState.LEARNING,
        AvatarState.STRUGGLING,
    ])

    # From LEARNING
    sm.add_transitions(AvatarState.LEARNING, [
        AvatarState.IDLE,
        AvatarState.ATTEMPTING_TASK,
        AvatarState.INDEPENDENT,
    ])

    # From INDEPENDENT
    sm.add_transitions(AvatarState.INDEPENDENT, [
        AvatarState.IDLE,
        AvatarState.ATTEMPTING_TASK,
    ])

    # From BURNOUT_RISK
    sm.add_transitions(AvatarState.BURNOUT_RISK, [
        AvatarState.RECEIVING_COACHING,
        AvatarState.BURNOUT,
        AvatarState.RECOVERING,
    ])

    # From BURNOUT
    sm.add_transitions(AvatarState.BURNOUT, [
        AvatarState.RECOVERING,
    ])

    # From RECOVERING
    sm.add_transitions(AvatarState.RECOVERING, [
        AvatarState.IDLE,
        AvatarState.BURNOUT_RISK,  # relapse
    ])

    return sm


# ---------------------------------------------------------------------------
# BaseAvatar
# ---------------------------------------------------------------------------

class BaseAvatar(ABC):
    """
    Base class for all ADHD trait Avatars.

    Each Avatar embodies a specific ADHD trait and experiences authentic
    struggles in simulation environments. They learn through repeated
    attempts, failures, and gradual improvement with Aide support.
    """

    def __init__(
        self,
        avatar_id: str,
        trait_config: Dict[str, Any],
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self.avatar_id = avatar_id
        self.trait_config = trait_config
        self.trait_name: str = trait_config.get("trait_name", "unknown")

        # State machine
        self._state_machine = _build_avatar_state_machine()

        # Event bus (shared across the simulation)
        self.event_bus = event_bus or EventBus()

        # Experience memory — the core of experiential learning
        self.experience_memory = ExperienceMemory(owner_id=avatar_id)

        # Interaction channel — set when paired with an Aide
        self.channel: Optional[InteractionChannel] = None

        # Emotional / cognitive state
        self.emotional_state: str = "neutral"
        self.cognitive_load: float = 0.0
        self.stress_level: float = 0.0

        # Learning tracking
        self.learning_progress: Dict[str, LearningProgress] = {}
        self.struggle_patterns: List[Dict[str, Any]] = []
        self.coaching_history: List[Dict[str, Any]] = []

        # Recent task results ring buffer (for burnout assessment)
        self._recent_results: List[TaskResult] = []
        self._max_recent: int = 20

        # Aggregate counters
        self.total_tasks_attempted: int = 0
        self.total_tasks_completed: int = 0
        self.total_coaching_sessions: int = 0
        self.burnout_risk_level: float = 0.0
        self._received_coaching_since_last_attempt: bool = False

        # Timestamps
        self.created_at = datetime.now()
        self.last_activity = datetime.now()

        # Wire state-change callback to emit signals
        for state in AvatarState:
            self._state_machine.on_enter(state, self._on_state_entered)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def current_state(self) -> AvatarState:
        return self._state_machine.current_state

    @current_state.setter
    def current_state(self, value: AvatarState) -> None:
        """Backwards-compatible setter that routes through the state machine."""
        if value == self._state_machine.current_state:
            return
        try:
            self._state_machine.transition_to(value, trigger="direct_set")
        except InvalidTransitionError:
            # Fall back to direct assignment for legacy callers
            self._state_machine.reset(value)

    # ------------------------------------------------------------------
    # Abstract interface — each ADHD trait implements these
    # ------------------------------------------------------------------

    @abstractmethod
    def get_adhd_trait_impact(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate how this Avatar's specific ADHD trait affects task performance.

        Returns a dict with at least:
            difficulty_modifier, struggle_indicators, quality_modifier,
            time_modifier, cognitive_load_modifier
        """

    @abstractmethod
    def simulate_struggle(self, task_context: Dict[str, Any]) -> List[str]:
        """Simulate authentic struggle patterns for this ADHD trait."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def bind_channel(self, channel: InteractionChannel) -> None:
        """Bind this Avatar to an Aide via an InteractionChannel."""
        self.channel = channel

    def attempt_task(self, task_context: Dict[str, Any]) -> TaskResult:
        """
        Attempt a task with ADHD trait affecting performance.

        The full loop:
        1. Transition to ATTEMPTING_TASK
        2. Compute trait impact and simulate struggles
        3. Determine outcome (success probability adjusted by trait)
        4. Record experience and emit signals
        5. Transition to LEARNING (success) or STRUGGLING (failure)
        """
        received_coaching_this_attempt = self._received_coaching_since_last_attempt
        self._received_coaching_since_last_attempt = False

        self._transition(AvatarState.ATTEMPTING_TASK, "task_start")
        self.last_activity = datetime.now()
        self.total_tasks_attempted += 1

        # Emit task-start signal
        self._emit(SignalType.AVATAR_TASK_STARTED, {
            "task_context": task_context,
            "emotional_state": self.emotional_state,
            "cognitive_load": self.cognitive_load,
        })

        # Trait impact
        trait_impact = self.get_adhd_trait_impact(task_context)

        # Simulate struggle
        struggle_indicators = self.simulate_struggle(task_context)
        if struggle_indicators:
            self._emit(SignalType.AVATAR_STRUGGLING, {
                "struggles": struggle_indicators,
                "task_context": task_context,
            })

        # Success probability
        base_success_rate = task_context.get("base_success_rate", 0.5)
        difficulty_modifier = trait_impact.get("difficulty_modifier", 1.0)

        # Experience-based adjustment: past successes boost confidence
        exp_bonus = self._experience_bonus(task_context)
        adjusted_rate = min(0.95, (base_success_rate / difficulty_modifier) + exp_bonus)

        success = random.random() < adjusted_rate

        # Quality
        quality_score = self._calculate_quality_score(
            success, trait_impact, struggle_indicators
        )

        # Emotional & cognitive updates
        self._update_emotional_state(success, struggle_indicators)
        self._update_cognitive_load(task_context, trait_impact)

        # Determine if attempt was independent (no coaching this attempt)
        independent = not received_coaching_this_attempt

        result = TaskResult(
            success=success,
            completion_time=self._calculate_completion_time(task_context, trait_impact),
            quality_score=quality_score,
            struggle_indicators=struggle_indicators,
            aide_interventions=[],
            emotional_state=self.emotional_state,
            cognitive_load=self.cognitive_load,
            strategies_used=task_context.get("strategies_applied", []),
            independent=independent,
        )

        # Record in recent results & learning progress
        self._store_recent_result(result)
        self._update_learning_progress(task_context, result)

        # Record experience
        self._record_experience(task_context, result, struggle_indicators)

        # Transition based on outcome
        if success:
            self.total_tasks_completed += 1
            if independent and self._check_independence(task_context):
                self._transition(AvatarState.INDEPENDENT, "independent_success")
                self._emit(SignalType.AVATAR_INDEPENDENCE_MILESTONE, {
                    "task_type": task_context.get("task_type", "unknown"),
                })
            else:
                self._transition(AvatarState.LEARNING, "task_success")
            self._emit(SignalType.AVATAR_TASK_COMPLETED, result.to_dict())
        else:
            self._transition(AvatarState.STRUGGLING, "task_failure")
            self._emit(SignalType.AVATAR_TASK_FAILED, result.to_dict())

        # Check burnout
        burnout = self.assess_burnout_risk()
        if burnout["risk_level"] in ("high", "critical"):
            self._emit(SignalType.AVATAR_BURNOUT_WARNING, burnout)

        return result

    def receive_coaching(self, coaching_action: Dict[str, Any]) -> None:
        """
        Receive a coaching intervention from the paired Aide.

        Transitions through RECEIVING_COACHING -> APPLYING_STRATEGY,
        then returns to ATTEMPTING_TASK (ready for retry).
        """
        avatar_state_before = self.current_state.value
        self._transition(AvatarState.RECEIVING_COACHING, "coaching_received")
        self.total_coaching_sessions += 1
        self._received_coaching_since_last_attempt = True

        self.coaching_history.append({
            "timestamp": datetime.now(),
            "coaching_action": coaching_action,
            "avatar_state_before": avatar_state_before,
            "emotional_state": self.emotional_state,
            "cognitive_load": self.cognitive_load,
        })

        self._apply_coaching_effects(coaching_action)

        # Send acknowledgement through channel
        if self.channel:
            self.channel.send(Message(
                message_type=MessageType.ACKNOWLEDGEMENT,
                sender_id=self.avatar_id,
                receiver_id=self.channel.aide_id,
                payload={"coaching_applied": True},
            ))

        self._transition(AvatarState.APPLYING_STRATEGY, "applying_coaching")

    def receive_coaching_intervention(self, intervention: CoachingIntervention) -> None:
        """
        Typed variant: receive a CoachingIntervention dataclass.
        """
        self.receive_coaching(intervention.to_dict())

    def get_observation_snapshot(self) -> ObservationReport:
        """Build a snapshot for the observing Aide."""
        recent_dicts = [r.to_dict() for r in self._recent_results[-5:]]
        return ObservationReport(
            avatar_id=self.avatar_id,
            current_state=self.current_state.value,
            emotional_state=self.emotional_state,
            cognitive_load=self.cognitive_load,
            stress_level=self.stress_level,
            active_struggles=(
                self.struggle_patterns[-1].get("indicators", [])
                if self.struggle_patterns
                else []
            ),
            recent_task_results=recent_dicts,
            independence_level=self.get_independence_level(),
            burnout_risk=self.burnout_risk_level,
        )

    def return_to_idle(self) -> None:
        """Convenience: transition back to IDLE after a learning/recovery cycle."""
        self._transition(AvatarState.IDLE, "reset_to_idle")

    def get_independence_level(self, task_type: Optional[str] = None) -> float:
        """Get independence level for a task type or overall average."""
        if task_type:
            progress = self.learning_progress.get(task_type)
            return progress.current_independence_level if progress else 0.0

        if not self.learning_progress:
            return 0.0
        total = sum(p.current_independence_level for p in self.learning_progress.values())
        return total / len(self.learning_progress)

    def assess_burnout_risk(self) -> Dict[str, Any]:
        """Assess current burnout risk from recent history."""
        recent_failures = self._count_recent_failures()
        coaching_frequency = self._calculate_coaching_frequency()
        stress_accumulation = self._calculate_stress_accumulation()

        risk_score = (
            recent_failures * 0.3
            + coaching_frequency * 0.3
            + stress_accumulation * 0.4
        )
        self.burnout_risk_level = min(risk_score, 1.0)

        if self.burnout_risk_level >= 0.8:
            risk_level = "critical"
        elif self.burnout_risk_level >= 0.6:
            risk_level = "high"
        elif self.burnout_risk_level >= 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "risk_level": risk_level,
            "risk_score": self.burnout_risk_level,
            "recent_failures": recent_failures,
            "coaching_frequency": coaching_frequency,
            "stress_accumulation": stress_accumulation,
            "recommendations": self._get_burnout_prevention_recommendations(),
        }

    def get_state_summary(self) -> Dict[str, Any]:
        """Comprehensive state snapshot for logging / monitoring."""
        return {
            "avatar_id": self.avatar_id,
            "trait_name": self.trait_name,
            "current_state": self.current_state.value,
            "emotional_state": self.emotional_state,
            "cognitive_load": self.cognitive_load,
            "stress_level": self.stress_level,
            "burnout_risk_level": self.burnout_risk_level,
            "overall_independence": self.get_independence_level(),
            "total_tasks_attempted": self.total_tasks_attempted,
            "total_tasks_completed": self.total_tasks_completed,
            "total_coaching_sessions": self.total_coaching_sessions,
            "success_rate": (
                self.total_tasks_completed / max(self.total_tasks_attempted, 1)
            ),
            "total_experiences": self.experience_memory.total_experiences,
            "learning_progress": {
                k: {
                    "attempts": v.attempts,
                    "successes": v.successes,
                    "independence": v.current_independence_level,
                    "independent_successes": v.independent_successes,
                    "consecutive_successes": v.consecutive_successes,
                }
                for k, v in self.learning_progress.items()
            },
            "recurring_struggles": self.experience_memory.get_recurring_struggles(),
            "effective_strategies": self.experience_memory.get_effective_strategies(),
            "last_activity": self.last_activity.isoformat(),
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _transition(self, target: AvatarState, trigger: str) -> None:
        """Attempt a state machine transition, falling back gracefully."""
        if target == self._state_machine.current_state:
            return
        try:
            self._state_machine.transition_to(target, trigger=trigger)
        except InvalidTransitionError:
            # Fallback: allow it but log
            self._state_machine.reset(target)

    def _on_state_entered(
        self, from_state: AvatarState, to_state: AvatarState, meta: Dict[str, Any]
    ) -> None:
        """Callback fired whenever the state machine enters a new state."""
        self._emit(SignalType.AVATAR_STATE_CHANGED, {
            "from_state": from_state.value,
            "to_state": to_state.value,
            "emotional_state": self.emotional_state,
            "cognitive_load": self.cognitive_load,
        })

    def _emit(self, signal_type: SignalType, data: Dict[str, Any]) -> None:
        """Emit a signal on the event bus."""
        self.event_bus.emit(Signal(
            signal_type=signal_type,
            source_id=self.avatar_id,
            source_type="avatar",
            data=data,
        ))

    def _experience_bonus(self, task_context: Dict[str, Any]) -> float:
        """
        Derive a small success-probability bonus from past experiences.

        This is experiential learning in action: the Avatar gets better
        at tasks it has practiced, especially when coaching strategies
        were internalised.
        """
        task_type = task_context.get("task_type", "unknown")
        past = self.experience_memory.recall_by_task(task_type, limit=10)
        if not past:
            return 0.0
        recent_successes = sum(1 for r in past if r.outcome_success)
        return min(0.15, recent_successes * 0.02)

    def _check_independence(self, task_context: Dict[str, Any]) -> bool:
        """Check if the Avatar qualifies as independent for this task."""
        task_type = task_context.get("task_type", "unknown")
        progress = self.learning_progress.get(task_type)
        if not progress:
            return False
        return progress.current_independence_level >= 0.8

    def _store_recent_result(self, result: TaskResult) -> None:
        self._recent_results.append(result)
        if len(self._recent_results) > self._max_recent:
            self._recent_results = self._recent_results[-self._max_recent:]

    def _record_experience(
        self,
        task_context: Dict[str, Any],
        result: TaskResult,
        struggles: List[str],
    ) -> None:
        """Commit this attempt to long-term experience memory."""
        coaching_recent = (
            [c["coaching_action"] for c in self.coaching_history[-2:]]
            if self.coaching_history
            else []
        )
        self.experience_memory.record(ExperienceRecord(
            task_type=task_context.get("task_type", "unknown"),
            task_context=task_context,
            struggles_experienced=struggles,
            emotional_journey=[self.emotional_state],
            cognitive_load_peak=self.cognitive_load,
            stress_peak=self.stress_level,
            outcome_success=result.success,
            quality_score=result.quality_score,
            coaching_received=coaching_recent,
            independence_delta=(
                INDEPENDENCE_GAIN_INDEPENDENT_SUCCESS
                if result.independent and result.success
                else 0.0
            ),
            strategy_discovered=(
                result.strategies_used[0] if result.strategies_used else None
            ),
        ))

    def _calculate_quality_score(
        self,
        success: bool,
        trait_impact: Dict[str, Any],
        struggle_indicators: List[str],
    ) -> float:
        if not success:
            return 0.0
        base_quality = 0.8
        struggle_penalty = len(struggle_indicators) * 0.1
        trait_penalty = trait_impact.get("quality_modifier", 0.0)
        return max(0.0, min(1.0, base_quality - struggle_penalty - trait_penalty))

    def _calculate_completion_time(
        self, task_context: Dict[str, Any], trait_impact: Dict[str, Any]
    ) -> timedelta:
        base_time = task_context.get("expected_duration", timedelta(minutes=10))
        time_modifier = trait_impact.get("time_modifier", 1.0)
        random_factor = random.uniform(0.8, 1.2)
        return base_time * time_modifier * random_factor

    def _update_emotional_state(
        self, success: bool, struggle_indicators: List[str]
    ) -> None:
        if success:
            self.emotional_state = "confident" if not struggle_indicators else "relieved"
        else:
            self.emotional_state = (
                "frustrated" if len(struggle_indicators) > 3 else "disappointed"
            )

    def _update_cognitive_load(
        self, task_context: Dict[str, Any], trait_impact: Dict[str, Any]
    ) -> None:
        base_load = task_context.get("cognitive_demand", 0.5)
        trait_load = trait_impact.get("cognitive_load_modifier", 0.0)
        self.cognitive_load = min(1.0, base_load + trait_load)

    def _update_learning_progress(
        self, task_context: Dict[str, Any], result: TaskResult
    ) -> None:
        task_type = task_context.get("task_type", "unknown")
        if task_type not in self.learning_progress:
            self.learning_progress[task_type] = LearningProgress(task_type=task_type)

        progress = self.learning_progress[task_type]
        progress.attempts += 1

        if result.success:
            progress.successes += 1
            progress.consecutive_successes += 1
            progress.consecutive_failures = 0

            if result.independent:
                progress.independent_successes += 1
                progress.independence_milestones.append(datetime.now())
                progress.current_independence_level = min(
                    1.0,
                    progress.current_independence_level
                    + INDEPENDENCE_GAIN_INDEPENDENT_SUCCESS,
                )
            else:
                progress.current_independence_level = min(
                    1.0,
                    progress.current_independence_level
                    + INDEPENDENCE_GAIN_COACHED_SUCCESS,
                )
            progress.last_improvement = datetime.now()
        else:
            progress.consecutive_failures += 1
            progress.consecutive_successes = 0
            # Slight independence regression on failure
            progress.current_independence_level = max(
                0.0,
                progress.current_independence_level - INDEPENDENCE_LOSS_ON_FAILURE,
            )

    def _apply_coaching_effects(self, coaching_action: Dict[str, Any]) -> None:
        stress_reduction = coaching_action.get("stress_reduction", 0.0)
        self.stress_level = max(0.0, self.stress_level - stress_reduction)

        focus_restoration = coaching_action.get("focus_restoration", 0.0)
        self.cognitive_load = max(0.0, self.cognitive_load - focus_restoration)

        emotional_boost = coaching_action.get("emotional_boost", 0.0)
        if emotional_boost > 0:
            if self.emotional_state in ("frustrated", "disappointed", "overwhelmed"):
                self.emotional_state = "hopeful"
            elif self.emotional_state == "hopeful":
                self.emotional_state = "confident"

    # --- Burnout helpers (replacing placeholders) -----------------------

    def _count_recent_failures(self) -> float:
        """Fraction of recent results that were failures (0.0 – 1.0)."""
        if not self._recent_results:
            return 0.0
        recent = self._recent_results[-10:]
        failures = sum(1 for r in recent if not r.success)
        return failures / len(recent)

    def _calculate_coaching_frequency(self) -> float:
        """
        Normalised coaching frequency (0.0 – 1.0).

        A ratio near 1.0 means the Avatar needed coaching almost every attempt —
        a sign it is not developing independence and may be overwhelmed.
        """
        if self.total_tasks_attempted == 0:
            return 0.0
        return min(1.0, self.total_coaching_sessions / max(self.total_tasks_attempted, 1))

    def _calculate_stress_accumulation(self) -> float:
        return self.stress_level

    def _get_burnout_prevention_recommendations(self) -> List[str]:
        recommendations: List[str] = []
        if self.burnout_risk_level > 0.6:
            recommendations.append("Reduce task difficulty")
            recommendations.append("Increase break frequency")
            recommendations.append("Focus on emotional support")
        if self.stress_level > 0.7:
            recommendations.append("Implement stress reduction techniques")
            recommendations.append("Consider task modification")
        if self._count_recent_failures() > 0.6:
            recommendations.append("Switch to easier tasks to rebuild confidence")
        return recommendations
