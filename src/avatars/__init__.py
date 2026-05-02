"""
Avatar System

Simulates authentic ADHD experiences and struggles. Each Avatar embodies
a specific ADHD trait and experiences realistic stress, frustration, and
failure patterns during simulation.
"""

from .base_avatar import BaseAvatar, AvatarState, TaskResult, LearningProgress
from .adhd_traits import (
    AttentionDeficit,
    # Additional traits will be imported here as they are implemented
    # Impulsivity,
    # WorkingMemory,
    # TimeBlindness,
    # EmotionalDysregulation,
    # Hyperfocus,
    # TaskInitiation,
    # FrustrationTolerance,
    # PlanningDeficit,
    # TransitionDifficulty,
    # SelfMonitoring,
    # ImpulseControl,
    # FocusFatigue,
    # EffortPerception,
    # StressSensitivity,
    # SensorySensitivity,
    # SocialChallenges,
    # SensorySeeking,
    # IdentityChallenges,
)

__all__ = [
    "BaseAvatar",
    "AvatarState",
    "TaskResult",
    "LearningProgress",
    "AttentionDeficit",
    # Additional traits will be added here as they are implemented
]
