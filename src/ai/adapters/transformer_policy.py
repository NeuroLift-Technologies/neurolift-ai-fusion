"""
Transformer Policy Backend (lazy torch/transformers import)

Wraps a HuggingFace text-generation model. ``torch`` and ``transformers``
are imported only inside the methods that need them, so importing this
module never pulls in heavy dependencies.

Real fine-tuning is OUT OF SCOPE: :meth:`update` only persists records to
JSONL (when a checkpoint path is provided). Prediction is a minimal,
defensive pass: build a prompt, generate text, attempt to parse JSON, and
fall back to a neutral baseline on any failure so the simulation keeps
running.
"""

import json
import os
from typing import Any, Dict, List, Optional

from ...core.protocols import ExperienceRecord
from ..protocol import ModelAdapter, AVATAR_MODEL_KIND, AIDE_MODEL_KIND


def _avatar_baseline() -> Dict[str, Any]:
    return {
        "trait_impact": {
            "difficulty_modifier": 1.0,
            "quality_modifier": 0.0,
            "time_modifier": 1.0,
            "cognitive_load_modifier": 0.0,
        },
        "struggle_indicators": [],
        "emotional_state": "neutral",
        "cognitive_load": 0.0,
        "stress_level": 0.0,
    }


def _aide_baseline() -> Dict[str, Any]:
    return {
        "strategy": "Rule-based fallback (no model)",
        "specific_techniques": [],
        "urgency": "low",
        "coaching_type": "preventive",
        "stress_reduction": 0.0,
        "emotional_boost": 0.0,
        "cognitive_support": 0.0,
        "focus_restoration": 0.0,
        "independence_building": 0.0,
    }


class TransformerPolicyBackend(ModelAdapter):
    """Minimal HuggingFace-backed policy backend."""

    model_id: str = "transformer_policy"
    model_version: str = "0.1.0"

    def __init__(
        self,
        checkpoint_path: Optional[str] = None,
        model_name: str = "distilgpt2",
        kind: str = "avatar",
        device: str = "cpu",
    ) -> None:
        self.checkpoint_path = checkpoint_path
        self.model_name = model_name
        self.kind = kind
        self.device = device

    def predict(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            import torch  # noqa: F401
            import transformers  # noqa: F401
        except ImportError as exc:
            raise ImportError(
                "transformer_policy adapter requires torch and transformers; "
                "install requirements-ai.txt"
            ) from exc

        try:
            prompt = json.dumps(inputs, default=str)
            model_ref = self.checkpoint_path or self.model_name
            pipe = transformers.pipeline(
                "text-generation", model=model_ref, device=self.device
            )
            generated = pipe(prompt, max_new_tokens=256)
            content = generated[0]["generated_text"][len(prompt):]
            parsed = json.loads(content)
            if isinstance(parsed, dict):
                if inputs.get("role", self.kind) == AVATAR_MODEL_KIND:
                    return {**_avatar_baseline(), **parsed}
                return {**_aide_baseline(), **parsed}
        except Exception:
            # Defensive: never break the simulation on model failures.
            pass
        return (
            _avatar_baseline()
            if inputs.get("role", self.kind) == AVATAR_MODEL_KIND
            else _aide_baseline()
        )

    def update(self, records: List[ExperienceRecord]) -> None:
        """Persist records to JSONL. Real fine-tuning is out of scope."""
        try:
            import torch  # noqa: F401
        except ImportError:
            # Still allow JSONL export without torch.
            pass
        if not self.checkpoint_path:
            return None
        from ..dataset import ExperienceDataset

        os.makedirs(self.checkpoint_path, exist_ok=True)
        path = os.path.join(self.checkpoint_path, "training_data.jsonl")
        ExperienceDataset(records).to_jsonl(path)
        return None
