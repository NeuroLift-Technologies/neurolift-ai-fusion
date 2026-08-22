"""Tests for model-level fusion (trajectory distillation harness)."""

import pytest

from src.ai import ExperienceDataset
from src.ai.protocol import ADVOCATE_MODEL_KIND
from src.advocates.base_advocate import AdvocateMode
from src.core.protocols import ExperienceRecord
from src.fusion import (
    ModelFusionEngine,
    PairedTrajectoryStep,
    RouterTeacher,
)
from src.avatars.base_avatar import BaseAvatar
from src.aides.base_aide import BaseAide
from src.core.events import EventBus


# -- helpers ---------------------------------------------------------------

class _TestAvatar(BaseAvatar):
    def get_adhd_trait_impact(self, task_context):
        return {
            "difficulty_modifier": 1.0,
            "quality_modifier": 0.0,
            "time_modifier": 1.0,
            "cognitive_load_modifier": 0.0,
        }

    def simulate_struggle(self, task_context):
        return []


class _TestAide(BaseAide):
    def get_expertise_strategies(self, context):
        return [{
            "strategy": "Structured reset",
            "techniques": ["pause", "reframe"],
            "effectiveness": 0.9,
            "stress_reduction": 0.3,
            "focus_restoration": 0.3,
        }]

    def get_real_world_insights(self, context):
        return []


def _make_avatar_aide():
    bus = EventBus()
    avatar = _TestAvatar("avatar_001", {"trait_name": "attention_test"}, event_bus=bus)
    aide = _TestAide("aide_001", {"expertise_area": "attention_test"}, event_bus=bus)
    aide.bind_to_avatar(avatar)
    return avatar, aide


def _make_record(success=True, stress=0.5, load=0.5):
    return ExperienceRecord(
        task_type="focus",
        task_context={"difficulty": 0.5},
        outcome_success=success,
        quality_score=0.8 if success else 0.3,
        struggles_experienced=["attention_lapse"],
        emotional_journey=["calm", "frustrated"] if not success else ["calm", "confident"],
        cognitive_load_peak=load,
        stress_peak=stress,
        coaching_received=[{"strategy": "Structured reset"}],
        coaching_helpful=success,
        strategy_discovered="chunking" if success else None,
        independence_delta=0.1 if success else 0.0,
    )


def _prep_ready_pair(avatar, aide, n_success=55, n_struggles=4):
    """Drive pair toward readiness thresholds (needs volume + variety + success)."""
    # Need EXPERIENCE_VOLUME_TARGET=50, variety 3, coaching confidence 20, etc.
    # Seed experience memory with enough volume/variety and with recoveries
    # for emotional resilience, and align strategy_discovered with aide's.
    for i in range(n_success):
        # Every 4th record introduces a negative episode that recovers next tick
        if i % 4 == 0:
            journey = ["frustrated", "overwhelmed"]
        else:
            journey = ["calm", "confident"]
        # Next record after a negative should recover, so ensure alternation
        # already covered by above pattern: 0:negative,1:positive,4:negative,5:positive etc.
        rec = ExperienceRecord(
            task_type=f"task_{i % 3}",
            outcome_success=True,
            quality_score=0.85,
            struggles_experienced=[f"struggle_{i % n_struggles}"],
            emotional_journey=journey,
            cognitive_load_peak=0.3,
            stress_peak=0.2,
            coaching_helpful=True,
            strategy_discovered="Structured reset",
            independence_delta=0.05,
        )
        avatar.experience_memory.record(rec)

    # Seed aide effectiveness: direct counters + strategy record
    aide.total_interventions = max(aide.total_interventions, 30)
    aide.successful_interventions = 27
    # Populate strategy effectiveness tracker
    from src.aides.base_aide import _StrategyRecord

    aide._strategy_records["Structured reset"] = _StrategyRecord(
        strategy_name="Structured reset", times_used=30, times_effective=27
    )
    aide.crisis_interventions = 0
    aide.independence_achievements = 5

    # Ensure avatar not burnt out
    avatar.stress_level = 0.2
    avatar.cognitive_load = 0.3
    avatar.emotional_state = "confident"

    # Seed some independent progress — set fields the readiness assessor reads
    for task_type in ["task_0", "task_1", "task_2"]:
        prog = avatar.learning_progress.get(task_type)
        if prog is None:
            # create entry if not yet present
            from src.avatars.base_avatar import LearningProgress

            prog = LearningProgress(task_type=task_type)
            avatar.learning_progress[task_type] = prog
        prog.attempts = 20
        prog.successes = 18
        prog.independent_successes = 16
        prog.current_independence_level = 0.85
        prog.consecutive_successes = 5


