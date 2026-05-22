"""
Tests for AttentionExpert

Covers all public methods of src/aides/expertise/attention_expert.py
and the expertise __init__ re-export.
"""

import pytest
from src.aides.expertise import AttentionExpert  # covers __init__.py
from src.aides.expertise.attention_expert import AttentionExpert as _AttentionExpertDirect


class TestAttentionExpertInit:
    def test_instantiation(self):
        expert = AttentionExpert()
        assert expert.expertise_area == "attention_management"
        assert isinstance(expert.strategies, dict)
        assert isinstance(expert.research_base, dict)

    def test_strategies_populated(self):
        expert = AttentionExpert()
        assert "pomodoro_technique" in expert.strategies
        assert "environmental_design" in expert.strategies
        assert "task_chunking" in expert.strategies
        assert "body_doubling" in expert.strategies
        assert "transition_rituals" in expert.strategies
        assert "external_accountability" in expert.strategies

    def test_research_base_populated(self):
        expert = AttentionExpert()
        assert "attention_restoration" in expert.research_base
        assert "dopamine_optimization" in expert.research_base
        assert "working_memory" in expert.research_base
        assert "hyperfocus" in expert.research_base


class TestGetAttentionStrategies:
    def setup_method(self):
        self.expert = AttentionExpert()

    def test_short_duration_uses_15min_pomodoro(self):
        context = {"estimated_duration_minutes": 10}
        strategies = self.expert.get_attention_strategies(context)
        assert any(s.get("duration_minutes") == 15 for s in strategies)

    def test_medium_duration_uses_25min_pomodoro(self):
        context = {"estimated_duration_minutes": 25}
        strategies = self.expert.get_attention_strategies(context)
        assert any(s.get("duration_minutes") == 25 for s in strategies)

    def test_long_duration_includes_task_chunking(self):
        context = {"estimated_duration_minutes": 60}
        strategies = self.expert.get_attention_strategies(context)
        names = [s.get("name") for s in strategies]
        assert "Task Chunking" in names

    def test_lost_focus_adds_environmental_and_transition(self):
        context = {
            "estimated_duration_minutes": 25,
            "struggle_indicators": ["lost_focus"],
        }
        strategies = self.expert.get_attention_strategies(context)
        names = [s.get("name") for s in strategies]
        assert "Environmental Optimization" in names
        assert "Transition Rituals" in names

    def test_attention_drift_adds_environmental_and_transition(self):
        context = {
            "estimated_duration_minutes": 25,
            "struggle_indicators": ["attention_drift"],
        }
        strategies = self.expert.get_attention_strategies(context)
        names = [s.get("name") for s in strategies]
        assert "Environmental Optimization" in names

    def test_overwhelmed_adds_chunking_and_body_doubling(self):
        context = {
            "estimated_duration_minutes": 25,
            "struggle_indicators": ["overwhelmed"],
        }
        strategies = self.expert.get_attention_strategies(context)
        names = [s.get("name") for s in strategies]
        assert "Task Chunking" in names
        assert "Body Doubling" in names

    def test_hyperfocus_on_subtask_adds_redirection_strategy(self):
        context = {
            "estimated_duration_minutes": 25,
            "struggle_indicators": ["hyperfocus_on_subtask"],
        }
        strategies = self.expert.get_attention_strategies(context)
        names = [s.get("name") for s in strategies]
        assert "Hyperfocus Redirection" in names

    def test_empty_context_returns_list(self):
        strategies = self.expert.get_attention_strategies({})
        assert isinstance(strategies, list)
        assert len(strategies) >= 1

    def test_multiple_struggle_indicators(self):
        context = {
            "estimated_duration_minutes": 25,
            "struggle_indicators": ["lost_focus", "overwhelmed", "hyperfocus_on_subtask"],
        }
        strategies = self.expert.get_attention_strategies(context)
        assert len(strategies) >= 3


class TestAdaptStrategy:
    def setup_method(self):
        self.expert = AttentionExpert()

    def test_adapt_pomodoro_changes_duration(self):
        adapted = self.expert._adapt_strategy("pomodoro_technique", 15, 3)
        assert adapted["duration_minutes"] == 15
        assert adapted["break_minutes"] == 3

    def test_adapt_preserves_other_fields(self):
        adapted = self.expert._adapt_strategy("pomodoro_technique", 20, 5)
        assert "name" in adapted
        assert "description" in adapted

    def test_adapt_does_not_mutate_original(self):
        original_duration = self.expert.strategies["pomodoro_technique"]["duration_minutes"]
        self.expert._adapt_strategy("pomodoro_technique", 10, 2)
        assert self.expert.strategies["pomodoro_technique"]["duration_minutes"] == original_duration


