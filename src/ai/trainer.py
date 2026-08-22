"""
Trainer and Training Pipeline

Glue between experience records (from Avatars/Aides) and model backends
in the :class:`~src.ai.registry.ModelRegistry`. The pipeline is fully
provider-agnostic and never requires torch.
"""

import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..core.protocols import ExperienceRecord
from .dataset import ExperienceDataset
from .protocol import ModelBackend
from .registry import ModelRegistry, get_registry


@dataclass
class TrainingMetrics:
    """Summary of a single training/update pass."""

    n_records: int
    model_id: str
    model_version: str
    started_at: str
    finished_at: str
    owner_id: str
    status: str = "completed"


class Trainer(ABC):
    """Abstract trainer interface."""

    @abstractmethod
    def fit(
        self, dataset: ExperienceDataset, backend: ModelBackend
    ) -> Dict[str, Any]:
        """Train/adapt ``backend`` on a full ``dataset``."""
        ...

    @abstractmethod
    def update(
        self, backend: ModelBackend, records: List[ExperienceRecord]
    ) -> Dict[str, Any]:
        """Incrementally update ``backend`` with new ``records``."""
        ...


class NoOpTrainer(Trainer):
    """Trainer that intentionally does nothing (baselines, dry runs)."""

    def fit(
        self, dataset: ExperienceDataset, backend: ModelBackend
    ) -> Dict[str, Any]:
        return {
            "n_records": len(dataset.to_records()),
            "status": "skipped",
        }

    def update(
        self, backend: ModelBackend, records: List[ExperienceRecord]
    ) -> Dict[str, Any]:
        return {"n_records": len(records), "status": "skipped"}


class ExperienceTrainer(Trainer):
    """Minimal trainer that forwards experience to ``backend.update``."""

    def fit(
        self, dataset: ExperienceDataset, backend: ModelBackend
    ) -> Dict[str, Any]:
        return self.update(backend, dataset.to_records())

    def update(
        self,
        backend: ModelBackend,
        records: List[ExperienceRecord],
        owner_id: str = "<unknown>",
    ) -> Dict[str, Any]:
        started = datetime.now().isoformat()
        backend.update(records)
        finished = datetime.now().isoformat()
        return TrainingMetrics(
            n_records=len(records),
            model_id=getattr(backend, "model_id", "unknown"),
            model_version=getattr(backend, "model_version", "0.0.0"),
            started_at=started,
            finished_at=finished,
            owner_id=owner_id,
            status="completed",
        ).__dict__


class TrainingPipeline:
    """Drive training of all registered backends for given owners."""

    def __init__(
        self,
        registry: Optional[ModelRegistry] = None,
        trainer: Optional[Trainer] = None,
    ) -> None:
        self.registry = registry or get_registry()
        self.trainer = trainer or ExperienceTrainer()

    def run(
        self,
        *,
        avatar: Any = None,
        aide: Any = None,
        avatar_id: Optional[str] = None,
        aide_id: Optional[str] = None,
        records: Optional[List[ExperienceRecord]] = None,
    ) -> Dict[str, Any]:
        # Resolve owner ids and union records by record_id.
        if avatar is not None:
            avatar_id = getattr(avatar, "avatar_id", avatar_id)
            if records is None and hasattr(avatar, "experience_memory"):
                records = list(avatar.experience_memory.get_records())
        if aide is not None:
            aide_id = getattr(aide, "aide_id", aide_id)
            if records is None and hasattr(aide, "experience_memory"):
                records = list(aide.experience_memory.get_records())

        records = list(records or [])
        owner_ids = [o for o in (avatar_id, aide_id) if o is not None]

        dataset = ExperienceDataset(records)
        metrics: Dict[str, Any] = {}
        owners_seen: List[str] = []

        for owner_id in owner_ids:
            backend = self.registry.get(owner_id)
            if backend is None:
                continue
            result = self.trainer.update(backend, dataset.to_records())
            self.registry.record_training(owner_id, result)
            self.registry.save_checkpoint(owner_id)
            metrics[owner_id] = result
            owners_seen.append(owner_id)

        return {
            "owners": owners_seen,
            "n_records": len(records),
            "metrics": metrics,
        }

    def run_async(self, **kwargs: Any) -> threading.Thread:
        """Spawn ``run`` in a daemon thread and return it immediately."""
        thread = threading.Thread(
            target=self.run, kwargs=kwargs, daemon=True
        )
        thread.start()
        return thread
