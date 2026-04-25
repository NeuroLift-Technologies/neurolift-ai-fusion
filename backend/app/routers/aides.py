"""
Aides Router
CRUD for Aide coaching instances.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List
import uuid

router = APIRouter()

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
