"""FastAPI entrypoint for NeuroLift simulation sessions."""

from fastapi import FastAPI

from .schemas import SessionRunRequest, SessionRunResponse
from .session_service import DEFAULT_SCENARIOS, run_session

app = FastAPI(title="NeuroLift Simulation API", version="0.1.0")


@app.get("/health")
def health() -> dict:
    """Liveness endpoint for clients and orchestration checks."""
    return {"status": "ok", "service": "simulation-api"}


@app.get("/sessions/demo-run", response_model=SessionRunResponse)
def demo_run() -> dict:
    """Run a deterministic demo session using default scenarios."""
    return run_session(DEFAULT_SCENARIOS)


@app.post("/sessions/run", response_model=SessionRunResponse)
def run(payload: SessionRunRequest) -> dict:
    """Run a session with caller-provided scenario inputs."""
    serialized_scenarios = [scenario.model_dump() for scenario in payload.scenarios]
    return run_session(
        scenarios=serialized_scenarios,
        avatar_id=payload.avatar_id,
        aide_id=payload.aide_id,
        model_config=payload.ai_config,
    )
