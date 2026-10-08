"""Tests for the Fusion -> world-engine state feed contract."""

from datetime import datetime, timezone

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
    avatar.struggle_patterns = [{"indicators": ["attention_drift", "time_blindness"]}]

    class InterventionStub:
        action_id = "action-1"
        strategy = "time_box_25"
        description = "Used a 25-minute cycle to restore focus."
        timestamp = datetime(2026, 10, 8, 5, 0, tzinfo=timezone.utc)
        helped = False

    aide.intervention_history = [InterventionStub()]
    burnout_episodes = [
        {
            "startTick": 30,
            "severity": 0.35,
            "peakBelow": 0.34,
            "recoveredTick": None,
            "recoveryMode": None,
        }
    ]

    feed = build_state_feed(
        avatar,
        aide,
        tick=42,
        scene_id="workplace_1",
        scene_kind="interior",
        burnout_episodes=burnout_episodes,
    )

    assert feed["schemaVersion"] == "nlt.state-feed.v1"
    assert feed["scene"] == {"id": "workplace_1", "kind": "interior"}
    assert len(feed["agents"]) == 1
    assert feed["agents"][0]["state"] == "overwhelmed"
    assert feed["agents"][0]["struggleSignals"] == [
        "attention_drift",
        "time_blindness",
    ]
    assert feed["agents"][0]["supportIndex"] is None
    assert feed["pairs"][0]["avatarId"] == "avatar_1"
    assert feed["pairs"][0]["aideId"] == "aide_1"
    assert feed["agents"][0]["burnout"] is True
    assert feed["burnoutEpisodes"] == burnout_episodes
    assert feed["burnoutEpisodes"][0]["startTick"] == 30
    assert feed["events"][0]["kind"] == "aide_intervention"
    assert feed["events"][0]["strategy"] == "time_box_25"
    assert feed["events"][0]["eventId"] == "action-1"
    assert feed["events"][0]["occurredAt"] == "2026-10-08T05:00:00Z"
    assert feed["events"][0]["helped"] is False

    later_feed = build_state_feed(
        avatar,
        aide,
        tick=43,
        burnout_episodes=burnout_episodes,
    )
    assert later_feed["events"][0]["tick"] == 43
    assert later_feed["events"][0]["eventId"] == feed["events"][0]["eventId"]
    assert later_feed["events"][0]["occurredAt"] == feed["events"][0]["occurredAt"]


def test_state_feed_does_not_infer_burnout_or_intervention_outcome():
    avatar = StayAlertAvatar("avatar_1", {})
    aide = StayAlertAide("aide_1", {})
    avatar.burnout_risk_level = 0.9

    class PendingInterventionStub:
        action_id = "action-pending"
        strategy = "time_box_25"
        timestamp = datetime(2026, 10, 8, 5, 0, tzinfo=timezone.utc)
        helped = None

    aide.intervention_history = [PendingInterventionStub()]
    feed = build_state_feed(avatar, aide, tick=43)

    assert feed["burnoutEpisodes"] == []
    assert feed["agents"][0]["burnout"] is False
    assert feed["events"] == []
