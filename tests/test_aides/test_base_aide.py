"""Focused tests for BaseAide outcome attribution behavior."""

from datetime import datetime

from src.core.events import EventBus, Signal, SignalType
from src.core.protocols import ObservationReport
from src.avatars.base_avatar import BaseAvatar, TaskResult
from src.aides.base_aide import BaseAide


class _TestAvatar(BaseAvatar):
    def get_adhd_trait_impact(self, task_context):
        return {
            "difficulty_modifier": 1.0,
            "quality_modifier": 0.0,
            "time_modifier": 1.0,
            "cognitive_load_modifier": 0.0,
        }

    def simulate_struggle(self, task_context):
        return []


class _TestAide(BaseAide):
    def get_expertise_strategies(self, context):
        return [{
            "strategy": "Structured reset",
            "techniques": ["pause", "reframe"],
            "effectiveness": 0.8,
            "stress_reduction": 0.2,
            "focus_restoration": 0.2,
        }]

    def get_real_world_insights(self, context):
        return []


class TestBaseAideOutcomeAttribution:
    def _make_pair(self):
        bus = EventBus()
        avatar = _TestAvatar("avatar_aide_test", {"trait_name": "attention"}, event_bus=bus)
        aide = _TestAide("aide_test", {"expertise_area": "attention"}, event_bus=bus)
        aide.bind_to_avatar(avatar)
        return avatar, aide

    def _task_completed_signal(self, avatar_id: str) -> Signal:
        return Signal(
            signal_type=SignalType.AVATAR_TASK_COMPLETED,
            source_id=avatar_id,
            source_type="avatar",
            data={"timestamp": datetime.now().isoformat()},
        )

    def test_task_completed_does_not_double_count_explicitly_tracked_intervention(self):
        avatar, aide = self._make_pair()
        action = aide._deliver_coaching(
            ObservationReport(avatar_id=avatar.avatar_id, stress_level=0.9),
            {"task_type": "focus"},
        )
        assert action is not None

        aide.track_intervention_effectiveness(
            action,
            TaskResult(
                success=False,
                completion_time=None,
                quality_score=0.0,
                struggle_indicators=["attention_lapse"],
                aide_interventions=[],
                emotional_state="frustrated",
                cognitive_load=0.8,
            ),
        )

        aide._on_avatar_task_completed(self._task_completed_signal(avatar.avatar_id))
        summary = aide.get_strategy_effectiveness_summary()
        assert summary[action.strategy]["times_used"] == 1

    def test_task_completed_credits_pending_intervention_only_once(self):
        avatar, aide = self._make_pair()
        action = aide._deliver_coaching(
            ObservationReport(avatar_id=avatar.avatar_id, stress_level=0.9),
            {"task_type": "focus"},
        )
        assert action is not None

        signal = self._task_completed_signal(avatar.avatar_id)
        aide._on_avatar_task_completed(signal)
        aide._on_avatar_task_completed(signal)

        summary = aide.get_strategy_effectiveness_summary()
        assert summary[action.strategy]["times_used"] == 1
        assert summary[action.strategy]["effectiveness"] == 1.0
