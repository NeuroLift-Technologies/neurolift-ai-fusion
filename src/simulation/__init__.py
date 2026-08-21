"""
Simulation Environment

Creates realistic scenarios where Avatars experience authentic ADHD
struggles while Aides provide real-time coaching.
"""

from .session_orchestrator import SessionOrchestrator, SessionConfig, SessionResult
from .environment import (
    WorldEngine,
    WorldEngineConfig,
    SimulationState,
    EventType,
    TimeManager,
    RelationshipManager,
    RelationshipComponent,
    FurnitureType,
    FurnitureComponent,
    RoomComponent,
    NeedsComponent,
    NeedType,
    ScheduleComponent,
    AgentInterface,
    PerceptionMap,
    Registry,
    Entity,
    Component,
    Position,
    Interactable,
    AgentController,
)

# Placeholder for SimulationEnvironment - define it here for now
class SimulationEnvironment(WorldEngine):
    """Alias for WorldEngine to maintain API compatibility"""
    pass

__all__ = [
    "SessionOrchestrator",
    "SessionConfig",
    "SessionResult",
    "SimulationEnvironment",
    "WorldEngine",
    "WorldEngineConfig",
    "SimulationState",
    "EventType",
    "TimeManager",
    "RelationshipManager",
    "RelationshipComponent",
    "FurnitureType",
    "FurnitureComponent",
    "RoomComponent",
    "NeedsComponent",
    "NeedType",
    "ScheduleComponent",
    "AgentInterface",
    "PerceptionMap",
    "Registry",
    "Entity",
    "Component",
    "Position",
    "Interactable",
    "AgentController",
]
