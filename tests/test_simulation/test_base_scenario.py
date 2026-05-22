"""
Tests for BaseScenario, ScenarioStep, ScenarioOutcome, and ScenarioPhase.

Covers src/simulation/scenarios/base_scenario.py and the scenarios __init__
re-export.  Uses a minimal concrete subclass to exercise the abstract base.
"""

import pytest
from src.simulation.scenarios import (  # covers __init__.py
    BaseScenario,
    ScenarioPhase,
    ScenarioStep,
    ScenarioOutcome,
)
from src.simulation.scenarios.base_scenario import BaseScenario as _BaseScenarioDirect


# ---------------------------------------------------------------------------
# Concrete subclass for testing
# ---------------------------------------------------------------------------

class _TestScenario(BaseScenario):
    """Two-step scenario used in all tests."""

    def _build_steps(self) -> None:
        self.steps = [
            ScenarioStep(name="step1", description="First step"),
            ScenarioStep(name="step2", description="Second step"),
        ]

    def evaluate_step_outcome(self, step: ScenarioStep, task_result: dict) -> dict:
        return {"passed": True, "step_name": step.name}


class _EmptyScenario(BaseScenario):
    """Scenario with no steps — tests edge cases."""

    def _build_steps(self) -> None:
        self.steps = []

    def evaluate_step_outcome(self, step: ScenarioStep, task_result: dict) -> dict:
        return {}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestBaseScenarioInit:
    def test_default_construction(self):
        s = _TestScenario()
        assert s.name == "Unnamed Scenario"
        assert s.config == {}
        assert s.current_step_index == 0
        assert s.completed is False
        assert len(s.steps) == 2

    def test_custom_id_and_name(self):
        s = _TestScenario(scenario_id="sc-001", name="My Scenario")
        assert s.scenario_id == "sc-001"
        assert s.name == "My Scenario"

    def test_auto_generated_scenario_id(self):
        s1 = _TestScenario()
        s2 = _TestScenario()
        assert s1.scenario_id != s2.scenario_id

    def test_config_passed_through(self):
        s = _TestScenario(config={"difficulty": "hard"})
        assert s.config["difficulty"] == "hard"


class TestGetCurrentStep:
    def test_returns_first_step_initially(self):
        s = _TestScenario()
        step = s.get_current_step()
        assert step is not None
        assert step.name == "step1"

    def test_returns_none_when_no_steps(self):
        s = _EmptyScenario()
        assert s.get_current_step() is None

    def test_returns_none_after_completion(self):
        s = _TestScenario()
        s.advance()
        s.advance()  # past last step
        assert s.get_current_step() is None


class TestAdvance:
    def test_advance_moves_to_next_step(self):
        s = _TestScenario()
        next_step = s.advance()
        assert next_step is not None
        assert next_step.name == "step2"

    def test_advance_past_last_step_returns_none(self):
        s = _TestScenario()
        s.advance()          # to step2
        result = s.advance() # past last
        assert result is None

    def test_advance_past_last_step_marks_completed(self):
        s = _TestScenario()
        s.advance()
        s.advance()
        assert s.completed is True

    def test_advance_does_not_complete_early(self):
        s = _TestScenario()
        s.advance()  # still one step left
        assert s.completed is False


class TestGetTaskContext:
    def test_returns_dict_with_defaults(self):
        s = _TestScenario()
        ctx = s.get_task_context()
        assert ctx["name"] == "step1"
        assert ctx["scenario_id"] == s.scenario_id
        assert ctx["scenario_name"] == s.name
        assert "phase" in ctx
        assert "difficulty_modifier" in ctx
        assert "environmental_factors" in ctx

    def test_returns_empty_dict_when_no_current_step(self):
        s = _EmptyScenario()
        ctx = s.get_task_context()
        assert ctx == {}

    def test_task_context_step_fields_merged(self):
        s = _TestScenario()
        step = s.get_current_step()
        step.task_context["custom_key"] = "custom_value"
        ctx = s.get_task_context()
        assert ctx["custom_key"] == "custom_value"


class TestGetOutcome:
    def test_outcome_before_completion(self):
        s = _TestScenario()
        outcome = s.get_outcome()
        assert outcome.scenario_id == s.scenario_id
        assert outcome.scenario_name == s.name
        assert outcome.steps_completed == 0
        assert outcome.total_steps == 2
        assert outcome.success is False

    def test_outcome_after_completion(self):
        s = _TestScenario()
        s.advance()
        s.advance()
        outcome = s.get_outcome()
        assert outcome.success is True
        assert outcome.steps_completed == 2

    def test_outcome_mid_scenario(self):
        s = _TestScenario()
        s.advance()
        outcome = s.get_outcome()
        assert outcome.steps_completed == 1
        assert outcome.success is False


class TestProgress:
    def test_progress_starts_at_zero(self):
        s = _TestScenario()
        assert s.progress == pytest.approx(0.0)

    def test_progress_after_one_advance(self):
        s = _TestScenario()
        s.advance()
        assert s.progress == pytest.approx(0.5)

    def test_progress_after_completion(self):
        s = _TestScenario()
        s.advance()
        s.advance()
        assert s.progress == pytest.approx(1.0)

    def test_empty_scenario_progress_is_one(self):
        s = _EmptyScenario()
        assert s.progress == pytest.approx(1.0)


class TestScenarioStep:
    def test_default_step(self):
        step = ScenarioStep()
        assert step.name == ""
        assert step.phase == ScenarioPhase.CHALLENGE
        assert step.duration_minutes == pytest.approx(10.0)
        assert step.difficulty_modifier == pytest.approx(1.0)
        assert step.task_context == {}
        assert step.npc_interactions == []
        assert step.environmental_factors == {}

    def test_custom_step(self):
        step = ScenarioStep(
            name="Standup",
            description="Daily standup",
            phase=ScenarioPhase.BUILDUP,
            duration_minutes=5.0,
            difficulty_modifier=0.8,
        )
        assert step.name == "Standup"
        assert step.phase == ScenarioPhase.BUILDUP
        assert step.duration_minutes == pytest.approx(5.0)

    def test_auto_step_id_unique(self):
        s1 = ScenarioStep()
        s2 = ScenarioStep()
        assert s1.step_id != s2.step_id


class TestScenarioOutcome:
    def test_default_outcome(self):
        outcome = ScenarioOutcome()
        assert outcome.scenario_id == ""
        assert outcome.success is False
        assert outcome.lessons_learned == []
        assert outcome.consequences == []

    def test_to_dict_keys(self):
        outcome = ScenarioOutcome(
            scenario_id="s-1",
            scenario_name="Test",
            steps_completed=3,
            total_steps=5,
            success=True,
            lessons_learned=["Stay focused"],
            consequences=[{"type": "missed_deadline"}],
        )
        d = outcome.to_dict()
        assert d["scenario_id"] == "s-1"
        assert d["scenario_name"] == "Test"
        assert d["steps_completed"] == 3
        assert d["total_steps"] == 5
        assert d["success"] is True
        assert d["lessons_learned"] == ["Stay focused"]
        assert d["consequences"] == [{"type": "missed_deadline"}]
        assert "timestamp" in d
        assert isinstance(d["timestamp"], str)


class TestEvaluateStepOutcome:
    def test_concrete_evaluate_called(self):
        s = _TestScenario()
        step = s.get_current_step()
        result = s.evaluate_step_outcome(step, {"completed": True})
        assert result["passed"] is True
        assert result["step_name"] == "step1"
