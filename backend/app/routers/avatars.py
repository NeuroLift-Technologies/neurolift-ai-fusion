"""
Avatars Router
CRUD and state management for Avatar instances.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import uuid

router = APIRouter()

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class AvatarCreate(BaseModel):
    trait_name: str
    trait_config: Dict[str, Any] = {}

class AvatarResponse(BaseModel):
    avatar_id: str
    trait_name: str
    trait_config: Dict[str, Any]
    current_state: str
    emotional_state: str
    cognitive_load: float
    stress_level: float
    burnout_risk_level: float
    total_tasks_attempted: int
    total_tasks_completed: int
    total_coaching_sessions: int

class AvatarStateUpdate(BaseModel):
    emotional_state: Optional[str] = None
    cognitive_load: Optional[float] = None
    stress_level: Optional[float] = None

# ---------------------------------------------------------------------------
# In-memory store (replace with Supabase in production)
# ---------------------------------------------------------------------------
_avatars: Dict[str, Dict[str, Any]] = {}

VALID_TRAITS = [
    "stay_alert", "impulse_guard", "focus_flow", "timely", "memory_mate",
    "mood_ease", "task_kickstart", "calm_core", "planner_pro", "smooth_switch",
    "aware_mate", "steady_mind", "focus_recharge", "effort_align",
    "stress_shield", "sensory_balance", "social_sync", "sensory_seeker",
    "confidence_coach",
]

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/", response_model=List[AvatarResponse], summary="List all avatars")
async def list_avatars():
    return list(_avatars.values())


@router.post("/", response_model=AvatarResponse, status_code=201, summary="Create a new avatar")
async def create_avatar(body: AvatarCreate):
    if body.trait_name not in VALID_TRAITS:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown trait '{body.trait_name}'. Valid traits: {VALID_TRAITS}",
        )
    avatar_id = str(uuid.uuid4())
    avatar = {
        "avatar_id": avatar_id,
        "trait_name": body.trait_name,
        "trait_config": body.trait_config,
        "current_state": "idle",
        "emotional_state": "neutral",
        "cognitive_load": 0.0,
        "stress_level": 0.0,
        "burnout_risk_level": 0.0,
        "total_tasks_attempted": 0,
        "total_tasks_completed": 0,
        "total_coaching_sessions": 0,
    }
    _avatars[avatar_id] = avatar
    return avatar


@router.get("/{avatar_id}", response_model=AvatarResponse, summary="Get avatar by ID")
async def get_avatar(avatar_id: str):
    avatar = _avatars.get(avatar_id)
    if not avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    return avatar


@router.patch("/{avatar_id}/state", response_model=AvatarResponse, summary="Update avatar state")
async def update_avatar_state(avatar_id: str, body: AvatarStateUpdate):
    avatar = _avatars.get(avatar_id)
    if not avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    if body.emotional_state is not None:
        avatar["emotional_state"] = body.emotional_state
    if body.cognitive_load is not None:
        avatar["cognitive_load"] = body.cognitive_load
    if body.stress_level is not None:
        avatar["stress_level"] = body.stress_level
    return avatar


@router.delete("/{avatar_id}", status_code=204, summary="Delete avatar")
async def delete_avatar(avatar_id: str):
    if avatar_id not in _avatars:
        raise HTTPException(status_code=404, detail="Avatar not found")
    del _avatars[avatar_id]


@router.get("/traits/list", summary="List all valid ADHD trait names")
async def list_traits():
    return {"traits": VALID_TRAITS}
