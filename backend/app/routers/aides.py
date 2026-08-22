"""
Aides Router
CRUD for Aide coaching instances.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import uuid

from src.ai.registry import get_registry

router = APIRouter()


class ModelBind(BaseModel):
    """Bind a model backend to an avatar/aide."""
    type: str
    checkpoint_path: Optional[str] = None
    model_name: Optional[str] = None
    base_url: Optional[str] = None
    api_key_env: Optional[str] = None

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class AideCreate(BaseModel):
    expertise_area: str
    expertise_config: Dict[str, Any] = {}

class AideResponse(BaseModel):
    aide_id: str
    expertise_area: str
    expertise_config: Dict[str, Any]
    total_interventions: int
    successful_interventions: int
    crisis_interventions: int
    independence_achievements: int

# ---------------------------------------------------------------------------
# In-memory store
# ---------------------------------------------------------------------------
_aides: Dict[str, Dict[str, Any]] = {}

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/", response_model=List[AideResponse], summary="List all aides")
async def list_aides():
    return list(_aides.values())


@router.post("/", response_model=AideResponse, status_code=201, summary="Create a new aide")
async def create_aide(body: AideCreate):
    aide_id = str(uuid.uuid4())
    aide = {
        "aide_id": aide_id,
        "expertise_area": body.expertise_area,
        "expertise_config": body.expertise_config,
        "total_interventions": 0,
        "successful_interventions": 0,
        "crisis_interventions": 0,
        "independence_achievements": 0,
    }
    _aides[aide_id] = aide
    return aide


@router.get("/{aide_id}", response_model=AideResponse, summary="Get aide by ID")
async def get_aide(aide_id: str):
    aide = _aides.get(aide_id)
    if not aide:
        raise HTTPException(status_code=404, detail="Aide not found")
    return aide


@router.delete("/{aide_id}", status_code=204, summary="Delete aide")
async def delete_aide(aide_id: str):
    if aide_id not in _aides:
        raise HTTPException(status_code=404, detail="Aide not found")
    del _aides[aide_id]


@router.post("/{aide_id}/bind-model", summary="Bind a model backend to an aide")
async def bind_aide_model(aide_id: str, body: ModelBind):
    reg = get_registry()
    backend = reg.build_backend({
        "type": body.type,
        "kind": "aide",
        "checkpoint_path": body.checkpoint_path,
        "model_name": body.model_name,
        "base_url": body.base_url,
        "api_key_env": body.api_key_env,
    })
    reg.register(aide_id, backend)
    reg.bind_config(aide_id, body.model_dump())
    return backend.to_metadata()


@router.delete("/{aide_id}/model", summary="Unbind a model from an aide")
async def unbind_aide_model(aide_id: str):
    reg = get_registry()
    reg.unregister(aide_id)
    return {"aide_id": aide_id, "status": "unbound"}
