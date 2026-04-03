"""
TaskKickstart Avatar - Task Initiation Difficulty

Embodiment of ADHD task initiation challenges. This Avatar struggles with
starting tasks despite understanding what needs to be done and being capable
of completing them once started.
"""

from typing import Dict, List, Any
import random
from datetime import timedelta

from ..base_avatar import BaseAvatar


class TaskKickstartAvatar(BaseAvatar):
    """
    Avatar embodying task initiation difficulty.

    Key characteristics:
    - Difficulty starting tasks (even simple ones)
    - Procrastination patterns
    - Task aversion despite capability
    - Internal resistance to initiation
    - Performance improves after successful start
    """

    def __init__(self, avatar_id: str, trait_config: Dict[str, Any]):
        trait_config["trait_name"] = "TaskKickstart"
        trait_config["initiation_difficulty"] = trait_config.get("initiation_difficulty", 0.6)
        trait_config["procrastination_likelihood"] = trait_config.get("procrastination_likelihood", 0.5)
        trait_config["resistance_decay"] = trait_config.get("resistance_decay", 0.1)

        super().__init__(avatar_id, trait_config)

        self.tasks_started = 0
        self.false_starts = 0
        self.last_initiation_difficulty = 0.0

    def get_adhd_trait_impact(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate task initiation difficulty impact.

        Returns difficulty modifiers based on perceived task aversiveness.
        """
        task_type = task_context.get("task_type", "unknown")
        estimated_duration = task_context.get("expected_duration", timedelta(minutes=15))
        aversiveness = task_context.get("aversiveness", 0.5)

        initiation_difficulty = (
            self.trait_config["initiation_difficulty"] +
            (aversiveness * 0.3) +
            (estimated_duration.total_seconds() / 3600 * 0.2)
        )
        initiation_difficulty = min(1.0, initiation_difficulty)
        self.last_initiation_difficulty = initiation_difficulty

        difficulty_modifier = 1.0 + (initiation_difficulty * 0.5)

        quality_modifier = 0.05 if initiation_difficulty > 0.7 else 0.0
        time_modifier = 1.3 if initiation_difficulty > 0.7 else 1.1

        cognitive_load = initiation_difficulty * 0.3

        return {
            "difficulty_modifier": difficulty_modifier,
            "quality_modifier": quality_modifier,
            "time_modifier": time_modifier,
            "cognitive_load_modifier": cognitive_load,
            "initiation_resistance": initiation_difficulty,
            "description": "Task initiation difficulty creates startup resistance"
        }

    def simulate_struggle(self, task_context: Dict[str, Any]) -> List[str]:
        """
        Simulate authentic task initiation struggle patterns.

        Returns struggle indicators experienced during initiation.
        """
        struggle_indicators = []

        if random.random() < self.last_initiation_difficulty:
            struggle_indicators.append("initiation_resistance")

        if random.random() < self.trait_config["procrastination_likelihood"]:
            struggle_indicators.append("procrastination_urge")
            if random.random() < 0.3:
                struggle_indicators.append("false_start")
                self.false_starts += 1

        if "initiation_resistance" in struggle_indicators:
            struggle_indicators.append("internal_resistance")

        if len(struggle_indicators) > 0:
            struggle_indicators.append("reduced_motivation")

        if self.false_starts > 2:
            struggle_indicators.append("frustration_building")

        return struggle_indicators

    def attempt_task(self, task_context: Dict[str, Any]) -> Any:
        """
        Attempt a task with initiation difficulty affecting performance.

        Overrides base to add initiation-specific dynamics.
        """
        result = super().attempt_task(task_context)

        if result.success:
            self.tasks_started += 1
            if "false_start" not in result.struggle_indicators:
                self.false_starts = max(0, self.false_starts - 1)
            else:
                self.emotional_state = "frustrated"

            if len(result.struggle_indicators) == 0 and random.random() < 0.4:
                self.emotional_state = "energized"

        else:
            if "initiation_resistance" in result.struggle_indicators:
                self.emotional_state = "avoidant"
                self.stress_level = min(1.0, self.stress_level + 0.1)

        return result
