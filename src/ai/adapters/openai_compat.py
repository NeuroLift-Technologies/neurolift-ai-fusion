"""
OpenAI-Compatible Backend (stdlib urllib only)

Talks to any OpenAI-style ``/chat/completions`` endpoint using only the
Python standard library (no ``requests`` import). The base URL is always
required (provider-agnostic — no vendor default host). The API key is
read from an environment variable; it is never logged or printed.
"""

import json
import os
import urllib.request
from typing import Any, Dict, List, Optional

from ...core.protocols import ExperienceRecord
from ..protocol import ModelAdapter, AVATAR_MODEL_KIND, AIDE_MODEL_KIND


def _avatar_baseline() -> Dict[str, Any]:
    return {
        "trait_impact": {
            "difficulty_modifier": 1.0,
            "quality_modifier": 0.0,
            "time_modifier": 1.0,
            "cognitive_load_modifier": 0.0,
        },
        "struggle_indicators": [],
        "emotional_state": "neutral",
        "cognitive_load": 0.0,
        "stress_level": 0.0,
    }


def _aide_baseline() -> Dict[str, Any]:
    return {
        "strategy": "Rule-based fallback (no model)",
        "specific_techniques": [],
        "urgency": "low",
        "coaching_type": "preventive",
        "stress_reduction": 0.0,
        "emotional_boost": 0.0,
        "cognitive_support": 0.0,
        "focus_restoration": 0.0,
        "independence_building": 0.0,
    }


class OpenAICompatBackend(ModelAdapter):
    """Provider-agnostic chat-completions backend (stdlib only)."""

    model_id: str = "openai_compat"
    model_version: str = "0.1.0"

    def __init__(
        self,
        base_url: str,
        api_key_env: str = "OPENAI_COMPAT_API_KEY",
        model_name: str = "gpt-4o-mini",
        kind: str = "aide",
        timeout: float = 30.0,
    ) -> None:
        if not base_url:
            raise ValueError("base_url is required for OpenAICompatBackend")
        self.base_url = base_url.rstrip("/")
        self.api_key_env = api_key_env
        self.model_name = model_name
        self.kind = kind
        self.timeout = timeout

    def predict(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        role = inputs.get("role", self.kind)
        if role == AVATAR_MODEL_KIND:
            system_prompt = (
                "You predict Avatar trait impacts and state changes from a "
                "provided input JSON. Respond ONLY with a JSON object matching "
                "the avatar contract."
            )
            baseline = _avatar_baseline()
        else:
            system_prompt = (
                "You are an ADHD Aide coach. Given an observation and task "
                "context as JSON, respond ONLY with a JSON object matching the "
                "aide coaching contract."
            )
            baseline = _aide_baseline()

        api_key = os.environ.get(self.api_key_env)
        if not api_key:
            return baseline

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(inputs, default=str)},
            ],
            "temperature": 0.2,
        }
        url = self.base_url + "/chat/completions"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            content = body["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as exc:
            raise RuntimeError(
                f"OpenAICompatBackend HTTP {exc.code} {exc.reason}"
            ) from exc
        except Exception as exc:
            raise RuntimeError(f"OpenAICompatBackend request failed: {exc}") from exc

        try:
            parsed = json.loads(content)
        except (json.JSONDecodeError, TypeError):
            return baseline
        if isinstance(parsed, dict):
            return {**baseline, **parsed}
        return baseline

    def update(self, records: List[ExperienceRecord]) -> None:
        """No-op: external LLM providers are not trained inline."""
        return None
