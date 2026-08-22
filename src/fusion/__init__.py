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

__all__ = [
    "FusionEngine",
    "FusionDimension",
    "FusionReadiness",
    "ReadinessAssessor",
    "DimensionScore",
    # Model-level fusion (trajectory distillation)
    "ModelFusionEngine",
    "ModelFusionReport",
    "ModelEvalResult",
    "PairedTrajectoryStep",
    "RouterTeacher",
    "NoOpStudentTrainer",
]
