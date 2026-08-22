"""Tests for the AI model backend routers (bind/unbind + training + status)."""

import os
import sys
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))
sys.path.insert(0, str(_PROJECT_ROOT / "backend"))

from backend.app.main import app
from src.ai.registry import get_registry


@pytest.fixture
def client():
    # Keep any checkpoints out of the repo data dir.
    tmp = tempfile.mkdtemp()
    os.environ["NEUROLIFT_MODELS_DIR"] = tmp
    with TestClient(app) as c:
        yield c
    os.environ.pop("NEUROLIFT_MODELS_DIR", None)
    # Clean up any global registry state created during the test.
    reg = get_registry()
    for rid in ("test_avatar_x", "test_aide_x", "orch_avatar", "orch_aide"):
        reg.unregister(rid)


@pytest.mark.ai
class TestAvatarModelBind:
    def test_bind_and_unbind(self, client):
        resp = client.post(
            "/api/avatars/test_avatar_x/bind-model",
            json={"type": "rule_fallback"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["model_id"] == "rule_fallback"
        assert data["kind"] == "avatar"

        resp = client.delete("/api/avatars/test_avatar_x/model")
        assert resp.status_code == 200
        assert resp.json()["status"] == "unbound"


@pytest.mark.ai
class TestAideModelBind:
    def test_bind_and_unbind(self, client):
        resp = client.post(
            "/api/aides/test_aide_x/bind-model",
            json={"type": "rule_fallback"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["model_id"] == "rule_fallback"
        assert data["kind"] == "aide"

        resp = client.delete("/api/aides/test_aide_x/model")
        assert resp.status_code == 200
        assert resp.json()["status"] == "unbound"


@pytest.mark.ai
class TestAIModelRouter:
    def test_status(self, client):
        resp = client.get("/api/ai/status")
        assert resp.status_code == 200
        data = resp.json()
        assert "models" in data
        assert "configs" in data
        assert "last_training" in data
        assert "metrics" in data

    def test_train_async(self, client):
        resp = client.post(
            "/api/ai/train",
            json={"avatar_id": None, "aide_id": None},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "training_started"
