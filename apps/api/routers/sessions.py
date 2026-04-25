"""Session endpoints — create, run, and query training sessions."""

from __future__ import annotations

import asyncio
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException, WebSocket, WebSocketDisconnect

from schemas.models import (
    AvatarType,
    ScenarioResult,
    SessionCreate,
    SessionResult,
    SessionStatus,
    SessionSummary,
)

router = APIRouter()

# In-memory session store (replace with Supabase persistence as needed)
_sessions: dict[UUID, SessionResult] = {}
_summaries: dict[UUID, SessionSummary] = {}

# Per-session asyncio.Events so WebSocket handlers wake up on state changes
# instead of polling with sleep(1). Supports one active WS listener per session.
_session_events: dict[UUID, asyncio.Event] = {}


def _resolve_src_path() -> None:
    """Ensure the repo root is in sys.path so ``import src.*`` works.

    In Docker, PYTHONPATH=/app covers this. Locally, we walk up the directory
    tree to find the first ancestor that contains ``src/__init__.py``.
    """
    try:
        import src  # noqa: F401  — already importable, nothing to do
        return
    except ImportError:
        pass
    for parent in Path(__file__).resolve().parents:
        if (parent / "src" / "__init__.py").exists():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return


def _notify_update(session_id: UUID, loop: asyncio.AbstractEventLoop) -> None:
    """Wake the WebSocket handler for this session (called from a worker thread)."""
    event = _session_events.get(session_id)
    if event is not None:
        loop.call_soon_threadsafe(event.set)


def _run_session(
    session_id: UUID,
    payload: SessionCreate,
    loop: asyncio.AbstractEventLoop,
) -> None:
    """Execute a training session in a thread-pool worker (sync, non-blocking)."""
    session = _sessions[session_id]

    try:
        _resolve_src_path()

        from src.avatars.stay_alert_avatar import StayAlertAvatar  # type: ignore[import]
        from src.avatars.task_kickstart_avatar import TaskKickstartAvatar  # type: ignore[import]
        from src.aides.coaching.stay_alert_aide import StayAlertAide  # type: ignore[import]
        from src.simulation.session_orchestrator import SessionOrchestrator, SessionConfig  # type: ignore[import]

        avatar_map = {
            AvatarType.STAY_ALERT: StayAlertAvatar,
            AvatarType.TASK_KICKSTART: TaskKickstartAvatar,
        }
        aide_map = {
            AvatarType.STAY_ALERT: StayAlertAide,
            AvatarType.TASK_KICKSTART: StayAlertAide,
        }

        AvatarClass = avatar_map[payload.avatar_type]
        AideClass = aide_map[payload.avatar_type]

        avatar = AvatarClass()
        aide = AideClass()

        cfg = SessionConfig(
            max_attempts_per_scenario=payload.max_attempts_per_scenario,
            max_coaching_per_attempt=payload.max_coaching_per_attempt,
            independence_target=payload.independence_target,
        )
        orchestrator = SessionOrchestrator(avatar=avatar, aide=aide, config=cfg)

        scenarios = [
            {"type": s.type.value, "difficulty": s.difficulty, "description": s.description}
            for s in payload.scenarios
        ] or [{"type": "workplace", "difficulty": 0.5, "description": "Default scenario"}]

        start = time.monotonic()
        result = orchestrator.run_session(scenarios=scenarios)
        elapsed = time.monotonic() - start

        scenario_results = []
        for i, sr in enumerate(getattr(result, "scenario_results", [])):
            scenario_results.append(
                ScenarioResult(
                    scenario_index=i,
                    scenario_type=getattr(sr, "scenario_type", "unknown"),
                    attempts=getattr(sr, "total_attempts", 0),
                    successes=getattr(sr, "successful_attempts", 0),
                    success_rate=getattr(sr, "success_rate", 0.0),
                    coaching_events=getattr(sr, "coaching_count", 0),
                    peak_burnout_risk=getattr(sr, "peak_burnout_risk", 0.0),
                    completed=getattr(sr, "completed", False),
                )
            )

        session.status = SessionStatus.COMPLETED
        session.scenario_results = scenario_results
        session.overall_success_rate = getattr(result, "overall_success_rate", 0.0)
        session.final_independence_level = getattr(result, "final_independence_level", 0.0)
        session.peak_burnout_risk = getattr(result, "peak_burnout_risk", 0.0)
        session.fusion_ready = getattr(result, "fusion_ready", False)
        session.duration_seconds = elapsed

    except Exception as exc:
        session.status = SessionStatus.FAILED
        session.error = str(exc)

    _sessions[session_id] = session
    _notify_update(session_id, loop)


@router.post("/", response_model=SessionSummary, status_code=201)
async def create_session(
    payload: SessionCreate,
    background_tasks: BackgroundTasks,
) -> SessionSummary:
    session_id = uuid4()
    now = datetime.now(timezone.utc).isoformat()

    result = SessionResult(
        session_id=session_id,
        status=SessionStatus.RUNNING,
        avatar_type=payload.avatar_type,
        aide_type=payload.aide_type,
    )
    summary = SessionSummary(
        session_id=session_id,
        status=SessionStatus.RUNNING,
        avatar_type=payload.avatar_type,
        aide_type=payload.aide_type,
        created_at=now,
    )
    _sessions[session_id] = result
    _summaries[session_id] = summary

    loop = asyncio.get_running_loop()
    background_tasks.add_task(_run_session, session_id, payload, loop)
    return summary


@router.get("/", response_model=list[SessionSummary])
async def list_sessions() -> list[SessionSummary]:
    return list(_summaries.values())


@router.get("/{session_id}", response_model=SessionResult)
async def get_session(session_id: UUID) -> SessionResult:
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.delete("/{session_id}", status_code=204)
async def delete_session(session_id: UUID) -> None:
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    _sessions.pop(session_id, None)
    _summaries.pop(session_id, None)
    _session_events.pop(session_id, None)


@router.websocket("/{session_id}/ws")
async def session_ws(websocket: WebSocket, session_id: UUID) -> None:
    """Stream session status updates, pushing only on state changes."""
    await websocket.accept()

    event = asyncio.Event()
    _session_events[session_id] = event

    try:
        while True:
            session = _sessions.get(session_id)
            if session is None:
                await websocket.send_json({"error": "Session not found"})
                break

            await websocket.send_json(session.model_dump(mode="json"))

            if session.status in (SessionStatus.COMPLETED, SessionStatus.FAILED, SessionStatus.ABORTED):
                break

            # Block until _notify_update() wakes us (no sleep polling)
            event.clear()
            await event.wait()

    except WebSocketDisconnect:
        pass
    finally:
        _session_events.pop(session_id, None)
