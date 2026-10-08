"""Fusion -> world-engine state feed serialization.

This module produces the renderer-facing state feed described in
`nlt-world-engine/docs/contracts/state-feed-v1.md`. The contract is intentionally
one-way: Fusion owns the semantic model and the renderer only consumes the feed.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

from ..avatars.base_avatar import BaseAvatar
from ..aides.base_aide import BaseAide
from .readiness_assessor import FusionDimension, ReadinessAssessor


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


def _build_events(avatar: BaseAvatar, aide: BaseAide, tick: int) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    for action in getattr(aide, "intervention_history", []):
        strategy = getattr(action, "strategy", "") or "general_coaching"
        text = getattr(action, "description", "") or (
            f"{avatar.avatar_id} received a coaching intervention using {strategy}."
        )
        events.append({
            "tick": tick,
            "agentId": avatar.avatar_id,
            "kind": "aide_intervention",
            "text": text,
            "strategy": strategy,
            "helped": True,
        })
    return events


def _build_burnout_episodes(avatar: BaseAvatar, tick: int) -> List[Dict[str, Any]]:
    risk = _clamp(float(getattr(avatar, "burnout_risk_level", 0.0)))
    if risk < 0.4:
        return []
    return [{
        "startTick": int(tick),
        "severity": round(risk, 3),
        "peakBelow": round(_clamp(max(0.0, 1.0 - risk), 0.0, 1.0), 3),
        "recoveredTick": None,
        "recoveryMode": None,
    }]


def build_state_feed(
    avatar: BaseAvatar,
    aide: BaseAide,
    *,
    tick: int = 0,
    scene_id: str = "open_world",
    scene_kind: str = "open_world",
    sim_time_iso: Optional[str] = None,
) -> Dict[str, Any]:
    """Build a renderer-facing state feed from a Fusion Avatar-Aide pair.

    The output intentionally matches the contract shape published in
    `nlt-world-engine/docs/contracts/state-feed-v1.md`, while remaining safe for the
    renderer to consume without needing to derive semantic state itself.
    """

    if sim_time_iso is None:
        sim_time_iso = datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")

    levels = _compute_levels(avatar)
    needs = _compute_needs(avatar)
    pair = _build_pair_projection(avatar, aide)

    return {
        "schemaVersion": "nlt.state-feed.v1",
        "tick": int(tick),
        "simTimeIso": sim_time_iso,
        "scene": {"id": scene_id, "kind": scene_kind},
        "agents": [{
            "id": avatar.avatar_id,
            "name": getattr(avatar, "trait_name", avatar.avatar_id),
            "role": "avatar",
            "scene": scene_id,
            "position": {"x": 0.0, "y": 0.0, "z": 0.0},
            "velocity": {"x": 0.0, "y": 0.0, "z": 0.0},
            "appearance": {"body": getattr(avatar, "trait_name", "avatar_base"), "walkPhase": 0.0},
            "levels": levels,
            "needs": needs,
            "state": _translate_state(avatar),
            "stateSince": tick,
            "currentGoal": "Build task competence",
            "currentTask": "Maintain attention amid cognitive load",
            "struggleSignals": list(getattr(avatar, "struggle_patterns", []) or []),
            "learnedStrategies": list(getattr(avatar, "experience_memory", None).get_effective_strategies() if getattr(avatar, "experience_memory", None) is not None else []),
            "burnout": bool(getattr(avatar, "burnout_risk_level", 0.0) >= 0.6),
            "supportIndex": 0,
        }],
        "pairs": [pair],
        "burnoutEpisodes": _build_burnout_episodes(avatar, tick),
        "selfRecognitions": [],
        "events": _build_events(avatar, aide, tick),
    }
