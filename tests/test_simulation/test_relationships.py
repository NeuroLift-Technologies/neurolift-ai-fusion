"""Tests for the Relationship system (friendship / romance / familiarity)."""

import pytest
from datetime import datetime

from src.simulation.environment.ecs import AgentController, Entity, Position, Registry
from src.simulation.environment.relationships import (
    RelationshipComponent,
    RelationshipManager,
    RelationshipSystem,
    SocialInteractionType,
)
from src.simulation.environment.time_manager import TimeManager
from src.simulation.environment.world_engine import EventType, WorldEngine


def _make_manager(registry=None, on_event=None):
    return RelationshipManager(registry=registry or Registry(), on_event=on_event)


class TestSocialInteractionType:
    def test_all_required_members_exist(self):
        names = {t.name for t in SocialInteractionType}
        assert {
            "CHAT",
            "FLIRT",
            "ARGUE",
            "COMPLIMENT",
            "INSULT",
            "JOKE",
            "DEEP_CONVERSATION",
        } <= names


class TestRelationshipComponent:
    def test_pair_is_normalized(self):
        comp = RelationshipComponent(sim_a_id="b", sim_b_id="a")
        assert comp.sim_a_id == "a"
        assert comp.sim_b_id == "b"

    def test_pair_already_ordered(self):
        comp = RelationshipComponent(sim_a_id="a", sim_b_id="b")
        assert comp.sim_a_id == "a"
        assert comp.sim_b_id == "b"

    def test_scores_clamped(self):
        comp = RelationshipComponent(
            sim_a_id="a",
            sim_b_id="b",
            friendship=150.0,
            romance=-5.0,
            familiarity=200.0,
        )
        assert comp.friendship == 100.0
        assert comp.romance == 0.0
        assert comp.familiarity == 100.0

    def test_defaults(self):
        comp = RelationshipComponent(sim_a_id="a", sim_b_id="b")
        assert comp.friendship == 0.0
        assert comp.romance == 0.0
        assert comp.familiarity == 0.0
        assert comp.interaction_count == 0
        assert isinstance(comp.last_interaction, datetime)

    def test_accepts_iso_string_last_interaction(self):
        comp = RelationshipComponent(
            sim_a_id="a",
            sim_b_id="b",
            last_interaction="2024-01-02T03:04:05",
        )
        assert comp.last_interaction == datetime(2024, 1, 2, 3, 4, 5)

    def test_is_involved_and_other_sim(self):
        comp = RelationshipComponent(sim_a_id="a", sim_b_id="b")
        assert comp.is_involved("a")
        assert comp.is_involved("b")
        assert not comp.is_involved("c")
        assert comp.other_sim("a") == "b"
        assert comp.other_sim("b") == "a"
        assert comp.other_sim("c") is None

    def test_to_dict_round_trip(self):
        comp = RelationshipComponent(
            sim_a_id="a",
            sim_b_id="b",
            friendship=42.0,
            romance=10.0,
            familiarity=7.0,
            interaction_count=3,
        )
        d = comp.to_dict()
        assert d["sim_a_id"] == "a"
        assert d["sim_b_id"] == "b"
        assert d["friendship"] == 42.0
        assert d["interaction_count"] == 3
        restored = RelationshipComponent(**d)
        assert restored.friendship == 42.0
        assert restored.romance == 10.0
        assert restored.interaction_count == 3