class TestGetRealWorldInsights:
    def setup_method(self):
        self.expert = AttentionExpert()

    def test_returns_list(self):
        insights = self.expert.get_real_world_insights()
        assert isinstance(insights, list)
        assert len(insights) >= 1

    def test_each_insight_has_required_keys(self):
        insights = self.expert.get_real_world_insights()
        for insight in insights:
            assert "insight" in insight
            assert "adaptation" in insight


class TestAssessAttentionCapacity:
    def setup_method(self):
        self.expert = AttentionExpert()

    def test_normal_state(self):
        result = self.expert.assess_attention_capacity({
            "cognitive_load": 0.3,
            "stress_level": 0.2,
            "recent_success_rate": 0.7,
        })
        assert "current_capacity" in result
        assert "optimal_duration_minutes" in result
        assert "recommended_break_interval" in result
        assert result["current_capacity"] > 0

    def test_high_stress_reduces_capacity(self):
        low_stress = self.expert.assess_attention_capacity({"stress_level": 0.1})
        high_stress = self.expert.assess_attention_capacity({"stress_level": 0.9})
        assert high_stress["current_capacity"] < low_stress["current_capacity"]

    def test_high_cognitive_load_triggers_recovery(self):
        result = self.expert.assess_attention_capacity({"cognitive_load": 0.8})
        assert result["recovery_needed"] is True

    def test_high_stress_triggers_recovery(self):
        result = self.expert.assess_attention_capacity({"stress_level": 0.7})
        assert result["recovery_needed"] is True

    def test_low_load_no_recovery(self):
        result = self.expert.assess_attention_capacity({
            "cognitive_load": 0.3,
            "stress_level": 0.2,
        })
        assert result["recovery_needed"] is False

    def test_capacity_floor_is_positive(self):
        result = self.expert.assess_attention_capacity({
            "cognitive_load": 1.0,
            "stress_level": 1.0,
        })
        assert result["current_capacity"] >= 0.1

    def test_empty_state_uses_defaults(self):
        result = self.expert.assess_attention_capacity({})
        assert result["current_capacity"] > 0


class TestGenerateAttentionPlan:
    def setup_method(self):
        self.expert = AttentionExpert()

    def test_returns_plan_structure(self):
        plan = self.expert.generate_attention_plan(
            {"name": "Write report", "task_type": "writing", "duration_minutes": 30},
            {"cognitive_load": 0.4, "stress_level": 0.3, "struggle_indicators": []},
        )
        assert "task" in plan
        assert "recommended_strategies" in plan
        assert "session_structure" in plan
        assert "success_indicators" in plan
        assert "recovery_actions" in plan

    def test_task_name_from_details(self):
        plan = self.expert.generate_attention_plan(
            {"name": "Specific Task"},
            {},
        )
        assert plan["task"] == "Specific Task"

    def test_default_task_name(self):
        plan = self.expert.generate_attention_plan({}, {})
        assert plan["task"] == "Task"

    def test_recovery_actions_present_when_needed(self):
        plan = self.expert.generate_attention_plan(
            {"duration_minutes": 25},
            {"cognitive_load": 0.9, "stress_level": 0.0},
        )
        assert len(plan["recovery_actions"]) > 0

    def test_recovery_actions_empty_when_not_needed(self):
        plan = self.expert.generate_attention_plan(
            {"duration_minutes": 25},
            {"cognitive_load": 0.2, "stress_level": 0.1},
        )
        assert plan["recovery_actions"] == []

    def test_recommended_strategies_capped_at_three(self):
        plan = self.expert.generate_attention_plan(
            {"duration_minutes": 120, "task_type": "complex"},
            {
                "cognitive_load": 0.8,
                "stress_level": 0.7,
                "struggle_indicators": ["lost_focus", "overwhelmed", "hyperfocus_on_subtask"],
            },
        )
        assert len(plan["recommended_strategies"]) <= 3


class TestGenerateRecoveryActions:
    def setup_method(self):
        self.expert = AttentionExpert()

    def test_high_cognitive_load_adds_actions(self):
        actions = self.expert._generate_recovery_actions({"cognitive_load": 0.8})
        assert len(actions) >= 3
        assert any("break" in a.lower() for a in actions)

    def test_high_stress_adds_actions(self):
        actions = self.expert._generate_recovery_actions({"stress_level": 0.7})
        assert len(actions) >= 3

    def test_both_high_adds_more_actions(self):
        both = self.expert._generate_recovery_actions({
            "cognitive_load": 0.8,
            "stress_level": 0.7,
        })
        cog_only = self.expert._generate_recovery_actions({"cognitive_load": 0.8})
        assert len(both) > len(cog_only)

    def test_low_values_returns_empty(self):
        actions = self.expert._generate_recovery_actions({
            "cognitive_load": 0.3,
            "stress_level": 0.2,
        })
        assert actions == []

    def test_empty_state_returns_empty(self):
        actions = self.expert._generate_recovery_actions({})
        assert actions == []
