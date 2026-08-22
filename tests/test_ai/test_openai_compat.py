"""Tests for the OpenAI-compatible backend (stdlib urllib, no network)."""

import json
import os
import urllib.error
from unittest.mock import MagicMock, patch

import pytest

from src.ai.adapters.openai_compat import OpenAICompatBackend, _aide_baseline, _avatar_baseline


def _make_backend(**kwargs):
    defaults = {
        "base_url": "https://example.invalid/v1",
        "api_key_env": "OPENAI_COMPAT_API_KEY",
        "model_name": "gpt-4o-mini",
        "kind": "aide",
        "timeout": 5.0,
    }
    defaults.update(kwargs)
    return OpenAICompatBackend(**defaults)


class TestOpenAICompatBackend:
    def test_missing_api_key_returns_baseline(self, monkeypatch):
        monkeypatch.delenv("OPENAI_COMPAT_API_KEY", raising=False)
        backend = _make_backend(kind="aide")
        result = backend.predict({"role": "aide", "aide_id": "a1"})
        assert result == _aide_baseline()

    def test_predict_avatar_role_uses_avatar_baseline(self, monkeypatch):
        monkeypatch.setenv("OPENAI_COMPAT_API_KEY", "fake-key")
        backend = _make_backend(kind="avatar")
        content = json.dumps({
            "trait_impact": {"difficulty_modifier": 1.2},
            "emotional_state": "calm",
        })
        body = json.dumps({
            "choices": [{"message": {"content": content}}]
        }).encode("utf-8")
        fake_response = MagicMock()
        fake_response.read.return_value = body
        fake_response.__enter__ = lambda self: self
        fake_response.__exit__ = lambda self, *args: None
        with patch("urllib.request.urlopen", return_value=fake_response):
            result = backend.predict({"role": "avatar", "avatar_id": "a1"})
        assert result["trait_impact"]["difficulty_modifier"] == 1.2
        assert result["emotional_state"] == "calm"
        assert result["cognitive_load"] == 0.0

    def test_predict_aide_role_parses_strategy_urgency(self, monkeypatch):
        monkeypatch.setenv("OPENAI_COMPAT_API_KEY", "fake-key")
        backend = _make_backend(kind="aide")
        payload = {
            "strategy": "break task into chunks",
            "urgency": "medium",
            "stress_reduction": 0.5,
        }
        body = json.dumps({
            "choices": [{"message": {"content": json.dumps(payload)}}]
        }).encode("utf-8")
        fake_response = MagicMock()
        fake_response.read.return_value = body
        fake_response.__enter__ = lambda self: self
        fake_response.__exit__ = lambda self, *args: None
        with patch("urllib.request.urlopen", return_value=fake_response):
            result = backend.predict({"role": "aide", "aide_id": "a1"})
        assert result["strategy"] == "break task into chunks"
        assert result["urgency"] == "medium"
        assert result["stress_reduction"] == 0.5
        assert result["coaching_type"] == "preventive"

    def test_predict_non_json_response_falls_back_to_baseline(self, monkeypatch):
        monkeypatch.setenv("OPENAI_COMPAT_API_KEY", "fake-key")
        backend = _make_backend(kind="aide")
        body = json.dumps({
            "choices": [{"message": {"content": "not valid json {{{"}}]
        }).encode("utf-8")
        fake_response = MagicMock()
        fake_response.read.return_value = body
        fake_response.__enter__ = lambda self: self
        fake_response.__exit__ = lambda self, *args: None
        with patch("urllib.request.urlopen", return_value=fake_response):
            result = backend.predict({"role": "aide", "aide_id": "a1"})
        assert result == _aide_baseline()

    def test_predict_http_error_raises_runtime_error(self, monkeypatch):
        monkeypatch.setenv("OPENAI_COMPAT_API_KEY", "fake-key")
        backend = _make_backend(kind="aide")
        err = urllib.error.HTTPError("https://example.invalid/v1/chat/completions", 500, "Server Error", {}, None)
        with patch("urllib.request.urlopen", side_effect=err):
            with pytest.raises(RuntimeError, match="HTTP 500"):
                backend.predict({"role": "aide", "aide_id": "a1"})

    def test_predict_connection_error_raises_runtime_error(self, monkeypatch):
        monkeypatch.setenv("OPENAI_COMPAT_API_KEY", "fake-key")
        backend = _make_backend(kind="aide")
        with patch("urllib.request.urlopen", side_effect=OSError("connection refused")):
            with pytest.raises(RuntimeError, match="request failed"):
                backend.predict({"role": "aide", "aide_id": "a1"})

    def test_update_is_noop(self):
        backend = _make_backend()
        assert backend.update([]) is None

    def test_missing_base_url_raises(self):
        with pytest.raises(ValueError, match="base_url"):
            _make_backend(base_url="")

    def test_predict_non_dict_parsed_falls_back_to_baseline(self, monkeypatch):
        monkeypatch.setenv("OPENAI_COMPAT_API_KEY", "fake-key")
        backend = _make_backend(kind="aide")
        body = json.dumps({
            "choices": [{"message": {"content": '["not", "a", "dict"]'}}]
        }).encode("utf-8")
        fake_response = MagicMock()
        fake_response.read.return_value = body
        fake_response.__enter__ = lambda self: self
        fake_response.__exit__ = lambda self, *args: None
        with patch("urllib.request.urlopen", return_value=fake_response):
            result = backend.predict({"role": "aide", "aide_id": "a1"})
        assert result == _aide_baseline()
