"""Tests for interaction protocols."""

import pytest
from src.core.protocols import (
    Message,
    MessageType,
    ObservationReport,
    CoachingIntervention,
    InteractionChannel,
    ExperienceMemory,
    ExperienceRecord,
)


class TestInteractionChannel:
    def test_create_channel(self):
        ch = InteractionChannel(avatar_id="a1", aide_id="aide1")
        assert ch.avatar_id == "a1"
        assert ch.aide_id == "aide1"
        assert ch.message_count == 0

    def test_send_and_retrieve(self):
        ch = InteractionChannel(avatar_id="a1", aide_id="aide1")
        msg = Message(
            message_type=MessageType.STRUGGLE_REPORT,
            sender_id="a1",
            receiver_id="aide1",
            payload={"struggle": "attention_lapse"},
        )
        ch.send(msg)
        assert ch.message_count == 1
        msgs = ch.get_messages()
        assert len(msgs) == 1
        assert msgs[0].payload["struggle"] == "attention_lapse"

    def test_filter_by_type(self):
        ch = InteractionChannel(avatar_id="a1", aide_id="aide1")
        ch.send(Message(message_type=MessageType.STRUGGLE_REPORT, sender_id="a1"))
        ch.send(Message(message_type=MessageType.COACHING_INTERVENTION, sender_id="aide1"))
        ch.send(Message(message_type=MessageType.ACKNOWLEDGEMENT, sender_id="a1"))

        coaching = ch.get_recent_coaching()
        assert len(coaching) == 1
        struggles = ch.get_recent_struggles()
        assert len(struggles) == 1

    def test_coaching_count(self):
        ch = InteractionChannel(avatar_id="a1", aide_id="aide1")
        ch.send(Message(message_type=MessageType.COACHING_INTERVENTION, sender_id="aide1"))
        ch.send(Message(message_type=MessageType.COACHING_INTERVENTION, sender_id="aide1"))
        assert ch.coaching_count == 2


class TestObservationReport:
    def test_needs_intervention_stress(self):
        obs = ObservationReport(stress_level=0.8)
        assert obs.needs_intervention is True

    def test_needs_intervention_normal(self):
        obs = ObservationReport(stress_level=0.3, cognitive_load=0.4)
        assert obs.needs_intervention is False

    def test_needs_intervention_emotional(self):
        obs = ObservationReport(emotional_state="frustrated")
        assert obs.needs_intervention is True

    def test_needs_intervention_many_struggles(self):
        obs = ObservationReport(active_struggles=["a", "b", "c"])
        assert obs.needs_intervention is True


class TestExperienceMemory:
    def _make_record(self, task_type="focus", success=True, struggles=None):
        return ExperienceRecord(
            task_type=task_type,
            outcome_success=success,
            struggles_experienced=struggles or [],
            independence_delta=0.1 if success else 0.0,
            strategy_discovered="pomodoro" if success else None,
        )

    def test_record_and_recall(self):
        mem = ExperienceMemory(owner_id="a1")
        mem.record(self._make_record())
        assert mem.total_experiences == 1
        assert len(mem.recall_by_task("focus")) == 1

    def test_recall_successes(self):
        mem = ExperienceMemory(owner_id="a1")
        mem.record(self._make_record(success=True))
        mem.record(self._make_record(success=False))
        assert len(mem.recall_successes()) == 1

    def test_recall_struggles(self):
        mem = ExperienceMemory(owner_id="a1")
        mem.record(self._make_record(struggles=["attention_lapse"]))
        mem.record(self._make_record(struggles=["distraction"]))
        assert len(mem.recall_struggles("attention_lapse")) == 1

    def test_recurring_struggles(self):
        mem = ExperienceMemory(owner_id="a1")
        for _ in range(5):
            mem.record(self._make_record(struggles=["attention_lapse"]))
        recurring = mem.get_recurring_struggles(min_occurrences=3)
        assert "attention_lapse" in recurring
        assert recurring["attention_lapse"] == 5

    def test_effective_strategies(self):
        mem = ExperienceMemory(owner_id="a1")
        for _ in range(4):
            mem.record(self._make_record(success=True))
        mem.record(self._make_record(success=False))
        effective = mem.get_effective_strategies()
        assert "pomodoro" in effective
        assert effective["pomodoro"] == 1.0  # all successes had this strategy

    def test_independence_trajectory(self):
        mem = ExperienceMemory(owner_id="a1")
        for _ in range(3):
            mem.record(self._make_record(success=True))
        traj = mem.get_independence_trajectory()
        assert len(traj) == 3
        assert traj[-1] > traj[0]

    def test_success_rate(self):
        mem = ExperienceMemory(owner_id="a1")
        mem.record(self._make_record(success=True))
        mem.record(self._make_record(success=False))
        assert mem.success_rate == 0.5

    def test_get_records_public_accessor(self):
        mem = ExperienceMemory(owner_id="a1")
        mem.record(self._make_record(task_type="a"))
        mem.record(self._make_record(task_type="b"))
        mem.record(self._make_record(task_type="c"))

        all_records = mem.get_records()
        assert len(all_records) == 3

        limited = mem.get_records(limit=2)
        assert len(limited) == 2
        assert [r.task_type for r in limited] == ["b", "c"]
