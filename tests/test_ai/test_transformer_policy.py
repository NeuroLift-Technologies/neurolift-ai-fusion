"""Tests for the TransformerPolicyBackend (requires torch/transformers in CI)."""

import json
import sys
import types
from unittest.mock import MagicMock, patch

import pytest

from src.ai.adapters.transformer_policy import TransformerPolicyBackend, _aide_baseline, _avatar_baseline


def _make_backend(**kwargs):
    defaults = {
        "checkpoint_path": None,
        "model_name": "distilgpt2",
        "kind": "avatar",
        "device": "cpu",
    }
    defaults.update(kwargs)
    return TransformerPolicyBackend(**defaults)


class TestTransformerPolicyBackend:
    def test_init_defaults(self):
        backend = _make_backend()
        assert backend.checkpoint_path is None
        assert backend.model_name == "distilgpt2"
        assert backend.kind == "avatar"
        assert backend.device == "cpu"

    def test_init_custom_values(self):
        backend = _make_backend(kind="aide", model_name="gpt2", device="cuda")
        assert backend.kind == "aide"
        assert backend.model_name == "gpt2"
        assert backend.device == "cuda"

    def test_predict_returns_neutral_baseline_on_model_error(self, monkeypatch):
        mock_transformers = types.ModuleType("transformers")
        mock_transformers.pipeline = MagicMock(side_effect=RuntimeError("boom"))
        monkeypatch.setitem(sys.modules, "transformers", mock_transformers)
        monkeypatch.setitem(sys.modules, "torch", types.ModuleType("torch"))
        backend = _make_backend(kind="aide")
        result = backend.predict({"role": "aide", "aide_id": "a1"})
        assert result == _aide_baseline()

    def test_predict_returns_neutral_baseline_on_parse_error(self, monkeypatch):
        mock_transformers = types.ModuleType("transformers")
        mock_pipe = MagicMock()
        mock_pipe.return_value = [{"generated_text": "not valid json!!!"}]
        mock_transformers.pipeline = MagicMock(return_value=mock_pipe)
        monkeypatch.setitem(sys.modules, "transformers", mock_transformers)
        monkeypatch.setitem(sys.modules, "torch", types.ModuleType("torch"))
        backend = _make_backend(kind="avatar")
        result = backend.predict({"role": "avatar", "avatar_id": "a1"})
        assert result == _avatar_baseline()

    def test_predict_parses_valid_json_and_merges(self, monkeypatch):
        mock_transformers = types.ModuleType("transformers")
        prompt = json.dumps({"role": "avatar", "avatar_id": "a1"}, default=str)
        generated_text = prompt + '{"emotional_state": "focused"}'
        mock_pipe = MagicMock()
        mock_pipe.return_value = [{"generated_text": generated_text}]
        mock_transformers.pipeline = MagicMock(return_value=mock_pipe)
        monkeypatch.setitem(sys.modules, "transformers", mock_transformers)
        monkeypatch.setitem(sys.modules, "torch", types.ModuleType("torch"))
        backend = _make_backend(kind="avatar")
        result = backend.predict({"role": "avatar", "avatar_id": "a1"})
        assert result["emotional_state"] == "focused"
        assert result["trait_impact"]["difficulty_modifier"] == 1.0

    def test_update_without_checkpoint_is_noop(self):
        backend = _make_backend(checkpoint_path=None)
        assert backend.update([]) is None

    def test_update_with_checkpoint_writes_jsonl(self, tmp_path, monkeypatch):
        mock_transformers = types.ModuleType("transformers")
        monkeypatch.setitem(sys.modules, "transformers", mock_transformers)
        monkeypatch.setitem(sys.modules, "torch", types.ModuleType("torch"))
        backend = _make_backend(checkpoint_path=str(tmp_path / "ckpt"))
        from src.core.protocols import ExperienceRecord

        rec = ExperienceRecord(
            task_type="coding",
            task_context={},
            outcome_success=True,
            quality_score=0.8,
            struggles_experienced=[],
            emotional_journey=[],
            cognitive_load_peak=0.3,
            stress_peak=0.2,
            coaching_received=[],
            strategy_discovered="",
            independence_delta=0.0,
        )
        backend.update([rec])
        jsonl_path = tmp_path / "ckpt" / "training_data.jsonl"
        assert jsonl_path.exists()
        with open(jsonl_path) as fh:
            line = json.loads(fh.readline())
        assert line["task_type"] == "coding"

    def test_predict_aide_role_parses_and_merges(self, monkeypatch):
        mock_transformers = types.ModuleType("transformers")
        prompt = json.dumps({"role": "aide", "aide_id": "a1"}, default=str)
        generated_text = prompt + '{"strategy": "chunking", "urgency": "medium"}'
        mock_pipe = MagicMock()
        mock_pipe.return_value = [{"generated_text": generated_text}]
        mock_transformers.pipeline = MagicMock(return_value=mock_pipe)
        monkeypatch.setitem(sys.modules, "transformers", mock_transformers)
        monkeypatch.setitem(sys.modules, "torch", types.ModuleType("torch"))
        backend = _make_backend(kind="aide")
        result = backend.predict({"role": "aide", "aide_id": "a1"})
        assert result["strategy"] == "chunking"
        assert result["urgency"] == "medium"
        assert result["coaching_type"] == "preventive"

    def test_predict_import_error_raises(self, monkeypatch):
        monkeypatch.delitem(sys.modules, "torch", raising=False)
        monkeypatch.delitem(sys.modules, "transformers", raising=False)
        backend = _make_backend()
        with pytest.raises(ImportError, match="transformer_policy adapter requires"):
            backend.predict({"role": "avatar", "avatar_id": "a1"})
