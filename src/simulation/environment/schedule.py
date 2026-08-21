"""
Daily Schedule System

Autonomous daily routines for Sims.  A Sim carries a :class:`ScheduleComponent`
describing a 24-hour :class:`DailySchedule` of time-blocked activities
(sleep, meals, work, socialize, ...).  The :class:`ScheduleSystem` runs every
tick, reads the :class:`TimeManager`, resolves the Sim's current activity,
emits an ``ACTIVITY_CHANGED`` signal on transitions, queues move intents when
the Sim is away from the furniture/room required by the activity, and fulfils
the activity's associated need when the Sim is in the right place.  When no
entry covers the current hour the :class:`IdleBehavior` fallback picks a random
nearby interactable and uses it.

Supporting ECS components (co-located here so the system is self-contained):
:class:`FurnitureComponent`, :class:`RoomComponent` and :class:`NeedsComponent`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import random

from .ecs import (
    AgentController,
    Component,
    Entity,
    Interactable,
    Position,
    Registry,
    System,
)
from .time_manager import TimeManager
from .world_engine import EventType


class NeedType(str, Enum):
    """Needs that a Sim can have.  ``100`` = fully satisfied, ``0`` = desperate."""

    HUNGER = "hunger"
    ENERGY = "energy"
    BLADDER = "bladder"
    HYGIENE = "hygiene"
    FUN = "fun"
    SOCIAL = "social"
    COMFORT = "comfort"
    MOTIVATION = "motivation"


class FurnitureType(str, Enum):
    """Kinds of furniture Sims can interact with."""

    BED = "bed"
    FRIDGE = "fridge"
    STOVE = "stove"
    COUNTER = "counter"
    TOILET = "toilet"
    SHOWER = "shower"
    COUCH = "couch"
    COMPUTER = "computer"
    TABLE = "table"
    DOOR = "door"


_NEED_DEFAULT = 50.0
_NEED_MIN = 0.0
_NEED_MAX = 100.0


def _clamp(value: float, lo: float = _NEED_MIN, hi: float = _NEED_MAX) -> float:
    return max(lo, min(hi, value))


def _coerce_enum(value: Any, enum_cls: type) -> Any:
    """Coerce ``value`` into an enum member of ``enum_cls`` (idempotent)."""
    if value is None:
        return None
    if isinstance(value, enum_cls):
        return value
    return enum_cls(value)


def is_weekend(day: int) -> bool:
    """
    Return whether the given simulation day is a weekend.

    Days are 1-based with day 1 = Monday, so weekends fall on
    ``day % 7 in (0, 6)`` (Sunday = 0, Saturday = 6).
    """
    return (day % 7) in (0, 6)


# ---------------------------------------------------------------------------
# Supporting ECS components
# ---------------------------------------------------------------------------


class FurnitureComponent(Component):
    """Tags an entity as a piece of furniture of a specific :class:`FurnitureType`."""

    def __init__(self, furniture_type: Union[FurnitureType, str]) -> None:
        self.furniture_type: FurnitureType = _coerce_enum(furniture_type, FurnitureType)

    def to_dict(self) -> Dict[str, Any]:
        return {"furniture_type": self.furniture_type.value}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FurnitureComponent":
        return cls(furniture_type=data["furniture_type"])

    def __repr__(self) -> str:
        return f"FurnitureComponent(furniture_type={self.furniture_type.value!r})"


class RoomComponent(Component):
    """Tags an entity with the name of the room it belongs to."""

    def __init__(self, room_name: str) -> None:
        self.room_name: str = room_name

    def to_dict(self) -> Dict[str, Any]:
        return {"room_name": self.room_name}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RoomComponent":
        return cls(room_name=data["room_name"])

    def __repr__(self) -> str:
        return f"RoomComponent(room_name={self.room_name!r})"


class NeedsComponent(Component):
    """
    Tracks a Sim's need levels in the range ``[0, 100]`` (``100`` = satisfied).

    The :class:`ScheduleSystem` raises the relevant need when a scheduled
    activity is performed at the right location.  A companion system is free
    to tick decay; until then levels are stable.
    """

    _DEFAULTS: Dict[NeedType, float] = {
        NeedType.HUNGER: _NEED_DEFAULT,
        NeedType.ENERGY: _NEED_DEFAULT,
        NeedType.BLADDER: _NEED_DEFAULT,
        NeedType.HYGIENE: _NEED_DEFAULT,
        NeedType.FUN: _NEED_DEFAULT,
        NeedType.SOCIAL: _NEED_DEFAULT,
        NeedType.COMFORT: _NEED_DEFAULT,
        NeedType.MOTIVATION: _NEED_DEFAULT,
    }

    def __init__(self, needs: Optional[Dict[Union[NeedType, str], float]] = None) -> None:
        merged: Dict[NeedType, float] = dict(self._DEFAULTS)
        if needs:
            for key, value in needs.items():
                merged[_coerce_enum(key, NeedType)] = float(value)
        self.needs: Dict[NeedType, float] = merged

    def fulfill(self, need_type: Union[NeedType, str], amount: float = 10.0) -> float:
        """Raise a need by ``amount`` (clamped to ``[_NEED_MIN, _NEED_MAX]``)."""
        key = _coerce_enum(need_type, NeedType)
        current = self.needs.get(key, _NEED_DEFAULT)
        new_level = _clamp(current + amount)
        self.needs[key] = new_level
        return new_level

    def get(self, need_type: Union[NeedType, str]) -> float:
        return self.needs.get(_coerce_enum(need_type, NeedType), _NEED_DEFAULT)

    def to_dict(self) -> Dict[str, Any]:
        return {"needs": {k.value: v for k, v in self.needs.items()}}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NeedsComponent":
        raw = data.get("needs", {})
        needs: Dict[NeedType, float] = {}
        for key, value in raw.items():
            needs[_coerce_enum(key, NeedType)] = float(value)
        return cls(needs=needs)

    def __repr__(self) -> str:
        return f"NeedsComponent(needs={self.needs})"


# ---------------------------------------------------------------------------
# Schedule data model
# ---------------------------------------------------------------------------


@dataclass
class ScheduleEntry:
    """A single time-blocked activity in a Sim's 24-hour schedule."""

    activity: str
    start_hour: int = 0
    end_hour: int = 23
    required_furniture: Optional[Union[FurnitureType, str]] = None
    required_room: Optional[str] = None
    need_fulfilled: Optional[Union[NeedType, str]] = None

    def __post_init__(self) -> None:
        self.required_furniture = _coerce_enum(self.required_furniture, FurnitureType)
        self.need_fulfilled = _coerce_enum(self.need_fulfilled, NeedType)
        if not (0 <= self.start_hour <= 23):
            raise ValueError(f"start_hour must be in 0-23, got {self.start_hour}")
        if not (0 <= self.end_hour <= 23):
            raise ValueError(f"end_hour must be in 0-23, got {self.end_hour}")

    def covers(self, hour: int) -> bool:
        """Return whether this entry is active at the given hour (0-23)."""
        if self.start_hour == self.end_hour:
            return True
        if self.end_hour > self.start_hour:
            return self.start_hour <= hour < self.end_hour
        # Entry spans midnight (e.g. sleep 23 -> 7).
        return hour >= self.start_hour or hour < self.end_hour

    def has_location_requirement(self) -> bool:
        return self.required_furniture is not None or self.required_room is not None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "activity": self.activity,
            "start_hour": self.start_hour,
            "end_hour": self.end_hour,
            "required_furniture": self.required_furniture.value if self.required_furniture else None,
            "required_room": self.required_room,
            "need_fulfilled": self.need_fulfilled.value if self.need_fulfilled else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScheduleEntry":
        return cls(
            activity=data["activity"],
            start_hour=data.get("start_hour", 0),
            end_hour=data.get("end_hour", 23),
            required_furniture=data.get("required_furniture"),
            required_room=data.get("required_room"),
            need_fulfilled=data.get("need_fulfilled"),
        )

    def __repr__(self) -> str:
        return (
            f"ScheduleEntry(activity={self.activity!r}, "
            f"{self.start_hour}-{self.end_hour}, "
            f"furniture={self.required_furniture}, room={self.required_room})"
        )


