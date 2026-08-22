"""Tests for the rule-fallback adapter contract."""

import pytest

from src.ai import RuleFallbackBackend


class TestRuleFallback:
    def test_avatar_contract(self):
        backend = RuleFallbackBackend(kind="avatar")
        out = backend.predict(
            {
                "role": "avatar",
                "avatar_id": "a1",
                "task_context": {},
                "current_emotional_state": "neutral",
                "current_cognitive_load": 0.2,
                "current_stress_level": 0.1,
            }
        )
        assert out["trait_impact"]["difficulty_modifier"] == 1.0
        assert out["emotional_state"] == "neutral"
        assert set(out.keys()) == {
            "trait_impact",
            "struggle_indicators",
            "emotional_state",
            "cognitive_load",
            "stress_level",
        }

    def test_aide_contract(self):
        backend = RuleFallbackBackend(kind="aide")
        out = backend.predict({"role": "aide", "aide_id": "x"})
        assert out["urgency"] == "low"
        assert set(out.keys()) == {
            "strategy",
            "specific_techniques",
            "urgency",
            "coaching_type",
            "stress_reduction",
            "emotional_boost",
            "cognitive_support",
            "focus_restoration",
            "independence_building",
        }

    def test_generic_role_returns_combined(self):
        backend = RuleFallbackBackend()
        out = backend.predict({})
        assert "trait_impact" in out
        assert "urgency" in out
