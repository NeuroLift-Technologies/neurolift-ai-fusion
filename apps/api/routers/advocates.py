"""Advocate endpoints."""

from fastapi import APIRouter

from schemas.models import AdvocateSummary, AvatarType, AideType

router = APIRouter()

_ADVOCATES: list[AdvocateSummary] = [
    AdvocateSummary(
        id="stay_alert_advocate",
        display_name="FocusAdvocate",
        avatar_type=AvatarType.STAY_ALERT,
        aide_type=AideType.STAY_ALERT_AIDE,
        fusion_score=0.0,
    ),
    AdvocateSummary(
        id="task_kickstart_advocate",
        display_name="InitiationAdvocate",
        avatar_type=AvatarType.TASK_KICKSTART,
        aide_type=AideType.TASK_KICKSTART_AIDE,
        fusion_score=0.0,
    ),
]


@router.get("/", response_model=list[AdvocateSummary])
async def list_advocates() -> list[AdvocateSummary]:
    return _ADVOCATES
