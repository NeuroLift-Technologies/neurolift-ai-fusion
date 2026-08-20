"""
Relationship System

Models social dynamics between Sims — friendship, romance, and familiarity.

The module provides three building blocks that integrate with the existing
ECS engine in :mod:`src.simulation.environment`:

* :class:`SocialInteractionType` — the catalog of social interactions.
* :class:`RelationshipComponent` — an ECS component stored on a dedicated
  "relationship entity" representing an ordered pair of Sims.
* :class:`RelationshipManager` — a service that owns relationships, resolves
  bidirectional lookups, applies interaction effects and decay, and emits
  relationship events through the engine's event bus.
* :class:`RelationshipSystem` — an ECS system that drives proximity-based
  social interactions and relationship decay during the simulation tick.

A Sim is any ECS entity that carries both a ``Position`` and an
``AgentController`` component (see :mod:`src.simulation.environment.agent_interface`).
The Sim id used by this system is the entity's ``entity_id``.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
import random

from .ecs import AgentController, Component, Entity, Position, Registry, System
from .time_manager import TimeManager
from .world_engine import EventType

# ---------------------------------------------------------------------------
# Public enums
# ---------------------------------------------------------------------------


class SocialInteractionType(Enum):
    """Kinds of social interactions that may occur between two Sims."""

    CHAT = "chat"
    FLIRT = "flirt"
    ARGUE = "argue"
    COMPLIMENT = "compliment"
    INSULT = "insult"
    JOKE = "joke"
    DEEP_CONVERSATION = "deep_conversation"


# ---------------------------------------------------------------------------
# Tunable constants
# ---------------------------------------------------------------------------

# Base score deltas applied per interaction type. ``quality`` (in [0, 1])
# scales these linearly — a quality of 1.0 is a perfectly executed interaction.
_INTERACTION_EFFECTS: Dict[SocialInteractionType, Dict[str, float]] = {
    SocialInteractionType.CHAT: {"friendship": 3.0, "romance": 0.0, "familiarity": 2.0},
    SocialInteractionType.COMPLIMENT: {
        "friendship": 8.0,
        "romance": 0.0,
        "familiarity": 2.0,
    },
    SocialInteractionType.JOKE: {"friendship": 4.0, "romance": 0.0, "familiarity": 3.0},
    SocialInteractionType.DEEP_CONVERSATION: {
        "friendship": 10.0,
        "romance": 0.0,
        "familiarity": 5.0,
    },
    SocialInteractionType.ARGUE: {
        "friendship": -7.0,
        "romance": -3.0,
        "familiarity": 2.0,
    },
    SocialInteractionType.INSULT: {
        "friendship": -12.0,
        "romance": -6.0,
        "familiarity": 1.0,
    },
    SocialInteractionType.FLIRT: {
        "friendship": 2.0,
        "romance": 8.0,
        "familiarity": 4.0,
    },
}

# Points lost per simulated hour when no interaction occurs.
_DECAY_RATE_PER_HOUR = 0.1

# Familiarity represents accumulated knowledge of the other Sim; it decays
# much more slowly than active social feelings.
_FAMILIARITY_DECAY_RATE_PER_HOUR = 0.02

# When two Sims share a grid cell, the probability that the system spontaneously
# triggers a social interaction during a tick.
_DEFAULT_INTERACTION_PROBABILITY = 0.15

# Quality range for system-triggered (random) interactions.
_RANDOM_QUALITY_MIN = 0.5
_RANDOM_QUALITY_MAX = 1.0

# Scores are clamped to [0, 100].
_SCORE_MIN = 0.0
_SCORE_MAX = 100.0


def _clamp_score(value: float, lo: float = _SCORE_MIN, hi: float = _SCORE_MAX) -> float:
    """Clamp a numeric score into the [lo, hi] range."""
    return max(lo, min(hi, value))


# ---------------------------------------------------------------------------
# ECS Component
# ---------------------------------------------------------------------------


class RelationshipComponent(Component):
    """
    ECS component storing the social relationship between an ordered pair of Sims.

    The pair ``(sim_a_id, sim_b_id)`` is normalized so that
    ``sim_a_id <= sim_b_id``.  This guarantees a single canonical relationship
    for any unordered pair and makes lookups bidirectional regardless of the
    argument order supplied by callers.

    Attributes:
        sim_a_id: First Sim id (always the lexicographically smaller id).
        sim_b_id: Second Sim id (always the lexicographically larger id).
        friendship: Friendship score in [0.0, 100.0].
        romance: Romance score in [0.0, 100.0].  Constrained to never exceed
            ``friendship`` (you cannot be more romantic than you are friendly).
        familiarity: Familiarity score in [0.0, 100.0].
        last_interaction: Timestamp of the most recent interaction.
        interaction_count: Number of interactions recorded for this pair.
    """

    def __init__(
        self,
        sim_a_id: str,
        sim_b_id: str,
        friendship: float = 0.0,
        romance: float = 0.0,
        familiarity: float = 0.0,
        last_interaction: Optional[Any] = None,
        interaction_count: int = 0,
    ) -> None:
        a_id, b_id = self._normalize_pair(sim_a_id, sim_b_id)
        self.sim_a_id: str = a_id
        self.sim_b_id: str = b_id
        self.friendship: float = _clamp_score(friendship)
        self.romance: float = _clamp_score(romance)
        self.familiarity: float = _clamp_score(familiarity)
        self.last_interaction: datetime = self._coerce_datetime(last_interaction)
        self.interaction_count: int = max(0, int(interaction_count))

    # -- helpers -----------------------------------------------------------
    @staticmethod
    def _normalize_pair(sim_a_id: str, sim_b_id: str) -> Tuple[str, str]:
        """Return the ordered (smaller, larger) pair for bidirectional lookup."""
        return (sim_a_id, sim_b_id) if sim_a_id <= sim_b_id else (sim_b_id, sim_a_id)

    @staticmethod
    def _coerce_datetime(value: Optional[Any]) -> datetime:
        """Coerce a datetime, an ISO-format string, or None into a datetime."""
        if value is None:
            return datetime.now()
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return datetime.now()

    def other_sim(self, sim_id: str) -> Optional[str]:
        """Return the partner's id for ``sim_id``, or ``None`` if not involved."""
        if sim_id == self.sim_a_id:
            return self.sim_b_id
        if sim_id == self.sim_b_id:
            return self.sim_a_id
        return None

    def is_involved(self, sim_id: str) -> bool:
        """Return whether this relationship involves the given Sim."""
        return sim_id == self.sim_a_id or sim_id == self.sim_b_id

    def pair_key(self) -> Tuple[str, str]:
        """Return the normalized canonical pair key."""
        return (self.sim_a_id, self.sim_b_id)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a JSON-safe dictionary (``last_interaction`` as ISO string)."""
        return {
            "sim_a_id": self.sim_a_id,
            "sim_b_id": self.sim_b_id,
            "friendship": self.friendship,
            "romance": self.romance,
            "familiarity": self.familiarity,
            "last_interaction": (
                self.last_interaction.isoformat() if self.last_interaction else None
            ),
            "interaction_count": self.interaction_count,
        }

    def __repr__(self) -> str:
        return (
            f"RelationshipComponent(sim_a={self.sim_a_id}, "
            f"sim_b={self.sim_b_id}, friendship={self.friendship:.1f}, "
            f"romance={self.romance:.1f}, familiarity={self.familiarity:.1f}, "
            f"interactions={self.interaction_count})"
        )


# ---------------------------------------------------------------------------
# Relationship Manager (service / singleton)
# ---------------------------------------------------------------------------


class RelationshipManager:
    """
    Service that owns all :class:`RelationshipComponent` instances and mediates
    social interactions between Sims.

    Relationships are backed by lightweight "relationship entities" in the ECS
    :class:`Registry`, so they participate in the engine's normal save/load
    cycle and ECS queries.  An in-memory index keyed by the normalized pair
    provides O(1) lookups; a registry scan is used as a fallback (notably
    after a world state is loaded).

    This class may be used as a per-engine service (instantiated directly with
    a registry) or as a process-wide singleton via :meth:`get_instance`.

    Interaction model
    -----------------
    * ``quality`` is a float in ``[0.0, 1.0]`` — the execution quality of the
      interaction.  It scales the base deltas linearly.
    * Each :class:`SocialInteractionType` carries a base
      ``(friendship, romance, familiarity)`` delta (positive or negative).
    * Romance can only grow from ``FLIRT`` interactions and is scaled by the
      current friendship fraction, so high friendship is required for romance
      to develop.  Romance is also clamped to never exceed friendship.
    * Friendship and romance decay at ``0.1`` points per simulated hour when
      the Sims are apart (see :meth:`apply_decay`).
    """

    _instance: Optional["RelationshipManager"] = None

    def __init__(
        self,
        registry: Optional[Registry] = None,
        on_event: Optional[Callable[[Any, Dict[str, Any]], None]] = None,
    ) -> None:
        self.registry: Optional[Registry] = registry
        self._on_event: Callable[[Any, Dict[str, Any]], None] = on_event or (
            lambda event_type, data: None
        )
        # pair key -> relationship entity
        self._index: Dict[Tuple[str, str], Entity] = {}

    # -- singleton plumbing ------------------------------------------------
    @classmethod
    def get_instance(
        cls,
        registry: Optional[Registry] = None,
        on_event: Optional[Callable[[Any, Dict[str, Any]], None]] = None,
    ) -> "RelationshipManager":
        """Return the process-wide singleton, creating or updating it as needed."""
        if cls._instance is None:
            if registry is None:
                raise ValueError(
                    "A registry is required to initialize RelationshipManager"
                )
            cls._instance = cls(registry=registry, on_event=on_event)
        else:
            if registry is not None:
                cls._instance.registry = registry
            if on_event is not None:
                cls._instance._on_event = on_event
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Drop the cached singleton (useful in tests)."""
        cls._instance = None

    # -- internal helpers --------------------------------------------------
    @staticmethod
    def _pair_key(sim_a_id: str, sim_b_id: str) -> Tuple[str, str]:
        return RelationshipComponent._normalize_pair(sim_a_id, sim_b_id)

    def _emit(self, event_type: Any, data: Dict[str, Any]) -> None:
        try:
            self._on_event(event_type, data)
        except Exception:
            pass

    @staticmethod
    def _component_data(comp: RelationshipComponent) -> Dict[str, Any]:
        return {
            "sim_a_id": comp.sim_a_id,
            "sim_b_id": comp.sim_b_id,
            "friendship": comp.friendship,
            "romance": comp.romance,
            "familiarity": comp.familiarity,
            "interaction_count": comp.interaction_count,
        }

    def _find_component_in_registry(
        self, sim_a_id: str, sim_b_id: str
    ) -> Optional[RelationshipComponent]:
        """Scan the registry for an existing relationship component for the pair."""
        if self.registry is None:
            return None
        for entity in self.registry.get_entities():
            comp = self.registry.get_component(entity, RelationshipComponent)
            if comp is None:
                continue
            if comp.is_involved(sim_a_id) and comp.is_involved(sim_b_id):
                self._index[comp.pair_key()] = entity
                return comp
        return None

    # -- public API --------------------------------------------------------
    def get_or_create(self, sim_a_id: str, sim_b_id: str) -> RelationshipComponent:
        """
        Return the relationship for the pair, creating it if necessary.

        Lookup is bidirectional: ``get_or_create(a, b)`` and
        ``get_or_create(b, a)`` return the same component.
        """
        key = self._pair_key(sim_a_id, sim_b_id)

        # Fast path: index hit.
        entity = self._index.get(key)
        if entity is not None:
            comp = (
                self.registry.get_component(entity, RelationshipComponent)
                if self.registry
                else None
            )
            if comp is not None:
                return comp

        # Fallback: scan the registry (handles relationships loaded from a save).
        comp = self._find_component_in_registry(key[0], key[1])
        if comp is not None:
            return comp

        # Create a new relationship entity + component.
        comp = RelationshipComponent(sim_a_id=key[0], sim_b_id=key[1])
        if self.registry is not None:
            entity = Entity()
            self.registry.add_entity(entity)
            self.registry.add_component(entity, comp)
            self._index[key] = entity
        self._emit(
            self._relationship_added_event_type(),
            {**self._component_data(comp), "pair": list(key)},
        )
        return comp

    def get_all_for_sim(self, sim_id: str) -> List[RelationshipComponent]:
        """Return every relationship that involves the given Sim."""
        results: List[RelationshipComponent] = []
        if self.registry is None:
            return results
        seen: set = set()
        for entity in self.registry.get_entities():
            comp = self.registry.get_component(entity, RelationshipComponent)
            if comp is None or not comp.is_involved(sim_id):
                continue
            if comp.pair_key() in seen:
                continue
            seen.add(comp.pair_key())
            results.append(comp)
        return results

    def interact(
        self,
        sim_a_id: str,
        sim_b_id: str,
        interaction_type: SocialInteractionType,
        quality: float = 1.0,
    ) -> RelationshipComponent:
        """
        Record an interaction between two Sims and update their relationship.

        Args:
            sim_a_id: First Sim id (order does not matter).
            sim_b_id: Second Sim id (order does not matter).
            interaction_type: The kind of social interaction.
            quality: Execution quality in ``[0.0, 1.0]`` (1.0 = perfect).

        Returns:
            The updated :class:`RelationshipComponent`.
        """
        comp = self.get_or_create(sim_a_id, sim_b_id)
        effects = _INTERACTION_EFFECTS.get(interaction_type)
        quality = _clamp_score(quality, 0.0, 1.0)

        prev_friendship = comp.friendship
        prev_romance = comp.romance
        prev_familiarity = comp.familiarity

        if effects is not None:
            friendship_delta = effects["friendship"] * quality
            familiarity_delta = effects["familiarity"] * quality
            romance_delta = effects["romance"] * quality

            # Romance only grows from FLIRT and is scaled by current friendship:
            # high friendship is required for romance to develop.
            if interaction_type == SocialInteractionType.FLIRT and romance_delta > 0:
                friendship_fraction = comp.friendship / _SCORE_MAX
                romance_delta *= friendship_fraction

            comp.friendship = _clamp_score(comp.friendship + friendship_delta)
            comp.familiarity = _clamp_score(comp.familiarity + familiarity_delta)
            comp.romance = _clamp_score(comp.romance + romance_delta)
            # Romance can never exceed friendship.
            comp.romance = min(comp.romance, comp.friendship)

        comp.last_interaction = datetime.now()
        comp.interaction_count += 1

        self._emit(
            self._social_interaction_event_type(),
            {
                "sim_a_id": comp.sim_a_id,
                "sim_b_id": comp.sim_b_id,
                "interaction_type": interaction_type.name,
                "quality": quality,
                "friendship_delta": comp.friendship - prev_friendship,
                "romance_delta": comp.romance - prev_romance,
                "familiarity_delta": comp.familiarity - prev_familiarity,
            },
        )
        self._emit(
            self._relationship_updated_event_type(),
            {**self._component_data(comp), "pair": list(comp.pair_key())},
        )
        return comp

    def apply_decay(self, elapsed_sim_hours: float) -> None:
        """
        Apply time-based decay to all relationships.

        Friendship and romance decay at ``0.1`` points per simulated hour;
        familiarity decays more slowly.  Decay only runs when time has
        advanced (``elapsed_sim_hours > 0``).
        """
        if elapsed_sim_hours <= 0 or self.registry is None:
            return

        friendship_decay = _DECAY_RATE_PER_HOUR * elapsed_sim_hours
        familiarity_decay = _FAMILIARITY_DECAY_RATE_PER_HOUR * elapsed_sim_hours

        for entity in self.registry.get_entities():
            comp = self.registry.get_component(entity, RelationshipComponent)
            if comp is None:
                continue
            prev_friendship, prev_romance, prev_familiarity = (
                comp.friendship,
                comp.romance,
                comp.familiarity,
            )
            comp.friendship = _clamp_score(comp.friendship - friendship_decay)
            comp.romance = min(
                _clamp_score(comp.romance - friendship_decay), comp.friendship
            )
            comp.familiarity = _clamp_score(comp.familiarity - familiarity_decay)

            if (
                comp.friendship != prev_friendship
                or comp.romance != prev_romance
                or comp.familiarity != prev_familiarity
            ):
                self._emit(
                    self._relationship_updated_event_type(),
                    {
                        **self._component_data(comp),
                        "pair": list(comp.pair_key()),
                        "decay": {
                            "friendship": comp.friendship - prev_friendship,
                            "romance": comp.romance - prev_romance,
                            "familiarity": comp.familiarity - prev_familiarity,
                        },
                    },
                )

    # -- event type accessors ------------------------------------------------
    def _relationship_added_event_type(self) -> EventType:
        return EventType.RELATIONSHIP_ADDED

    def _relationship_updated_event_type(self) -> EventType:
        return EventType.RELATIONSHIP_UPDATED

    def _social_interaction_event_type(self) -> EventType:
        return EventType.SOCIAL_INTERACTION


