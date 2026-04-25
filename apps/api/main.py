"""NeuroLift AI Fusion — FastAPI backend.

Exposes the Avatar-Aide-Advocate simulation engine over HTTP/WebSocket.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import avatars, aides, sessions, advocates


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="NeuroLift AI Fusion API",
    description="Avatar-Aide-Advocate training platform API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(avatars.router, prefix="/api/v1/avatars", tags=["avatars"])
app.include_router(aides.router, prefix="/api/v1/aides", tags=["aides"])
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["sessions"])
app.include_router(advocates.router, prefix="/api/v1/advocates", tags=["advocates"])


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "neurolift-api"}
