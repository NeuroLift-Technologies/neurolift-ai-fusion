"""Fusion -> world-engine state feed serialization.

This module produces the renderer-facing state feed described in
`nlt-world-engine/docs/contracts/state-feed-v1.md`. The contract is intentionally
one-way: Fusion owns the semantic model and the renderer only consumes the feed.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from src.aides.base_aide import BaseAide
from src.avatars.base_avatar import BaseAvatar
from src.fusion.readiness_assessor import FusionDimension, ReadinessAssessor


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _translate_state(avatar: BaseAvatar) -> str:
    mapping = {
        "idle": "settled",
        "attempting_task": "drifting",
        "struggling": "resisting",
        "receiving_coaching": "coached",
        "applying_strategy": "coached",
        "learning": "settled",
        "independent": "settled",
        "burnout_risk": "overwhelmed",
        "burnout": "overwhelmed",
        "recovering": "recovering",
    }
    return mapping.get(avatar.current_state.value, "settled")


def _compute_levels(avatar: BaseAvatar) -> Dict[str, float]:
    independence = _clamp(float(avatar.get_independence_level()))
    stress = _clamp(float(getattr(avatar, "stress_level", 0.0)))
    burnout = _clamp(float(getattr(avatar, "burnout_risk_level", 0.0)))
    cognitive = _clamp(float(getattr(avatar, "cognitive_load", 0.0)))
    confidence = _clamp((independence * 0.7) + ((1.0 - stress) * 0.3))
    attention = _clamp((1.0 - stress) * 0.6 + independence * 0.4)
    support_need = _clamp((1.0 - independence) * 0.7 + burnout * 0.3)

    return {
        "attentionEnergy": attention,
        "stressLevel": stress,
        "confidence": confidence,
        "cognitiveLoad": cognitive,
        "independenceScore": independence,
        "supportNeedLevel": support_need,
    }


def _compute_needs(avatar: BaseAvatar) -> Dict[str, float]:
    stress = _clamp(float(getattr(avatar, "stress_level", 0.0)))
    cognitive = _clamp(float(getattr(avatar, "cognitive_load", 0.0)))
    independence = _clamp(float(avatar.get_independence_level()))
    return {
        "quiet": _clamp(1.0 - stress),
        "rest": _clamp(1.0 - (stress * 0.8 + (1.0 - independence) * 0.2)),
        "social": _clamp(0.5 + (1.0 - stress) * 0.4),
        "stimulation": _clamp(0.5 + cognitive * 0.5),
    }


def _build_pair_projection(avatar: BaseAvatar, aide: BaseAide) -> Dict[str, Any]:
    previous_risk = getattr(avatar, "burnout_risk_level", 0.0)
    try:
        readiness = ReadinessAssessor().assess(avatar, aide)
    finally:
        setattr(avatar, "burnout_risk_level", previous_risk)

    dims: Dict[str, Any] = {}
    for dimension in FusionDimension:
        score = readiness.dimension_scores.get(dimension)
        if score is None:
            continue
        dims[dimension.name] = {
            "score": round(_clamp(float(score.score)), 3),
            "passes": bool(score.passes),
        }

    return {
        "avatarId": avatar.avatar_id,
        "aideId": aide.aide_id,
        "ready": bool(readiness.ready),
        "overallScore": round(_clamp(float(readiness.overall_score)), 3),
        "blockingDimensions": [d.name for d in readiness.blocking_dimensions],
        "dimensions": dims,
        "recommendations": list(readiness.recommendations),
    }


def _build_events(
    avatar: BaseAvatar, aide: BaseAide, tick: int
) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    for action in getattr(aide, "intervention_history", []):
        helped = getattr(action, "helped", None)
        occurred_at = getattr(action, "timestamp", None)
        event_id = getattr(action, "action_id", None)
        if helped is None:
            continue
        if not isinstance(helped, bool):
            raise TypeError("intervention helped outcome must be boolean or None")
        if not isinstance(occurred_at, datetime):
            raise TypeError("intervention timestamp must be a datetime")
        if not isinstance(event_id, str) or not event_id:
            raise ValueError("intervention action_id is required for event identity")

        occurred_at_iso = (
            occurred_at.astimezone(timezone.utc)
            .replace(microsecond=0)
            .strftime("%Y-%m-%dT%H:%M:%SZ")
        )
        strategy = getattr(action, "strategy", "") or "general_coaching"
        text = getattr(action, "description", "") or (
            f"{avatar.avatar_id} received a coaching intervention using {strategy}."
        )
        events.append(
            {
                "eventId": event_id,
                "occurredAt": occurred_at_iso,
                "tick": tick,
                "agentId": avatar.avatar_id,
                "kind": "aide_intervention",
                "text": text,
                "strategy": strategy,
                "helped": helped,
            }
        )
    return events


def _build_struggle_signals(avatar: BaseAvatar) -> List[str]:
    patterns = getattr(avatar, "struggle_patterns", []) or []
    if not patterns or not isinstance(patterns[-1], dict):
        return []
    indicators = patterns[-1].get("indicators", [])
    if not isinstance(indicators, list):
        return []
    return [indicator for indicator in indicators if isinstance(indicator, str)]


def _is_active_burnout_episode(episode: Dict[str, Any]) -> bool:
    return episode.get("recoveredTick") is None


def build_state_feed(
    avatar: BaseAvatar,
    aide: BaseAide,
    *,
    tick: int = 0,
    scene_id: str = "open_world",
    scene_kind: str = "open_world",
    sim_time_iso: Optional[str] = None,
    burnout_episodes: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Build a renderer-facing state feed from a Fusion Avatar-Aide pair.

    The output intentionally matches the contract shape published in
    `nlt-world-engine/docs/contracts/state-feed-v1.md`, while remaining safe for the
    renderer to consume without needing to derive semantic state itself.

    Burnout episodes are supplied from authoritative episode history. Burnout risk alone
    is not enough to reconstruct their start, peak, or recovery ticks.
    """

    if sim_time_iso is None:
        sim_time_iso = (
            datetime.now(timezone.utc)
            .replace(microsecond=0)
            .strftime("%Y-%m-%dT%H:%M:%SZ")
        )

    levels = _compute_levels(avatar)
    needs = _compute_needs(avatar)
    pair = _build_pair_projection(avatar, aide)
    experience_memory = getattr(avatar, "experience_memory", None)
    episodes = list(burnout_episodes or [])

    return {
        "schemaVersion": "nlt.state-feed.v1",
        "tick": int(tick),
        "simTimeIso": sim_time_iso,
        "scene": {"id": scene_id, "kind": scene_kind},
        "agents": [
            {
                "id": avatar.avatar_id,
                "name": getattr(avatar, "trait_name", avatar.avatar_id),
                "role": "avatar",
                "scene": scene_id,
                "position": {"x": 0.0, "y": 0.0, "z": 0.0},
                "velocity": {"x": 0.0, "y": 0.0, "z": 0.0},
                "appearance": {
                    "body": getattr(avatar, "trait_name", "avatar_base"),
                    "walkPhase": 0.0,
                },
                "levels": levels,
                "needs": needs,
                "state": _translate_state(avatar),
                "stateSince": tick,
                "currentGoal": "Build task competence",
                "currentTask": "Maintain attention amid cognitive load",
                "struggleSignals": _build_struggle_signals(avatar),
                "learnedStrategies": list(
                    experience_memory.get_effective_strategies()
                    if experience_memory is not None
                    else []
                ),
                "burnout": any(_is_active_burnout_episode(e) for e in episodes),
                "supportIndex": None,
            }
        ],
        "pairs": [pair],
        "burnoutEpisodes": episodes,
        "selfRecognitions": [],
        "events": _build_events(avatar, aide, tick),
    }
