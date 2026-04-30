"""Application service layer for simulation session runs."""

from typing import Any, Dict, List

from src.aides.executive_function_expertise.attention_coaching import AttentionCoaching
from src.avatars.adhd_traits.stay_alert_avatar import StayAlertAvatar
from src.simulation.session_orchestrator import SessionConfig, SessionOrchestrator


DEFAULT_SCENARIOS: List[Dict[str, Any]] = [
    {
        "name": "Morning planning sprint",
        "task_type": "planning",
        "base_success_rate": 0.55,
        "cognitive_demand": 0.65,
    },
    {
        "name": "Inbox triage",
        "task_type": "email_management",
        "base_success_rate": 0.50,
        "cognitive_demand": 0.60,
    },
]


def run_session(
    scenarios: List[Dict[str, Any]],
    avatar_id: str = "stay_alert_api",
    aide_id: str = "stay_alert_aide_api",
) -> Dict[str, Any]:
    """Run a simulation session and return serialized results."""
    avatar = StayAlertAvatar(
        avatar_id=avatar_id,
        trait_config={
            "attention_duration": 12,
            "drift_probability": 0.35,
            "hyperfocus_tendency": 0.2,
        },
    )
    aide = AttentionCoaching(
        aide_id=aide_id,
        expertise_config={"expertise_area": "sustained_attention"},
    )

    orchestrator = SessionOrchestrator(
        avatar=avatar,
        aide=aide,
        config=SessionConfig(max_attempts_per_scenario=4, max_coaching_per_attempt=2),
    )

    result = orchestrator.run_session(scenarios or DEFAULT_SCENARIOS)
    return result.to_dict()
