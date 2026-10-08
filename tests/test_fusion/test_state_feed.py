"""Tests for the Fusion -> world-engine state feed contract."""

from src.avatars.adhd_traits.stay_alert_avatar import StayAlertAvatar
from src.avatars.base_avatar import AvatarState
from src.aides.coaching.stay_alert_aide import StayAlertAide
from src.fusion import build_state_feed


def test_build_state_feed_matches_renderer_contract():
    avatar = StayAlertAvatar("avatar_1", {})
    aide = StayAlertAide("aide_1", {})

    avatar.current_state = AvatarState.BURNOUT_RISK
    avatar.stress_level = 0.72
    avatar.cognitive_load = 0.81
    avatar.burnout_risk_level = 0.66
    avatar.struggle_patterns = ["attention_drift", "time_blindness"]

    class InterventionStub:
        strategy = "time_box_25"
        description = "Used a 25-minute cycle to restore focus."

    aide.intervention_history = [InterventionStub()]

    feed = build_state_feed(
        avatar,
        aide,
        tick=42,
        scene_id="workplace_1",
        scene_kind="interior",
    )

    assert feed["schemaVersion"] == "nlt.state-feed.v1"
    assert feed["scene"] == {"id": "workplace_1", "kind": "interior"}
    assert len(feed["agents"]) == 1
    assert feed["agents"][0]["state"] == "overwhelmed"
    assert feed["pairs"][0]["avatarId"] == "avatar_1"
    assert feed["pairs"][0]["aideId"] == "aide_1"
    assert feed["burnoutEpisodes"][0]["startTick"] == 42
    assert feed["events"][0]["kind"] == "aide_intervention"
    assert feed["events"][0]["strategy"] == "time_box_25"
