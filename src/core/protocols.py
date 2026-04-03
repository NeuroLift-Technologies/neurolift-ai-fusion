"""
Interaction Protocols

Defines the formal message types and communication channels between
Avatars and Aides.  Also provides ExperienceMemory — the system that
lets Avatars learn through doing rather than through data.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, ClassVar, Deque, Dict, List, Optional
from collections import deque
from datetime import datetime
import uuid


# ---------------------------------------------------------------------------
# Message types exchanged between Avatar and Aide
# ---------------------------------------------------------------------------

class MessageType(Enum):
    """Types of messages passed through the InteractionChannel."""

    # Avatar -> Aide
    STRUGGLE_REPORT = auto()        # Avatar reports current struggles
    HELP_REQUEST = auto()           # Avatar explicitly asks for help
    STATUS_UPDATE = auto()          # Periodic state snapshot
    TASK_RESULT = auto()            # Outcome of a task attempt

    # Aide -> Avatar
    COACHING_INTERVENTION = auto()  # Coaching action to apply
    ENCOURAGEMENT = auto()          # Emotional support without technique
    STRATEGY_SUGGESTION = auto()    # Suggestion for Avatar to try
    INDEPENDENCE_PROMPT = auto()    # Nudge toward independent action

    # Bidirectional
    ACKNOWLEDGEMENT = auto()        # Simple receipt confirmation


@dataclass
class Message:
    """A single message between Avatar and Aide."""

    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message_type: MessageType = MessageType.STATUS_UPDATE
    sender_id: str = ""
    receiver_id: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    in_response_to: Optional[str] = None  # message_id of the prompt

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "message_type": self.message_type.name,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "in_response_to": self.in_response_to,
        }


# ---------------------------------------------------------------------------
# Structured observation and coaching payloads
# ---------------------------------------------------------------------------

@dataclass
class ObservationReport:
    """
    What an Aide sees when observing an Avatar.

    Populated automatically by the InteractionChannel so the Aide
    receives a consistent snapshot every observation tick.
    """

    avatar_id: str = ""
    current_state: str = ""
    emotional_state: str = ""
    cognitive_load: float = 0.0
    stress_level: float = 0.0
    active_struggles: List[str] = field(default_factory=list)
    recent_task_results: List[Dict[str, Any]] = field(default_factory=list)
    independence_level: float = 0.0
    burnout_risk: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

    STRESS_INTERVENTION_THRESHOLD: ClassVar[float] = 0.7
    LOAD_INTERVENTION_THRESHOLD: ClassVar[float] = 0.8
    BURNOUT_INTERVENTION_THRESHOLD: ClassVar[float] = 0.6
    STRUGGLE_COUNT_INTERVENTION_THRESHOLD: ClassVar[int] = 3
    INTERVENTION_EMOTIONAL_STATES: ClassVar[tuple[str, ...]] = (
        "frustrated",
        "overwhelmed",
        "defeated",
    )

    @property
    def needs_intervention(self) -> bool:
        """Quick check: does this snapshot warrant aide action?"""
        return (
            self.stress_level > self.STRESS_INTERVENTION_THRESHOLD
            or self.cognitive_load > self.LOAD_INTERVENTION_THRESHOLD
            or self.burnout_risk > self.BURNOUT_INTERVENTION_THRESHOLD
            or self.emotional_state in self.INTERVENTION_EMOTIONAL_STATES
            or len(self.active_struggles) >= self.STRUGGLE_COUNT_INTERVENTION_THRESHOLD
        )


@dataclass
class CoachingIntervention:
    """
    A structured coaching action delivered through the channel.

    Separates the *what* (strategy + techniques) from the *how*
    (stress_reduction, emotional_boost, etc.) so the Avatar can
    apply effects deterministically.
    """

    intervention_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    strategy_name: str = ""
    techniques: List[str] = field(default_factory=list)
    rationale: str = ""

    # Quantified effects the Avatar applies to its state
    stress_reduction: float = 0.0
    emotional_boost: float = 0.0
    cognitive_support: float = 0.0
    focus_restoration: float = 0.0
    independence_nudge: float = 0.0

    # Metadata
    source: str = ""  # "phd_expertise", "real_world", "rrt"
    urgency: str = "medium"  # "low", "medium", "high", "critical"
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "intervention_id": self.intervention_id,
            "strategy_name": self.strategy_name,
            "techniques": self.techniques,
            "rationale": self.rationale,
            "stress_reduction": self.stress_reduction,
            "emotional_boost": self.emotional_boost,
            "cognitive_support": self.cognitive_support,
            "focus_restoration": self.focus_restoration,
            "independence_nudge": self.independence_nudge,
            "source": self.source,
            "urgency": self.urgency,
            "timestamp": self.timestamp.isoformat(),
        }


# ---------------------------------------------------------------------------
# Interaction Channel — the pipe between one Avatar and one Aide
# ---------------------------------------------------------------------------

class InteractionChannel:
    """
    Bidirectional communication channel binding one Avatar to one Aide.

    Maintains a message log and provides helpers for the common
    interaction patterns (observe, coach, acknowledge).
    """

    def __init__(self, avatar_id: str, aide_id: str, max_history: int = 500) -> None:
        self.channel_id = str(uuid.uuid4())
        self.avatar_id = avatar_id
        self.aide_id = aide_id
        self._messages: Deque[Message] = deque(maxlen=max_history)
        self.created_at = datetime.now()

    def send(self, message: Message) -> None:
        """Add a message to the channel."""
        self._messages.append(message)

    def get_messages(
        self,
        message_type: Optional[MessageType] = None,
        sender_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[Message]:
        """Retrieve messages with optional filters."""
        msgs: List[Message] = list(self._messages)
        if message_type:
            msgs = [m for m in msgs if m.message_type == message_type]
        if sender_id:
            msgs = [m for m in msgs if m.sender_id == sender_id]
        return msgs[-limit:]

    def get_recent_coaching(self, limit: int = 5) -> List[Message]:
        """Shortcut: last N coaching interventions."""
        return self.get_messages(
            message_type=MessageType.COACHING_INTERVENTION, limit=limit
        )

    def get_recent_struggles(self, limit: int = 5) -> List[Message]:
        """Shortcut: last N struggle reports."""
        return self.get_messages(
            message_type=MessageType.STRUGGLE_REPORT, limit=limit
        )

    @property
    def message_count(self) -> int:
        return len(self._messages)

    @property
    def coaching_count(self) -> int:
        return sum(
            1
            for m in self._messages
            if m.message_type == MessageType.COACHING_INTERVENTION
        )


# ---------------------------------------------------------------------------
# Experience Memory — how Avatars learn through doing
# ---------------------------------------------------------------------------

@dataclass
class ExperienceRecord:
    """
    A single experiential learning record.

    Captures the full loop: what the Avatar tried, what happened,
    what coaching was received, and what worked.  This is the raw
    material for experiential learning — not training data, but
    *lived experience*.
    """

    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_type: str = ""
    task_context: Dict[str, Any] = field(default_factory=dict)

    # What happened
    struggles_experienced: List[str] = field(default_factory=list)
    emotional_journey: List[str] = field(default_factory=list)  # sequence of states
    cognitive_load_peak: float = 0.0
    stress_peak: float = 0.0
    outcome_success: bool = False
    quality_score: float = 0.0

    # What coaching was received
    coaching_received: List[Dict[str, Any]] = field(default_factory=list)
    coaching_helpful: Optional[bool] = None

    # What was learned
    strategy_discovered: Optional[str] = None
    independence_delta: float = 0.0  # change in independence level

    timestamp: datetime = field(default_factory=datetime.now)


class ExperienceMemory:
    """
    Long-term experiential memory for an Avatar.

    Stores ExperienceRecords and provides retrieval patterns that
    support experiential learning:
    - What strategies worked for similar tasks?
    - What struggles recur most often?
    - Where has independence improved?

    This is explicitly *not* a training dataset.  It is a structured
    autobiography that the Avatar and (later) the Advocate draw on
    to empathise and strategise.
    """

    def __init__(self, owner_id: str, capacity: int = 5000) -> None:
        self.owner_id = owner_id
        self._records: Deque[ExperienceRecord] = deque(maxlen=capacity)

    def record(self, experience: ExperienceRecord) -> None:
        """Store a new experience."""
        self._records.append(experience)

    def get_records(self, limit: Optional[int] = None) -> List[ExperienceRecord]:
        """Public accessor for stored experience records."""
        records = list(self._records)
        if limit is None:
            return records
        return records[-limit:]

    def get_all_records(self) -> List[ExperienceRecord]:
        """Backward-compatible alias for full record access."""
        return self.get_records()

    def recall_by_task(self, task_type: str, limit: int = 20) -> List[ExperienceRecord]:
        """Recall experiences for a specific task type."""
        return [r for r in self._records if r.task_type == task_type][-limit:]

    def recall_successes(self, limit: int = 20) -> List[ExperienceRecord]:
        """Recall successful experiences."""
        return [r for r in self._records if r.outcome_success][-limit:]

    def recall_struggles(self, struggle_type: str, limit: int = 20) -> List[ExperienceRecord]:
        """Recall experiences involving a specific struggle."""
        return [
            r for r in self._records if struggle_type in r.struggles_experienced
        ][-limit:]

    def get_recurring_struggles(self, min_occurrences: int = 3) -> Dict[str, int]:
        """Identify struggles that keep happening."""
        counts: Dict[str, int] = {}
        for record in self._records:
            for struggle in record.struggles_experienced:
                counts[struggle] = counts.get(struggle, 0) + 1
        return {s: c for s, c in counts.items() if c >= min_occurrences}

    def get_effective_strategies(self) -> Dict[str, float]:
        """
        Find strategies that correlated with success.

        Returns strategy_name -> success_rate mapping.
        """
        strategy_outcomes: Dict[str, List[bool]] = {}
        for record in self._records:
            if record.strategy_discovered:
                if record.strategy_discovered not in strategy_outcomes:
                    strategy_outcomes[record.strategy_discovered] = []
                strategy_outcomes[record.strategy_discovered].append(
                    record.outcome_success
                )
        return {
            s: sum(outcomes) / len(outcomes)
            for s, outcomes in strategy_outcomes.items()
            if len(outcomes) >= 2
        }

    def get_independence_trajectory(self, task_type: Optional[str] = None) -> List[float]:
        """Track independence level over time for a task type."""
        records = self._records
        if task_type:
            records = deque(r for r in records if r.task_type == task_type)
        cumulative = 0.0
        trajectory: List[float] = []
        for r in records:
            cumulative += r.independence_delta
            trajectory.append(min(1.0, max(0.0, cumulative)))
        return trajectory

    @property
    def total_experiences(self) -> int:
        return len(self._records)

    @property
    def success_rate(self) -> float:
        if not self._records:
            return 0.0
        return sum(1 for r in self._records if r.outcome_success) / len(self._records)
