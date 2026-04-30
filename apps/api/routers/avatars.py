"""Avatar endpoints."""

from fastapi import APIRouter

from schemas.models import AvatarDetail, AvatarSummary, AvatarType

router = APIRouter()

_AVATARS: list[AvatarDetail] = [
    AvatarDetail(
        id="stay_alert",
        type=AvatarType.STAY_ALERT,
        display_name="StayAlert",
        description="Simulates sustained attention deficit — difficulty maintaining focus over time.",
        traits=["attention_drift", "hyperfocus_episodes", "fatigue_sensitivity"],
        config={
            "burnout_threshold": 0.85,
            "initial_difficulty": 0.6,
            "learning_rate": 0.1,
            "attention_decay_rate": 0.05,
        },
    ),
    AvatarDetail(
        id="task_kickstart",
        type=AvatarType.TASK_KICKSTART,
        display_name="TaskKickstart",
        description="Simulates task initiation difficulty — struggles to begin tasks despite knowing how.",
        traits=["initiation_paralysis", "perfectionism", "decision_fatigue"],
        config={
            "burnout_threshold": 0.80,
            "initial_difficulty": 0.65,
            "learning_rate": 0.12,
            "initiation_delay_factor": 0.7,
        },
    ),
]

_INDEX = {a.id: a for a in _AVATARS}


@router.get("/", response_model=list[AvatarSummary])
async def list_avatars() -> list[AvatarSummary]:
    return [AvatarSummary(**a.model_dump()) for a in _AVATARS]


@router.get("/{avatar_id}", response_model=AvatarDetail)
async def get_avatar(avatar_id: str) -> AvatarDetail:
    from fastapi import HTTPException

    avatar = _INDEX.get(avatar_id)
    if not avatar:
        raise HTTPException(status_code=404, detail=f"Avatar '{avatar_id}' not found")
    return avatar
