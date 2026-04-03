"""
Aide System

Provides expert coaching and support during Avatar struggles. Each Aide
combines PhD-level expertise with real-world feedback plus RRT foundation
for burnout response.
"""

from .base_aide import BaseAide, CoachingAction, CoachingContext, BurnoutRisk
# RRT Foundation module not yet implemented
# from .rrt_foundation import (
#     RRTFoundation,
#     BurnoutDetector,
#     CrisisIntervention,
#     RecoveryProtocols,
# )
from .executive_function_expertise import (
    AttentionCoaching,
    # Additional expertise modules will be imported here as they are implemented
    # ImpulseManagement,
    # WorkingMemoryStrategies,
    # TimeManagement,
    # EmotionalRegulation,
    # FocusTechniques,
    # TaskInitiationSupport,
    # FrustrationManagement,
    # PlanningSupport,
    # TransitionCoaching,
    # SelfAwareness,
)
# Real world feedback module not yet implemented
# from .real_world_feedback import (
#     SuccessStories,
#     FailureAnalysis,
#     FeedbackProcessor,
# )

__all__ = [
    "BaseAide",
    "CoachingAction",
    "CoachingContext",
    "BurnoutRisk",
    # RRT Foundation exports will be added here when implemented
    # "RRTFoundation",
    # "BurnoutDetector",
    # "CrisisIntervention",
    # "RecoveryProtocols",
    "AttentionCoaching",
    # Additional expertise exports will be added here as they are implemented
]