class RelationshipSystem(System):
    """
    ECS system that drives proximity-based social dynamics.

    Each tick it:

    1. **Decays** every relationship proportionally to the simulated time
       elapsed since the previous tick (friendship/romance at
       ``0.1`` per sim-hour, familiarity more slowly).
    2. **Spontaneously interacts** Sims that share a grid cell ("same room").
       With probability :attr:`interaction_probability` a random
       :class:`SocialInteractionType` is applied between each co-located pair.

    Sims are entities carrying both ``Position`` and ``AgentController``.
    """

    def __init__(
        self,
        relationship_manager: RelationshipManager,
        time_manager: TimeManager,
        interaction_probability: float = _DEFAULT_INTERACTION_PROBABILITY,
        seed: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.relationship_manager = relationship_manager
        self.time_manager = time_manager
        self.interaction_probability = interaction_probability
        self._rng = random.Random(seed)
        self._last_sim_minutes: int = time_manager.total_minutes_elapsed

    def update(self, delta_time: float) -> None:
        if self.registry is None or self.relationship_manager.registry is None:
            return

        # --- decay --------------------------------------------------------
        current_sim_minutes = self.time_manager.total_minutes_elapsed
        elapsed_minutes = current_sim_minutes - self._last_sim_minutes
        self._last_sim_minutes = current_sim_minutes
        if elapsed_minutes > 0:
            self.relationship_manager.apply_decay(elapsed_minutes / 60.0)

        # --- proximity socialising ---------------------------------------
        sim_entities = self.registry.get_entities_with(Position, AgentController)
        if len(sim_entities) < 2:
            return

        cell_to_sims: Dict[Tuple[int, int], List[Entity]] = {}
        for entity in sim_entities:
            pos = self.registry.get_component(entity, Position)
            if pos is None:
                continue
            cell_to_sims.setdefault((pos.x, pos.y), []).append(entity)

        for sims_in_cell in cell_to_sims.values():
            for i in range(len(sims_in_cell)):
                for j in range(i + 1, len(sims_in_cell)):
                    if self._rng.random() < self.interaction_probability:
                        interaction_type = self._rng.choice(list(SocialInteractionType))
                        quality = self._rng.uniform(
                            _RANDOM_QUALITY_MIN, _RANDOM_QUALITY_MAX
                        )
                        self.relationship_manager.interact(
                            sims_in_cell[i].entity_id,
                            sims_in_cell[j].entity_id,
                            interaction_type,
                            quality,
                        )
