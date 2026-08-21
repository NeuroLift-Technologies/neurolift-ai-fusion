"""Tests for the Daily Schedule system (autonomous Sims routines)."""

import pytest

from src.simulation.environment.ecs import (
    AgentController,
    Entity,
    Interactable,
    Position,
    Registry,
)
from src.simulation.environment.schedule import (
    DailySchedule,
    FurnitureComponent,
    FurnitureType,
    IdleBehavior,
    NeedType,
    NeedsComponent,
    RoomComponent,
    ScheduleComponent,
    ScheduleEntry,
    ScheduleSystem,
    get_weekend_schedule,
    get_workday_schedule,
    is_weekend,
)
from src.simulation.environment.time_manager import TimeManager
from src.simulation.environment.world_engine import EventType, WorldEngine


# ---------------------------------------------------------------------------
# Enums & helpers
# ---------------------------------------------------------------------------


class TestNeedType:
    def test_all_expected_members(self):
        names = {member.name for member in NeedType}
        for expected in ("HUNGER", "ENERGY", "FUN", "SOCIAL", "COMFORT"):
            assert expected in names

    def test_is_string_enum(self):
        assert NeedType.HUNGER.value == "hunger"


class TestFurnitureType:
    def test_expected_members(self):
        assert FurnitureType.BED.value == "bed"
        assert FurnitureType.COMPUTER.value == "computer"

    def test_str_enum_round_trip(self):
        assert FurnitureType(FurnitureType.BED.value) is FurnitureType.BED


class TestIsWeekend:
    @pytest.mark.parametrize(
        "day,expected",
        [
            (1, False),  # Monday
            (5, False),  # Friday
            (6, True),   # Saturday
            (7, True),   # Sunday
            (8, False),  # next Monday
            (13, True),  # next Saturday
        ],
    )
    def test_weekend_detection(self, day, expected):
        assert is_weekend(day) is expected


# ---------------------------------------------------------------------------
# ScheduleEntry
# ---------------------------------------------------------------------------


class TestScheduleEntry:
    def test_covers_normal_range(self):
        entry = ScheduleEntry("work", 8, 12)
        assert entry.covers(8)
        assert entry.covers(11)
        assert not entry.covers(12)
        assert not entry.covers(7)

    def test_covers_wraps_midnight(self):
        entry = ScheduleEntry("sleep", 23, 7)
        assert entry.covers(23)
        assert entry.covers(0)
        assert entry.covers(6)
        assert not entry.covers(7)
        assert not entry.covers(12)

    def test_covers_full_day_when_equal(self):
        entry = ScheduleEntry("idle", 0, 0)
        assert entry.covers(0)
        assert entry.covers(23)

    def test_invalid_hours_raise(self):
        with pytest.raises(ValueError):
            ScheduleEntry("bad", -1, 10)
        with pytest.raises(ValueError):
            ScheduleEntry("bad", 10, 25)

    def test_has_location_requirement(self):
        assert ScheduleEntry("x", 1, 2, FurnitureType.BED, "bedroom").has_location_requirement()
        assert ScheduleEntry("x", 1, 2, required_room="living_room").has_location_requirement()
        assert not ScheduleEntry("x", 1, 2).has_location_requirement()

    def test_to_dict_from_dict_round_trip(self):
        entry = ScheduleEntry(
            "work", 8, 17, FurnitureType.COMPUTER, "office", NeedType.MOTIVATION
        )
        restored = ScheduleEntry.from_dict(entry.to_dict())
        assert restored.activity == "work"
        assert restored.start_hour == 8
        assert restored.end_hour == 17
        assert restored.required_furniture is FurnitureType.COMPUTER
        assert restored.required_room == "office"
        assert restored.need_fulfilled is NeedType.MOTIVATION


# ---------------------------------------------------------------------------
# DailySchedule
# ---------------------------------------------------------------------------


class TestDailySchedule:
    def test_get_entry_for_hour_returns_first_match(self):
        sched = DailySchedule([
            ScheduleEntry("work", 8, 12),
            ScheduleEntry("eat_lunch", 12, 13),
        ])
        assert sched.get_entry_for_hour(9).activity == "work"
        assert sched.get_entry_for_hour(12).activity == "eat_lunch"
        assert sched.get_entry_for_hour(7) is None

    def test_add_entry(self):
        sched = DailySchedule()
        assert sched.add_entry(ScheduleEntry("sleep", 22, 6)) is sched
        assert len(sched.entries) == 1

    def test_from_entries(self):
        sched = DailySchedule.from_entries(
            ScheduleEntry("a", 0, 1), ScheduleEntry("b", 1, 2)
        )
        assert len(sched.entries) == 2

    def test_to_dict_from_dict_round_trip(self):
        sched = get_workday_schedule()
        restored = DailySchedule.from_dict(sched.to_dict())
        assert len(restored.entries) == len(sched.entries)
        assert restored.get_entry_for_hour(23).activity == "sleep"
        assert restored.get_entry_for_hour(12).activity == "eat_lunch"


