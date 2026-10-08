"""Tests for the transport-neutral engine/Fusion agent-loop seam."""

import copy

import pytest

from src.fusion.agent_loop import (
    AgentLoopProtocolError,
    FusionAgentLoop,
    PROTOCOL_VERSION,
    validate_intent,
    validate_perception,
    validate_result,
)


@pytest.fixture
def observation():
    return {
        "protocolVersion": PROTOCOL_VERSION,
        "messageType": "perception",
        "messageId": "obs-42-avatar-1",
        "agentId": "avatar_1",
        "tick": 42,
        "scene": {"id": "workplace_1", "kind": "interior"},
        "self": {
            "position": {"x": 1.0, "y": 0.0, "z": 2.0},
            "velocity": {"x": 0.0, "y": 0.0, "z": 0.0},
        },
        "visibleEntities": [
            {
                "id": "desk_1",
                "kind": "object",
                "position": {"x": 2.0, "y": 0.0, "z": 2.0},
                "affordances": ["use", "sit"],
                "occupied": False,
            }
        ],
    }


def make_intent(**overrides):
    message = {
        "protocolVersion": PROTOCOL_VERSION,
        "messageType": "intent",
        "messageId": "intent-42-avatar-1",
        "agentId": "avatar_1",
        "observedTick": 42,
        "verb": "approach",
        "targetId": "desk_1",
    }
    message.update(overrides)
    return message


def test_fusion_loop_returns_correlated_semantic_intent(observation):
    source_snapshot = copy.deepcopy(observation)
    loop = FusionAgentLoop(lambda seen: make_intent())

    intent = loop.handle_observation(observation)

    assert intent["verb"] == "approach"
    assert intent["targetId"] == "desk_1"
    assert observation == source_snapshot


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"observedTick": 41}, "stale"),
        ({"agentId": "avatar_2"}, "does not match"),
        ({"targetId": "hidden_object"}, "was not in the observation"),
        ({"verb": "communicate", "targetId": None}, "requires targetId"),
        ({"verb": "teleport"}, "unsupported intent verb"),
        ({"position": {"x": 10, "y": 0, "z": 0}}, "unknown fields"),
    ],
)
def test_invalid_intents_are_rejected(observation, overrides, message):
    intent = make_intent(**overrides)
    if overrides.get("verb") == "communicate":
        intent.pop("targetId")
    with pytest.raises(AgentLoopProtocolError, match=message):
        validate_intent(intent, observation)


def test_perception_rejects_duplicate_entities_and_non_finite_coordinates(observation):
    duplicate = copy.deepcopy(observation)
    duplicate["visibleEntities"].append(copy.deepcopy(duplicate["visibleEntities"][0]))
    with pytest.raises(AgentLoopProtocolError, match="duplicate"):
        validate_perception(duplicate)

    non_finite = copy.deepcopy(observation)
    non_finite["self"]["position"]["x"] = float("inf")
    with pytest.raises(AgentLoopProtocolError, match="finite"):
        validate_perception(non_finite)


def test_decision_source_cannot_return_physical_writes(observation):
    loop = FusionAgentLoop(lambda seen: make_intent(position={"x": 9, "y": 0, "z": 0}))

    with pytest.raises(AgentLoopProtocolError, match="unknown fields"):
        loop.handle_observation(observation)


def test_engine_result_is_correlated_and_rejection_has_reason():
    intent = make_intent()
    rejected = {
        "protocolVersion": PROTOCOL_VERSION,
        "messageType": "result",
        "messageId": "result-42-avatar-1",
        "intentMessageId": intent["messageId"],
        "agentId": intent["agentId"],
        "tick": 42,
        "status": "rejected",
        "reason": "target is occupied",
    }
    validate_result(rejected, intent)

    without_reason = dict(rejected)
    without_reason.pop("reason")
    with pytest.raises(AgentLoopProtocolError, match="requires a reason"):
        validate_result(without_reason, intent)

    mismatched = dict(rejected, intentMessageId="other-intent")
    with pytest.raises(AgentLoopProtocolError, match="does not match"):
        validate_result(mismatched, intent)

    stale = dict(rejected, tick=41)
    with pytest.raises(AgentLoopProtocolError, match="precedes"):
        validate_result(stale, intent)


@pytest.mark.parametrize(
    "overrides",
    [
        {"protocolVersion": "nlt.agent-loop.v0"},
        {"messageType": "perception"},
    ],
)
def test_engine_result_rejects_unsupported_correlated_intent(overrides):
    intent = make_intent(**overrides)
    result = {
        "protocolVersion": PROTOCOL_VERSION,
        "messageType": "result",
        "messageId": "result-42-avatar-1",
        "intentMessageId": intent["messageId"],
        "agentId": intent["agentId"],
        "tick": 42,
        "status": "accepted",
    }

    with pytest.raises(AgentLoopProtocolError, match="unsupported correlated intent"):
        validate_result(result, intent)
