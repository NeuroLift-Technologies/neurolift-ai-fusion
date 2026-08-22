"""
AI Models Router
Trigger model training and inspect the model registry status.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from src.ai.registry import get_registry
from src.ai.trainer import TrainingPipeline

router = APIRouter()


class TrainRequest(BaseModel):
    """Request to trigger async training for an avatar/aide pair."""
    avatar_id: Optional[str] = None
    aide_id: Optional[str] = None


@router.post("/train", summary="Trigger async model training for a pair")
async def train_models(body: TrainRequest):
    reg = get_registry()
    pipeline = TrainingPipeline(registry=reg)
    pipeline.run_async(avatar_id=body.avatar_id, aide_id=body.aide_id)
    return {"status": "training_started", "avatar_id": body.avatar_id, "aide_id": body.aide_id}


@router.get("/status", summary="Model registry status")
async def model_status():
    return get_registry().status()
