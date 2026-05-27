"""Pydantic schemas for the NeuroLift API."""

from __future__ import annotations

from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


# ── Enums ──────────────────────────────────────────────────────────────────────

class AvatarType(str, Enum):
    STAY_ALERT = "stay_alert"
    TASK_KICKSTART = "task_kickstart"


class AideType(str, Enum):
    STAY_ALERT_AIDE = "stay_alert_aide"
    TASK_KICKSTART_AIDE = "task_kickstart_aide"


class SessionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    ABORTED = "aborted"
    FAILED = "failed"


class ScenarioType(str, Enum):
    WORKPLACE = "workplace"
    PERSONAL = "personal"
    SOCIAL = "social"


# ── Avatar ──────────────────────────────────────────────────────────────────────

class AvatarSummary(BaseModel):
    id: str
    type: AvatarType
    display_name: str
    description: str
    traits: list[str]


class AvatarDetail(AvatarSummary):
    config: dict[str, Any] = Field(default_factory=dict)


# ── Aide ────────────────────────────────────────────────────────────────────────

class AideSummary(BaseModel):
    id: str
    type: AideType
    display_name: str
    description: str
    expertise: list[str]


class AideDetail(AideSummary):
    config: dict[str, Any] = Field(default_factory=dict)


# ── Session ─────────────────────────────────────────────────────────────────────

class ScenarioConfig(BaseModel):
    type: ScenarioType = ScenarioType.WORKPLACE
    difficulty: float = Field(0.5, ge=0.0, le=1.0)
    description: str = ""


class SessionCreate(BaseModel):
    avatar_type: AvatarType
    aide_type: AideType
    scenarios: list[ScenarioConfig] = Field(default_factory=list)
    max_attempts_per_scenario: int = Field(10, ge=1, le=50)
    max_coaching_per_attempt: int = Field(3, ge=1, le=10)
    independence_target: float = Field(0.8, ge=0.0, le=1.0)


class ScenarioResult(BaseModel):
    scenario_index: int
    scenario_type: str
    attempts: int
    successes: int
    success_rate: float
    coaching_events: int
    peak_burnout_risk: float
    completed: bool


class SessionResult(BaseModel):
    session_id: UUID
    status: SessionStatus
    avatar_type: AvatarType
    aide_type: AideType
    scenario_results: list[ScenarioResult] = Field(default_factory=list)
    overall_success_rate: float = 0.0
    final_independence_level: float = 0.0
    peak_burnout_risk: float = 0.0
    fusion_ready: bool = False
    duration_seconds: float = 0.0
    error: str | None = None


class SessionSummary(BaseModel):
    session_id: UUID
    status: SessionStatus
    avatar_type: AvatarType
    aide_type: AideType
    created_at: str


# ── Advocate ─────────────────────────────────────────────────────────────────────

class AdvocateSummary(BaseModel):
    id: str
    display_name: str
    avatar_type: AvatarType
    aide_type: AideType
    fusion_score: float
