"""Integration tests: make BaseAvatar model-aware (gated, default OFF)."""

import pytest

from src.ai import RuleFallbackBackend
from src.avatars.base_avatar import BaseAvatar, TaskResult


class TestAvatar(BaseAvatar):
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


class _FailingBackend:
    """Minimal backend whose predict always raises (to test fallback)."""

    model_id = "failing"
    model_version = "0.0.1"
    kind = "avatar"

    def predict(self, inputs):
        raise RuntimeError("simulated model failure")

    def update(self, records):
        return None


@pytest.mark.ai
class TestAvatarModelAwareness:
    def test_default_rule_based_behavior(self):
        avatar = TestAvatar("av_default", {"trait_name": "t"})
        assert avatar.use_model is False
        assert avatar.model is None
        result = avatar.attempt_task({"task_type": "focus", "base_success_rate": 0.8})
        assert isinstance(result, TaskResult)
        assert isinstance(result.struggle_indicators, list)

    def test_bind_model_enables_model_path(self):
        avatar = TestAvatar("av_bound", {"trait_name": "t"})
        backend = RuleFallbackBackend(kind="avatar")
        avatar.bind_model(backend)
        assert avatar.use_model is True
        assert avatar.model is backend

        result = avatar.attempt_task({"task_type": "focus", "base_success_rate": 0.8})
        assert isinstance(result, TaskResult)
        assert isinstance(result.struggle_indicators, list)

    def test_model_predict_failure_falls_back(self):
        avatar = TestAvatar("av_fail", {"trait_name": "t"})
        avatar.bind_model(_FailingBackend())
        # Must not raise; rule-based path is used.
        result = avatar.attempt_task({"task_type": "focus", "base_success_rate": 0.8})
        assert isinstance(result, TaskResult)
        assert avatar.use_model is True  # still bound, just degraded

    def test_unbind_model_resets_flag(self):
        avatar = TestAvatar("av_unbind", {"trait_name": "t"})
        avatar.bind_model(RuleFallbackBackend(kind="avatar"))
        assert avatar.use_model is True
        avatar.unbind_model()
        assert avatar.use_model is False
        assert avatar.model is None

        # After unbind, rule-based path works unaffected.
        result = avatar.attempt_task({"task_type": "focus", "base_success_rate": 0.8})
        assert isinstance(result, TaskResult)
