"""
NeuroLift AI-Fusion — FastAPI Backend
Exposes the simulation engine as a REST API consumed by the web and mobile apps.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import avatars, aides, sessions, fusion, scenarios, health

app = FastAPI(
    title="NeuroLift AI-Fusion API",
    description=(
        "REST API for the NeuroLift simulation training environment. "
        "Manages Avatars, Aides, training sessions, and the Avatar→Advocate fusion process."
    ),
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# ---------------------------------------------------------------------------
# CORS — allow the web app and mobile apps to call the API
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(avatars.router, prefix="/api/avatars", tags=["Avatars"])
app.include_router(aides.router, prefix="/api/aides", tags=["Aides"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["Training Sessions"])
app.include_router(fusion.router, prefix="/api/fusion", tags=["Fusion"])
app.include_router(scenarios.router, prefix="/api/scenarios", tags=["Scenarios"])
