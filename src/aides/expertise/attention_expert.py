"""
Attention Expertise Module

PhD-level expertise on sustained attention and attention management for ADHD.
Provides evidence-based strategies for improving focus and managing attention drift.
"""

from typing import Dict, List, Any, Optional


class AttentionExpert:
    """
    Expert in attention management and sustained focus strategies.

    Combines research from cognitive psychology, neuroscience, and behavioral interventions
    to provide evidence-based coaching for attention-related challenges.
    """

    def __init__(self):
        self.expertise_area = "attention_management"
        self.strategies = self._initialize_strategies()
        self.research_base = self._initialize_research()

    def _initialize_strategies(self) -> Dict[str, Dict[str, Any]]:
        """Initialize evidence-based attention strategies"""
        return {
            "pomodoro_technique": {
                "name": "Pomodoro Technique",
                "description": "Time-boxed work sessions with breaks",
                "duration_minutes": 25,
                "break_minutes": 5,
                "long_break_after": 4,
                "effectiveness": 0.8,
                "implementation": ["Set timer for 25 minutes", "Work without interruption", "Take 5-minute break"]
            },
            "environmental_design": {
                "name": "Environmental Optimization",
                "description": "Reduce distractions and optimize workspace",
                "effectiveness": 0.75,
                "techniques": [
                    "Remove visual distractions",
                    "Minimize auditory stimuli",
                    "Organize workspace",
                    "Use white noise if helpful"
                ]
            },
            "task_chunking": {
                "name": "Task Chunking",
                "description": "Break large tasks into smaller, manageable pieces",
                "effectiveness": 0.85,
                "implementation": [
                    "Identify subtasks",
                    "Order by dependency",
                    "Estimate time for each",
                    "Complete one at a time"
                ]
            },
            "body_doubling": {
                "name": "Body Doubling",
                "description": "Work alongside another person for accountability",
                "effectiveness": 0.7,
                "implementation": ["Work with partner", "Check in periodically", "Share progress"]
            },
            "transition_rituals": {
                "name": "Transition Rituals",
                "description": "Create consistent routines to maintain focus through transitions",
                "effectiveness": 0.72,
                "rituals": [
                    "Brief stretch",
                    "Mental reset",
                    "Review next task",
                    "Start within 1 minute"
                ]
            },
            "external_accountability": {
                "name": "External Accountability",
                "description": "Use external structures to maintain focus",
                "effectiveness": 0.78,
                "methods": ["Accountability partner", "Public commitment", "Progress tracking"]
            }
        }

    def _initialize_research(self) -> Dict[str, Any]:
        """Initialize research-based findings"""
        return {
            "attention_restoration": {
                "finding": "Nature exposure restores attention capacity",
                "source": "Attention Restoration Theory (Kaplan & Kaplan)",
                "application": "Short outdoor breaks improve sustained attention"
            },
            "dopamine_optimization": {
                "finding": "ADHD involves dopamine regulation differences",
                "source": "Neurobiological Research",
                "application": "Use stimulating but productive activities to optimize dopamine"
            },
            "working_memory": {
                "finding": "External aids reduce working memory load",
                "source": "Cognitive Psychology Research",
                "application": "Use written reminders, lists, and external organization"
            },
            "hyperfocus": {
                "finding": "ADHD individuals can achieve hyperfocus on interesting tasks",
                "source": "Clinical ADHD Research",
                "application": "Leverage hyperfocus capacity for important tasks"
            }
        }

    def get_attention_strategies(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get appropriate attention strategies for the current context"""
        task_type = context.get("task_type", "general")
        duration_minutes = context.get("estimated_duration_minutes", 25)
        struggle_indicators = context.get("struggle_indicators", [])

        strategies = []

        if duration_minutes <= 15:
            strategies.append(self._adapt_strategy("pomodoro_technique", 15, 5))
        elif duration_minutes <= 30:
            strategies.append(self._adapt_strategy("pomodoro_technique", 25, 5))
        else:
            strategies.append(self._adapt_strategy("pomodoro_technique", 25, 5))
            strategies.append(self.strategies["task_chunking"])

        if "lost_focus" in struggle_indicators or "attention_drift" in struggle_indicators:
            strategies.append(self.strategies["environmental_design"])
            strategies.append(self.strategies["transition_rituals"])

        if "overwhelmed" in struggle_indicators:
            strategies.append(self.strategies["task_chunking"])
            strategies.append(self.strategies["body_doubling"])

        if "hyperfocus_on_subtask" in struggle_indicators:
            strategies.append({
                "name": "Hyperfocus Redirection",
                "description": "Channel hyperfocus toward main objective",
                "techniques": [
                    "Identify hyperfocus trigger",
                    "Redirect to main task",
                    "Use hyperfocus as reward after primary task"
                ],
                "effectiveness": 0.8
            })

        return strategies

    def _adapt_strategy(self, strategy_name: str, duration: int, break_duration: int) -> Dict[str, Any]:
        """Adapt a strategy for specific timing needs"""
        strategy = self.strategies[strategy_name].copy()
        strategy["duration_minutes"] = duration
        strategy["break_minutes"] = break_duration
        return strategy

    def get_real_world_insights(self) -> List[Dict[str, Any]]:
        """Get real-world insights from successful ADHD individuals"""
        return [
            {
                "insight": "Music without lyrics helps focus for some, complete silence for others",
                "adaptation": "Experiment to find optimal auditory environment"
            },
            {
                "insight": "Standing or moving while working improves focus",
                "adaptation": "Try treadmill desk or standing desk setup"
            },
            {
                "insight": "Starting is harder than continuing",
                "adaptation": "Use lowest-friction method to begin task"
            },
            {
                "insight": "External deadlines create needed urgency",
                "adaptation": "Create artificial deadlines or accountability structures"
            },
            {
                "insight": "Frequent small wins build motivation",
                "adaptation": "Break tasks into checkpoint-based structure"
            },
            {
                "insight": "Interest level dramatically affects focus ability",
                "adaptation": "Find genuine interest angle or connect to values"
            }
        ]

    def assess_attention_capacity(self, avatar_state: Dict[str, Any]) -> Dict[str, Any]:
        """Assess current attention capacity and limitations"""
        cognitive_load = avatar_state.get("cognitive_load", 0.5)
        stress_level = avatar_state.get("stress_level", 0.0)
        recent_successes = avatar_state.get("recent_success_rate", 0.5)

        capacity = 1.0 - (cognitive_load * 0.4 + stress_level * 0.3)
        capacity = max(0.1, capacity)

        return {
            "current_capacity": capacity,
            "optimal_duration_minutes": int(25 * capacity),
            "recommended_break_interval": max(15, int(25 * capacity * 0.8)),
            "stress_impact": stress_level,
            "cognitive_load_impact": cognitive_load,
            "recovery_needed": cognitive_load > 0.7 or stress_level > 0.6
        }

    def generate_attention_plan(self, task_details: Dict[str, Any],
                               avatar_state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a personalized attention management plan"""
        strategies = self.get_attention_strategies({
            "task_type": task_details.get("task_type", "general"),
            "estimated_duration_minutes": task_details.get("duration_minutes", 25),
            "struggle_indicators": avatar_state.get("struggle_indicators", [])
        })

        capacity = self.assess_attention_capacity(avatar_state)

        return {
            "task": task_details.get("name", "Task"),
            "recommended_strategies": strategies[:3],
            "session_structure": {
                "work_duration_minutes": capacity["optimal_duration_minutes"],
                "break_duration_minutes": capacity["recommended_break_interval"],
                "total_estimated_time_minutes": task_details.get("duration_minutes", 25) * 1.3
            },
            "success_indicators": [
                "No attention drift during work sessions",
                "Completed all task components",
                "Maintained positive emotional state"
            ],
            "recovery_actions": self._generate_recovery_actions(avatar_state) if capacity["recovery_needed"] else []
        }

    def _generate_recovery_actions(self, avatar_state: Dict[str, Any]) -> List[str]:
        """Generate recovery actions for stressed avatars"""
        actions = []

        if avatar_state.get("cognitive_load", 0) > 0.7:
            actions.append("Take extended break (10+ minutes)")
            actions.append("Change environment or activity")
            actions.append("Practice brief relaxation")

        if avatar_state.get("stress_level", 0) > 0.6:
            actions.append("Stress reduction exercise")
            actions.append("Talk through challenges")
            actions.append("Reduce task complexity")

        return actions
