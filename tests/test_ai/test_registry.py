"""Tests for the ModelRegistry and singleton."""

import os

import pytest

from src.ai import ModelRegistry, RuleFallbackBackend, get_registry


class TestRegistry:
    def test_singleton(self):
        assert get_registry() is get_registry()

    def test_register_get_unregister(self):
        reg = ModelRegistry()
        backend = RuleFallbackBackend(kind="avatar")
        reg.register("a1", backend)
        assert reg.get("a1") is backend
        reg.unregister("a1")
        assert reg.get("a1") is None

    def test_build_rule_fallback(self):
        reg = ModelRegistry()
        backend = reg.build_backend({"type": "rule_fallback", "kind": "avatar"})
        assert isinstance(backend, RuleFallbackBackend)
        assert backend.kind == "avatar"

    def test_build_unknown_raises(self):
        reg = ModelRegistry()
        with pytest.raises(ValueError):
            reg.build_backend({"type": "bogus"})

    def test_build_openai_compat_missing_base_url_raises(self):
        reg = ModelRegistry()
        with pytest.raises(ValueError, match="base_url"):
            reg.build_backend({"type": "openai_compat", "kind": "aide"})

    def test_config_binding(self):
        reg = ModelRegistry()
        reg.bind_config("a1", {"type": "rule_fallback"})
        assert reg.get_config("a1") == {"type": "rule_fallback"}
        assert reg.list_configs()["a1"] == {"type": "rule_fallback"}

    def test_checkpoint_roundtrip(self, tmp_path, monkeypatch):
        monkeypatch.setenv("NEUROLIFT_MODELS_DIR", str(tmp_path))
        reg = ModelRegistry()
        reg.register("a1", RuleFallbackBackend(kind="avatar"))
        path = reg.save_checkpoint("a1")
        assert os.path.exists(path)
        meta = reg.load_checkpoint("a1")
        assert meta["model_id"] == "rule_fallback"
        assert meta["kind"] == "avatar"
        assert "updated_at" in meta

    def test_status_includes_models(self):
        reg = ModelRegistry()
        reg.register("a1", RuleFallbackBackend())
        status = reg.status()
        assert "a1" in status["models"]
        assert status["models"]["a1"]["model_id"] == "rule_fallback"
