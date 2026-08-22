"""
Experience Dataset

Converts :class:`~src.core.protocols.ExperienceRecord` objects into
flat dictionaries, summaries, JSONL, and (lazily) torch tensors for
downstream model training.
"""

import json
import os
from typing import Any, Dict, List, Optional

from ..core.protocols import ExperienceRecord


class ExperienceDataset:
    """A collection of experience records for model training/eval."""

    def __init__(self, records: List[ExperienceRecord]) -> None:
        self._records: List[ExperienceRecord] = list(records or [])

    def to_records(self) -> List[ExperienceRecord]:
        """Return the underlying list of experience records."""
        return self._records

    def to_dicts(self) -> List[Dict[str, Any]]:
        """Flatten each record into a model-friendly dictionary."""
        flat: List[Dict[str, Any]] = []
        for r in self._records:
            flat.append(
                {
                    "record_id": r.record_id,
                    "task_type": r.task_type,
                    "task_context": r.task_context,
                    "outcome_success": r.outcome_success,
                    "quality_score": r.quality_score,
                    "struggles_experienced": r.struggles_experienced,
                    "emotional_journey": r.emotional_journey,
                    "cognitive_load_peak": r.cognitive_load_peak,
                    "stress_peak": r.stress_peak,
                    "coaching_received": r.coaching_received,
                    "coaching_helpful": r.coaching_helpful,
                    "strategy_discovered": r.strategy_discovered,
                    "independence_delta": r.independence_delta,
                }
            )
        return flat

    def to_jsonl(self, path: str) -> str:
        """Write the flattened records to a JSONL file; return the path."""
        with open(path, "w", encoding="utf-8") as fh:
            for row in self.to_dicts():
                fh.write(json.dumps(row, default=str) + "\n")
        return path

    def summary(self) -> Dict[str, Any]:
        """Return aggregate statistics over the dataset."""
        total = len(self._records)
        successes = sum(1 for r in self._records if r.outcome_success)
        failures = total - successes
        avg_quality = (
            sum(r.quality_score for r in self._records) / total if total else 0.0
        )
        distinct_types = {r.task_type for r in self._records}
        return {
            "total": total,
            "successes": successes,
            "failures": failures,
            "avg_quality": avg_quality,
            "distinct_task_types": sorted(distinct_types),
        }

    def to_tensors(self) -> Dict[str, Any]:
        """Build stacked tensors from numeric fields.

        ``torch`` is imported lazily; an informative ``ImportError`` is
        raised if it is not installed.
        """
        try:
            import torch  # noqa: WPS433 (deliberate lazy import)
        except ImportError as exc:  # pragma: no cover - env dependent
            raise ImportError(
                "to_tensors() requires torch; install requirements-ai.txt"
            ) from exc

        numeric_keys = [
            "quality_score",
            "cognitive_load_peak",
            "stress_peak",
            "independence_delta",
        ]
        tensors: Dict[str, Any] = {}
        for key in numeric_keys:
            values = [float(getattr(r, key)) for r in self._records]
            tensors[key] = torch.tensor(values, dtype=torch.float32)
        tensors["outcome_success"] = torch.tensor(
            [1.0 if r.outcome_success else 0.0 for r in self._records],
            dtype=torch.float32,
        )
        return tensors

    def to_paired_trajectory_steps(
        self,
        avatar_outputs: Optional[List[Dict[str, Any]]] = None,
        aide_outputs: Optional[List[Optional[Dict[str, Any]]]] = None,
        observations: Optional[List[Dict[str, Any]]] = None,
        scenarios: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Serialize as paired trajectory steps for model fusion.

        Each ``ExperienceRecord`` is paired with the Avatar and Aide
        ``ModelBackend`` outputs at that tick (when available).  The
        output is a list of dicts matching
        ``PairedTrajectoryStep.to_dict()`` — suitable for JSONL export
        or direct ``ModelFusionEngine.build_paired_corpus`` input.

        Parallel arrays (``avatar_outputs``, etc.) must match
        ``len(self._records)`` when provided; omitted arrays fall back
        to per-record derivations.
        """
        # Lazy import to avoid cycle at module import time
        from ..fusion.model_fusion import PairedTrajectoryStep  # noqa: WPS433

        # Reuse the engine's validated builder for consistency
        from ..fusion.model_fusion import ModelFusionEngine  # noqa: WPS433

        corpus = ModelFusionEngine.build_paired_corpus(
            self._records,
            avatar_outputs=avatar_outputs,
            aide_outputs=aide_outputs,
            observations=observations,
            scenarios=scenarios,
        )
        return [s.to_dict() for s in corpus]

    @classmethod
    def from_experience_memory(cls, memory: Any) -> "ExperienceDataset":
        """Build a dataset from an :class:`ExperienceMemory` instance."""
        return cls(memory.get_records())
