"""
Attention Coaching Expertise

PhD-level expertise and coaching strategies for sustained attention and focus
management. Combines academic research with real-world success stories to
provide evidence-based coaching interventions.
"""

from typing import Any, Dict, List

from ..base_aide import BaseAide, CoachingContext


class AttentionCoaching(BaseAide):
    """
    Aide specialized in coaching sustained attention and focus management.

    Combines PhD-level research on attention deficit with real-world
    strategies from successful ADHD individuals.
    """

    def __init__(self, aide_id: str, expertise_config: Dict[str, Any]):
        super().__init__(aide_id, expertise_config)

        # Attention-specific expertise
        self.attention_techniques = expertise_config.get("attention_techniques", [])
        self.distraction_management = expertise_config.get("distraction_management", [])
        self.focus_building_strategies = expertise_config.get("focus_building_strategies", [])
        self.mental_endurance_training = expertise_config.get("mental_endurance_training", [])

        # Evidence-based strategies
        self.pomodoro_technique = {
            "strategy": "Pomodoro Technique",
            "description": "Work in 25-minute focused intervals with 5-minute breaks",
            "effectiveness": 0.8,
            "techniques": [
                "Set timer for 25 minutes",
                "Focus solely on the task",
                "Take 5-minute break when timer rings",
                "Repeat cycle 4 times",
                "Take longer 15-30 minute break",
            ],
            "expected_outcomes": [
                "Improved sustained attention",
                "Reduced mental fatigue",
            ],
            "stress_reduction": 0.2,
            "emotional_boost": 0.1,
            "cognitive_support": 0.3,
            "focus_restoration": 0.3,
            "independence_building": 0.2,
        }

        self.mindfulness_attention_training = {
            "strategy": "Mindfulness Attention Training",
            "description": "Mindfulness-based attention training to improve focus",
            "effectiveness": 0.7,
            "techniques": [
                "Notice when attention wanders",
                "Gently redirect attention back to task",
                "Practice non-judgmental awareness",
                "Use breath as anchor point",
                "Gradually extend focus periods",
            ],
            "expected_outcomes": [
                "Better attention awareness",
                "Reduced self-criticism after lapses",
            ],
            "stress_reduction": 0.3,
            "emotional_boost": 0.2,
            "cognitive_support": 0.2,
            "focus_restoration": 0.2,
            "independence_building": 0.3,
        }

        self.environmental_optimization = {
            "strategy": "Environmental Optimization",
            "description": "Optimize environment to minimize distractions",
            "effectiveness": 0.9,
            "techniques": [
                "Remove visual distractions",
                "Use noise-cancelling headphones",
                "Organize workspace for efficiency",
                "Set up dedicated focus space",
                "Eliminate digital distractions",
            ],
            "expected_outcomes": [
                "Significantly reduced distractions",
                "Faster focus achievement",
            ],
            "stress_reduction": 0.4,
            "emotional_boost": 0.2,
            "cognitive_support": 0.5,
            "focus_restoration": 0.4,
            "independence_building": 0.4,
        }

        self.task_chunking = {
            "strategy": "Task Chunking",
            "description": "Break large tasks into smaller, manageable chunks",
            "effectiveness": 0.8,
            "techniques": [
                "Identify the main task",
                "Break into 15-30 minute chunks",
                "Focus on one chunk at a time",
                "Take breaks between chunks",
                "Celebrate completion of each chunk",
            ],
            "expected_outcomes": [
                "Better task completion rates",
                "Increased work satisfaction",
            ],
            "stress_reduction": 0.3,
            "emotional_boost": 0.2,
            "cognitive_support": 0.4,
            "focus_restoration": 0.2,
            "independence_building": 0.3,
        }

        self.attention_anchoring = {
            "strategy": "Attention Anchoring",
            "description": "Use specific techniques to anchor and maintain attention",
            "effectiveness": 0.7,
            "techniques": [
                "Choose an attention anchor (breath, task, object)",
                "Return to anchor when mind wanders",
                "Practice gentle redirection",
                "Build anchor strength over time",
                "Use anchor during challenging moments",
            ],
            "expected_outcomes": [
                "Faster focus recovery",
                "Better overall attention management",
            ],
            "stress_reduction": 0.2,
            "emotional_boost": 0.3,
            "cognitive_support": 0.3,
            "focus_restoration": 0.4,
            "independence_building": 0.4,
        }

    def get_expertise_strategies(self, context: CoachingContext) -> List[Dict[str, Any]]:
        """Get PhD-level expertise strategies for attention coaching."""
        strategies: List[Dict[str, Any]] = []
        issues = self._analyze_attention_issues(context)

        if "sustained_attention" in issues:
            strategies.append(self.pomodoro_technique)
            strategies.append(self.task_chunking)

        if "distraction" in issues:
            strategies.append(self.environmental_optimization)
            strategies.append(self.mindfulness_attention_training)

        if "focus_recovery" in issues:
            strategies.append(self.attention_anchoring)
            strategies.append(self.mindfulness_attention_training)

        if "mental_fatigue" in issues:
            strategies.append(self._get_fatigue_management_strategy())

        strategies.extend(self._get_context_specific_strategies(context))
        return strategies

    def get_real_world_insights(self, context: CoachingContext) -> List[Dict[str, Any]]:
        """Get real-world insights from successful ADHD individuals."""
        return [
            {
                "source": "real_world",
                "strategy": "Adapted Pomodoro for ADHD",
                "description": "Use shorter work periods (15-20 min) with longer breaks (10-15 min)",
                "effectiveness": 0.9,
                "context_match": 0.8,
                "techniques": [
                    "Start with 15-minute work periods",
                    "Take 10-minute active breaks",
                    "Gradually increase work period length",
                    "Adjust based on daily energy levels",
                    "Use physical movement during breaks",
                ],
                "expected_outcomes": [
                    "Improved sustained attention",
                    "Reduced mental fatigue",
                    "Better task completion rates",
                ],
                "stress_reduction": 0.3,
                "emotional_boost": 0.2,
                "cognitive_support": 0.4,
                "focus_restoration": 0.3,
                "independence_building": 0.3,
            },
            {
                "source": "real_world",
                "strategy": "Personalized Focus Environment",
                "description": "Create a highly personalized workspace for attention needs",
                "effectiveness": 0.95,
                "context_match": 0.7,
                "techniques": [
                    "Experiment with different lighting",
                    "Find optimal noise level",
                    "Use fidget tools for restless energy",
                    "Set up visual reminders and cues",
                    "Create ritual for entering focus mode",
                ],
                "expected_outcomes": [
                    "Significantly reduced distractions",
                    "Longer sustained attention periods",
                ],
                "stress_reduction": 0.4,
                "emotional_boost": 0.3,
                "cognitive_support": 0.5,
                "focus_restoration": 0.4,
                "independence_building": 0.4,
            },
            {
                "source": "real_world",
                "strategy": "Gentle Attention Recovery",
                "description": "Non-judgmental techniques to recover focus after lapses",
                "effectiveness": 0.8,
                "context_match": 0.9,
                "techniques": [
                    "Notice lapse without self-criticism",
                    "Take 3 deep breaths to reset",
                    "Use a physical anchor (touch desk, feel feet)",
                    "Whisper the task name to refocus",
                    "Start with easiest part of task",
                ],
                "expected_outcomes": [
                    "Faster focus recovery",
                    "Improved self-compassion",
                ],
                "stress_reduction": 0.5,
                "emotional_boost": 0.4,
                "cognitive_support": 0.3,
                "focus_restoration": 0.5,
                "independence_building": 0.5,
            },
        ]

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _analyze_attention_issues(self, context: CoachingContext) -> List[str]:
        """Analyze attention issues from the observation snapshot."""
        issues: List[str] = []
        obs = context.observation

        # Check active struggles from the observation
        for struggle in obs.active_struggles:
            if "attention_lapse" in struggle:
                issues.append("sustained_attention")
            if "distraction" in struggle:
                issues.append("distraction")
            if "focus_recovery" in struggle:
                issues.append("focus_recovery")
            if "fatigue" in struggle:
                issues.append("mental_fatigue")

        if obs.cognitive_load > 0.8:
            issues.append("cognitive_overload")

        if obs.emotional_state in ("frustrated", "overwhelmed"):
            issues.append("emotional_interference")

        # Default to general strategies if nothing specific detected
        if not issues:
            issues.append("sustained_attention")

        return issues

    def _get_fatigue_management_strategy(self) -> Dict[str, Any]:
        return {
            "strategy": "Mental Fatigue Management",
            "description": "Mental fatigue management and recovery techniques",
            "effectiveness": 0.8,
            "techniques": [
                "Recognize early fatigue signals",
                "Take proactive micro-breaks (2-3 minutes)",
                "Use different types of breaks",
                "Practice energy management",
                "Build mental endurance gradually",
            ],
            "expected_outcomes": [
                "Reduced mental fatigue",
                "Improved sustained performance",
            ],
            "stress_reduction": 0.3,
            "emotional_boost": 0.2,
            "cognitive_support": 0.4,
            "focus_restoration": 0.3,
            "independence_building": 0.2,
        }

    def _get_context_specific_strategies(
        self, context: CoachingContext
    ) -> List[Dict[str, Any]]:
        strategies: List[Dict[str, Any]] = []
        task_type = context.task_context.get("task_type", "unknown")

        if task_type == "repetitive":
            strategies.append({
                "strategy": "Engagement Boosting for Repetitive Tasks",
                "description": "Make repetitive tasks more engaging",
                "techniques": [
                    "Add variety to task execution",
                    "Use gamification elements",
                    "Set mini-goals and rewards",
                    "Change environment periodically",
                ],
                "expected_outcomes": ["Improved engagement", "Better completion rates"],
                "effectiveness": 0.7,
            })
        elif task_type == "complex":
            strategies.append({
                "strategy": "Complex Task Decomposition",
                "description": "Break down complex tasks for better attention",
                "techniques": [
                    "Create detailed task breakdown",
                    "Focus on one component at a time",
                    "Use visual organization tools",
                    "Set clear milestones",
                ],
                "expected_outcomes": ["Reduced overwhelm", "Better focus per component"],
                "effectiveness": 0.8,
            })

        return strategies