class DailySchedule:
    """
    An ordered list of :class:`ScheduleEntry` objects covering a 24-hour day.

    Iteration order defines priority: the *first* entry that :meth:`covers`
    a given hour wins, so more specific activities (meals) should be listed
    before broader ones (work).
    """

    def __init__(self, entries: Optional[List[ScheduleEntry]] = None) -> None:
        self.entries: List[ScheduleEntry] = list(entries) if entries else []

    def add_entry(self, entry: ScheduleEntry) -> "DailySchedule":
        self.entries.append(entry)
        return self

    def get_entry_for_hour(self, hour: int) -> Optional[ScheduleEntry]:
        """Return the first entry covering ``hour``, or ``None``."""
        for entry in self.entries:
            if entry.covers(hour):
                return entry
        return None

    @classmethod
    def from_entries(cls, *entries: ScheduleEntry) -> "DailySchedule":
        return cls(list(entries))

    def to_dict(self) -> Dict[str, Any]:
        return {"entries": [e.to_dict() for e in self.entries]}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DailySchedule":
        if not data:
            return cls()
        raw = data.get("entries", [])
        return cls([ScheduleEntry.from_dict(e) for e in raw])

    def __repr__(self) -> str:
        return f"DailySchedule(entries={len(self.entries)})"


# ---------------------------------------------------------------------------
# Default factory schedules
# ---------------------------------------------------------------------------


