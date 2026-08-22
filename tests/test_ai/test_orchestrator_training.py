"""Integration tests: wiring model training into SessionOrchestrator."""

import os
import tempfile

import pytest

from src.ai import ModelRegistry, RuleFallbackBackend, TrainingPipeline, get_registry
from src.avatars.base_avatar import BaseAvatar
from src.aides.base_aide import BaseAide
from src.simulation.session_orchestrator import (
    SessionConfig,
    SessionOrchestrator,
)


class _TestAvatar(BaseAvatar):
    def get_adhd_trait_impact(self, task_context):
        return {
            "difficulty_modifier": 1.0,
            "struggle_indicators": [],
            "quality_modifier": 0.0,
            "time_modifier": 1.0,
            "cognitive_load_modifier": 0.0,
        }

    def simulate_struggle(self, task_context):
        return []


class _TestAide(BaseAide):
    def get_expertise_strategies(self, context):
        return []

    def get_real_world_insights(self, context):
        return []


SCENARIOS = [
    {"name": "Planning", "task_type": "planning", "base_success_rate": 0.55, "cognitive_demand": 0.65},
    {"name": "Inbox", "task_type": "email_management", "base_success_rate": 0.50, "cognitive_demand": 0.60},
]


@pytest.mark.ai
class TestOrchestratorTraining:
    def setup_method(self):
        # Keep checkpoints out of the repo's data/ dir.
        self._tmp = tempfile.mkdtemp()
        os.environ["NEUROLIFT_MODELS_DIR"] = self._tmp
        self.reg = get_registry()
        self.avatar_id = "orch_avatar"
        self.aide_id = "orch_aide"
        self.avatar = _TestAvatar(self.avatar_id, {"trait_name": "t"})
        self.aide = _TestAide(self.aide_id, {"expertise_area": "attention"})
        self.aide.bind_to_avatar(self.avatar)
        self.avatar.bind_model(RuleFallbackBackend(kind="avatar"))
        self.aide.bind_model(RuleFallbackBackend(kind="aide"))
        self.reg.register(self.avatar_id, self.avatar.model)
        self.reg.register(self.aide_id, self.aide.model)

    def teardown_method(self):
        self.reg.unregister(self.avatar_id)
        self.reg.unregister(self.aide_id)
        os.environ.pop("NEUROLIFT_MODELS_DIR", None)

    def test_model_versions_collected(self):
        orch = SessionOrchestrator(
            avatar=self.avatar,
            aide=self.aide,
            config=SessionConfig(max_attempts_per_scenario=2, max_coaching_per_attempt=1),
            training_pipeline=TrainingPipeline(registry=self.reg),
            auto_train=False,
        )
        result = orch.run_session(SCENARIOS)
        assert self.avatar_id in result.model_versions
        assert self.aide_id in result.model_versions
        assert result.model_versions[self.avatar_id] == "0.1.0"
        assert result.to_dict()["model_versions"] == result.model_versions

    def test_train_models_sync(self):
        orch = SessionOrchestrator(
            avatar=self.avatar,
            aide=self.aide,
            config=SessionConfig(max_attempts_per_scenario=2, max_coaching_per_attempt=1),
            training_pipeline=TrainingPipeline(registry=self.reg),
            auto_train=False,
        )
        orch.run_session(SCENARIOS)
        summary = orch.train_models_sync()
        assert self.avatar_id in summary["owners"]
        assert self.aide_id in summary["owners"]
        status = self.reg.status()
        assert self.avatar_id in status["last_training"]
        assert self.aide_id in status["last_training"]

    def test_auto_train_triggers_async_without_error(self):
        orch = SessionOrchestrator(
            avatar=self.avatar,
            aide=self.aide,
            config=SessionConfig(max_attempts_per_scenario=2, max_coaching_per_attempt=1),
            training_pipeline=TrainingPipeline(registry=self.reg),
            auto_train=True,
        )
        # Should return normally; async thread may still be running.
        result = orch.run_session(SCENARIOS)
        assert isinstance(result.model_versions, dict)