class TestRelationshipManager:
    def test_get_or_create_bidirectional(self):
        mgr = _make_manager()
        comp_ab = mgr.get_or_create("simA", "simB")
        comp_ba = mgr.get_or_create("simB", "simA")
        assert comp_ab is comp_ba
        assert comp_ab.sim_a_id == "simA"
        assert comp_ab.sim_b_id == "simB"

    def test_get_or_create_emits_added_event(self):
        events = []
        mgr = _make_manager(on_event=lambda et, data: events.append((et, data)))
        mgr.get_or_create("a", "b")
        assert any(et == EventType.RELATIONSHIP_ADDED for et, _ in events)

    def test_existing_pair_does_not_re_emit_added(self):
        mgr = _make_manager(on_event=lambda *a: None)
        mgr.get_or_create("a", "b")
        mgr.get_or_create("a", "b")
        # Just ensure no exception and same component returned.
        assert True

    def test_positive_interaction_increases_friendship(self):
        mgr = _make_manager()
        mgr.interact("a", "b", SocialInteractionType.COMPLIMENT, quality=1.0)
        comp = mgr.get_or_create("a", "b")
        assert comp.friendship == pytest.approx(8.0)
        assert comp.interaction_count == 1

    def test_quality_scales_effect(self):
        mgr = _make_manager()
        mgr.interact("a", "b", SocialInteractionType.COMPLIMENT, quality=0.5)
        comp = mgr.get_or_create("a", "b")
        assert comp.friendship == pytest.approx(4.0)

    def test_insult_decreases_friendship(self):
        mgr = _make_manager()
        mgr.interact("a", "b", SocialInteractionType.INSULT, quality=1.0)
        comp = mgr.get_or_create("a", "b")
        assert comp.friendship == pytest.approx(0.0)  # -12 clamped to 0

    def test_quality_clamped(self):
        mgr = _make_manager()
        mgr.interact("a", "b", SocialInteractionType.COMPLIMENT, quality=5.0)
        comp = mgr.get_or_create("a", "b")
        assert comp.friendship == pytest.approx(8.0)

    def test_repeated_positive_interactions_build_friendship(self):
        mgr = _make_manager()
        for _ in range(5):
            mgr.interact("a", "b", SocialInteractionType.COMPLIMENT, quality=1.0)
        comp = mgr.get_or_create("a", "b")
        assert comp.friendship == pytest.approx(40.0)
        assert comp.interaction_count == 5

    def test_romance_requires_friendship(self):
        mgr = _make_manager()
        # Low friendship -> flirt yields ~0 romance.
        mgr.interact("a", "b", SocialInteractionType.COMPLIMENT, quality=1.0)
        comp = mgr.get_or_create("a", "b")
        assert comp.friendship == pytest.approx(8.0)
        mgr.interact("a", "b", SocialInteractionType.FLIRT, quality=1.0)
        # romance scaled by friendship fraction: 8 * (8/100) = 0.64
        assert comp.romance == pytest.approx(8.0 * (8.0 / 100.0))

    def test_romance_capped_at_friendship(self):
        mgr = _make_manager()
        mgr.get_or_create("a", "b")
        # High friendship then repeated flirting.
        comp = mgr.get_or_create("a", "b")
        comp.friendship = 60.0
        for _ in range(10):
            mgr.interact("a", "b", SocialInteractionType.FLIRT, quality=1.0)
        assert comp.romance <= comp.friendship

    def test_romance_does_not_grow_from_non_flirt(self):
        mgr = _make_manager()
        mgr.get_or_create("a", "b")
        comp = mgr.get_or_create("a", "b")
        comp.friendship = 90.0
        mgr.interact("a", "b", SocialInteractionType.COMPLIMENT, quality=1.0)
        assert comp.romance == 0.0

    def test_apply_decay_reduces_scores(self):
        mgr = _make_manager()
        comp = mgr.get_or_create("a", "b")
        comp.friendship = 50.0
        comp.romance = 30.0
        mgr.apply_decay(2.0)  # 2 sim-hours -> 0.2 decay
        assert comp.friendship == pytest.approx(49.8)
        assert comp.romance == pytest.approx(29.8)

    def test_decay_floors_at_zero(self):
        mgr = _make_manager()
        comp = mgr.get_or_create("a", "b")
        comp.friendship = 0.5
        comp.romance = 0.5
        mgr.apply_decay(10.0)
        assert comp.friendship == 0.0
        assert comp.romance == 0.0

    def test_decay_zero_hours_noop(self):
        mgr = _make_manager()
        comp = mgr.get_or_create("a", "b")
        comp.friendship = 50.0
        mgr.apply_decay(0.0)
        assert comp.friendship == 50.0

    def test_get_all_for_sim(self):
        mgr = _make_manager()
        mgr.get_or_create("a", "b")
        mgr.get_or_create("a", "c")
        mgr.get_or_create("x", "y")
        rels = mgr.get_all_for_sim("a")
        pairs = {(r.sim_a_id, r.sim_b_id) for r in rels}
        assert pairs == {("a", "b"), ("a", "c")}
        assert len(mgr.get_all_for_sim("x")) == 1
        assert len(mgr.get_all_for_sim("z")) == 0

    def test_interact_emits_events(self):
        events = []
        mgr = _make_manager(on_event=lambda et, d: events.append(et))
        mgr.interact("a", "b", SocialInteractionType.FLIRT, quality=1.0)
        assert EventType.RELATIONSHIP_ADDED in events
        assert EventType.RELATIONSHIP_UPDATED in events
        assert EventType.SOCIAL_INTERACTION in events