# ---------------------------------------------------------------------------
# Default factory schedules
# ---------------------------------------------------------------------------


class TestDefaultSchedules:
    def test_workday_schedule(self):
        sched = get_workday_schedule()
        assert sched.get_entry_for_hour(23).activity == "sleep"
        assert sched.get_entry_for_hour(7).activity == "eat_breakfast"
        assert sched.get_entry_for_hour(9).activity == "work"
        assert sched.get_entry_for_hour(12).activity == "eat_lunch"
        assert sched.get_entry_for_hour(18).activity == "relax"
        assert sched.get_entry_for_hour(22).activity == "socialize"

    def test_weekend_schedule(self):
        sched = get_weekend_schedule()
        assert sched.get_entry_for_hour(23).activity == "sleep"
        assert sched.get_entry_for_hour(10).activity == "relax"
        assert sched.get_entry_for_hour(13).activity == "exercise"


# ---------------------------------------------------------------------------
# Supporting components
# ---------------------------------------------------------------------------


class TestSupportComponents:
    def test_furniture_component_coerces_value(self):
        comp = FurnitureComponent("bed")
        assert comp.furniture_type is FurnitureType.BED
        # Round-trip through to_dict / from_dict
        restored = FurnitureComponent.from_dict(comp.to_dict())
        assert restored.furniture_type is FurnitureType.BED

    def test_room_component_round_trip(self):
        comp = RoomComponent("kitchen")
        restored = RoomComponent.from_dict(comp.to_dict())
        assert restored.room_name == "kitchen"

    def test_needs_component_defaults(self):
        needs = NeedsComponent()
        assert needs.get(NeedType.HUNGER) == 50.0
        assert needs.get(NeedType.ENERGY) == 50.0

    def test_needs_fulfill_clamped(self):
        needs = NeedsComponent({NeedType.ENERGY: 95.0})
        assert needs.fulfill(NeedType.ENERGY, 10.0) == 100.0
        needs2 = NeedsComponent()
        assert needs2.fulfill(NeedType.HUNGER, 10.0) == 60.0

    def test_needs_fulfill_string_key(self):
        needs = NeedsComponent()
        assert needs.fulfill("fun", 10.0) == 60.0

    def test_needs_to_dict_from_dict_round_trip(self):
        needs = NeedsComponent({NeedType.HUNGER: 25.0, NeedType.SOCIAL: 75.0})
        restored = NeedsComponent.from_dict(needs.to_dict())
        assert restored.get(NeedType.HUNGER) == 25.0
        assert restored.get(NeedType.SOCIAL) == 75.0
        assert restored.get(NeedType.ENERGY) == 50.0  # default preserved


# ---------------------------------------------------------------------------
# ScheduleComponent
# ---------------------------------------------------------------------------


class TestScheduleComponent:
    def test_defaults_to_factory_schedules(self):
        comp = ScheduleComponent()
        assert len(comp.workday_schedule.entries) == len(get_workday_schedule().entries)
        assert len(comp.weekend_schedule.entries) == len(get_weekend_schedule().entries)
        assert comp.current_activity is None
        assert comp.weekend is False

    def test_schedule_property_switches_on_weekend(self):
        comp = ScheduleComponent()
        assert comp.schedule is comp.workday_schedule
        comp.weekend = True
        assert comp.schedule is comp.weekend_schedule

    def test_to_dict_from_dict_round_trip(self):
        comp = ScheduleComponent()
        comp.current_activity = "work"
        comp.weekend = True
        restored = ScheduleComponent.from_dict(comp.to_dict())
        assert restored.current_activity == "work"
        assert restored.weekend is True
        assert len(restored.workday_schedule.entries) == len(comp.workday_schedule.entries)
        assert len(restored.weekend_schedule.entries) == len(comp.weekend_schedule.entries)

    def test_accepts_schedule_argument(self):
        sched = DailySchedule([ScheduleEntry("x", 1, 2)])
        comp = ScheduleComponent(schedule=sched)
        assert len(comp.workday_schedule.entries) == 1


# ---------------------------------------------------------------------------
# IdleBehavior
# ---------------------------------------------------------------------------