def get_workday_schedule() -> DailySchedule:
    """Default weekday (Mon-Fri) schedule."""
    return DailySchedule([
        ScheduleEntry("sleep", 23, 7, FurnitureType.BED, "bedroom", NeedType.ENERGY),
        ScheduleEntry("eat_breakfast", 7, 8, FurnitureType.FRIDGE, "kitchen", NeedType.HUNGER),
        ScheduleEntry("work", 8, 12, FurnitureType.COMPUTER, "office"),
        ScheduleEntry("eat_lunch", 12, 13, FurnitureType.TABLE, "dining", NeedType.HUNGER),
        ScheduleEntry("work", 13, 17, FurnitureType.COMPUTER, "office"),
        ScheduleEntry("relax", 17, 19, FurnitureType.COUCH, "living_room", NeedType.FUN),
        ScheduleEntry("eat_dinner", 19, 20, FurnitureType.TABLE, "dining", NeedType.HUNGER),
        ScheduleEntry("socialize", 20, 23, FurnitureType.COUCH, "living_room", NeedType.SOCIAL),
    ])


def get_weekend_schedule() -> DailySchedule:
    """Default weekend (Sat/Sun) schedule."""
    return DailySchedule([
        ScheduleEntry("sleep", 23, 8, FurnitureType.BED, "bedroom", NeedType.ENERGY),
        ScheduleEntry("eat_breakfast", 8, 9, FurnitureType.FRIDGE, "kitchen", NeedType.HUNGER),
        ScheduleEntry("relax", 9, 12, FurnitureType.COUCH, "living_room", NeedType.FUN),
        ScheduleEntry("eat_lunch", 12, 13, FurnitureType.TABLE, "dining", NeedType.HUNGER),
        ScheduleEntry("exercise", 13, 14, None, None, NeedType.COMFORT),
        ScheduleEntry("relax", 14, 17, FurnitureType.COUCH, "living_room", NeedType.COMFORT),
        ScheduleEntry("eat_dinner", 17, 18, FurnitureType.TABLE, "dining", NeedType.HUNGER),
        ScheduleEntry("socialize", 18, 23, FurnitureType.COUCH, "living_room", NeedType.SOCIAL),
    ])


# ---------------------------------------------------------------------------
# Schedule component
# ---------------------------------------------------------------------------


