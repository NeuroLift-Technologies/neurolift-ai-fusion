"""Tests for the full-stack API session service."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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
