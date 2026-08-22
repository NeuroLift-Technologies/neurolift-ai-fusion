"""Tests for the full-stack API session service."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ai.registry import get_registry

from services.api.app.session_service import run_session


def test_run_session_returns_serializable_payload() -> None:
    scenarios = [
        {
            "name": "Quick focus drill",
            "task_type": "focus_task",
            "base_success_rate": 0.6,
            "cognitive_demand": 0.5,
        }
    ]

    payload = run_session(scenarios=scenarios)

    assert payload["avatar_id"] == "stay_alert_api"
    assert payload["aide_id"] == "stay_alert_aide_api"
    assert payload["session_id"]
    assert payload["total_attempts"] >= 1
    assert isinstance(payload["scenarios"], list)
    assert payload["scenarios"][0]["name"] == "Quick focus drill"


def test_run_session_with_model_config_binds_and_returns_versions() -> None:
    scenarios = [
        {
            "name": "Quick focus drill",
            "task_type": "focus_task",
            "base_success_rate": 0.6,
            "cognitive_demand": 0.5,
        }
    ]
    model_config = {
        "avatar": {"type": "rule_fallback"},
        "aide": {"type": "rule_fallback"},
    }
    payload = run_session(scenarios=scenarios, model_config=model_config)

    # Rule-based model versions are collected into the result.
    assert "model_versions" in payload
    assert payload["model_versions"].get("stay_alert_api") == "0.1.0"
    assert payload["model_versions"].get("stay_alert_aide_api") == "0.1.0"
    assert payload["total_attempts"] >= 1

    # Avoid leaking the globally-registered backends into other tests.
    reg = get_registry()
    reg.unregister("stay_alert_api")
    reg.unregister("stay_alert_aide_api")


def test_run_session_default_has_empty_model_versions() -> None:
    payload = run_session(scenarios=[])
    assert payload["model_versions"] == {}


def test_run_session_with_train_flag_builds_pipeline() -> None:
    scenarios = [
        {
            "name": "Quick focus drill",
            "task_type": "focus_task",
            "base_success_rate": 0.6,
            "cognitive_demand": 0.5,
        }
    ]
    model_config = {
        "avatar": {"type": "rule_fallback"},
        "aide": {"type": "rule_fallback"},
        "train": True,
    }
    payload = run_session(scenarios=scenarios, model_config=model_config)
    # train=True builds a TrainingPipeline; the session still completes.
    assert payload["total_attempts"] >= 1
    assert payload["model_versions"].get("stay_alert_api") == "0.1.0"

    reg = get_registry()
    reg.unregister("stay_alert_api")
    reg.unregister("stay_alert_aide_api")
