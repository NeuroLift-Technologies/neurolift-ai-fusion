"""
Core infrastructure for NeuroLift AI Fusion.

Provides the foundational protocols, state machines, and event systems
that all Avatar, Aide, and Advocate components build upon.
"""

from .events import EventBus, Signal, SignalType
from .state_machine import StateMachine, StateTransition
from .protocols import (
    Message,
    MessageType,
    ObservationReport,
    CoachingIntervention,
    InteractionChannel,
    ExperienceMemory,
    ExperienceRecord,
)

__all__ = [
    "EventBus",
    "Signal",
    "SignalType",
    "StateMachine",
    "StateTransition",
    "Message",
    "MessageType",
    "ObservationReport",
    "CoachingIntervention",
    "InteractionChannel",
    "ExperienceMemory",
    "ExperienceRecord",
]
