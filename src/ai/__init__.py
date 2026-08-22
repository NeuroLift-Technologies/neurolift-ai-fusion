"""
NeuroLift AI model layer.

Provider-agnostic adapters that connect trainable ML models to Avatar/Aide
pairs. The package is importable WITHOUT torch/transformers/requests; heavy
dependencies are imported lazily inside the adapters that need them.

Note: ``transformer_policy`` and ``openai_compat`` are NOT imported at
top-level — the registry factory imports them lazily. ``adapters.rule_fallback``
is safe to import eagerly (no heavy deps).
"""

from .adapters.rule_fallback import RuleFallbackBackend
from .dataset import ExperienceDataset
from .protocol import (
    AIDE_MODEL_KIND,
    AVATAR_MODEL_KIND,
    ModelAdapter,
    ModelBackend,
    ModelPrediction,
)
from .registry import ModelRegistry, get_registry
from .trainer import (
    ExperienceTrainer,
    NoOpTrainer,
    Trainer,
    TrainingPipeline,
)

__all__ = [
    "ModelBackend",
    "ModelAdapter",
    "ModelPrediction",
    "AVATAR_MODEL_KIND",
    "AIDE_MODEL_KIND",
    "ExperienceDataset",
    "ModelRegistry",
    "get_registry",
    "Trainer",
    "NoOpTrainer",
    "ExperienceTrainer",
    "TrainingPipeline",
    "RuleFallbackBackend",
]
