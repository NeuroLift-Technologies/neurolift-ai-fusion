"""Coverage tests for the src/ai model framework (PR #97).

These exercise the new Avatar/Aide model layer without requiring torch or
any external network/API access, keeping the suite fast and dependency-free.
"""

import json
import os

import pytest

from src.ai import (
    ExperienceDataset,
    ModelRegistry,
    NoOpTrainer,
    RuleFallbackBackend,
    TrainingPipeline,
    get_registry,
)
from src.ai.trainer import ExperienceTrainer, TrainingMetrics
from src.ai.adapters.transformer_policy import TransformerPolicyBackend
from src.ai.adapters.openai_compat import OpenAICompatBackend
from src.core.protocols import ExperienceRecord


def _make_record(task_type, success=True, quality=0.8):
    return ExperienceRecord(
        task_type=task_type,
        task_context={"x": 1},
        outcome_success=success,
        quality_score=quality,
        struggles_experienced=["focus"],
        emotional_journey=["calm", "frustrated"],
        cognitive_load_peak=0.5,
        stress_peak=0.4,
        coaching_received=[{"technique": "break"}],
        strategy_discovered="chunking",
        independence_delta=0.1,
    )


class TestRegistryBuildBackends:
    def test_build_transformer_backend(self):
        reg = ModelRegistry()
        backend = reg.build_backend(
            {"type": "transformer", "kind": "avatar", "model_name": "distilgpt2"}
        )
        assert isinstance(backend, TransformerPolicyBackend)
        assert backend.kind == "avatar"
        assert backend.model_name == "distilgpt2"

    def test_build_openai_compat_backend(self):
        reg = ModelRegistry()
        backend = reg.build_backend(
            {
                "type": "openai_compat",
                "kind": "aide",
                "base_url": "https://example.invalid/v1",
            }
        )
        assert isinstance(backend, OpenAICompatBackend)
        assert backend.kind == "aide"
        assert backend.base_url == "https://example.invalid/v1"

    def test_build_unknown_backend_raises(self):
        reg = ModelRegistry()
        with pytest.raises(ValueError):
            reg.build_backend({"type": "does_not_exist"})


class TestRegistryCheckpointExplicitPath:
    def test_save_load_with_explicit_path(self, tmp_path):
        reg = ModelRegistry()
        reg.register("ex1", RuleFallbackBackend(kind="avatar"))
        target = tmp_path / "nested" / "ex1.json"
        path = reg.save_checkpoint("ex1", str(target))
        assert os.path.exists(path)
        meta = reg.load_checkpoint("ex1", str(target))
        assert meta["model_id"] == "rule_fallback"

    def test_load_checkpoint_missing_returns_none(self, tmp_path):
        reg = ModelRegistry()
        missing = tmp_path / "no_such.json"
        assert reg.load_checkpoint("ex1", str(missing)) is None

    def test_record_training_and_status(self):
        reg = ModelRegistry()
        reg.register("st1", RuleFallbackBackend())
        reg.record_training("st1", {"status": "completed", "n_records": 3})
        status = reg.status()
        assert "st1" in status["last_training"]
        assert status["metrics"]["st1"]["n_records"] == 3


class TestTrainerClasses:
    def test_noop_trainer_fit_and_update(self):
        trainer = NoOpTrainer()
        ds = ExperienceDataset([_make_record("coding")])
        result = trainer.fit(ds, RuleFallbackBackend(kind="avatar"))
        assert result["status"] == "skipped"
        upd = trainer.update(RuleFallbackBackend(kind="avatar"), [_make_record("x")])
        assert upd["status"] == "skipped"

    def test_experience_trainer_fit_returns_metrics(self):
        trainer = ExperienceTrainer()
        ds = ExperienceDataset([_make_record("coding"), _make_record("write", False)])
        backend = RuleFallbackBackend(kind="avatar")
        result = trainer.fit(ds, backend)
        assert isinstance(result, dict)
        assert result["n_records"] == 2
        assert result["status"] == "completed"

    def test_training_metrics_dataclass(self):
        metrics = TrainingMetrics(
            n_records=4,
            model_id="m",
            model_version="1.0.0",
            started_at="s",
            finished_at="f",
            owner_id="o",
        )
        assert metrics.n_records == 4
        assert metrics.owner_id == "o"


class TestDatasetPairedCorpus:
    def test_to_jsonl_roundtrip(self, tmp_path):
        ds = ExperienceDataset([_make_record("coding")])
        path = ds.to_jsonl(str(tmp_path / "r.jsonl"))
        with open(path) as fh:
            row = json.loads(fh.readline())
        assert row["task_type"] == "coding"