class TestIdleBehavior:
    def _make_world(self):
        registry = Registry()
        sim = Entity(entity_id="sim1")
        registry.add_entity(sim)
        registry.add_component(sim, Position(5, 5, 0))
        registry.add_component(sim, AgentController("sim1"))

        couch = Entity(entity_id="couch1")
        registry.add_entity(couch)
        registry.add_component(couch, Position(6, 5, 0))
        registry.add_component(couch, FurnitureComponent(FurnitureType.COUCH))
        registry.add_component(couch, Interactable(["sit"]))

        far = Entity(entity_id="far1")
        registry.add_entity(far)
        registry.add_component(far, Position(20, 20, 0))
        registry.add_component(far, FurnitureComponent(FurnitureType.TABLE))
        registry.add_component(far, Interactable(["use"]))
        return registry, sim, couch, far

    def test_choose_target_picks_nearby(self):
        registry, sim, couch, far = self._make_world()
        behavior = IdleBehavior(registry, vision_radius=5, seed=1)
        target = behavior.choose_target(sim)
        assert target is not None
        assert target.entity_id == couch.entity_id

    def test_choose_target_returns_none_when_empty(self):
        registry, sim, couch, far = self._make_world()
        behavior = IdleBehavior(registry, vision_radius=1, seed=1)
        # couch is at distance 1 (Chebyshev) -> actually within radius 1
        # move sim far away instead
        registry.get_component(sim, Position).x = 0
        registry.get_component(sim, Position).y = 0
        assert behavior.choose_target(sim) is None

    def test_act_queues_use_intent(self):
        registry, sim, couch, far = self._make_world()
        behavior = IdleBehavior(registry, vision_radius=5, seed=1)
        result = behavior.act(sim)
        assert result is not None
        assert result["action"] == "idle_use"
        controller = registry.get_component(sim, AgentController)
        assert controller.current_intent["type"] == "use"
        assert controller.current_intent["target_id"] == couch.entity_id

    def test_act_does_not_override_existing_intent(self):
        registry, sim, couch, far = self._make_world()
        controller = registry.get_component(sim, AgentController)
        controller.current_intent = {"type": "move", "target_id": None, "data": {"x": 0}}
        behavior = IdleBehavior(registry, vision_radius=5, seed=1)
        result = behavior.act(sim)
        assert result is None
        assert controller.current_intent["type"] == "move"

    def test_act_respects_idle_probability(self):
        registry, sim, couch, far = self._make_world()
        behavior = IdleBehavior(registry, vision_radius=5, seed=2)
        result = behavior.act(sim, idle_probability=0.0)
        assert result is None
        assert registry.get_component(sim, AgentController).current_intent is None


# ---------------------------------------------------------------------------
# ScheduleSystem
# ---------------------------------------------------------------------------


def _make_registry_with_sim(
    registry: Registry,
    sim_id: str = "sim1",
    x: int = 5,
    y: int = 5,
    schedule: ScheduleComponent = None,
    needs: bool = False,
) -> Entity:
    sim = Entity(entity_id=sim_id)
    registry.add_entity(sim)
    registry.add_component(sim, Position(x, y, 0))
    registry.add_component(sim, AgentController(sim_id))
    registry.add_component(sim, schedule or ScheduleComponent())
    if needs:
        registry.add_component(sim, NeedsComponent())
    return sim


