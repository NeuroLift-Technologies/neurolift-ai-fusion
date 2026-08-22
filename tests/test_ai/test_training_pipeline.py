"""Tests for the TrainingPipeline."""

import pytest

from src.ai import ModelRegistry, RuleFallbackBackend, TrainingPipeline
from src.core.protocols import ExperienceMemory, ExperienceRecord


def _make_record(task_type, success=True):
    return ExperienceRecord(
        task_type=task_type,
        outcome_success=success,
        quality_score=0.7,
        cognitive_load_peak=0.4,
        stress_peak=0.3,
        independence_delta=0.1,
    )


class TestTrainingPipeline:
    def test_run_with_registered_backend(self):
        reg = ModelRegistry()
        owner = "avatar_1"
        reg.register(owner, RuleFallbackBackend(kind="avatar"))
        records = [_make_record("coding"), _make_record("writing", False), _make_record("coding")]
        pipeline = TrainingPipeline(registry=reg, trainer=None)
        summary = pipeline.run(avatar_id=owner, records=records)
        assert owner in summary["owners"]
        assert summary["n_records"] == 3
        assert owner in summary["metrics"]
        assert owner in reg.status()["last_training"]

    def test_run_no_backends_returns_empty(self):
        reg = ModelRegistry()
        pipeline = TrainingPipeline(registry=reg)
        summary = pipeline.run(avatar_id="nobody", records=[_make_record("coding")])
        assert summary["owners"] == []
        assert summary["n_records"] == 1

    def test_run_pulls_from_avatar_memory(self):
        reg = ModelRegistry()
        owner = "avatar_2"
        reg.register(owner, RuleFallbackBackend(kind="avatar"))
        mem = ExperienceMemory(owner_id=owner)
        for _ in range(3):
            mem.record(_make_record("reading"))
        avatar = type("Avatar", (), {"avatar_id": owner, "experience_memory": mem})()
        pipeline = TrainingPipeline(registry=reg)
        summary = pipeline.run(avatar=avatar)
        assert owner in summary["owners"]
        assert summary["n_records"] == 3

    def test_run_pulls_from_aide_memory(self):
        reg = ModelRegistry()
        owner = "aide_1"
        reg.register(owner, RuleFallbackBackend(kind="aide"))
        mem = ExperienceMemory(owner_id=owner)
        for _ in range(3):
            mem.record(_make_record("reading"))
        aide = type("Aide", (), {"aide_id": owner, "experience_memory": mem})()
        pipeline = TrainingPipeline(registry=reg)
        summary = pipeline.run(aide=aide)
        assert owner in summary["owners"]
        assert summary["n_records"] == 3

    def test_run_async_returns_thread(self):
        import threading

        reg = ModelRegistry()
        pipeline = TrainingPipeline(registry=reg)
        t = pipeline.run_async(avatar_id="nobody", records=[])
        assert isinstance(t, threading.Thread)
        t.join(timeout=5)
