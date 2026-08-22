"""
Rule-Fallback Backend

Provider-agnostic, dependency-free baseline that returns neutral
predictions for both Avatar and Aide roles. Used when no trainable
model is available.
"""

from typing import Any, Dict, List

from ..protocol import ModelAdapter, AVATAR_MODEL_KIND, AIDE_MODEL_KIND


class RuleFallbackBackend(ModelAdapter):
    """Deterministic neutral baseline backend (no ML dependency)."""

    model_id: str = "rule_fallback"
    model_version: str = "0.1.0"

    def __init__(self, kind: str = "generic") -> None:
        self.kind = kind

    def predict(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        role = inputs.get("role", "generic")
        if role == AVATAR_MODEL_KIND:
            return {
                "trait_impact": {
                    "difficulty_modifier": 1.0,
                    "quality_modifier": 0.0,
                    "time_modifier": 1.0,
                    "cognitive_load_modifier": 0.0,
                },
                "struggle_indicators": [],
                "emotional_state": inputs.get("current_emotional_state", "neutral"),
                "cognitive_load": float(inputs.get("current_cognitive_load", 0.0)),
                "stress_level": float(inputs.get("current_stress_level", 0.0)),
            }
        if role == AIDE_MODEL_KIND:
            return {
                "strategy": "Rule-based fallback (no model)",
                "specific_techniques": [],
                "urgency": "low",
                "coaching_type": "preventive",
                "stress_reduction": 0.0,
                "emotional_boost": 0.0,
                "cognitive_support": 0.0,
                "focus_restoration": 0.0,
                "independence_building": 0.0,
            }
        # Unknown/generic role: safe neutral combination.
        return {
            "trait_impact": {
                "difficulty_modifier": 1.0,
                "quality_modifier": 0.0,
                "time_modifier": 1.0,
                "cognitive_load_modifier": 0.0,
            },
            "struggle_indicators": [],
            "emotional_state": inputs.get("current_emotional_state", "neutral"),
            "cognitive_load": float(inputs.get("current_cognitive_load", 0.0)),
            "stress_level": float(inputs.get("current_stress_level", 0.0)),
            "strategy": "Rule-based fallback (no model)",
            "specific_techniques": [],
            "urgency": "low",
            "coaching_type": "preventive",
            "stress_reduction": 0.0,
            "emotional_boost": 0.0,
            "cognitive_support": 0.0,
            "focus_restoration": 0.0,
            "independence_building": 0.0,
        }

    def update(self, records: List[Any]) -> None:
        """No-op: rule fallback is not trainable."""
        return None
