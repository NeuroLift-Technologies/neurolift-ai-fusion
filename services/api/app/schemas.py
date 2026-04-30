"""Pydantic schemas for the simulation API."""

from typing import Any, Dict, List
from pydantic import BaseModel, Field


class ScenarioInput(BaseModel):
    """Scenario payload accepted by API session endpoints."""

    name: str = Field(..., description="Scenario name")
    task_type: str = Field(default="focus_task")
    base_success_rate: float = Field(default=0.5, ge=0.0, le=1.0)
    cognitive_demand: float = Field(default=0.6, ge=0.0, le=1.0)


class SessionRunRequest(BaseModel):
    """Request model for running a session."""

    avatar_id: str = Field(default="stay_alert_api")
    aide_id: str = Field(default="stay_alert_aide_api")
    scenarios: List[ScenarioInput]


class SessionRunResponse(BaseModel):
    """Response model for API session runs."""

    session_id: str
    avatar_id: str
    aide_id: str
    total_attempts: int
    total_successes: int
    total_coaching: int
    success_rate: float
    final_independence: float
    fusion_ready: bool
    scenarios: List[Dict[str, Any]]
