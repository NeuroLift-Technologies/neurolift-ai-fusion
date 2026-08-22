"""Pydantic schemas for the simulation API."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ScenarioInput(BaseModel):
    """Scenario payload accepted by API session endpoints."""

    name: str = Field(..., description="Scenario name")
    task_type: str = Field(default="focus_task")
    base_success_rate: float = Field(default=0.5, ge=0.0, le=1.0)
    cognitive_demand: float = Field(default=0.6, ge=0.0, le=1.0)


class ModelBindConfig(BaseModel):
    """Configuration for binding a model backend to an avatar/aide."""

    type: str  # rule_fallback | transformer | openai_compat
    kind: Optional[str] = None
    checkpoint_path: Optional[str] = None
    model_name: Optional[str] = None
    base_url: Optional[str] = None
    api_key_env: Optional[str] = None


class SessionRunRequest(BaseModel):
    """Request model for running a session."""

    model_config = ConfigDict(populate_by_name=True)

    avatar_id: str = Field(default="stay_alert_api")
    aide_id: str = Field(default="stay_alert_aide_api")
    scenarios: List[ScenarioInput]
    ai_config: Optional[Dict[str, Any]] = Field(default=None, alias="model_config")


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
    model_versions: Dict[str, str] = Field(default_factory=dict)
    scenarios: List[Dict[str, Any]]
