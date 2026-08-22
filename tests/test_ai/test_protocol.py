"""Tests for the model protocol and base adapter."""

import pytest

from src.ai import ModelAdapter, ModelBackend, ModelPrediction, RuleFallbackBackend


class TestProtocol:
    def test_rule_fallback_is_model_backend(self):
        assert isinstance(RuleFallbackBackend(kind="avatar"), ModelBackend)

    def test_model_adapter_update_is_noop(self):
        adapter = ModelAdapter()
        assert adapter.update([]) is None

    def test_base_model_adapter_predict_raises(self):
        adapter = ModelAdapter()
        with pytest.raises(NotImplementedError):
            adapter.predict({"role": "avatar"})

    def test_model_prediction_dataclass(self):
        pred = ModelPrediction(outputs={"a": 1}, model_id="m", model_version="1.2.3")
        assert pred.outputs == {"a": 1}
        assert pred.model_id == "m"
        assert pred.model_version == "1.2.3"
