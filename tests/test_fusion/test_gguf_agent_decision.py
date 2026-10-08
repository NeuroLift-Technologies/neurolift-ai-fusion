"""Tests for the separate local GGUF agent-loop decision path."""

import os
from pathlib import Path

import pytest

from src.fusion import (
    FusionAgentLoop,
    GgufAgentLoopModelOutputError,
    LlamaCppAgentLoopDecision,
    PROTOCOL_VERSION,
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
                "affordances": ["approach", "use"],
                "occupied": False,
            }
        ],
    }


class FakeLlama:
    def __init__(self, content):
        self.content = content
        self.kwargs = None

    def create_chat_completion(self, **kwargs):
        self.kwargs = kwargs
        return {"choices": [{"message": {"content": self.content}}]}


def test_gguf_adapter_emits_grounded_approach_intent(observation):
    model = FakeLlama('{"verb":"approach","targetId":"desk_1"}')
    adapter = LlamaCppAgentLoopDecision("unused-injected-model.gguf", model=model)

    intent = FusionAgentLoop(adapter).handle_observation(observation)

    assert intent["protocolVersion"] == PROTOCOL_VERSION
    assert intent["messageType"] == "intent"
    assert intent["agentId"] == observation["agentId"]
    assert intent["observedTick"] == observation["tick"]
    assert intent["verb"] == "approach"
    assert intent["targetId"] == "desk_1"
    assert model.kwargs["temperature"] == 0.0
    assert model.kwargs["max_tokens"] == 48
    assert model.kwargs["response_format"] == {
        "type": "json_object",
        "schema": {
            "oneOf": [
                {
                    "type": "object",
                    "properties": {"verb": {"const": "wait"}},
                    "required": ["verb"],
                    "additionalProperties": False,
                },
                {
                    "type": "object",
                    "properties": {
                        "verb": {"const": "approach"},
                        "targetId": {"enum": ["desk_1"]},
                    },
                    "required": ["verb", "targetId"],
                    "additionalProperties": False,
                },
            ]
        },
    }
    assert "Never output coordinates" in model.kwargs["messages"][0]["content"]


def test_gguf_adapter_emits_wait_intent(observation):
    adapter = LlamaCppAgentLoopDecision(
        "unused-injected-model.gguf",
        model=FakeLlama('{"verb":"wait"}'),
    )

    intent = adapter(observation)

    assert intent["verb"] == "wait"
    assert "targetId" not in intent


@pytest.mark.parametrize(
    "content",
    [
        "not json",
        '{"verb":"wait","verb":"approach","targetId":"desk_1"}',
        '{"verb":"teleport"}',
        '{"verb":"wait","targetId":"desk_1"}',
        '{"verb":"approach","targetId":"hidden"}',
        '{"verb":"approach","targetId":"desk_1","position":{"x":9}}',
        "```json\n{\"verb\":\"wait\"}\n```",
    ],
)
def test_gguf_adapter_rejects_malformed_or_ungrounded_output(observation, content):
    adapter = LlamaCppAgentLoopDecision(
        "unused-injected-model.gguf",
        model=FakeLlama(content),
    )

    with pytest.raises(GgufAgentLoopModelOutputError):
        adapter(observation)


def test_gguf_adapter_rejects_malformed_runtime_response(observation):
    class BadResponse:
        def create_chat_completion(self, **kwargs):
            return {"choices": []}

    adapter = LlamaCppAgentLoopDecision(
        "unused-injected-model.gguf",
        model=BadResponse(),
    )

    with pytest.raises(GgufAgentLoopModelOutputError, match="did not contain"):
        adapter(observation)


@pytest.mark.slow
def test_local_qwen_gguf_smoke(observation):
    model_path = os.environ.get("NLT_AGENT_LOOP_GGUF_PATH")
    if not model_path:
        pytest.skip("Set NLT_AGENT_LOOP_GGUF_PATH to run local GGUF inference")

    adapter = LlamaCppAgentLoopDecision(Path(model_path), context_size=2048, threads=2)
    intent = FusionAgentLoop(adapter).handle_observation(observation)

    assert intent["verb"] in {"approach", "wait"}
    if intent["verb"] == "approach":
        assert intent["targetId"] == "desk_1"
