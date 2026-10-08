"""Tests for the local Transformers agent-loop decision adapter."""

import os
from pathlib import Path

import pytest

from src.fusion import (
    AgentLoopModelOutputError,
    FusionAgentLoop,
    PROTOCOL_VERSION,
    TransformersAgentLoopDecision,
)


class FakeTensor:
    def __init__(self, tokens):
        self.tokens = list(tokens)

    @property
    def shape(self):
        return (1, len(self.tokens))

    def to(self, device):
        return self

    def __getitem__(self, index):
        if index == 0:
            return self.tokens
        raise IndexError(index)


class FakeTokenizer:
    eos_token_id = 0

    def __init__(self, response):
        self.response = response
        self.messages = None

    def apply_chat_template(self, messages, **kwargs):
        self.messages = messages
        assert kwargs == {
            "tokenize": True,
            "add_generation_prompt": True,
            "enable_thinking": False,
            "return_tensors": "pt",
        }
        return FakeTensor([1, 2, 3])

    def decode(self, tokens, *, skip_special_tokens):
        assert skip_special_tokens is True
        assert tokens == [99]
        return self.response


class FakeModel:
    def __init__(self):
        self.generation_options = None

    def to(self, device):
        return self

    def eval(self):
        return self

    def generate(self, input_ids, **kwargs):
        self.generation_options = kwargs
        return FakeTensor(input_ids.tokens + [99])


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


def make_decision(response):
    tokenizer = FakeTokenizer(response)
    model = FakeModel()
    return TransformersAgentLoopDecision(
        "unused-injected-model",
        tokenizer=tokenizer,
        model=model,
    ), tokenizer, model


def test_adapter_emits_grounded_correlated_approach_intent(observation):
    adapter, tokenizer, model = make_decision(
        '{"verb":"approach","targetId":"desk_1"}'
    )

    intent = FusionAgentLoop(adapter).handle_observation(observation)

    assert intent["protocolVersion"] == PROTOCOL_VERSION
    assert intent["messageType"] == "intent"
    assert intent["agentId"] == observation["agentId"]
    assert intent["observedTick"] == observation["tick"]
    assert intent["verb"] == "approach"
    assert intent["targetId"] == "desk_1"
    assert tokenizer.messages[0]["role"] == "system"
    assert "Never output coordinates" in tokenizer.messages[0]["content"]
    assert model.generation_options == {
        "max_new_tokens": 48,
        "do_sample": False,
        "pad_token_id": 0,
    }


def test_adapter_emits_wait_without_target(observation):
    adapter, _, _ = make_decision('{"verb":"wait"}')

    intent = adapter(observation)

    assert intent["verb"] == "wait"
    assert "targetId" not in intent


@pytest.mark.parametrize(
    "response",
    [
        "not json",
        '{"verb":"teleport"}',
        '{"verb":"wait","verb":"approach","targetId":"desk_1"}',
        '{"verb":"wait","targetId":"desk_1"}',
        '{"verb":"approach","targetId":"hidden"}',
        '{"verb":"approach","targetId":"desk_1","position":{"x":9}}',
        '```json\n{"verb":"wait"}\n```',
    ],
)
def test_adapter_rejects_malformed_or_ungrounded_model_output(observation, response):
    adapter, _, _ = make_decision(response)

    with pytest.raises(AgentLoopModelOutputError):
        adapter(observation)


def test_adapter_surfaces_inference_errors(observation):
    class FailedModel(FakeModel):
        def generate(self, input_ids, **kwargs):
            raise RuntimeError("inference failed")

    adapter = TransformersAgentLoopDecision(
        "unused-injected-model",
        tokenizer=FakeTokenizer('{"verb":"wait"}'),
        model=FailedModel(),
    )

    with pytest.raises(RuntimeError, match="inference failed"):
        adapter(observation)


@pytest.mark.slow
def test_local_qwen_model_smoke(observation):
    model_path = os.environ.get("NLT_AGENT_LOOP_MODEL_PATH")
    if not model_path:
        pytest.skip("Set NLT_AGENT_LOOP_MODEL_PATH to run local model inference")

    adapter = TransformersAgentLoopDecision(Path(model_path))
    intent = FusionAgentLoop(adapter).handle_observation(observation)

    assert intent["verb"] in {"approach", "wait"}
    if intent["verb"] == "approach":
        assert intent["targetId"] == "desk_1"
