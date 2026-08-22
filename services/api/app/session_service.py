"""Application service layer for simulation session runs."""

from typing import Any, Dict, List, Optional

from src.ai.registry import get_registry
from src.ai.trainer import TrainingPipeline
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
    model_config: Optional[Dict[str, Any]] = None,
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

    if model_config:
        reg = get_registry()
        av_cfg = model_config.get("avatar") or {}
        ai_cfg = model_config.get("aide") or {}
        if av_cfg.get("type"):
            backend = reg.build_backend({**av_cfg, "kind": "avatar"})
            avatar.bind_model(backend)
            reg.register(avatar.avatar_id, backend)
        if ai_cfg.get("type"):
            backend = reg.build_backend({**ai_cfg, "kind": "aide"})
            aide.bind_model(backend)
            reg.register(aide.aide_id, backend)

    auto_train = bool(model_config.get("auto_train")) if model_config else False
    train = bool(model_config.get("train")) if model_config else False
    pipeline = TrainingPipeline(registry=get_registry()) if (auto_train or train) else None

    orchestrator = SessionOrchestrator(
        avatar=avatar,
        aide=aide,
        config=SessionConfig(max_attempts_per_scenario=4, max_coaching_per_attempt=2),
        training_pipeline=pipeline,
        auto_train=auto_train,
    )

    result = orchestrator.run_session(scenarios or DEFAULT_SCENARIOS)
    return result.to_dict()
