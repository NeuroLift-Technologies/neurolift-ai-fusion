"""
Training Sessions Router
Start, monitor, and retrieve training sessions.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

router = APIRouter()

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class SessionCreate(BaseModel):
    avatar_id: str
    aide_id: str
    scenario_id: str
    session_type: str = "standard"

class TaskResultPayload(BaseModel):
    success: bool
    quality_score: float
    struggle_indicators: List[str] = []
    aide_interventions: List[str] = []
    emotional_state: str = "neutral"
    cognitive_load: float = 0.0

class SessionResponse(BaseModel):
    session_id: str
    avatar_id: str
    aide_id: str
    scenario_id: str
    session_type: str
    status: str
    started_at: str
    ended_at: Optional[str]
    task_results: List[Dict[str, Any]]
    coaching_actions: List[Dict[str, Any]]

# ---------------------------------------------------------------------------
# In-memory store
# ---------------------------------------------------------------------------
_sessions: Dict[str, Dict[str, Any]] = {}

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/", response_model=List[SessionResponse], summary="List all sessions")
async def list_sessions(avatar_id: Optional[str] = None):
    sessions = list(_sessions.values())
    if avatar_id:
        sessions = [s for s in sessions if s["avatar_id"] == avatar_id]
    return sessions


@router.post("/", response_model=SessionResponse, status_code=201, summary="Start a new training session")
async def create_session(body: SessionCreate):
    session_id = str(uuid.uuid4())
    session = {
        "session_id": session_id,
        "avatar_id": body.avatar_id,
        "aide_id": body.aide_id,
        "scenario_id": body.scenario_id,
        "session_type": body.session_type,
        "status": "active",
        "started_at": datetime.utcnow().isoformat(),
        "ended_at": None,
        "task_results": [],
        "coaching_actions": [],
    }
    _sessions[session_id] = session
    return session


@router.get("/{session_id}", response_model=SessionResponse, summary="Get session by ID")
async def get_session(session_id: str):
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/{session_id}/task-result", response_model=SessionResponse, summary="Record a task result")
async def record_task_result(session_id: str, body: TaskResultPayload):
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session["status"] != "active":
        raise HTTPException(status_code=409, detail="Session is not active")
    result = {
        "attempt": len(session["task_results"]) + 1,
        "success": body.success,
        "quality_score": body.quality_score,
        "struggle_indicators": body.struggle_indicators,
        "aide_interventions": body.aide_interventions,
        "emotional_state": body.emotional_state,
        "cognitive_load": body.cognitive_load,
        "recorded_at": datetime.utcnow().isoformat(),
    }
    session["task_results"].append(result)
    return session


@router.post("/{session_id}/complete", response_model=SessionResponse, summary="Complete a session")
async def complete_session(session_id: str):
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session["status"] = "completed"
    session["ended_at"] = datetime.utcnow().isoformat()
    return session


@router.delete("/{session_id}", status_code=204, summary="Delete session")
async def delete_session(session_id: str):
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    del _sessions[session_id]