class ScheduleComponent(Component):
    """
    ECS component attaching a daily schedule to a Sim.

    Holds both a weekday and a weekend :class:`DailySchedule`; the active
    schedule is selected by :meth:`schedule`, which honours the ``weekend``
    flag.  The :class:`ScheduleSystem` keeps ``weekend`` in sync with the
    simulated day.
    """

    def __init__(
        self,
        schedule: Optional[DailySchedule] = None,
        workday_schedule: Optional[Union[DailySchedule, Dict[str, Any]]] = None,
        weekend_schedule: Optional[Union[DailySchedule, Dict[str, Any]]] = None,
        current_activity: Optional[str] = None,
        weekend: bool = False,
    ) -> None:
        if schedule is not None:
            workday_schedule = schedule
        self.workday_schedule: DailySchedule = self._coerce_schedule(workday_schedule)
        if self.workday_schedule.entries == []:
            self.workday_schedule = get_workday_schedule()
        self.weekend_schedule: DailySchedule = self._coerce_schedule(weekend_schedule)
        if self.weekend_schedule.entries == []:
            self.weekend_schedule = get_weekend_schedule()
        self.current_activity: Optional[str] = current_activity
        self.weekend: bool = weekend

    @staticmethod
    def _coerce_schedule(
        value: Optional[Union[DailySchedule, Dict[str, Any]]]
    ) -> DailySchedule:
        if value is None:
            return DailySchedule()
        if isinstance(value, DailySchedule):
            return value
        return DailySchedule.from_dict(value or {})

    @property
    def schedule(self) -> DailySchedule:
        """The schedule currently in effect, based on the ``weekend`` flag."""
        return self.weekend_schedule if self.weekend else self.workday_schedule

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workday_schedule": self.workday_schedule.to_dict(),
            "weekend_schedule": self.weekend_schedule.to_dict(),
            "current_activity": self.current_activity,
            "weekend": self.weekend,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScheduleComponent":
        return cls(
            workday_schedule=data.get("workday_schedule"),
            weekend_schedule=data.get("weekend_schedule"),
            current_activity=data.get("current_activity"),
            weekend=data.get("weekend", False),
        )

    def __repr__(self) -> str:
        return (
            f"ScheduleComponent(weekend={self.weekend}, "
            f"current_activity={self.current_activity})"
        )


# ---------------------------------------------------------------------------
# Idle behavior fallback
# ---------------------------------------------------------------------------


class IdleBehavior:
    """
    Fallback behavior used when a Sim's schedule has no entry for the current
    hour.  The Sim picks a random nearby interactable and queues a ``use``
    intent for it.
    """

    def __init__(
        self,
        registry: Registry,
        vision_radius: int = 5,
        seed: Optional[int] = None,
    ) -> None:
        self.registry = registry
        self.vision_radius = vision_radius
        self._rng = random.Random(seed)

    def _nearby_interactables(
        self, sim_position: Position, sim_id: str
    ) -> List[Entity]:
        candidates = self.registry.get_entities_with(Position, Interactable)
        results: List[Entity] = []
        for ent in candidates:
            if ent.entity_id == sim_id:
                continue
            pos = self.registry.get_component(ent, Position)
            if pos is None:
                continue
            dist = abs(pos.x - sim_position.x) + abs(pos.y - sim_position.y)
            if dist <= self.vision_radius:
                results.append(ent)
        return results

    def choose_target(self, sim: Entity) -> Optional[Entity]:
        """Return a random nearby interactable (excluding the Sim itself)."""
        pos = self.registry.get_component(sim, Position)
        if pos is None:
            return None
        interactables = self._nearby_interactables(pos, sim.entity_id)
        if not interactables:
            return None
        return self._rng.choice(interactables)

    def act(
        self,
        sim: Entity,
        idle_probability: float = 1.0,
    ) -> Optional[Dict[str, Any]]:
        """
        Queue a ``use`` intent on the Sim for a random nearby interactable.

        Returns a description dict (suitable for emitting as an event) or
        ``None`` when no target is available or the behavior did not trigger.
        """
        controller = self.registry.get_component(sim, AgentController)
        if controller is None:
            return None
        if controller.current_intent is not None:
            return None
        if idle_probability < 1.0 and self._rng.random() >= idle_probability:
            return None

        target = self.choose_target(sim)
        if target is None:
            return None
        target_pos = self.registry.get_component(target, Position)
        if target_pos is None:
            return None

        controller.current_intent = {
            "type": "use",
            "target_id": target.entity_id,
            "data": {"x": target_pos.x, "y": target_pos.y},
        }
        controller.intent_progress = 0.0

        return {
            "sim_id": sim.entity_id,
            "action": "idle_use",
            "target_id": target.entity_id,
            "target_position": {"x": target_pos.x, "y": target_pos.y},
        }


# ---------------------------------------------------------------------------
# Schedule system
# ---------------------------------------------------------------------------


