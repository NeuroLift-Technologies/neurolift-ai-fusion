"""
Fusion Engine

Manages the process of combining an Avatar's experiential knowledge
with an Aide's expertise to produce a fused Advocate.
"""

from .fusion_engine import FusionEngine
from .model_fusion import (
    ModelEvalResult,
    ModelFusionEngine,
    ModelFusionReport,
    NoOpStudentTrainer,
    PairedTrajectoryStep,
    RouterTeacher,
)
from .readiness_assessor import (
    ReadinessAssessor,
    DimensionScore,
    FusionDimension,
    FusionReadiness,
)
from .state_feed import build_state_feed
from .agent_loop import AgentLoopProtocolError, FusionAgentLoop

__all__ = [
    "FusionEngine",
    "FusionDimension",
    "FusionReadiness",
    "ReadinessAssessor",
    "DimensionScore",
    "build_state_feed",
    "AgentLoopProtocolError",
    "FusionAgentLoop",
    # Model-level fusion (trajectory distillation)
    "ModelFusionEngine",
    "ModelFusionReport",
    "ModelEvalResult",
    "PairedTrajectoryStep",
    "RouterTeacher",
    "NoOpStudentTrainer",
]
