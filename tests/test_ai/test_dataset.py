"""Tests for the ExperienceDataset."""

import json
import os

import pytest

from src.ai import ExperienceDataset
from src.core.protocols import ExperienceMemory, ExperienceRecord


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


class TestExperienceDataset:
    def test_to_dicts_keys_and_length(self):
        recs = [_make_record("coding"), _make_record("writing", False, 0.3)]
        ds = ExperienceDataset(recs)
        d = ds.to_dicts()
        assert len(d) == 2
        assert set(d[0].keys()) >= {
            "task_type",
            "outcome_success",
            "quality_score",
            "struggles_experienced",
            "emotional_journey",
            "cognitive_load_peak",
            "stress_peak",
            "coaching_received",
            "strategy_discovered",
            "independence_delta",
            "task_context",
        }

    def test_summary_counts(self):
        ds = ExperienceDataset(
            [_make_record("coding", True, 0.9), _make_record("coding", False, 0.2)]
        )
        s = ds.summary()
        assert s["total"] == 2
        assert s["successes"] == 1
        assert s["failures"] == 1
        assert s["distinct_task_types"] == ["coding"]

    def test_from_experience_memory(self):
        mem = ExperienceMemory(owner_id="a1")
        mem.record(_make_record("coding"))
        ds = ExperienceDataset.from_experience_memory(mem)
        assert len(ds.to_records()) == 1

    def test_to_jsonl_writes_file(self, tmp_path):
        ds = ExperienceDataset([_make_record("coding")])
        path = ds.to_jsonl(str(tmp_path / "out.jsonl"))
        assert os.path.exists(path)
        with open(path) as fh:
            line = json.loads(fh.readline())
        assert line["task_type"] == "coding"

    def test_to_tensors_raises_without_torch(self):
        ds = ExperienceDataset([_make_record("coding")])
        try:
            import torch  # noqa: F401

            pytest.skip("torch is installed; cannot test ImportError path")
        except ImportError:
            with pytest.raises(ImportError):
                ds.to_tensors()