# -- export / contract tests ----------------------------------------------

class TestModelFusionExports:
    def test_package_exports(self):
        from src.fusion import ModelFusionEngine, PairedTrajectoryStep, RouterTeacher  # noqa: F401

        assert ModelFusionEngine is not None
        assert PairedTrajectoryStep is not None
        assert RouterTeacher is not None

    def test_advocate_kind_constant(self):
        assert ADVOCATE_MODEL_KIND == "advocate"


# -- PairedTrajectoryStep --------------------------------------------------

class TestPairedTrajectoryStep:
    def test_from_experience_record_defaults(self):
        rec = _make_record()
        step = PairedTrajectoryStep.from_experience_record(rec)
        assert step.scenario["task_type"] == "focus"
        assert step.outcome["outcome_success"] is True
        assert step.avatar_output["struggles_experienced"] == ["attention_lapse"]

    def test_to_dict_roundtrip(self):
        rec = _make_record()
        step = PairedTrajectoryStep.from_experience_record(
            rec,
            avatar_output={"struggle_indicators": ["x"], "stress_peak": 0.6},
            aide_output={"strategy": "Structured reset"},
            observation={"stress_level": 0.6, "cognitive_load": 0.5},
        )
        d = step.to_dict()
        assert d["avatar_output"]["stress_peak"] == 0.6
        assert d["aide_output"]["strategy"] == "Structured reset"
        assert d["observation"]["stress_level"] == 0.6

    def test_build_paired_corpus_length_validation(self):
        recs = [_make_record(), _make_record()]
        with pytest.raises(ValueError, match="avatar_outputs length"):
            ModelFusionEngine.build_paired_corpus(recs, avatar_outputs=[{"x": 1}])

    def test_build_paired_corpus_happy(self):
        recs = [_make_record(), _make_record(success=False)]
        corpus = ModelFusionEngine.build_paired_corpus(recs)
        assert len(corpus) == 2
        assert corpus[0].outcome["outcome_success"] is True
        assert corpus[1].outcome["outcome_success"] is False


# -- ExperienceDataset serializer -----------------------------------------

class TestDatasetPairedSerializer:
    def test_to_paired_trajectory_steps_basic(self):
        ds = ExperienceDataset([_make_record(), _make_record(success=False)])
        steps = ds.to_paired_trajectory_steps()
        assert len(steps) == 2
        assert steps[0]["outcome"]["outcome_success"] is True
        assert "scenario" in steps[0]
        assert "observation" in steps[0]

    def test_to_paired_trajectory_steps_with_parallel_arrays(self):
        ds = ExperienceDataset([_make_record(), _make_record()])
        steps = ds.to_paired_trajectory_steps(
            avatar_outputs=[{"struggle_indicators": ["a"]}, {"struggle_indicators": ["b"]}],
            aide_outputs=[{"strategy": "Structured reset"}, None],
        )
        assert steps[0]["avatar_output"]["struggle_indicators"] == ["a"]
        assert steps[1]["aide_output"] is None


# -- RouterTeacher --------------------------------------------------------

class TestRouterTeacher:
    def test_route_produces_valid_mode(self):
        teacher = RouterTeacher()
        step = PairedTrajectoryStep(
            observation={"stress_level": 0.3, "cognitive_load": 0.3},
            avatar_output={"struggles_experienced": [], "stress_peak": 0.3, "cognitive_load_peak": 0.3},
        )
        gold = teacher.route(step)
        assert gold["mode"] in {m.value for m in AdvocateMode}
        assert gold["mode"] == AdvocateMode.PROACTIVE.value

    def test_route_crisis_mode(self):
        teacher = RouterTeacher()
        step = PairedTrajectoryStep(
            observation={"stress_level": 0.95, "cognitive_load": 0.9},
            avatar_output={"stress_peak": 0.95, "cognitive_load_peak": 0.9},
        )
        gold = teacher.route(step)
        assert gold["mode"] == AdvocateMode.CRISIS.value

    def test_route_reactive_mode(self):
        teacher = RouterTeacher()
        step = PairedTrajectoryStep(
            observation={"stress_level": 0.7, "cognitive_load": 0.5},
            avatar_output={"stress_peak": 0.7, "cognitive_load_peak": 0.5},
        )
        gold = teacher.route(step)
        assert gold["mode"] == AdvocateMode.REACTIVE.value

    def test_outcome_weighting(self):
        teacher = RouterTeacher()
        success_step = PairedTrajectoryStep(outcome={"outcome_success": True, "coaching_helpful": True})
        fail_step = PairedTrajectoryStep(outcome={"outcome_success": False})
        assert teacher._outcome_weight(success_step) > teacher._outcome_weight(fail_step)


