"""
StayAlert Aide - Attention Deficit Coach

Specialized coaching for sustained attention challenges. Provides expert strategies
for maintaining focus, managing attention drift, and leveraging hyperfocus.
"""

from typing import Dict, List, Any, Optional
import uuid

from ..base_aide import BaseAide, CoachingContext, CoachingType, InterventionUrgency
from ..expertise.attention_expert import AttentionExpert


class StayAlertAide(BaseAide):
    """
    Aide specializing in attention management coaching.

    Combines attention science expertise with real-world coaching strategies
    to help Avatars build sustained attention capacity.
    """

    def __init__(self, aide_id: str, expertise_config: Dict[str, Any]):
        expertise_config["expertise_area"] = "sustained_attention"
        super().__init__(aide_id, expertise_config)

        self.attention_expert = AttentionExpert()
        self.phd_expertise = self.attention_expert
        self.intervention_patterns = {}

    def get_expertise_strategies(self, context: CoachingContext) -> List[Dict[str, Any]]:
        """
        Get PhD-level expertise strategies for attention management.

        Returns evidence-based strategies from cognitive psychology and neuroscience.
        """
        strategies = []

        struggle_context = {
            "task_type": context.task_context.get("task_type", "general"),
            "estimated_duration_minutes": context.task_context.get("duration_minutes", 25),
            "struggle_indicators": context.current_struggle
        }

        expert_strategies = self.attention_expert.get_attention_strategies(struggle_context)

        for strategy in expert_strategies:
            strategies.append({
                "strategy": strategy["name"],
                "description": strategy["description"],
                "techniques": strategy.get("implementation", strategy.get("techniques", [])),
                "expected_outcomes": [
                    "Improved sustained focus",
                    "Reduced attention drift",
                    "Increased task completion rate"
                ],
                "stress_reduction": 0.2,
                "emotional_boost": 0.15,
                "cognitive_support": 0.3,
                "independence_building": 0.25,
                "effectiveness": strategy.get("effectiveness", 0.7),
                "context_match": self._calculate_context_match(strategy, context)
            })

        return strategies

    def get_real_world_insights(self, context: CoachingContext) -> List[Dict[str, Any]]:
        """
        Get real-world insights from successful ADHD individuals.

        Returns practical wisdom from community experience.
        """
        insights = self.attention_expert.get_real_world_insights()
        real_world_strategies = []

        for insight in insights:
            real_world_strategies.append({
                "strategy": f"Real-World Insight: {insight['insight']}",
                "description": insight["adaptation"],
                "techniques": [insight["adaptation"]],
                "expected_outcomes": [
                    "Practical implementation",
                    "Community-tested effectiveness"
                ],
                "stress_reduction": 0.1,
                "emotional_boost": 0.2,
                "cognitive_support": 0.15,
                "independence_building": 0.3,
                "effectiveness": 0.75,
                "context_match": 0.7
            })

        return real_world_strategies

    def _calculate_context_match(self, strategy: Dict[str, Any], context: CoachingContext) -> float:
        """Calculate how well a strategy matches the current context"""
        match_score = 0.5

        if "lost_focus" in context.current_struggle and "Environmental" in strategy["name"]:
            match_score += 0.25

        if "overwhelmed" in context.current_struggle and "Chunking" in strategy["name"]:
            match_score += 0.25

        if context.cognitive_load > 0.7:
            if "break" in strategy["description"].lower():
                match_score += 0.15

        if context.stress_level > 0.6:
            if any(word in strategy["name"].lower() for word in ["transition", "ritual", "structure"]):
                match_score += 0.15

        return min(1.0, match_score)

    def create_focus_intervention(self, context: CoachingContext) -> Dict[str, Any]:
        """
        Create a specific focus intervention for immediate use.

        Returns actionable coaching with specific techniques.
        """
        capacity = self.attention_expert.assess_attention_capacity({
            "cognitive_load": context.cognitive_load,
            "stress_level": context.stress_level,
            "recent_success_rate": 0.5
        })

        plan = self.attention_expert.generate_attention_plan(
            context.task_context,
            {
                "struggle_indicators": context.current_struggle,
                "cognitive_load": context.cognitive_load,
                "stress_level": context.stress_level
            }
        )

        intervention = {
            "intervention_type": "focus_session",
            "session_structure": plan["session_structure"],
            "strategies": plan["recommended_strategies"],
            "success_indicators": plan["success_indicators"],
            "recovery_actions": plan["recovery_actions"],
            "coaching_points": [
                "Focus on ONE task component at a time",
                "Use timer to create structure",
                "Take breaks before attention drifts completely",
                "Note when focus naturally breaks for pattern analysis"
            ]
        }

        return intervention

    def adapt_strategy_to_context(self, strategy: str, context: CoachingContext) -> Dict[str, Any]:
        """
        Adapt a strategy to the specific Avatar context.

        Returns context-appropriate strategy parameters.
        """
        if "pomodoro" in strategy.lower():
            optimal_duration = int(context.task_context.get("duration_minutes", 25) * 0.6)
            return {
                "work_duration": max(15, min(25, optimal_duration)),
                "break_duration": 5,
                "adaptations": [
                    "Shorter sessions if stress is high",
                    "Longer breaks if cognitive load is high"
                ]
            }

        elif "chunking" in strategy.lower():
            return {
                "chunk_size": "small" if context.cognitive_load > 0.7 else "medium",
                "check_in_frequency": "every chunk" if context.stress_level > 0.6 else "every 2 chunks",
                "adaptations": [
                    "Make chunks very small if overwhelmed",
                    "Celebrate completion of each chunk"
                ]
            }

        elif "environmental" in strategy.lower():
            return {
                "priority_changes": [
                    "Remove primary distraction source",
                    "Add single focus aid (white noise or music)",
                    "Clear immediate visual field"
                ],
                "adaptations": [
                    "Minimal changes if stressed",
                    "Gradual optimization approach"
                ]
            }

        return {}

    def _identify_risk_factors(self, avatar) -> List[str]:
        """Override to add attention-specific risk factors"""
        risk_factors = super()._identify_risk_factors(avatar)

        if hasattr(avatar, 'minutes_focused') and avatar.minutes_focused > 60:
            risk_factors.append("Extended focus without breaks")

        return risk_factors

    def _detect_early_warning_signs(self, avatar) -> List[str]:
        """Override to add attention-specific warning signs"""
        warning_signs = super()._detect_early_warning_signs(avatar)

        if avatar.emotional_state == "overwhelmed":
            warning_signs.append("Cognitive overload from sustained focus")

        return warning_signs
