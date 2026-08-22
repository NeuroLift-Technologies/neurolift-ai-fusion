"""Tests for the services/api FastAPI app (session run + model_config)."""

import os
import sys
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from services.api.app.main import app
from src.ai.registry import get_registry


@pytest.fixture
def client():
    tmp = tempfile.mkdtemp()
    os.environ["NEUROLIFT_MODELS_DIR"] = tmp
    with TestClient(app) as c:
        yield c
    os.environ.pop("NEUROLIFT_MODELS_DIR", None)
    reg = get_registry()
    reg.unregister("stay_alert_api")
    reg.unregister("stay_alert_aide_api")


@pytest.mark.ai
class TestSessionRunWithModelConfig:
    def test_run_with_model_config_returns_versions(self, client):
        resp = client.post(
            "/sessions/run",
            json={
                "scenarios": [
                    {
                        "name": "Focus drill",
                        "task_type": "focus_task",
                        "base_success_rate": 0.6,
                        "cognitive_demand": 0.5,
                    }
                ],
                "model_config": {
                    "avatar": {"type": "rule_fallback"},
                    "aide": {"type": "rule_fallback"},
                },
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["model_versions"]["stay_alert_api"] == "0.1.0"
        assert data["model_versions"]["stay_alert_aide_api"] == "0.1.0"

    def test_demo_run_returns_200(self, client):
        resp = client.get("/sessions/demo-run")
        assert resp.status_code == 200
        assert "model_versions" in resp.json()
