"""
Fusion Router
Trigger and monitor the Avatar + Aide → Advocate fusion process.
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

class FusionRequest(BaseModel):
    avatar_id: str
    aide_id: str

class FusionReport(BaseModel):
    fusion_id: str
    avatar_id: str
    aide_id: str
    success: bool
    advocate_id: Optional[str]
    readiness_score: float
    failure_reason: Optional[str]
    timestamp: str

# ---------------------------------------------------------------------------
# In-memory store
# ---------------------------------------------------------------------------
_fusions: Dict[str, Dict[str, Any]] = {}
_advocates: Dict[str, Dict[str, Any]] = {}

# Minimum readiness thresholds (mirrors ReadinessAssessor logic)
MIN_READINESS_SCORE = 0.75

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/", response_model=List[FusionReport], summary="List all fusion reports")
async def list_fusions():
    return list(_fusions.values())


@router.post("/", response_model=FusionReport, status_code=201, summary="Attempt a fusion")
async def attempt_fusion(body: FusionRequest):
    """
    Attempt to fuse an Avatar and Aide into an Advocate.
    In production this delegates to the FusionEngine and ReadinessAssessor.
    """
    fusion_id = str(uuid.uuid4())

    # Placeholder readiness calculation — replace with real ReadinessAssessor
    import random
    readiness_score = round(random.uniform(0.5, 1.0), 3)
    success = readiness_score >= MIN_READINESS_SCORE

    advocate_id = None
    failure_reason = None

    if success:
        advocate_id = str(uuid.uuid4())
        _advocates[advocate_id] = {
            "advocate_id": advocate_id,
            "avatar_id": body.avatar_id,
            "aide_id": body.aide_id,
            "fusion_id": fusion_id,
            "created_at": datetime.utcnow().isoformat(),
        }
    else:
        failure_reason = (
            f"Readiness score {readiness_score:.2f} is below the required "
            f"threshold of {MIN_READINESS_SCORE}. Continue training."
        )

    report = {
        "fusion_id": fusion_id,
        "avatar_id": body.avatar_id,
        "aide_id": body.aide_id,
        "success": success,
        "advocate_id": advocate_id,
        "readiness_score": readiness_score,
        "failure_reason": failure_reason,
        "timestamp": datetime.utcnow().isoformat(),
    }
    _fusions[fusion_id] = report
    return report


@router.get("/{fusion_id}", response_model=FusionReport, summary="Get fusion report by ID")
async def get_fusion(fusion_id: str):
    report = _fusions.get(fusion_id)
    if not report:
        raise HTTPException(status_code=404, detail="Fusion report not found")
    return report


@router.get("/advocates/", summary="List all Advocates")
async def list_advocates():
    return list(_advocates.values())