class TestScheduleSystem:
    def test_no_sims_is_safe(self):
        registry = Registry()
        system = ScheduleSystem(TimeManager(), on_event=lambda *a: None)
        system.set_registry(registry)
        system.update(1.0)  # must not raise

    def test_activity_change_emits_signal(self):
        registry = Registry()
        _make_registry_with_sim(registry, x=5, y=5)
        tm = TimeManager(start_day=1, start_hour=6)
        events = []
        system = ScheduleSystem(tm, on_event=lambda et, d: events.append((et, d)))
        system.set_registry(registry)

        # At hour 6 nothing covers it in workday schedule (sleep ends at 7,
        # breakfast starts at 7) -> idle. Let's use hour 23 (sleep) first.
        tm.set_time(23, 0)
        system.update(1.0)
        assert events
        assert all(et == EventType.SCHEDULE_ACTIVITY_CHANGED for et, _ in events)
        assert events[-1][1]["new_activity"] == "sleep"

    def test_follows_workday_schedule(self):
        registry = Registry()
        sim = _make_registry_with_sim(registry)
        tm = TimeManager(start_day=1)  # day 1 = Monday (weekday)
        system = ScheduleSystem(tm)
        system.set_registry(registry)
        comp = registry.get_component(sim, ScheduleComponent)

        tm.set_time(23, 0)
        system.update(1.0)
        assert comp.current_activity == "sleep"
        assert comp.weekend is False

        tm.set_time(9, 0)
        system.update(1.0)
        assert comp.current_activity == "work"

        tm.set_time(12, 0)
        system.update(1.0)
        assert comp.current_activity == "eat_lunch"

    def test_weekend_schedule_selected(self):
        registry = Registry()
        sim = _make_registry_with_sim(registry)
        tm = TimeManager(start_day=6)  # Saturday
        system = ScheduleSystem(tm)
        system.set_registry(registry)
        comp = registry.get_component(sim, ScheduleComponent)

        tm.set_time(10, 0)
        system.update(1.0)
        assert comp.weekend is True
        assert comp.current_activity == "relax"

    def test_move_queued_when_at_wrong_location(self):
        registry = Registry()
        # Sim starts in the "kitchen" area; sleep requires a bed in bedroom.
        sim = _make_registry_with_sim(registry, x=5, y=5)
        bed = Entity(entity_id="bed1")
        registry.add_entity(bed)
        registry.add_component(bed, Position(2, 2, 0))
        registry.add_component(bed, FurnitureComponent(FurnitureType.BED))
        registry.add_component(bed, RoomComponent("bedroom"))

        tm = TimeManager(start_day=1)
        events = []
        system = ScheduleSystem(tm, on_event=lambda et, d: events.append((et, d)))
        system.set_registry(registry)
        controller = registry.get_component(sim, AgentController)

        tm.set_time(23, 0)
        system.update(1.0)

        move_events = [d for et, d in events if et == EventType.SCHEDULE_MOVE_QUEUED]
        assert len(move_events) == 1
        assert move_events[0]["to"] == {"x": 2, "y": 2}
        assert controller.current_intent is not None
        assert controller.current_intent["type"] == "move"
        assert controller.current_intent["data"] == {"x": 2, "y": 2}

    def test_no_move_when_already_at_destination(self):
        registry = Registry()
        sim = _make_registry_with_sim(registry, x=2, y=2, needs=True)
        bed = Entity(entity_id="bed1")
        registry.add_entity(bed)
        registry.add_component(bed, Position(2, 2, 0))
        registry.add_component(bed, FurnitureComponent(FurnitureType.BED))
        registry.add_component(bed, RoomComponent("bedroom"))

        tm = TimeManager(start_day=1)
        events = []
        system = ScheduleSystem(
            tm, on_event=lambda et, d: events.append((et, d))
        )
        system.set_registry(registry)
        controller = registry.get_component(sim, AgentController)
        needs = registry.get_component(sim, NeedsComponent)
        energy_before = needs.get(NeedType.ENERGY)

        tm.set_time(23, 0)
        system.update(1.0)

        assert controller.current_intent is None
        assert any(et == EventType.NEED_FULFILLED for et, _ in events)
        assert needs.get(NeedType.ENERGY) > energy_before

    def test_does_not_queue_move_while_busy(self):
        registry = Registry()
        sim = _make_registry_with_sim(registry, x=5, y=5)
        bed = Entity(entity_id="bed1")
        registry.add_entity(bed)
        registry.add_component(bed, Position(1, 1, 0))
        registry.add_component(bed, FurnitureComponent(FurnitureType.BED))
        registry.add_component(bed, RoomComponent("bedroom"))

        tm = TimeManager(start_day=1)
        system = ScheduleSystem(tm)
        system.set_registry(registry)
        controller = registry.get_component(sim, AgentController)
        controller.current_intent = {"type": "move", "target_id": None, "data": {"x": 0}}

        tm.set_time(23, 0)
        system.update(1.0)

        # Existing intent preserved, no new move queued.
        assert controller.current_intent["type"] == "move"

    def test_idle_behavior_when_no_entry(self):
        registry = Registry()
        sim = Entity(entity_id="sim1")
        registry.add_entity(sim)
        registry.add_component(sim, Position(5, 5, 0))
        registry.add_component(sim, AgentController("sim1"))
        # A schedule that only covers hour 9.
        custom = DailySchedule([ScheduleEntry("work", 9, 17, FurnitureType.COMPUTER, "office")])
        sched = ScheduleComponent(schedule=custom)
        registry.add_component(sim, sched)
        controller = registry.get_component(sim, AgentController)

        # Nearby interactable for idle pick-up.
        couch = Entity(entity_id="couch1")
        registry.add_entity(couch)
        registry.add_component(couch, Position(5, 6, 0))
        registry.add_component(couch, FurnitureComponent(FurnitureType.COUCH))
        registry.add_component(couch, Interactable(["sit"]))

        tm = TimeManager(start_day=1)
        events = []
        system = ScheduleSystem(tm, on_event=lambda et, d: events.append((et, d)))
        system.set_registry(registry)

        tm.set_time(8, 0)  # before the work window (9-17) -> no entry -> idle
        system.update(1.0)

        assert sched.current_activity == "idle"
        assert controller.current_intent is not None
        assert controller.current_intent["type"] == "use"
        assert any(et == EventType.IDLE_BEHAVIOR_TRIGGERED for et, _ in events)

    def test_no_location_requirement_fulfills_in_place(self):
        registry = Registry()
        sim = Entity(entity_id="sim1")
        registry.add_entity(sim)
        registry.add_component(sim, Position(5, 5, 0))
        registry.add_component(sim, AgentController("sim1"))
        custom = DailySchedule([ScheduleEntry("exercise", 6, 7, None, None, NeedType.COMFORT)])
        sched = ScheduleComponent(schedule=custom)
        registry.add_component(sim, sched)
        registry.add_component(sim, NeedsComponent())
        needs = registry.get_component(sim, NeedsComponent)
        energy_before = needs.get(NeedType.COMFORT)

        tm = TimeManager(start_day=1)
        events = []
        system = ScheduleSystem(tm, on_event=lambda et, d: events.append((et, d)))
        system.set_registry(registry)

        tm.set_time(6, 0)
        system.update(1.0)

        controller = registry.get_component(sim, AgentController)
        assert controller.current_intent is None  # no move needed
        assert any(et == EventType.NEED_FULFILLED for et, _ in events)
        assert needs.get(NeedType.COMFORT) > energy_before


