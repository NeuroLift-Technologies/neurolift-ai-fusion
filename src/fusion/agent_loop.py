"""Transport-neutral validation seam for the Fusion <-> world-engine agent loop.

The world engine supplies physical perception. A Fusion decision source consumes that snapshot
alongside Fusion-owned semantic state and returns an intent. This module validates that boundary;
it does not own a transport or simulate physical consequences.
"""

from __future__ import annotations

from copy import deepcopy
from math import isfinite
from typing import Any, Callable, Mapping

PROTOCOL_VERSION = "nlt.agent-loop.v1"
INTENT_VERBS = frozenset(
    {
        "approach",
        "look_at",
        "use",
        "sit",
        "rest",
        "communicate",
        "wait",
    }
)
TARGET_REQUIRED_VERBS = frozenset(
    {
        "approach",
        "look_at",
        "use",
        "sit",
        "communicate",
    }
)

_PERCEPTION_KEYS = frozenset(
    {
        "protocolVersion",
        "messageType",
        "messageId",
        "agentId",
        "tick",
        "scene",
        "self",
        "visibleEntities",
    }
)
_INTENT_KEYS = frozenset(
    {
        "protocolVersion",
        "messageType",
        "messageId",
        "agentId",
        "observedTick",
        "verb",
        "targetId",
    }
)
_RESULT_KEYS = frozenset(
    {
        "protocolVersion",
        "messageType",
        "messageId",
        "intentMessageId",
        "agentId",
        "tick",
        "status",
        "reason",
    }
)
_VECTOR_KEYS = frozenset({"x", "y", "z"})


class AgentLoopProtocolError(ValueError):
    """A message violates the versioned agent-loop contract."""


