"""
Base Scenario

Defines the structure of a training scenario — a sequence of tasks
and environmental conditions that an Avatar must navigate.

Scenarios provide the *context* in which experiential learning happens:
workplace meetings, personal deadlines, social interactions, etc.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid


class ScenarioPhase(Enum):
    """Phases within a scenario."""
    INTRODUCTION = auto()
    BUILDUP = auto()
    CHALLENGE = auto()
    CLIMAX = auto()
    RESOLUTION = auto()


@dataclass
class ScenarioStep:
    """One step within a scenario."""
    step_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    phase: ScenarioPhase = ScenarioPhase.CHALLENGE
    task_context: Dict[str, Any] = field(default_factory=dict)
    npc_interactions: List[Dict[str, Any]] = field(default_factory=list)
    environmental_factors: Dict[str, Any] = field(default_factory=dict)
    duration_minutes: float = 10.0
    difficulty_modifier: float = 1.0


@dataclass
class ScenarioOutcome:
    """Outcome of a completed scenario."""
    scenario_id: str = ""
    scenario_name: str = ""
    steps_completed: int = 0
    total_steps: int = 0
    success: bool = False
    lessons_learned: List[str] = field(default_factory=list)
    consequences: List[Dict[str, Any]] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "scenario_name": self.scenario_name,
            "steps_completed": self.steps_completed,
            "total_steps": self.total_steps,
            "success": self.success,
            "lessons_learned": self.lessons_learned,
            "consequences": self.consequences,
            "timestamp": self.timestamp.isoformat(),
        }


class BaseScenario(ABC):
    """
    Base class for training scenarios.

    A scenario defines:
    - A sequence of steps with increasing challenge
    - Environmental context (workplace, home, social)
    - NPC interactions that create realistic social dynamics
    - Consequences that make outcomes feel meaningful
    """

    def __init__(
        self,
        scenario_id: Optional[str] = None,
        name: str = "Unnamed Scenario",
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.scenario_id = scenario_id or str(uuid.uuid4())
        self.name = name
        self.config = config or {}

        self.steps: List[ScenarioStep] = []
        self.current_step_index: int = 0
        self.completed: bool = False

        # Build steps from subclass
        self._build_steps()

    @abstractmethod
    def _build_steps(self) -> None:
        """Populate self.steps with the scenario's sequence."""

    @abstractmethod
    def evaluate_step_outcome(
        self, step: ScenarioStep, task_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate the outcome of a completed step.

        Returns consequences and narrative progression.
        """

    def get_current_step(self) -> Optional[ScenarioStep]:
        """Get the current step, or None if scenario is complete."""
        if self.current_step_index >= len(self.steps):
            return None
        return self.steps[self.current_step_index]

    def advance(self) -> Optional[ScenarioStep]:
        """Move to the next step. Returns the new current step or None."""
        self.current_step_index += 1
        if self.current_step_index >= len(self.steps):
            self.completed = True
            return None
        return self.steps[self.current_step_index]

    def get_task_context(self) -> Dict[str, Any]:
        """Get a task_context dict suitable for Avatar.attempt_task()."""
        step = self.get_current_step()
        if step is None:
            return {}

        ctx = dict(step.task_context)
        ctx.setdefault("name", step.name)
        ctx.setdefault("scenario_id", self.scenario_id)
        ctx.setdefault("scenario_name", self.name)
        ctx.setdefault("phase", step.phase.name)
        ctx.setdefault("difficulty_modifier", step.difficulty_modifier)
        ctx["environmental_factors"] = step.environmental_factors
        return ctx

    def get_outcome(self) -> ScenarioOutcome:
        """Build the final ScenarioOutcome."""
        return ScenarioOutcome(
            scenario_id=self.scenario_id,
            scenario_name=self.name,
            steps_completed=self.current_step_index,
            total_steps=len(self.steps),
            success=self.completed,
        )

    @property
    def progress(self) -> float:
        """Fraction of steps completed (0.0 – 1.0)."""
        if not self.steps:
            return 1.0
        return self.current_step_index / len(self.steps)
