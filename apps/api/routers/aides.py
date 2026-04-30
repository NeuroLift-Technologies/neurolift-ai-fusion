"""Aide endpoints."""

from fastapi import APIRouter

from schemas.models import AideDetail, AideSummary, AideType

router = APIRouter()

_AIDES: list[AideDetail] = [
    AideDetail(
        id="stay_alert_aide",
        type=AideType.STAY_ALERT_AIDE,
        display_name="AttentionCoach",
        description="Coaching aide specialising in sustained attention and focus strategies.",
        expertise=["attention_training", "break_scheduling", "environmental_design"],
        config={
            "intervention_threshold": 0.6,
            "coaching_style": "collaborative",
            "max_strategies_per_session": 5,
        },
    ),
    AideDetail(
        id="task_kickstart_aide",
        type=AideType.TASK_KICKSTART_AIDE,
        display_name="InitiationCoach",
        description="Coaching aide specialising in task initiation and activation energy reduction.",
        expertise=["task_decomposition", "implementation_intentions", "environment_priming"],
        config={
            "intervention_threshold": 0.55,
            "coaching_style": "directive",
            "max_strategies_per_session": 4,
        },
    ),
]

_INDEX = {a.id: a for a in _AIDES}


@router.get("/", response_model=list[AideSummary])
async def list_aides() -> list[AideSummary]:
    return [AideSummary(**a.model_dump()) for a in _AIDES]


@router.get("/{aide_id}", response_model=AideDetail)
async def get_aide(aide_id: str) -> AideDetail:
    from fastapi import HTTPException

    aide = _INDEX.get(aide_id)
    if not aide:
        raise HTTPException(status_code=404, detail=f"Aide '{aide_id}' not found")
    return aide