# -- ModelFusionEngine ----------------------------------------------------

class TestModelFusionEngine:
    def test_empty_corpus_fails(self):
        avatar, aide = _make_avatar_aide()
        _prep_ready_pair(avatar, aide)
        engine = ModelFusionEngine()
        report = engine.fuse_models(avatar, aide, corpus=[], force=True)
        assert report.success is False
        assert report.failure_reason is not None and "Empty corpus" in report.failure_reason

    def test_not_eligible_without_force(self):
        avatar, aide = _make_avatar_aide()
        # Do NOT prep readiness -> should be not ready
        engine = ModelFusionEngine()
        corpus = ModelFusionEngine.build_paired_corpus([_make_record()])
        report = engine.fuse_models(avatar, aide, corpus=corpus, force=False)
        assert report.success is False
        assert report.readiness is not None
        assert report.readiness.ready is False
        assert report.failure_reason is not None and "Not eligible" in report.failure_reason

    def test_force_bypasses_eligibility_and_succeeds(self):
        avatar, aide = _make_avatar_aide()
        engine = ModelFusionEngine()
        corpus = ModelFusionEngine.build_paired_corpus([_make_record(), _make_record()])
        report = engine.fuse_models(avatar, aide, corpus=corpus, force=True)
        assert report.success is True
        assert report.model_checkpoint is not None
        assert report.fusion_result is not None
        assert report.fusion_result.model_checkpoint == report.model_checkpoint
        assert report.fusion_result.model_evals  # non-empty

    def test_ready_pair_succeeds_without_force(self):
        avatar, aide = _make_avatar_aide()
        _prep_ready_pair(avatar, aide)
        engine = ModelFusionEngine()
        corpus = ModelFusionEngine.build_paired_corpus([_make_record() for _ in range(5)])
        report = engine.fuse_models(avatar, aide, corpus=corpus, force=False)
        # May still fail if some readiness dimension not met; at least verify report shape
        assert report.readiness is not None
        # With seeded ready pair, expect success
        assert report.success is True
        assert report.model_checkpoint is not None and report.model_checkpoint.startswith("advocate_ckpt_")

    def test_held_out_split_default(self):
        avatar, aide = _make_avatar_aide()
        _prep_ready_pair(avatar, aide)
        engine = ModelFusionEngine()
        corpus = ModelFusionEngine.build_paired_corpus([_make_record() for _ in range(10)])
        report = engine.fuse_models(avatar, aide, corpus=corpus, force=True)
        assert report.success is True
        # Evals should include held_out_non_empty
        eval_names = {e.eval_name for e in report.model_evals}
        assert "held_out_non_empty" in eval_names
        assert "teacher_mode_validity" in eval_names

    def test_custom_trainer_injected(self):
        avatar, aide = _make_avatar_aide()

        class _CustomTrainer:
            def train(self, corpus, gold_outputs, config):
                assert len(corpus) == 2
                assert len(gold_outputs) == 2
                assert config.get("epochs") == 1
                return {"checkpoint_id": "custom_ckpt_123", "metrics": {"ok": True}}

        engine = ModelFusionEngine(trainer=_CustomTrainer())
        corpus = ModelFusionEngine.build_paired_corpus([_make_record(), _make_record()])
        report = engine.fuse_models(avatar, aide, corpus=corpus, force=True, trainer_config={"epochs": 1})
        assert report.success is True
        assert report.model_checkpoint == "custom_ckpt_123"

    def test_fusion_result_to_dict_includes_model_fields(self):
        avatar, aide = _make_avatar_aide()
        engine = ModelFusionEngine()
        corpus = ModelFusionEngine.build_paired_corpus([_make_record(), _make_record()])
        report = engine.fuse_models(avatar, aide, corpus=corpus, force=True)
        assert report.fusion_result is not None
        d = report.fusion_result.to_dict()
        assert "model_checkpoint" in d
        assert "model_evals" in d
        assert d["model_checkpoint"] == report.model_checkpoint
