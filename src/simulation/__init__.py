"""
Simulation Environment

Creates realistic scenarios where Avatars experience authentic ADHD
struggles while Aides provide real-time coaching.
"""

from .session_orchestrator import SessionOrchestrator, SessionConfig, SessionResult
from .environment import (
    WorldEngine,
    SimulationState,
    Event,
    # Additional environment exports will be added as modules are implemented
)

# Placeholder for SimulationEnvironment - define it here for now
class SimulationEnvironment(WorldEngine):
    """Alias for WorldEngine to maintain API compatibility"""
    pass

# Additional modules not yet implemented
# from .scenarios import (
#     Scenario,
#     WorkplaceScenario,
#     PersonalScenario,
#     SocialScenario,
#     ScenarioGenerator,
# )
# from .npcs import (
#     BaseNPC,
#     NeurotypicalNPC,
#     BiasedNPC,
#     SupportiveNPC,
#     NPCManager,
# )
# from .challenges import (
#     ChallengeInjector,
#     DifficultyScaling,
#     BurnoutSimulator,
# )
# from .training_loop import (
#     SessionManager,
#     AvatarAideCoordinator,
#     InteractionLogger,
# )

__all__ = [
    "SessionOrchestrator",
    "SessionConfig",
    "SessionResult",
    "SimulationEnvironment",
    "WorldEngine",
    "SimulationState",
    "Event",
    # Additional exports will be added as modules are implemented
]
