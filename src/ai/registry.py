"""
Model Registry

Central registry of model backends keyed by owner (Avatar/Aide) id,
plus a factory :meth:`ModelRegistry.build_backend` that lazily imports
the appropriate adapter (so torch/requests are only pulled in when a
backend of that type is actually constructed).
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

from ..core.protocols import ExperienceRecord
from .protocol import ModelBackend


def _models_dir() -> str:
    """Resolve the model checkpoint directory from env or default."""
    env = os.environ.get("NEUROLIFT_MODELS_DIR")
    if env:
        return env
    return os.path.join(os.getcwd(), "data", "models")


class ModelRegistry:
    """In-memory registry of model backends and their configuration."""

    def __init__(self) -> None:
        self._backends: Dict[str, ModelBackend] = {}
        self._configs: Dict[str, Dict[str, Any]] = {}
        self._last_training: Dict[str, str] = {}
        self._metrics: Dict[str, Dict[str, Any]] = {}

    # -- backend lifecycle --------------------------------------------------

    def register(self, owner_id: str, backend: ModelBackend) -> None:
        """Register a backend for ``owner_id``."""
        self._backends[owner_id] = backend

    def get(self, owner_id: str) -> Optional[ModelBackend]:
        """Return the backend for ``owner_id`` or ``None``."""
        return self._backends.get(owner_id)

    def unregister(self, owner_id: str) -> None:
        """Remove a backend and its config/bindings for ``owner_id``."""
        self._backends.pop(owner_id, None)
        self._configs.pop(owner_id, None)
        self._last_training.pop(owner_id, None)
        self._metrics.pop(owner_id, None)

    # -- config binding -----------------------------------------------------

    def bind_config(self, owner_id: str, config: Dict[str, Any]) -> None:
        """Associate a configuration dictionary with ``owner_id``."""
        self._configs[owner_id] = dict(config)

    def get_config(self, owner_id: str) -> Optional[Dict[str, Any]]:
        """Return the bound config for ``owner_id`` or ``None``."""
        return self._configs.get(owner_id)

    def list_configs(self) -> Dict[str, Dict[str, Any]]:
        """Return a copy of all bound configs."""
        return dict(self._configs)

    # -- factory ------------------------------------------------------------

    def build_backend(self, config: Dict[str, Any]) -> ModelBackend:
        """Construct a backend from a config dict.

        Reads ``config["type"]`` (``"rule_fallback"``, ``"transformer"``,
        or ``"openai_compat"``) and lazily imports the matching adapter
        module so heavy dependencies are only loaded on demand.
        """
        kind = config.get("kind", "generic")
        btype = config.get("type")
        if btype == "rule_fallback":
            from .adapters.rule_fallback import RuleFallbackBackend

            return RuleFallbackBackend(kind=kind)
        if btype == "transformer":
            from .adapters.transformer_policy import TransformerPolicyBackend

            return TransformerPolicyBackend(
                checkpoint_path=config.get("checkpoint_path"),
                model_name=config.get("model_name", "distilgpt2"),
                kind=kind,
                device=config.get("device", "cpu"),
            )
        if btype == "openai_compat":
            from .adapters.openai_compat import OpenAICompatBackend

            base_url = config.get("base_url")
            if not base_url:
                raise ValueError("openai_compat backend requires 'base_url' in config")

            return OpenAICompatBackend(
                base_url=config["base_url"],
                api_key_env=config.get("api_key_env", "OPENAI_COMPAT_API_KEY"),
                model_name=config.get("model_name", "gpt-4o-mini"),
                kind=kind,
                timeout=float(config.get("timeout", 30.0)),
            )
        raise ValueError(f"Unknown backend type: {btype!r}")

    # -- checkpoints --------------------------------------------------------

    def save_checkpoint(
        self, owner_id: str, path: Optional[str] = None
    ) -> str:
        """Write backend metadata JSON; return the written path."""
        backend = self.get(owner_id)
        meta = (
            backend.to_metadata()
            if backend is not None
            else {"model_id": owner_id, "model_version": "0.0.0", "kind": "generic"}
        )
        meta["updated_at"] = datetime.now().isoformat()
        if path is None:
            directory = _models_dir()
            os.makedirs(directory, exist_ok=True)
            path = os.path.join(directory, f"{owner_id}.json")
        else:
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(meta, fh, indent=2)
        return path

    def load_checkpoint(
        self, owner_id: str, path: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Read backend metadata JSON; return ``None`` if absent."""
        if path is None:
            path = os.path.join(_models_dir(), f"{owner_id}.json")
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    # -- training bookkeeping ----------------------------------------------

    def record_training(self, owner_id: str, metrics: Dict[str, Any]) -> None:
        """Record the last training timestamp and metrics for ``owner_id``."""
        self._last_training[owner_id] = datetime.now().isoformat()
        self._metrics[owner_id] = metrics

    def status(self) -> Dict[str, Any]:
        """Return a snapshot of registered models and metadata."""
        models = {
            owner_id: backend.to_metadata()
            for owner_id, backend in self._backends.items()
        }
        return {
            "models": models,
            "configs": self.list_configs(),
            "last_training": dict(self._last_training),
            "metrics": dict(self._metrics),
        }


_REGISTRY: Optional[ModelRegistry] = None


def get_registry() -> ModelRegistry:
    """Return the process-wide singleton :class:`ModelRegistry`."""
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = ModelRegistry()
    return _REGISTRY
