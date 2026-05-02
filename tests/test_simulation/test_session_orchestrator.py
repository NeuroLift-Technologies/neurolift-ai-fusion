"""Tests for the SessionOrchestrator."""

import pytest
from unittest.mock import patch

from src.core.events import EventBus
from src.avatars.base_avatar import BaseAvatar, AvatarState
from src.aides.base_aide import BaseAide, CoachingContext
from src.core.protocols import ObservationReport
from src.simulation.session_orchestrator import (
    SessionOrchestrator,
    SessionConfig,
    SessionPhase,
)


# -- Test doubles --

class _TestAvatar(BaseAvatar):
    def get_adhd_trait_impact(self, task_context):
        return {
            "difficulty_modifier": 1.2,
            "quality_modifier": 0.1,
            "time_modifier": 1.0,
            "cognitive_load_modifier": 0.1,
        }

    def simulate_struggle(self, task_context):
        return ["mild_struggle"]


class _TestAide(BaseAide):
    def get_expertise_strategies(self, context):
        return [{
            "strategy": "Test Strategy",
            "techniques": ["technique_1"],
            "expected_outcomes": ["improvement"],
            "effectiveness": 0.8,
            "stress_reduction": 0.2,
            "emotional_boost": 0.1,
            "focus_restoration": 0.2,
            "independence_building": 0.1,
        }]

    def get_real_world_insights(self, context):
        return [{
            "source": "real_world",
            "strategy": "Real World Tip",
            "techniques": ["tip_1"],
            "expected_outcomes": ["better_outcome"],
            "effectiveness": 0.9,
            "context_match": 0.8,
            "stress_reduction": 0.3,
            "emotional_boost": 0.2,
            "focus_restoration": 0.3,
            "independence_building": 0.2,
        }]


class TestSessionOrchestrator:
    def _make_pair(self):
        bus = EventBus()
        avatar = _TestAvatar("avatar_test", {"trait_name": "attention"}, event_bus=bus)
        aide = _TestAide("aide_test", {"expertise_area": "attention_coaching"}, event_bus=bus)
        return avatar, aide

    def test_basic_session(self):
        avatar, aide = self._make_pair()
        config = SessionConfig(max_attempts_per_scenario=5, max_coaching_per_attempt=2)
        orchestrator = SessionOrchestrator(avatar, aide, config)

        scenarios = [
            {
                "name": "Simple Focus Task",
                "task_type": "focus",
                "base_success_rate": 0.7,
                "cognitive_demand": 0.5,
            },
        ]

        result = orchestrator.run_session(scenarios)

        assert result.phase == SessionPhase.COMPLETED
        assert result.total_attempts > 0
        assert len(result.scenario_results) == 1
        assert result.completed_at is not None

    def test_multiple_scenarios(self):
        avatar, aide = self._make_pair()
        orchestrator = SessionOrchestrator(avatar, aide)

        scenarios = [
            {"name": "Task A", "task_type": "a", "base_success_rate": 0.8, "cognitive_demand": 0.4},
            {"name": "Task B", "task_type": "b", "base_success_rate": 0.6, "cognitive_demand": 0.6},
        ]

        result = orchestrator.run_session(scenarios)
        assert len(result.scenario_results) == 2

    def test_burnout_abort(self):
        avatar, aide = self._make_pair()
        avatar.stress_level = 0.95
        config = SessionConfig(burnout_abort_threshold=0.3)
        orchestrator = SessionOrchestrator(avatar, aide, config)

        scenarios = [
            {"name": "Hard Task", "task_type": "hard", "base_success_rate": 0.1, "cognitive_demand": 0.9},
        ]

        result = orchestrator.run_session(scenarios)
        sr = result.scenario_results[0]
        assert sr.aborted is True

    def test_single_attempt(self):
        avatar, aide = self._make_pair()
        orchestrator = SessionOrchestrator(avatar, aide)

        result = orchestrator.run_single_attempt({
            "task_type": "quick",
            "base_success_rate": 0.8,
            "cognitive_demand": 0.3,
        })

        assert avatar.total_tasks_attempted >= 1

    def test_fusion_readiness_checked(self):
        avatar, aide = self._make_pair()
        config = SessionConfig(
            check_fusion_readiness=True,
            max_attempts_per_scenario=3,
        )
        orchestrator = SessionOrchestrator(avatar, aide, config)

        result = orchestrator.run_session([
            {"name": "Test", "task_type": "t", "base_success_rate": 0.8, "cognitive_demand": 0.4},
        ])

        assert result.fusion_readiness is not None
        assert hasattr(result.fusion_readiness, "ready")

    def test_session_result_to_dict(self):
        avatar, aide = self._make_pair()
        orchestrator = SessionOrchestrator(avatar, aide)

        result = orchestrator.run_session([
            {"name": "T", "task_type": "t", "base_success_rate": 0.8, "cognitive_demand": 0.3},
        ])

        d = result.to_dict()
        assert "session_id" in d
        assert "scenarios" in d
        assert isinstance(d["scenarios"], list)

    def test_retry_respects_global_max_attempts(self):
        avatar, aide = self._make_pair()
        config = SessionConfig(
            max_attempts_per_scenario=1,
            max_coaching_per_attempt=5,
        )
        orchestrator = SessionOrchestrator(avatar, aide, config)

        with patch("random.random", return_value=0.99):
            result = orchestrator.run_session([
                {
                    "name": "Cap Attempts",
                    "task_type": "cap_test",
                    "base_success_rate": 0.1,
                    "cognitive_demand": 0.8,
                }
            ])

        sr = result.scenario_results[0]
        assert sr.total_attempts == 1

    def test_failed_retry_is_tracked_for_intervention_effectiveness(self):
        avatar, aide = self._make_pair()
        config = SessionConfig(
            max_attempts_per_scenario=2,
            max_coaching_per_attempt=1,
            check_fusion_readiness=False,
        )
        orchestrator = SessionOrchestrator(avatar, aide, config)

        with patch.object(aide, "track_intervention_effectiveness") as tracker:
            with patch("random.random", return_value=0.99):
                orchestrator.run_session([
                    {
                        "name": "Retry Tracking",
                        "task_type": "retry_tracking",
                        "base_success_rate": 0.1,
                        "cognitive_demand": 0.8,
                    }
                ])

        assert tracker.called
        _, tracked_result = tracker.call_args.args
        assert tracked_result.success is False

    def test_min_attempts_for_success_check_is_configurable(self):
        avatar, aide = self._make_pair()
        config = SessionConfig(
            max_attempts_per_scenario=5,
            max_coaching_per_attempt=0,
            min_attempts_for_success_check=1,
            success_rate_target=0.7,
            check_fusion_readiness=False,
        )
        orchestrator = SessionOrchestrator(avatar, aide, config)

        with patch("random.random", return_value=0.01):
            result = orchestrator.run_session([
                {
                    "name": "Fast Exit",
                    "task_type": "fast_exit",
                    "base_success_rate": 0.9,
                    "cognitive_demand": 0.2,
                }
            ])

        sr = result.scenario_results[0]
        assert sr.total_attempts == 1