class ScheduleSystem(System):
    """
    ECS system that drives autonomous daily routines for Sims.

    Each tick, for every Sim carrying a :class:`ScheduleComponent` (together
    with :class:`Position` and :class:`AgentController`):

    1. The active schedule is resolved from the Sim's weekday/weekend data,
       with the ``weekend`` flag kept in sync via :func:`is_weekend`.
    2. The current :class:`ScheduleEntry` for the TimeManager's hour is found.
    3. If the resolved activity changed since the last tick, an
       :attr:`EventType.SCHEDULE_ACTIVITY_CHANGED` signal is emitted.
    4. If the activity requires a piece of furniture / room and the Sim is
       not there, a ``move`` intent is queued on the Sim's
       :class:`AgentController`.
    5. If the Sim *is* at the required place, the activity's
       :attr:`NeedType` is fulfilled (via :class:`NeedsComponent` when
       present) and a :attr:`EventType.NEED_FULFILLED` signal is emitted.
    6. When no entry covers the current hour, :class:`IdleBehavior` kicks in.
    """

    def __init__(
        self,
        time_manager: TimeManager,
        on_event: Optional[Callable[[Any, Dict[str, Any]], None]] = None,
        idle_probability: float = 1.0,
        idle_vision_radius: int = 5,
        need_fulfillment_amount: float = 10.0,
        seed: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.time_manager = time_manager
        self._on_event: Callable[[Any, Dict[str, Any]], None] = on_event or (
            lambda event_type, data: None
        )
        self.idle_probability = idle_probability
        self.idle_vision_radius = idle_vision_radius
        self.need_fulfillment_amount = need_fulfillment_amount
        self._rng = random.Random(seed)
        self._idle_behavior: Optional[IdleBehavior] = None
        # sim_id -> last resolved activity (None means "idle").
        self._sim_activities: Dict[str, Optional[str]] = {}

    # -- event emission ------------------------------------------------------
    def _emit(self, event_type: Any, data: Dict[str, Any]) -> None:
        try:
            self._on_event(event_type, data)
        except Exception:
            pass

    @property
    def idle_behavior(self) -> IdleBehavior:
        """Lazily construct the idle behavior once a registry is available."""
        if self._idle_behavior is None:
            if self.registry is None:
                raise RuntimeError("ScheduleSystem registry is not set")
            self._idle_behavior = IdleBehavior(
                registry=self.registry,
                vision_radius=self.idle_vision_radius,
                seed=self._rng.randint(0, 2**31 - 1) if self._rng is not None else None,
            )
        return self._idle_behavior

    # -- entity queries ------------------------------------------------------
    def _find_furniture_entities(
        self,
        furniture_type: Optional[FurnitureType],
        room_name: Optional[str],
    ) -> List[Entity]:
        """Entities matching the requested furniture (optionally in a room)."""
        candidates = self.registry.get_entities_with(FurnitureComponent)
        results: List[Entity] = []
        for ent in candidates:
            furniture = self.registry.get_component(ent, FurnitureComponent)
            if furniture is None:
                continue
            if furniture_type is not None and furniture.furniture_type != furniture_type:
                continue
            if room_name is not None:
                room = self.registry.get_component(ent, RoomComponent)
                if room is None or room.room_name != room_name:
                    continue
            results.append(ent)
        return results

    def _target_entities(self, entry: ScheduleEntry) -> List[Entity]:
        """Furniture entities the Sim must reach for this entry."""
        if not entry.has_location_requirement():
            return []
        return self._find_furniture_entities(entry.required_furniture, entry.required_room)

    def _nearest_target(
        self, position: Position, target_entities: List[Entity]
    ) -> Optional[Tuple[Entity, Position]]:
        """Closest target furniture entity by Manhattan distance."""
        best_entity: Optional[Entity] = None
        best_pos: Optional[Position] = None
        best_dist: Optional[int] = None
        for ent in target_entities:
            pos = self.registry.get_component(ent, Position)
            if pos is None:
                continue
            dist = abs(pos.x - position.x) + abs(pos.y - position.y)
            if best_dist is None or dist < best_dist:
                best_dist = dist
                best_pos = pos
                best_entity = ent
        if best_pos is None:
            return None
        return best_entity, best_pos

    # -- per-sim processing --------------------------------------------------
    def update(self, delta_time: float) -> None:
        if self.registry is None:
            return

        current_hour = self.time_manager.hour
        sims = self.registry.get_entities_with(
            Position, AgentController, ScheduleComponent
        )
        for sim in sims:
            self._process_sim(sim, current_hour)

    def _process_sim(self, sim: Entity, current_hour: int) -> None:
        controller = self.registry.get_component(sim, AgentController)
        schedule_comp = self.registry.get_component(sim, ScheduleComponent)
        position = self.registry.get_component(sim, Position)
        if controller is None or schedule_comp is None or position is None:
            return

        sim_id = sim.entity_id

        # Keep the weekend flag in sync with the simulated day, without
        # clobbering manual overrides set within the same tick batch.
        if schedule_comp.weekend != is_weekend(self.time_manager.day):
            schedule_comp.weekend = is_weekend(self.time_manager.day)

        entry = schedule_comp.schedule.get_entry_for_hour(current_hour)
        effective_activity = entry.activity if entry is not None else "idle"
        schedule_comp.current_activity = effective_activity

        prev_activity = self._sim_activities.get(sim_id)
        if effective_activity != prev_activity:
            self._emit(
                EventType.SCHEDULE_ACTIVITY_CHANGED,
                {
                    "sim_id": sim_id,
                    "old_activity": prev_activity,
                    "new_activity": effective_activity,
                    "hour": current_hour,
                    "weekend": schedule_comp.weekend,
                },
            )
            self._sim_activities[sim_id] = effective_activity

        if entry is not None:
            self._handle_scheduled_activity(sim, controller, position, entry)
        else:
            self._handle_idle(sim, controller, position)

    def _handle_scheduled_activity(
        self,
        sim: Entity,
        controller: AgentController,
        position: Position,
        entry: ScheduleEntry,
    ) -> None:
        if not entry.has_location_requirement():
            # Activity has no location requirement — fulfil the need in place.
            self._fulfill_need(sim, entry)
            return

        target_entities = self._target_entities(entry)
        if not target_entities:
            # Required furniture/room is not present in the world yet.
            return

        nearest = self._nearest_target(position, target_entities)
        if nearest is None:
            return
        target_entity, nearest_pos = nearest

        at_destination = (
            position.x == nearest_pos.x and position.y == nearest_pos.y
        )
        if at_destination:
            self._fulfill_need(sim, entry, target_entity=target_entity)
            controller.current_intent = None
            controller.intent_progress = 0.0
        else:
            # Not at the required furniture/room — queue a move if idle.
            if controller.current_intent is None:
                controller.current_intent = {
                    "type": "move",
                    "target_id": target_entity.entity_id,
                    "data": {"x": nearest_pos.x, "y": nearest_pos.y},
                }
                controller.intent_progress = 0.0
                self._emit(
                    EventType.SCHEDULE_MOVE_QUEUED,
                    {
                        "sim_id": sim.entity_id,
                        "activity": entry.activity,
                        "from": {"x": position.x, "y": position.y},
                        "to": {"x": nearest_pos.x, "y": nearest_pos.y},
                        "target_entity_id": target_entity.entity_id,
                    },
                )

    def _handle_idle(
        self,
        sim: Entity,
        controller: AgentController,
        position: Position,
    ) -> None:
        result = self.idle_behavior.act(sim, idle_probability=self.idle_probability)
        if result is not None:
            self._emit(EventType.IDLE_BEHAVIOR_TRIGGERED, result)

    def _fulfill_need(
        self,
        sim: Entity,
        entry: ScheduleEntry,
        target_entity: Optional[Entity] = None,
    ) -> None:
        if entry.need_fulfilled is None:
            return
        new_level: Optional[float] = None
        needs = self.registry.get_component(sim, NeedsComponent)
        if needs is not None:
            new_level = needs.fulfill(entry.need_fulfilled, self.need_fulfillment_amount)
        self._emit(
            EventType.NEED_FULFILLED,
            {
                "sim_id": sim.entity_id,
                "need_type": entry.need_fulfilled.value,
                "activity": entry.activity,
                "new_level": new_level,
                "target_entity_id": target_entity.entity_id if target_entity else None,
            },
        )
