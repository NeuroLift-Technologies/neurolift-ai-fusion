"""
Base Aide Class

The foundation for all coaching Aides. Implements core coaching behavior,
expertise integration, and real-time intervention capabilities.

Each Aide combines PhD-level expertise in specific executive functions with
real-world feedback from successful ADHD individuals, plus RRT foundation
for burnout response and crisis intervention.

Architecture notes
------------------
* The Aide *observes* its paired Avatar through an InteractionChannel
  and ObservationReport snapshots — never by reaching into Avatar internals.
* Strategy selection is driven by a lightweight effectiveness tracker
  that learns which strategies work for which contexts over time.
* The Aide subscribes to Avatar signals via the EventBus so it can
  react to state changes, burnout warnings, and independence milestones
  without polling.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import uuid
from datetime import datetime, timedelta

from ..core.events import EventBus, Signal, SignalType
from ..core.protocols import (
    CoachingIntervention,
    InteractionChannel,
    Message,
    MessageType,
    ObservationReport,
)
from ..avatars.base_avatar import BaseAvatar, AvatarState, TaskResult


# ---------------------------------------------------------------------------
# Tuning constants
# ---------------------------------------------------------------------------

INTERVENTION_ATTRIBUTION_WINDOW = timedelta(minutes=10)
HIGH_STRESS_RISK_THRESHOLD = 0.7
HIGH_COGNITIVE_LOAD_RISK_THRESHOLD = 0.8
NEGATIVE_EMOTIONAL_STATES = ("frustrated", "overwhelmed")


# ---------------------------------------------------------------------------
# Enums and data classes
# ---------------------------------------------------------------------------

class CoachingType(Enum):
    """Types of coaching interventions."""
    PREVENTIVE = "preventive"
    REACTIVE = "reactive"
    CRISIS = "crisis"
    RECOVERY = "recovery"
    INDEPENDENCE_BUILDING = "independence_building"


class InterventionUrgency(Enum):
    """Urgency levels for interventions."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class CoachingContext:
    """Context snapshot assembled for a coaching decision."""
    avatar_id: str
    observation: ObservationReport
    task_context: Dict[str, Any]
    coaching_history_summary: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class CoachingAction:
    """A coaching intervention action (legacy compat wrapper)."""
    action_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    coaching_type: CoachingType = CoachingType.REACTIVE
    urgency: InterventionUrgency = InterventionUrgency.MEDIUM
    strategy: str = ""
    specific_techniques: List[str] = field(default_factory=list)
    expected_outcomes: List[str] = field(default_factory=list)
    stress_reduction: float = 0.0
    emotional_boost: float = 0.0
    cognitive_support: float = 0.0
    focus_restoration: float = 0.0
    independence_building: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "coaching_type": self.coaching_type.value,
            "urgency": self.urgency.value,
            "strategy": self.strategy,
            "specific_techniques": self.specific_techniques,
            "expected_outcomes": self.expected_outcomes,
            "stress_reduction": self.stress_reduction,
            "emotional_boost": self.emotional_boost,
            "cognitive_support": self.cognitive_support,
            "focus_restoration": self.focus_restoration,
            "independence_building": self.independence_building,
            "timestamp": self.timestamp.isoformat(),
        }

    def to_intervention(self) -> CoachingIntervention:
        """Convert to the typed CoachingIntervention protocol object."""
        return CoachingIntervention(
            strategy_name=self.strategy,
            techniques=self.specific_techniques,
            rationale=f"{self.coaching_type.value} intervention",
            stress_reduction=self.stress_reduction,
            emotional_boost=self.emotional_boost,
            cognitive_support=self.cognitive_support,
            focus_restoration=self.focus_restoration,
            independence_nudge=self.independence_building,
            source="aide",
            urgency=self.urgency.value,
        )


@dataclass
class BurnoutRisk:
    """Burnout risk assessment."""
    risk_level: str  # "low", "medium", "high", "critical"
    risk_score: float  # 0.0 to 1.0
    contributing_factors: List[str]
    early_warning_signs: List[str]
    intervention_recommendations: List[str]
    rrt_activation_needed: bool = False
    timestamp: datetime = field(default_factory=datetime.now)


