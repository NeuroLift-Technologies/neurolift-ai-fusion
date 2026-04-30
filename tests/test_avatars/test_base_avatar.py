"""Tests for BaseAvatar class and Avatar system components."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch

from src.core.events import EventBus, SignalType
from src.core.protocols import InteractionChannel
from src.avatars.base_avatar import (
    BaseAvatar,
    AvatarState,
    TaskResult,
    LearningProgress,
    TaskDifficulty,
)


class TestAvatar(BaseAvatar):
    """Test implementation of BaseAvatar."""

    def get_adhd_trait_impact(self, task_context):
        return {
            "difficulty_modifier": 1.5,
            "struggle_indicators": ["test_struggle"],
            "quality_modifier": 0.1,
            "time_modifier": 1.2,
            "cognitive_load_modifier": 0.2,
        }

    def simulate_struggle(self, task_context):
        return ["test_struggle", "attention_lapse"]


class TestBaseAvatar:
    def test_avatar_initialization(self):
        config = {"trait_name": "test_trait"}
        avatar = TestAvatar("test_001", config)

        assert avatar.avatar_id == "test_001"
        assert avatar.trait_name == "test_trait"
        assert avatar.current_state == AvatarState.IDLE
        assert avatar.emotional_state == "neutral"
        assert avatar.cognitive_load == 0.0
        assert avatar.stress_level == 0.0
        assert avatar.total_tasks_attempted == 0
        assert avatar.experience_memory.total_experiences == 0

    def test_avatar_with_shared_event_bus(self):
        bus = EventBus()
        avatar = TestAvatar("a1", {"trait_name": "t"}, event_bus=bus)
        assert avatar.event_bus is bus

    def test_state_transitions_on_task(self):
        avatar = TestAvatar("a1", {"trait_name": "t"})
        task = {"task_type": "test", "base_success_rate": 0.8}
        result = avatar.attempt_task(task)

        assert avatar.current_state in (
            AvatarState.LEARNING,
            AvatarState.STRUGGLING,
            AvatarState.INDEPENDENT,
        )
        assert avatar.total_tasks_attempted == 1

    def test_task_result_structure(self):
        avatar = TestAvatar("a1", {"trait_name": "t"})
        task = {
            "task_type": "test",
            "base_success_rate": 0.8,
            "expected_duration": timedelta(minutes=10),
            "cognitive_demand": 0.6,
        }
        result = avatar.attempt_task(task)

        assert isinstance(result, TaskResult)
        assert result.struggle_indicators == ["test_struggle", "attention_lapse"]
        assert result.emotional_state in ("confident", "relieved", "frustrated", "disappointed")
        assert 0.0 <= result.quality_score <= 1.0
        assert 0.0 <= result.cognitive_load <= 1.0

    def test_coaching_reception(self):
        avatar = TestAvatar("a1", {"trait_name": "t"})
        # Force into a state that can receive coaching
        avatar.current_state = AvatarState.STRUGGLING
        avatar.stress_level = 0.5

        coaching = {"strategy": "test", "stress_reduction": 0.3, "emotional_boost": 0.2}
        initial_stress = avatar.stress_level
        avatar.receive_coaching(coaching)

        assert avatar.current_state == AvatarState.APPLYING_STRATEGY
        assert avatar.total_coaching_sessions == 1
        # Verify stress was reduced by coaching effects
        assert avatar.stress_level <= initial_stress
        assert avatar.stress_level < initial_stress
        assert len(avatar.coaching_history) == 1
        assert avatar.coaching_history[0]["avatar_state_before"] == AvatarState.STRUGGLING.value

    def test_attempt_not_marked_independent_when_coached_before_attempt(self):
        avatar = TestAvatar("a1", {"trait_name": "t"})
        avatar.current_state = AvatarState.STRUGGLING

        coaching = {"strategy": "test", "stress_reduction": 0.2, "emotional_boost": 0.1}
        avatar.receive_coaching(coaching)
        # Simulate delayed retry so timestamp-only checks would misclassify.
        avatar.coaching_history[-1]["timestamp"] = datetime.now() - timedelta(minutes=5)

        with patch("random.random", return_value=0.01):
            result = avatar.attempt_task({"task_type": "focus", "base_success_rate": 0.9})

        assert result.independent is False

    def test_learning_progress_tracking(self):
        avatar = TestAvatar("a1", {"trait_name": "t"})
        task = {"task_type": "focus_task", "base_success_rate": 0.5}
        avatar.attempt_task(task)

        assert "focus_task" in avatar.learning_progress
        progress = avatar.learning_progress["focus_task"]
        assert progress.attempts == 1

    def test_independence_level(self):
        avatar = TestAvatar("a1", {"trait_name": "t"})
        assert avatar.get_independence_level() == 0.0

        task = {"task_type": "test", "base_success_rate": 0.99}
        with patch("random.random", return_value=0.01):
            for _ in range(5):
                avatar.attempt_task(task)
                avatar.return_to_idle()

        assert avatar.get_independence_level("test") > 0.0

    def test_burnout_risk_assessment(self):
        avatar = TestAvatar("a1", {"trait_name": "t"})
        avatar.stress_level = 0.8
        assessment = avatar.assess_burnout_risk()

        assert "risk_level" in assessment
        assert "risk_score" in assessment
        assert 0.0 <= assessment["risk_score"] <= 1.0

    def test_state_summary(self):
        avatar = TestAvatar("a1", {"trait_name": "t"})
        avatar.attempt_task({"task_type": "test", "base_success_rate": 0.8})

        summary = avatar.get_state_summary()
        assert summary["avatar_id"] == "a1"
        assert summary["total_tasks_attempted"] == 1
        assert "total_experiences" in summary
        assert "recurring_struggles" in summary

    def test_experience_memory_populated(self):
        avatar = TestAvatar("a1", {"trait_name": "t"})
        task = {"task_type": "focus", "base_success_rate": 0.8}
        avatar.attempt_task(task)

        assert avatar.experience_memory.total_experiences == 1
        records = avatar.experience_memory.recall_by_task("focus")
        assert len(records) == 1

    def test_observation_snapshot(self):
        avatar = TestAvatar("a1", {"trait_name": "t"})
        snapshot = avatar.get_observation_snapshot()
        assert snapshot.avatar_id == "a1"
        assert snapshot.current_state == "idle"

    def test_bind_channel(self):
        avatar = TestAvatar("a1", {"trait_name": "t"})
        ch = InteractionChannel(avatar_id="a1", aide_id="aide1")
        avatar.bind_channel(ch)
        assert avatar.channel is ch

    def test_emotional_state_scenarios(self):
        avatar = TestAvatar("a1", {"trait_name": "t"})

        # Force success with no struggles
        with patch("random.random", return_value=0.01):
            with patch.object(avatar, "simulate_struggle", return_value=[]):
                avatar.attempt_task({"task_type": "t", "base_success_rate": 0.99})
                assert avatar.emotional_state == "confident"

    def test_signals_emitted_on_task(self):
        bus = EventBus()
        avatar = TestAvatar("a1", {"trait_name": "t"}, event_bus=bus)
        avatar.attempt_task({"task_type": "test", "base_success_rate": 0.8})

        history = bus.get_history(source_id="a1")
        types = {s.signal_type for s in history}
        assert SignalType.AVATAR_TASK_STARTED in types
        assert (
            SignalType.AVATAR_TASK_COMPLETED in types
            or SignalType.AVATAR_TASK_FAILED in types
        )

    def test_experience_bonus_improves_with_practice(self):
        avatar = TestAvatar("a1", {"trait_name": "t"})
        task = {"task_type": "practice_task", "base_success_rate": 0.8}

        bonus_before = avatar._experience_bonus(task)

        with patch("random.random", return_value=0.01):
            for _ in range(5):
                avatar.attempt_task(task)
                avatar.return_to_idle()

        bonus_after = avatar._experience_bonus(task)
        assert bonus_after > bonus_before

    def test_consecutive_failure_tracking(self):
        avatar = TestAvatar("a1", {"trait_name": "t"})
        task = {"task_type": "hard_task", "base_success_rate": 0.01}

        with patch("random.random", return_value=0.99):
            avatar.attempt_task(task)
            avatar.return_to_idle()
            avatar.attempt_task(task)

        progress = avatar.learning_progress["hard_task"]
        assert progress.consecutive_failures >= 1