def _object(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise AgentLoopProtocolError(f"{name} must be an object")
    return value


def _non_empty_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AgentLoopProtocolError(f"{name} must be a non-empty string")
    return value


def _tick(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise AgentLoopProtocolError(f"{name} must be a non-negative integer")
    return value


def _vector(value: Any, name: str) -> None:
    vector = _object(value, name)
    if set(vector) != _VECTOR_KEYS:
        raise AgentLoopProtocolError(f"{name} must contain exactly x, y, and z")
    for axis in _VECTOR_KEYS:
        coordinate = vector[axis]
        if isinstance(coordinate, bool) or not isinstance(coordinate, (int, float)):
            raise AgentLoopProtocolError(f"{name}.{axis} must be numeric")
        try:
            finite = isfinite(coordinate)
        except OverflowError:
            finite = False
        if not finite:
            raise AgentLoopProtocolError(f"{name}.{axis} must be finite")


def validate_perception(message: Mapping[str, Any]) -> None:
    """Raise a protocol error unless `message` is a valid engine-owned snapshot."""
    data = _object(message, "perception")
    if set(data) != _PERCEPTION_KEYS:
        raise AgentLoopProtocolError("perception has missing or unknown fields")
    if (
        data["protocolVersion"] != PROTOCOL_VERSION
        or data["messageType"] != "perception"
    ):
        raise AgentLoopProtocolError("unsupported perception protocol")
    _non_empty_string(data["messageId"], "messageId")
    _non_empty_string(data["agentId"], "agentId")
    _tick(data["tick"], "tick")

    scene = _object(data["scene"], "scene")
    if set(scene) != {"id", "kind"}:
        raise AgentLoopProtocolError("scene must contain exactly id and kind")
    _non_empty_string(scene["id"], "scene.id")
    if not isinstance(scene["kind"], str) or scene["kind"] not in {
        "open_world",
        "interior",
    }:
        raise AgentLoopProtocolError("scene.kind must be open_world or interior")

    own_state = _object(data["self"], "self")
    if set(own_state) != {"position", "velocity"}:
        raise AgentLoopProtocolError("self must contain exactly position and velocity")
    _vector(own_state["position"], "self.position")
    _vector(own_state["velocity"], "self.velocity")

    entities = data["visibleEntities"]
    if not isinstance(entities, list):
        raise AgentLoopProtocolError("visibleEntities must be an array")
    seen_ids: set[str] = set()
    for index, raw_entity in enumerate(entities):
        entity = _object(raw_entity, f"visibleEntities[{index}]")
        expected = {"id", "kind", "position", "affordances", "occupied"}
        if set(entity) != expected:
            raise AgentLoopProtocolError(
                f"visibleEntities[{index}] has missing or unknown fields"
            )
        entity_id = _non_empty_string(entity["id"], f"visibleEntities[{index}].id")
        if entity_id in seen_ids:
            raise AgentLoopProtocolError(f"duplicate visible entity id '{entity_id}'")
        seen_ids.add(entity_id)
        if not isinstance(entity["kind"], str) or entity["kind"] not in {
            "agent",
            "object",
            "place",
        }:
            raise AgentLoopProtocolError(
                f"visible entity '{entity_id}' has unsupported kind"
            )
        _vector(entity["position"], f"visibleEntities[{index}].position")
        affordances = entity["affordances"]
        if (
            not isinstance(affordances, list)
            or any(not isinstance(item, str) or not item for item in affordances)
            or len(set(affordances)) != len(affordances)
        ):
            raise AgentLoopProtocolError(
                f"visible entity '{entity_id}' has invalid affordances"
            )
        if not isinstance(entity["occupied"], bool):
            raise AgentLoopProtocolError(
                f"visible entity '{entity_id}' occupied must be boolean"
            )


def validate_intent(
    message: Mapping[str, Any],
    observation: Mapping[str, Any],
) -> None:
    """Raise a protocol error for an invalid, stale, or ungrounded semantic intent."""
    validate_perception(observation)
    intent = _object(message, "intent")
    intent_keys = frozenset(intent)
    if intent_keys not in {_INTENT_KEYS, _INTENT_KEYS - {"targetId"}}:
        raise AgentLoopProtocolError("intent has missing or unknown fields")
    if (
        intent["protocolVersion"] != PROTOCOL_VERSION
        or intent["messageType"] != "intent"
    ):
        raise AgentLoopProtocolError("unsupported intent protocol")
    _non_empty_string(intent["messageId"], "messageId")

    agent_id = _non_empty_string(intent["agentId"], "agentId")
    if agent_id != observation["agentId"]:
        raise AgentLoopProtocolError("intent agentId does not match observation")
    observed_tick = _tick(intent["observedTick"], "observedTick")
    if observed_tick != observation["tick"]:
        raise AgentLoopProtocolError(
            "intent observedTick is stale or does not match observation"
        )

    verb = _non_empty_string(intent["verb"], "verb")
    if verb not in INTENT_VERBS:
        raise AgentLoopProtocolError(f"unsupported intent verb '{verb}'")

    has_target = "targetId" in intent
    target = intent.get("targetId")
    if verb in TARGET_REQUIRED_VERBS and not has_target:
        raise AgentLoopProtocolError(f"intent verb '{verb}' requires targetId")
    if has_target:
        target_id = _non_empty_string(target, "targetId")
        visible_ids = {entity["id"] for entity in observation["visibleEntities"]}
        if target_id not in visible_ids:
            raise AgentLoopProtocolError(
                f"intent target '{target_id}' was not in the observation"
            )


def validate_result(
    message: Mapping[str, Any],
    intent: Mapping[str, Any],
) -> None:
    """Raise a protocol error unless the engine result correlates to the intent."""
    result = _object(message, "result")
    intent_data = _object(intent, "intent")
    if (
        intent_data.get("protocolVersion") != PROTOCOL_VERSION
        or intent_data.get("messageType") != "intent"
    ):
        raise AgentLoopProtocolError("unsupported correlated intent protocol")
    result_keys = frozenset(result)
    if result_keys not in {_RESULT_KEYS, _RESULT_KEYS - {"reason"}}:
        raise AgentLoopProtocolError("result has missing or unknown fields")
    if (
        result["protocolVersion"] != PROTOCOL_VERSION
        or result["messageType"] != "result"
    ):
        raise AgentLoopProtocolError("unsupported result protocol")
    _non_empty_string(result["messageId"], "messageId")
    _non_empty_string(result["intentMessageId"], "intentMessageId")
    _non_empty_string(result["agentId"], "agentId")
    intent_id = _non_empty_string(intent_data.get("messageId"), "intent.messageId")
    intent_agent = _non_empty_string(intent_data.get("agentId"), "intent.agentId")
    intent_tick = _tick(intent_data.get("observedTick"), "intent.observedTick")
    if result["intentMessageId"] != intent_id or result["agentId"] != intent_agent:
        raise AgentLoopProtocolError("result does not match intent")
    result_tick = _tick(result["tick"], "tick")
    if result_tick < intent_tick:
        raise AgentLoopProtocolError("result tick precedes intent")
    status = result["status"]
    if not isinstance(status, str) or status not in {"accepted", "rejected"}:
        raise AgentLoopProtocolError("result status must be accepted or rejected")
    if status == "rejected" and "reason" not in result:
        raise AgentLoopProtocolError("rejected result requires a reason")
    if "reason" in result:
        _non_empty_string(result["reason"], "reason")


class FusionAgentLoop:
    """Validates the neutral seam around an injected Fusion semantic decision source.

    The decision source owns how Avatar/Aide state informs cognition. The caller owns process
    lifecycle and transport. Exceptions are intentionally surfaced to the caller.
    """

    def __init__(
        self,
        decide: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    ) -> None:
        self._decide = decide

    def handle_observation(self, observation: Mapping[str, Any]) -> dict[str, Any]:
        """Validate a perception, request an intent, then validate the intent.

        Raises:
            AgentLoopProtocolError: If the perception or returned intent violates the protocol.
            Exception: Any exception raised by the injected decision source.
        """
        validate_perception(observation)
        intent = self._decide(deepcopy(dict(observation)))
        validate_intent(intent, observation)
        return deepcopy(dict(intent))
