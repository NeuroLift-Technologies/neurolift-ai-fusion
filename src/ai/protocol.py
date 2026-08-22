"""
Model Protocols for the NeuroLift AI layer.

Defines the :class:`ModelBackend` contract shared by every Avatar/Aide
model adapter, the concrete :class:`ModelAdapter` base class, and the
:class:`ModelPrediction` value object.

This module is the ONLY place the ``ai`` package depends on ``core``.
It deliberately imports nothing from ``avatars`` or ``aides`` to avoid
import cycles: adapters receive plain ``dict`` payloads and emit plain
``dict`` predictions.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Protocol, runtime_checkable

from ..core.protocols import ExperienceRecord

# ---------------------------------------------------------------------------
# Kind constants
# ---------------------------------------------------------------------------

AVATAR_MODEL_KIND = "avatar"
AIDE_MODEL_KIND = "aide"
ADVOCATE_MODEL_KIND = "advocate"

# ---------------------------------------------------------------------------
# Prediction value object
# ---------------------------------------------------------------------------


@dataclass
class ModelPrediction:
    """Structured result returned by a model backend.

    Attributes:
        outputs: The model output payload. Shape depends on ``kind``
            (see the AVATAR / AIDE contracts documented on
            :class:`ModelBackend`).
        model_id: Identifier of the producing model.
        model_version: Version of the producing model.
    """

    outputs: Dict[str, Any]
    model_id: str = "unknown"
    model_version: str = "0.0.0"


# ---------------------------------------------------------------------------
# Backend contract
# ---------------------------------------------------------------------------


@runtime_checkable
class ModelBackend(Protocol):
    """Duck-typed contract every model backend must satisfy.

    A backend is any object exposing:

    * ``model_id: str``
    * ``model_version: str``
    * ``kind: str``
    * ``predict(inputs: Dict[str, Any]) -> Dict[str, Any]``
    * ``update(records: List[ExperienceRecord]) -> None``

    AVATAR model I/O contract
    --------------------------
    ``predict`` inputs::

        {
            "role": "avatar",
            "avatar_id": str,
            "task_context": dict,
            "current_emotional_state": str,
            "current_cognitive_load": float,
            "current_stress_level": float,
            "experience_summary": Optional[dict],
        }

    ``predict`` outputs::

        {
            "trait_impact": {
                "difficulty_modifier": float,
                "quality_modifier": float,
                "time_modifier": float,
                "cognitive_load_modifier": float,
            },
            "struggle_indicators": List[str],
            "emotional_state": str,
            "cognitive_load": float,
            "stress_level": float,
        }

    AIDE model I/O contract
    -----------------------
    ``predict`` inputs::

        {
            "role": "aide",
            "aide_id": str,
            "observation": dict,            # ObservationReport.to_dict()
            "task_context": dict,
            "coaching_history_summary": dict,
        }

    ``predict`` outputs::

        {
            "strategy": str,
            "specific_techniques": List[str],
            "urgency": str,                 # "low"|"medium"|"high"|"critical"
            "coaching_type": str,
            "stress_reduction": float,
            "emotional_boost": float,
            "cognitive_support": float,
            "focus_restoration": float,
            "independence_building": float,
        }

    ADVOCATE model I/O contract (unified, post-fusion)
    ---------------------------------------------------
    ``predict`` inputs::

        {
            "role": "advocate",
            "advocate_id": str,
            "user_context": dict,           # { struggles, stress_level, cognitive_load, building_independence, ... }
            "observation": dict,            # ObservationReport.to_dict() (optional, for Sims-grounded eval)
            "task_context": dict,
        }

    ``predict`` outputs::

        {
            "mode": str,                    # AdvocateMode value
            "empathic_understanding": dict, # { struggles, emotional_journey, stress_peak, ... }
            "expert_guidance": dict,        # { strategy, techniques, rationale, ... }
            "actionable_steps": List[str],  # capped at 5
            "encouragement": str,
        }
    """

    model_id: str
    model_version: str
    kind: str

    def predict(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Produce a prediction for the given input payload."""
        ...

    def update(self, records: List[ExperienceRecord]) -> None:
        """Absorb experience records for (optional) training."""
        ...


class ModelAdapter:
    """Base class for model adapters.

    Implements the :class:`ModelBackend` contract with safe defaults:
    ``predict`` raises ``NotImplementedError`` while ``update`` is a
    no-op so non-trainable baselines do not break the training pipeline.

    Subclasses override ``predict`` (and optionally ``update``).
    """

    model_id: str = "base_adapter"
    model_version: str = "0.1.0"
    kind: str = "generic"

    def predict(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Raise by default — subclasses must implement prediction."""
        raise NotImplementedError(
            f"{type(self).__name__} does not implement predict()."
        )

    def update(self, records: List[ExperienceRecord]) -> None:
        """Default no-op. Non-trainable baselines may inherit this."""
        return None

    def to_metadata(self) -> Dict[str, Any]:
        """Return a serialisable description of this backend."""
        return {
            "model_id": self.model_id,
            "model_version": self.model_version,
            "kind": self.kind,
        }