# ---------------------------------------------------------------------------
# Engine integration
# ---------------------------------------------------------------------------


class TestEngineIntegration:
    def test_schedule_system_registered(self):
        engine = WorldEngine()
        types = [type(s) for s in engine.registry._systems]
        assert any(t is ScheduleSystem for t in types)

    def test_engine_tick_drives_schedule(self):
        engine = WorldEngine({"grid_width": 20, "grid_height": 20})
        sim = engine.spawn_entity()
        engine.registry.add_component(sim, Position(5, 5, 0))
        engine.registry.add_component(sim, AgentController("sim1"))
        engine.registry.add_component(sim, ScheduleComponent())
        comp = engine.registry.get_component(sim, ScheduleComponent)

        engine.time_manager.set_time(9, 0)
        engine.run_simulation_step()
        assert comp.current_activity == "work"

        engine.time_manager.set_time(23, 0)
        engine.run_simulation_step()
        assert comp.current_activity == "sleep"

    def test_save_load_preserves_schedule(self):
        engine = WorldEngine({"grid_width": 20, "grid_height": 20})
        sim = engine.spawn_entity()
        engine.registry.add_component(sim, Position(1, 2, 0))
        engine.registry.add_component(sim, AgentController("sim1"))
        comp = ScheduleComponent()
        comp.current_activity = "work"
        comp.weekend = True
        engine.registry.add_component(sim, comp)
        engine.registry.add_component(sim, NeedsComponent({NeedType.HUNGER: 25.0}))

        bed = engine.spawn_entity()
        engine.registry.add_component(bed, Position(3, 3, 0))
        engine.registry.add_component(bed, FurnitureComponent(FurnitureType.BED))
        engine.registry.add_component(bed, RoomComponent("bedroom"))

        state = engine.save_state()
        engine2 = WorldEngine({"grid_width": 20, "grid_height": 20})
        engine2.load_state(state)

        sims = [
            e for e in engine2.registry.get_entities()
            if engine2.registry.has_component(e, ScheduleComponent)
        ]
        assert len(sims) == 1
        restored = engine2.registry.get_component(sims[0], ScheduleComponent)
        assert restored.current_activity == "work"
        assert restored.weekend is True
        assert len(restored.workday_schedule.entries) == len(comp.workday_schedule.entries)

        beds = [
            e for e in engine2.registry.get_entities()
            if engine2.registry.has_component(e, FurnitureComponent)
        ]
        assert len(beds) == 1
        assert engine2.registry.get_component(beds[0], FurnitureComponent).furniture_type is FurnitureType.BED
        assert engine2.registry.get_component(beds[0], RoomComponent).room_name == "bedroom"

        needs = engine2.registry.get_component(sims[0], NeedsComponent)
        assert needs.get(NeedType.HUNGER) == 25.0