# ---------------------------------------------------------------------------
# Strategy effectiveness tracker
# ---------------------------------------------------------------------------

@dataclass
class _StrategyRecord:
    """Internal record for tracking how a strategy performs."""
    strategy_name: str
    times_used: int = 0
    times_effective: int = 0

    @property
    def effectiveness(self) -> float:
        if self.times_used == 0:
            return 0.5  # prior
        return self.times_effective / self.times_used


# ---------------------------------------------------------------------------
# BaseAide
# ---------------------------------------------------------------------------

class BaseAide(ABC):
    """
    Base class for all coaching Aides.

    Combines PhD-level expertise with real-world wisdom and an RRT
    foundation for crisis response.
    """

    def __init__(
        self,
        aide_id: str,
        expertise_config: Dict[str, Any],
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self.aide_id = aide_id
        self.expertise_config = expertise_config
        self.expertise_area: str = expertise_config.get("expertise_area", "unknown")

        # Event bus (shared with Avatar and WorldEngine)
        self.event_bus = event_bus or EventBus()

        # Interaction channel — set when paired with an Avatar
        self.channel: Optional[InteractionChannel] = None

        # Paired Avatar reference (for observation convenience)
        self._avatar: Optional[BaseAvatar] = None

        # Strategy effectiveness learning
        self._strategy_records: Dict[str, _StrategyRecord] = {}
        self._pending_interventions: Dict[str, datetime] = {}

        # Coaching state
        self.intervention_history: List[CoachingAction] = []
        self.success_patterns: Dict[str, Any] = {}
        self.failure_patterns: Dict[str, Any] = {}

        # Counters
        self.total_interventions: int = 0
        self.successful_interventions: int = 0
        self.crisis_interventions: int = 0
        self.independence_achievements: int = 0

        # Event subscriptions (populated on bind)
        self._subscriptions: List[str] = []

        # Timestamps
        self.created_at = datetime.now()
        self.last_intervention = datetime.now()

    # ------------------------------------------------------------------
    # Abstract interface — each expertise area implements these
    # ------------------------------------------------------------------

    @abstractmethod
    def get_expertise_strategies(self, context: CoachingContext) -> List[Dict[str, Any]]:
        """Return PhD-level strategies for the current context."""

    @abstractmethod
    def get_real_world_insights(self, context: CoachingContext) -> List[Dict[str, Any]]:
        """Return real-world insights from successful ADHD individuals."""

    # ------------------------------------------------------------------
    # Binding & lifecycle
    # ------------------------------------------------------------------

    def bind_to_avatar(
        self,
        avatar: BaseAvatar,
        channel: Optional[InteractionChannel] = None,
    ) -> InteractionChannel:
        """
        Pair this Aide with an Avatar.

        Creates an InteractionChannel (or uses the provided one),
        binds both sides, and subscribes to the Avatar's signals.
        """
        self._avatar = avatar

        # Create or reuse channel
        if channel is None:
            channel = InteractionChannel(
                avatar_id=avatar.avatar_id,
                aide_id=self.aide_id,
            )
        self.channel = channel
        avatar.bind_channel(channel)

        # Share event bus
        if avatar.event_bus is not self.event_bus:
            self.event_bus = avatar.event_bus

        # Subscribe to Avatar signals
        self._subscriptions.append(
            self.event_bus.subscribe(
                SignalType.AVATAR_STRUGGLING,
                self._on_avatar_struggling,
                source_filter=avatar.avatar_id,
            )
        )
        self._subscriptions.append(
            self.event_bus.subscribe(
                SignalType.AVATAR_BURNOUT_WARNING,
                self._on_avatar_burnout_warning,
                source_filter=avatar.avatar_id,
            )
        )
        self._subscriptions.append(
            self.event_bus.subscribe(
                SignalType.AVATAR_TASK_COMPLETED,
                self._on_avatar_task_completed,
                source_filter=avatar.avatar_id,
            )
        )
        self._subscriptions.append(
            self.event_bus.subscribe(
                SignalType.AVATAR_INDEPENDENCE_MILESTONE,
                self._on_avatar_independence,
                source_filter=avatar.avatar_id,
            )
        )

        return channel

    def unbind(self) -> None:
        """Unsubscribe from Avatar signals and clear references."""
        for sub_id in self._subscriptions:
            self.event_bus.unsubscribe(sub_id)
        self._subscriptions.clear()
        self._avatar = None
        self.channel = None

    # ------------------------------------------------------------------
    # Signal handlers (reactive coaching)
    # ------------------------------------------------------------------

    def _on_avatar_struggling(self, signal: Signal) -> None:
        """React to an Avatar entering the STRUGGLING state."""
        if self._avatar is None:
            return
        observation = self._avatar.get_observation_snapshot()
        if observation.needs_intervention:
            self._deliver_coaching(observation, signal.data.get("task_context", {}))

    def _on_avatar_burnout_warning(self, signal: Signal) -> None:
        """React to a burnout warning — trigger crisis protocol."""
        if self._avatar is None:
            return
        observation = self._avatar.get_observation_snapshot()
        self._deliver_crisis_coaching(observation)

    def _on_avatar_task_completed(self, signal: Signal) -> None:
        """Track effectiveness when Avatar completes a task after coaching."""
        if not self.intervention_history:
            return

        last_action = self.intervention_history[-1]
        if last_action.action_id not in self._pending_interventions:
            return

        signal_data = getattr(signal, "data", {}) or {}
        completed_raw = signal_data.get("timestamp")
        if isinstance(completed_raw, datetime):
            completion_time = completed_raw
        elif isinstance(completed_raw, str):
            try:
                completion_time = datetime.fromisoformat(completed_raw)
            except ValueError:
                completion_time = datetime.now()
        else:
            completion_time = datetime.now()

        if completion_time < last_action.timestamp:
            return

        if completion_time - last_action.timestamp > INTERVENTION_ATTRIBUTION_WINDOW:
            self._pending_interventions.pop(last_action.action_id, None)
            return

        self._record_strategy_outcome(last_action.strategy, effective=True)
        self._pending_interventions.pop(last_action.action_id, None)

    def _on_avatar_independence(self, signal: Signal) -> None:
        """Celebrate and record independence milestones."""
        self.independence_achievements += 1
        self._emit(SignalType.AIDE_STRATEGY_ADAPTED, {
            "event": "independence_achieved",
            "task_type": signal.data.get("task_type", "unknown"),
        })

    # ------------------------------------------------------------------
    # Core coaching API
    # ------------------------------------------------------------------

    def observe_and_coach(
        self,
        task_context: Dict[str, Any],
    ) -> Optional[CoachingAction]:
        """
        One-shot observe-then-coach cycle.

        Useful for synchronous orchestration.  The SessionOrchestrator
        calls this after each Avatar task attempt.
        """
        if self._avatar is None:
            return None

        observation = self._avatar.get_observation_snapshot()

        if not self._should_intervene(observation):
            return None

        return self._deliver_coaching(observation, task_context)

    def observe_avatar_struggle(
        self, avatar: BaseAvatar, task_context: Dict[str, Any]
    ) -> None:
        """Legacy API: observe and optionally coach."""
        if self._avatar is None:
            self._avatar = avatar
        observation = avatar.get_observation_snapshot()
        if self._should_intervene(observation):
            self._deliver_coaching(observation, task_context)

    def provide_coaching(self, context: CoachingContext) -> Optional[CoachingAction]:
        """
        Build and return a CoachingAction for the given context.

        Does NOT deliver it to the Avatar — the caller is responsible
        for that.
        """
        if self._requires_crisis_intervention(context.observation):
            return self._build_crisis_action()

        expertise = self.get_expertise_strategies(context)
        insights = self.get_real_world_insights(context)
        combined = self._combine_strategies(expertise, insights)
        selected = self._select_optimal_strategy(combined, context)

        if not selected:
            return None

        return CoachingAction(
            coaching_type=self._determine_coaching_type(context.observation),
            urgency=self._assess_urgency(context.observation),
            strategy=selected["strategy"],
            specific_techniques=selected.get("techniques", []),
            expected_outcomes=selected.get("expected_outcomes", []),
            stress_reduction=selected.get("stress_reduction", 0.0),
            emotional_boost=selected.get("emotional_boost", 0.0),
            cognitive_support=selected.get("cognitive_support", 0.0),
            focus_restoration=selected.get("focus_restoration", 0.0),
            independence_building=selected.get("independence_building", 0.0),
        )

    def assess_burnout_risk(self, avatar: BaseAvatar) -> BurnoutRisk:
        """Evaluate burnout risk, combining Avatar self-assessment with Aide expertise."""
        avatar_burnout = avatar.assess_burnout_risk()
        return BurnoutRisk(
            risk_level=avatar_burnout["risk_level"],
            risk_score=avatar_burnout["risk_score"],
            contributing_factors=self._identify_risk_factors(avatar),
            early_warning_signs=self._detect_early_warning_signs(avatar),
            intervention_recommendations=self._generate_intervention_recommendations(avatar),
            rrt_activation_needed=avatar_burnout["risk_level"] in ("high", "critical"),
        )

    def track_intervention_effectiveness(
        self, action: CoachingAction, avatar_result: TaskResult
    ) -> None:
        """Track whether a coaching intervention was effective."""
        success_indicators = [
            avatar_result.success,
            avatar_result.quality_score > 0.7,
            len(avatar_result.struggle_indicators) < len(action.specific_techniques),
            avatar_result.emotional_state in ("confident", "relieved", "hopeful"),
        ]
        effective = sum(success_indicators) >= 2

        if effective:
            self.successful_interventions += 1
            self._record_success_pattern(action, avatar_result)
        else:
            self._record_failure_pattern(action, avatar_result)

        self._record_strategy_outcome(action.strategy, effective)
        self._pending_interventions.pop(action.action_id, None)

    def get_coaching_effectiveness_metrics(self) -> Dict[str, Any]:
        total = max(self.total_interventions, 1)
        return {
            "aide_id": self.aide_id,
            "expertise_area": self.expertise_area,
            "total_interventions": self.total_interventions,
            "successful_interventions": self.successful_interventions,
            "success_rate": self.successful_interventions / total,
            "crisis_interventions": self.crisis_interventions,
            "independence_achievements": self.independence_achievements,
            "strategy_effectiveness": self.get_strategy_effectiveness_summary(),
            "last_intervention": self.last_intervention.isoformat(),
        }

    # ------------------------------------------------------------------
    # Private helpers — coaching delivery
    # ------------------------------------------------------------------

    def _deliver_coaching(
        self,
        observation: ObservationReport,
        task_context: Dict[str, Any],
    ) -> Optional[CoachingAction]:
        """Build, send, and record a coaching intervention."""
        context = CoachingContext(
            avatar_id=observation.avatar_id,
            observation=observation,
            task_context=task_context,
        )

        action = self.provide_coaching(context)
        if action is None:
            return None

        # Deliver to Avatar
        if self._avatar is not None:
            self._avatar.receive_coaching(action.to_dict())

        # Send through channel
        if self.channel:
            self.channel.send(Message(
                message_type=MessageType.COACHING_INTERVENTION,
                sender_id=self.aide_id,
                receiver_id=observation.avatar_id,
                payload=action.to_dict(),
            ))

        self.intervention_history.append(action)
        self.total_interventions += 1
        self.last_intervention = datetime.now()
        self._pending_interventions[action.action_id] = action.timestamp

        self._emit(SignalType.AIDE_COACHING_DELIVERED, {
            "strategy": action.strategy,
            "urgency": action.urgency.value,
            "avatar_id": observation.avatar_id,
        })

        return action

    def _deliver_crisis_coaching(self, observation: ObservationReport) -> CoachingAction:
        """Deliver an immediate crisis intervention."""
        action = self._build_crisis_action()

        if self._avatar is not None:
            self._avatar.receive_coaching(action.to_dict())

        if self.channel:
            self.channel.send(Message(
                message_type=MessageType.COACHING_INTERVENTION,
                sender_id=self.aide_id,
                receiver_id=observation.avatar_id,
                payload=action.to_dict(),
            ))

        self.intervention_history.append(action)
        self.total_interventions += 1
        self.crisis_interventions += 1
        self.last_intervention = datetime.now()
        self._pending_interventions[action.action_id] = action.timestamp
        return action

    def _build_crisis_action(self) -> CoachingAction:
        """Build a crisis-level coaching action (RRT protocol)."""
        return CoachingAction(
            coaching_type=CoachingType.CRISIS,
            urgency=InterventionUrgency.CRITICAL,
            strategy="Crisis stabilization and immediate support",
            specific_techniques=[
                "Immediate stress reduction",
                "Emotional validation",
                "Task modification or removal",
                "Recovery protocol activation",
            ],
            expected_outcomes=[
                "Reduced immediate stress",
                "Stabilized emotional state",
                "Prevented burnout",
                "Initiated recovery process",
            ],
            stress_reduction=0.5,
            emotional_boost=0.3,
            cognitive_support=0.4,
            focus_restoration=0.3,
        )

    # ------------------------------------------------------------------
    # Private helpers — intervention decisions
    # ------------------------------------------------------------------

    def _should_intervene(self, obs: ObservationReport) -> bool:
        """Decide whether the Aide should step in."""
        if obs.needs_intervention:
            return True
        # Also intervene if independence is low and Avatar just failed
        if obs.independence_level < 0.3 and obs.recent_task_results:
            last = obs.recent_task_results[-1]
            if not last.get("success", True):
                return True
        return False

    def _requires_crisis_intervention(self, obs: ObservationReport) -> bool:
        return obs.burnout_risk > 0.8 or obs.stress_level > 0.9

    def _determine_coaching_type(self, obs: ObservationReport) -> CoachingType:
        if obs.burnout_risk > 0.7:
            return CoachingType.CRISIS
        if obs.current_state == AvatarState.STRUGGLING.value:
            return CoachingType.REACTIVE
        if obs.independence_level > 0.6:
            return CoachingType.INDEPENDENCE_BUILDING
        return CoachingType.PREVENTIVE

    def _assess_urgency(self, obs: ObservationReport) -> InterventionUrgency:
        if obs.burnout_risk > 0.8:
            return InterventionUrgency.CRITICAL
        if obs.stress_level > 0.8 or obs.cognitive_load > 0.9:
            return InterventionUrgency.HIGH
        if obs.emotional_state in ("frustrated", "overwhelmed"):
            return InterventionUrgency.MEDIUM
        return InterventionUrgency.LOW

    # ------------------------------------------------------------------
    # Private helpers — strategy selection & learning
    # ------------------------------------------------------------------

    def _combine_strategies(
        self,
        expertise: List[Dict[str, Any]],
        insights: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        combined: List[Dict[str, Any]] = []
        for s in expertise:
            s.setdefault("source", "phd_expertise")
            combined.append(s)
        for s in insights:
            s.setdefault("source", "real_world")
            combined.append(s)
        return combined

    def _select_optimal_strategy(
        self,
        strategies: List[Dict[str, Any]],
        context: CoachingContext,
    ) -> Optional[Dict[str, Any]]:
        if not strategies:
            return None

        scored = []
        for s in strategies:
            score = self._score_strategy(s, context)
            scored.append((score, s))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1]

    def _score_strategy(
        self, strategy: Dict[str, Any], context: CoachingContext
    ) -> float:
        score = 0.3  # base

        # Prefer real-world insights slightly
        if strategy.get("source") == "real_world":
            score += 0.1

        # Context match
        score += strategy.get("context_match", 0.0) * 0.3

        # Historical effectiveness from our tracker
        name = strategy.get("strategy", strategy.get("description", ""))
        record = self._strategy_records.get(name)
        if record:
            score += record.effectiveness * 0.3
        else:
            score += strategy.get("effectiveness", 0.5) * 0.2

        return score

    def _record_strategy_outcome(self, strategy_name: str, effective: bool) -> None:
        if strategy_name not in self._strategy_records:
            self._strategy_records[strategy_name] = _StrategyRecord(
                strategy_name=strategy_name
            )
        rec = self._strategy_records[strategy_name]
        rec.times_used += 1
        if effective:
            rec.times_effective += 1

    def get_strategy_effectiveness_summary(self) -> Dict[str, Any]:
        return {
            name: {
                "times_used": rec.times_used,
                "effectiveness": round(rec.effectiveness, 3),
            }
            for name, rec in self._strategy_records.items()
        }

    def _get_strategy_effectiveness_summary(self) -> Dict[str, Any]:
        """Backward-compatible alias for existing callers."""
        return self.get_strategy_effectiveness_summary()

    # ------------------------------------------------------------------
    # Private helpers — risk assessment
    # ------------------------------------------------------------------

    def _identify_risk_factors(self, avatar: BaseAvatar) -> List[str]:
        factors: List[str] = []
        if avatar.stress_level > HIGH_STRESS_RISK_THRESHOLD:
            factors.append("High stress level")
        if avatar.cognitive_load > HIGH_COGNITIVE_LOAD_RISK_THRESHOLD:
            factors.append("High cognitive load")
        if avatar.emotional_state in NEGATIVE_EMOTIONAL_STATES:
            factors.append("Negative emotional state")
        return factors

    def _detect_early_warning_signs(self, avatar: BaseAvatar) -> List[str]:
        signs: List[str] = []
        if avatar.burnout_risk_level > 0.5:
            signs.append("Elevated burnout risk score")
        if avatar.emotional_state == "frustrated":
            signs.append("Increased frustration")
        if avatar.cognitive_load > 0.7:
            signs.append("High cognitive load")
        return signs

    def _generate_intervention_recommendations(self, avatar: BaseAvatar) -> List[str]:
        recs: List[str] = []
        if avatar.stress_level > HIGH_STRESS_RISK_THRESHOLD:
            recs.append("Implement stress reduction techniques")
        if avatar.cognitive_load > HIGH_COGNITIVE_LOAD_RISK_THRESHOLD:
            recs.append("Reduce task complexity")
        if avatar.emotional_state in NEGATIVE_EMOTIONAL_STATES:
            recs.append("Provide emotional support and validation")
        return recs

    # ------------------------------------------------------------------
    # Private helpers — pattern recording
    # ------------------------------------------------------------------

    def _record_success_pattern(self, action: CoachingAction, result: TaskResult) -> None:
        key = f"{action.strategy}_{action.coaching_type.value}"
        if key not in self.success_patterns:
            self.success_patterns[key] = {"count": 0, "contexts": []}
        self.success_patterns[key]["count"] += 1
        self.success_patterns[key]["contexts"].append({
            "emotional_state": result.emotional_state,
            "cognitive_load": result.cognitive_load,
        })

    def _record_failure_pattern(self, action: CoachingAction, result: TaskResult) -> None:
        key = f"{action.strategy}_{action.coaching_type.value}"
        if key not in self.failure_patterns:
            self.failure_patterns[key] = {"count": 0, "contexts": []}
        self.failure_patterns[key]["count"] += 1
        self.failure_patterns[key]["contexts"].append({
            "emotional_state": result.emotional_state,
            "cognitive_load": result.cognitive_load,
        })

    # ------------------------------------------------------------------
    # Event emission
    # ------------------------------------------------------------------

    def _emit(self, signal_type: SignalType, data: Dict[str, Any]) -> None:
        self.event_bus.emit(Signal(
            signal_type=signal_type,
            source_id=self.aide_id,
            source_type="aide",
            data=data,
        ))