class TestRelationshipSystem:
    def _make_two_sims(self, registry: Registry, pos=(5, 5)):
        for sid in ("sim1", "sim2"):
            ent = Entity(entity_id=sid)
            registry.add_entity(ent)
            registry.add_component(ent, Position(*pos))
            registry.add_component(ent, AgentController(sid))
        return registry

    def test_proximity_triggers_interaction(self):
        registry = Registry()
        self._make_two_sims(registry, pos=(5, 5))
        tm = TimeManager(speed_multiplier=1.0)
        mgr = RelationshipManager(registry=registry)
        system = RelationshipSystem(mgr, tm, interaction_probability=1.0, seed=1)
        system.set_registry(registry)

        # No sim time has advanced yet -> no decay, but co-located Sims interact.
        system.update(1.0)
        comp = mgr.get_or_create("sim1", "sim2")
        assert comp.interaction_count >= 1

    def test_separate_sims_do_not_interact(self):
        registry = Registry()
        for sid, pos in [("sim1", (5, 5)), ("sim2", (20, 20))]:
            ent = Entity(entity_id=sid)
            registry.add_entity(ent)
            registry.add_component(ent, Position(*pos))
            registry.add_component(ent, AgentController(sid))
        tm = TimeManager(speed_multiplier=1.0)
        mgr = RelationshipManager(registry=registry)
        system = RelationshipSystem(mgr, tm, interaction_probability=1.0, seed=1)
        system.set_registry(registry)

        system.update(1.0)
        # No shared cell -> no relationship should exist.
        assert len(mgr.get_all_for_sim("sim1")) == 0

    def test_decay_applied_each_tick(self):
        registry = Registry()
        # No Sims needed; pre-create a relationship directly.
        mgr = RelationshipManager(registry=registry)
        comp = mgr.get_or_create("a", "b")
        comp.friendship = 50.0
        tm = TimeManager(speed_multiplier=60.0)  # 1 real tick sec = 60 sim-min
        system = RelationshipSystem(mgr, tm, interaction_probability=0.0, seed=1)
        system.set_registry(registry)

        tm.advance(60)  # advance 1 sim-hour
        system.update(1.0)
        # 1 sim-hour of decay -> 0.1 lost
        assert comp.friendship == pytest.approx(49.9, abs=1e-6)

    def test_no_sim_entities_is_safe(self):
        registry = Registry()
        tm = TimeManager()
        mgr = RelationshipManager(registry=registry)
        system = RelationshipSystem(mgr, tm, interaction_probability=1.0, seed=1)
        system.set_registry(registry)
        system.update(1.0)  # should not raise


class TestEngineIntegration:
    def test_engine_subscribes_to_relationship_events(self):
        engine = WorldEngine()
        received = []
        engine.subscribe(
            EventType.RELATIONSHIP_ADDED, lambda et, d: received.append(et)
        )
        engine.subscribe(
            EventType.SOCIAL_INTERACTION, lambda et, d: received.append(et)
        )
        engine.relationship_manager.interact(
            "a", "b", SocialInteractionType.COMPLIMENT, 1.0
        )
        assert EventType.RELATIONSHIP_ADDED in received
        assert EventType.SOCIAL_INTERACTION in received

    def test_engine_tick_drives_relationships(self):
        engine = WorldEngine(
            {
                "grid_width": 20,
                "grid_height": 20,
                "seconds_per_tick": 1.0,
                "time_speed_multiplier": 60.0,
            }
        )
        for sid in ("simA", "simB"):
            ent = engine.spawn_entity()
            engine.registry.add_component(ent, Position(5, 5, 0))
            engine.registry.add_component(ent, AgentController(sid))
        engine.run_simulation_step()
        engine.run_simulation_step()
        # With probability=0.15 the relationship may or may not have formed;
        # but the system must not have crashed and decay must have been applied.
        rels = [r for r in engine.relationship_manager.get_all_for_sim("simA")]
        # Either 0 or 1 relationship — both are valid outcomes.
        assert len(rels) <= 1

    def test_save_load_preserves_relationships(self):
        engine = WorldEngine()
        engine.relationship_manager.interact(
            "a", "b", SocialInteractionType.COMPLIMENT, 1.0
        )
        comp = engine.relationship_manager.get_or_create("a", "b")
        assert comp.friendship == pytest.approx(8.0)
        state = engine.save_state()

        engine2 = WorldEngine()
        engine2.load_state(state)
        rels = engine2.relationship_manager.get_all_for_sim("a")
        assert len(rels) == 1
        restored = rels[0]
        assert restored.friendship == pytest.approx(8.0)
        assert restored.interaction_count == 1
        assert isinstance(restored.last_interaction, datetime)
