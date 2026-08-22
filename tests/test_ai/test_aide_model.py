"""Integration tests: make BaseAide model-aware (gated, default OFF)."""

import pytest

from src.ai import RuleFallbackBackend
from src.avatars.base_avatar import BaseAvatar
from src.aides.base_aide import (
    BaseAide,
    CoachingAction,
    CoachingContext,
    InterventionUrgency,
)


class _TestAvatar(BaseAvatar):
    def get_adhd_trait_impact(self, task_context):
        return {
            "difficulty_modifier": 1.0,
            "struggle_indicators": [],
            "quality_modifier": 0.0,
            "time_modifier": 1.0,
            "cognitive_load_modifier": 0.0,
        }

    def simulate_struggle(self, task_context):
        return []


class _TestAide(BaseAide):
    def get_expertise_strategies(self, context):
        return []

    def get_real_world_insights(self, context):
        return []


class _FailingBackend:
    """Minimal backend whose predict always raises (to test fallback)."""

    model_id = "failing"
    model_version = "0.0.1"
    kind = "aide"

    def predict(self, inputs):
        raise RuntimeError("simulated model failure")

    def update(self, records):
        return None


@pytest.mark.ai
class TestAideModelAwareness:
    def _make_pair(self):
        avatar = _TestAvatar("aid_avatar", {"trait_name": "t"})
        aide = _TestAide("aid_test", {"expertise_area": "attention"})
        aide.bind_to_avatar(avatar)
        return avatar, aide

    def test_default_rule_based_path(self):
        avatar, aide = self._make_pair()
        ctx = CoachingContext(
            avatar_id=avatar.avatar_id,
            observation=avatar.get_observation_snapshot(),
            task_context={"task_type": "focus"},
        )
        assert aide.use_model is False
        result = aide.provide_coaching(ctx)
        # No strategies -> None is the valid rule-based outcome.
        assert result is None or isinstance(result, CoachingAction)

    def test_model_path_used_when_bound(self):
        avatar, aide = self._make_pair()
        aide.bind_model(RuleFallbackBackend(kind="aide"))
        assert aide.use_model is True

        ctx = CoachingContext(
            avatar_id=avatar.avatar_id,
            observation=avatar.get_observation_snapshot(),
            task_context={"task_type": "focus"},
        )
        action = aide.provide_coaching(ctx)
        assert isinstance(action, CoachingAction)
        assert action.urgency == InterventionUrgency.LOW
        assert "fallback" in action.strategy

    def test_model_predict_failure_falls_back(self):
        avatar, aide = self._make_pair()
        aide.bind_model(_FailingBackend())
        ctx = CoachingContext(
            avatar_id=avatar.avatar_id,
            observation=avatar.get_observation_snapshot(),
            task_context={"task_type": "focus"},
        )
        # Must not raise; rule-based path proceeds.
        result = aide.provide_coaching(ctx)
        assert result is None or isinstance(result, CoachingAction)

    def test_unbind_model_resets_flag(self):
        avatar, aide = self._make_pair()
        aide.bind_model(RuleFallbackBackend(kind="aide"))
        assert aide.use_model is True
        aide.unbind_model()
        assert aide.use_model is False
        assert aide.model is None
