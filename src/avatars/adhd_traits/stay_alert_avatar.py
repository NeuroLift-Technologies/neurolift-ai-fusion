"""
StayAlert Avatar - Sustained Attention Deficit

Embodiment of ADHD sustained attention challenges. This Avatar struggles with
maintaining focus over time, experiences attention drift, and finds it difficult
to stay engaged with tasks requiring prolonged concentration.
"""

from typing import Dict, List, Any
import random
from datetime import timedelta

from ..base_avatar import BaseAvatar, AvatarState


class StayAlertAvatar(BaseAvatar):
    """
    Avatar embodying sustained attention deficit.

    Key characteristics:
    - Difficulty maintaining focus over time
    - Attention drift during long tasks
    - Hyperfocus vulnerability (gets stuck in one aspect)
    - Time blindness while focused
    - Difficulty with task transitions
    """

    def __init__(self, avatar_id: str, trait_config: Dict[str, Any]):
        trait_config["trait_name"] = "StayAlert"
        trait_config["attention_duration"] = trait_config.get("attention_duration", 15)
        trait_config["drift_probability"] = trait_config.get("drift_probability", 0.3)
        trait_config["hyperfocus_tendency"] = trait_config.get("hyperfocus_tendency", 0.2)

        super().__init__(avatar_id, trait_config)

        self.minutes_focused = 0
        self.hyperfocused_on_subtask = False

    def get_adhd_trait_impact(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate sustained attention deficit impact on task performance.

        Returns difficulty modifiers based on task duration and complexity.
        """
        task_duration = task_context.get("expected_duration", timedelta(minutes=10))
        task_complexity = task_context.get("complexity", "medium")
        requires_sustained_focus = task_context.get("requires_sustained_focus", True)

        duration_minutes = task_duration.total_seconds() / 60

        if not requires_sustained_focus:
            return {
                "difficulty_modifier": 1.0,
                "quality_modifier": 0.0,
                "time_modifier": 1.0,
                "cognitive_load_modifier": 0.0,
                "description": "Task doesn't require sustained focus"
            }

        if duration_minutes < 5:
            difficulty_modifier = 1.1
        elif duration_minutes < 15:
            difficulty_modifier = 1.3
        elif duration_minutes < 30:
            difficulty_modifier = 1.6
        else:
            difficulty_modifier = 2.0

        if task_complexity == "high":
            difficulty_modifier *= 1.2

        cognitive_load = min(0.3 + (duration_minutes / 60) * 0.4, 0.8)

        return {
            "difficulty_modifier": difficulty_modifier,
            "quality_modifier": 0.15,
            "time_modifier": 1.2,
            "cognitive_load_modifier": cognitive_load,
            "attention_threshold": self.trait_config["attention_duration"],
            "description": "Sustained attention deficit reduces focus capability"
        }

    def simulate_struggle(self, task_context: Dict[str, Any]) -> List[str]:
        """
        Simulate authentic sustained attention struggle patterns.

        Returns struggle indicators experienced during task attempt.
        """
        struggle_indicators = []
        task_duration = task_context.get("expected_duration", timedelta(minutes=10))
        duration_minutes = task_duration.total_seconds() / 60

        if duration_minutes > self.trait_config["attention_duration"]:
            struggle_indicators.append("attention_drift")

        if random.random() < self.trait_config["drift_probability"]:
            struggle_indicators.append("lost_focus")

        if random.random() < self.trait_config["hyperfocus_tendency"]:
            struggle_indicators.append("hyperfocus_on_subtask")
            self.hyperfocused_on_subtask = True

        if "attention_drift" in struggle_indicators or "lost_focus" in struggle_indicators:
            if random.random() < 0.5:
                struggle_indicators.append("forgot_main_objective")

        if len(struggle_indicators) > 1:
            struggle_indicators.append("increased_frustration")

        if self.cognitive_load > 0.7:
            struggle_indicators.append("overwhelmed")

        return struggle_indicators

    def attempt_task(self, task_context: Dict[str, Any]) -> Any:
        """
        Attempt a task with attention deficit affecting performance.

        Overrides base to add attention-specific dynamics.
        """
        result = super().attempt_task(task_context)

        self.minutes_focused = 0
        self.hyperfocused_on_subtask = False

        if result.success and "hyperfocus_on_subtask" in result.struggle_indicators:
            self.emotional_state = "overwhelmed"

        if not result.success and len(result.struggle_indicators) > 2:
            self.stress_level = min(1.0, self.stress_level + 0.15)

        return result
