"""
Model-Level Fusion Engine

Implements the model-fusion layer described in
``docs/specs/advocate-model-fusion-spec.md``.

This module is **fusion-only**: it does not train Avatar or Aide models
and does not serve the Advocate.  It fuses two simulation-trained
``ModelBackend`` instances (Avatar + Aide) into a single unified
Advocate model via trajectory distillation.

Pipeline
--------
0. Eligibility gate  — delegate to ``ReadinessAssessor`` (six dimensions,
   overall >= 0.65, zero blocking). Reuses existing symbolic gates.
1. Gold generation   — run a router teacher over a paired-trajectory corpus
   to produce gold outputs per step.
2. Student training  — distill into a single student via an injectable
   ``StudentTrainer`` (default is a no-op stub; real torch loop injected
   in training infra).
3. Acceptance evals  — held-out evals mapping to FusionDimension + mode
   contracts; blocking eval failure => report.success=False.
4. Emit ``FusionResult`` with ``model_checkpoint`` + ``model_evals``.

Parents are treated as black boxes; fusion sees only behaviors and
logged trajectories (``PairedTrajectoryStep``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable
import uuid

from ..advocates.base_advocate import AdvocateMode, FusionResult
from ..core.events import EventBus, Signal, SignalType
from ..core.protocols import ExperienceRecord
from .readiness_assessor import FusionDimension, FusionReadiness, ReadinessAssessor


# ---------------------------------------------------------------------------
# Paired trajectory contract (Sec. 5 of the spec)
# ---------------------------------------------------------------------------

@dataclass
class PairedTrajectoryStep:
    """
    One attempt-tick of the Avatar-Aide interaction.

    Each field maps to the spec's ``PairedTrajectoryStep`` schema and to
    existing protocol types (``ObservationReport``, ``Message``,
    ``ExperienceRecord``, ``ModelPrediction.outputs``).
    """

    step_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    scenario: Dict[str, Any] = field(default_factory=dict)
    observation: Dict[str, Any] = field(default_factory=dict)
    avatar_output: Dict[str, Any] = field(default_factory=dict)
    aide_output: Optional[Dict[str, Any]] = None
    channel_messages: List[Dict[str, Any]] = field(default_factory=list)
    outcome: Dict[str, Any] = field(default_factory=dict)
    counterfactual_label: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "scenario": self.scenario,
            "observation": self.observation,
            "avatar_output": self.avatar_output,
            "aide_output": self.aide_output,
            "channel_messages": self.channel_messages,
            "outcome": self.outcome,
            "counterfactual_label": self.counterfactual_label,
        }

    @classmethod
    def from_experience_record(
        cls,
        record: ExperienceRecord,
        avatar_output: Optional[Dict[str, Any]] = None,
        aide_output: Optional[Dict[str, Any]] = None,
        observation: Optional[Dict[str, Any]] = None,
        scenario: Optional[Dict[str, Any]] = None,
        channel_messages: Optional[List[Dict[str, Any]]] = None,
    ) -> "PairedTrajectoryStep":
        """Build a step from an ExperienceRecord plus paired outputs."""
        return cls(
            scenario=scenario or {"task_type": record.task_type, "task_context": record.task_context},
            observation=observation or {},
            avatar_output=avatar_output or {
                "struggles_experienced": record.struggles_experienced,
                "emotional_journey": record.emotional_journey,
                "cognitive_load_peak": record.cognitive_load_peak,
                "stress_peak": record.stress_peak,
            },
            aide_output=aide_output,
            channel_messages=channel_messages or [],
            outcome={
                "outcome_success": record.outcome_success,
                "quality_score": record.quality_score,
                "independence_delta": record.independence_delta,
                "coaching_helpful": record.coaching_helpful,
                "strategy_discovered": record.strategy_discovered,
            },
            counterfactual_label=None,
        )


# ---------------------------------------------------------------------------
# Evals (Sec. 7)
# ---------------------------------------------------------------------------

@dataclass
class ModelEvalResult:
    """Result of a single acceptance eval."""

    eval_name: str
    passed: bool
    score: float
    threshold: float
    detail: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "eval_name": self.eval_name,
            "passed": self.passed,
            "score": round(self.score, 4),
            "threshold": self.threshold,
            "detail": self.detail,
        }


# ---------------------------------------------------------------------------
# Router teacher (Sec. 4.3) — gold fused behavior
# ---------------------------------------------------------------------------

class RouterTeacher:
    """
    Gated blend over frozen parents; defines gold fused behavior.

    This is NOT the product — it is the teacher the student distills
    toward and the regression ceiling for evals.
    """

    def __init__(self, empathy_weight: float = 0.5, expertise_weight: float = 0.5) -> None:
        if not 0.0 <= empathy_weight <= 1.0 or not 0.0 <= expertise_weight <= 1.0:
            raise ValueError("weights must be in [0, 1]")
        self.empathy_weight = empathy_weight
        self.expertise_weight = expertise_weight

    def route(self, step: PairedTrajectoryStep) -> Dict[str, Any]:
        """
        Produce gold fused outputs for one step.

        Combines avatar internal-state + aide coaching + mode selection.
        """
        # Empathy bag: what the avatar felt
        empathy = {
            "struggles": step.avatar_output.get("struggles_experienced")
            or step.avatar_output.get("struggle_indicators")
            or [],
            "emotional_journey": step.avatar_output.get("emotional_journey", []),
            "stress_peak": step.avatar_output.get("stress_peak", step.observation.get("stress_level", 0.0)),
            "cognitive_load_peak": step.avatar_output.get(
                "cognitive_load_peak", step.observation.get("cognitive_load", 0.0)
            ),
        }

        # Expertise bag: what the aide would do
        expertise = dict(step.aide_output or {})

        # Mode selection: mirrors BaseAdvocate._determine_mode thresholds
        stress = float(step.observation.get("stress_level", empathy["stress_peak"] or 0.5))
        load = float(step.observation.get("cognitive_load", empathy["cognitive_load_peak"] or 0.5))
        building_independence = bool(step.observation.get("building_independence", False))

        if stress > 0.8 or load > 0.9:
            mode = AdvocateMode.CRISIS.value
        elif stress > 0.6 or load > 0.7:
            mode = AdvocateMode.REACTIVE.value
        elif building_independence:
            mode = AdvocateMode.INDEPENDENCE_BUILDING.value
        else:
            mode = AdvocateMode.PROACTIVE.value

        return {
            "empathy": empathy,
            "expertise": expertise,
            "mode": mode,
            "gold_weight": self._outcome_weight(step),
        }

    def route_corpus(self, corpus: List[PairedTrajectoryStep]) -> List[Dict[str, Any]]:
        return [self.route(s) for s in corpus]

    @staticmethod
    def _outcome_weight(step: PairedTrajectoryStep) -> float:
        """Up-weight trajectories where the pair succeeded."""
        outcome = step.outcome
        if outcome.get("outcome_success") and outcome.get("coaching_helpful"):
            return 1.0
        if outcome.get("outcome_success"):
            return 0.8
        return 0.4


# ---------------------------------------------------------------------------
# Student trainer protocol — inject real torch loop in training infra
# ---------------------------------------------------------------------------

@runtime_checkable
class StudentTrainer(Protocol):
    """Protocol for the student distillation loop."""

    def train(
        self,
        corpus: List[PairedTrajectoryStep],
        gold_outputs: List[Dict[str, Any]],
        config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Train / distill and return ``{"checkpoint_id": str, "metrics": dict}``.
        """
        ...


class NoOpStudentTrainer:
    """
    Default stub trainer: no gradients, just mints a checkpoint id.

    Real training infra replaces this with a torch implementation.
    """

    def train(
        self,
        corpus: List[PairedTrajectoryStep],
        gold_outputs: List[Dict[str, Any]],
        config: Dict[str, Any],
    ) -> Dict[str, Any]:
        _ = (corpus, gold_outputs, config)
        return {
            "checkpoint_id": f"advocate_ckpt_{uuid.uuid4().hex[:8]}",
            "metrics": {"distill_loss": 0.0, "steps_trained": len(corpus)},
        }


# ---------------------------------------------------------------------------
# Model fusion report
# ---------------------------------------------------------------------------

@dataclass
class ModelFusionReport:
    """Detailed report of a model-level fusion attempt."""

    fusion_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    avatar_model_id: str = ""
    aide_model_id: str = ""
    readiness: Optional[FusionReadiness] = None
    success: bool = False
    fusion_result: Optional[FusionResult] = None
    model_checkpoint: Optional[str] = None
    model_evals: List[ModelEvalResult] = field(default_factory=list)
    failure_reason: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fusion_id": self.fusion_id,
            "avatar_model_id": self.avatar_model_id,
            "aide_model_id": self.aide_model_id,
            "success": self.success,
            "readiness": self.readiness.to_dict() if self.readiness else None,
            "fusion_result": self.fusion_result.to_dict() if self.fusion_result else None,
            "model_checkpoint": self.model_checkpoint,
            "model_evals": [e.to_dict() for e in self.model_evals],
            "failure_reason": self.failure_reason,
            "timestamp": self.timestamp.isoformat(),
        }


# ---------------------------------------------------------------------------
# ModelFusionEngine
# ---------------------------------------------------------------------------

class ModelFusionEngine:
    """
    Model-level fusion: Avatar model + Aide model -> unified Advocate.

    Parents are black boxes conforming to ``ModelBackend``; fusion sees
    only ``PairedTrajectoryStep`` corpora.  The harness is provider-
    agnostic and delegates real optimization to an injectable
    ``StudentTrainer``.
    """

    def __init__(
        self,
        event_bus: Optional[EventBus] = None,
        readiness_assessor: Optional[ReadinessAssessor] = None,
        teacher: Optional[RouterTeacher] = None,
        trainer: Optional[StudentTrainer] = None,
    ) -> None:
        self.event_bus = event_bus or EventBus()
        self._assessor = readiness_assessor or ReadinessAssessor()
        self._teacher = teacher or RouterTeacher()
        self._trainer: StudentTrainer = trainer or NoOpStudentTrainer()
        self._history: List[ModelFusionReport] = []

    # -- eligibility (symbolic gate) ---------------------------------------

    def check_eligibility(self, avatar: Any, aide: Any) -> FusionReadiness:
        """Delegate to ReadinessAssessor; avatar/aide are BaseAvatar/BaseAide."""
        return self._assessor.assess(avatar, aide)

    # -- corpus helpers ----------------------------------------------------

    @staticmethod
    def build_paired_corpus(
        records: List[ExperienceRecord],
        avatar_outputs: Optional[List[Dict[str, Any]]] = None,
        aide_outputs: Optional[List[Optional[Dict[str, Any]]]] = None,
        observations: Optional[List[Dict[str, Any]]] = None,
        scenarios: Optional[List[Dict[str, Any]]] = None,
    ) -> List[PairedTrajectoryStep]:
        """
        Build a paired corpus from parallel arrays.

        ``records`` is required; the optional parallel arrays default to
        per-record derivations when omitted.  All provided arrays must
        match ``len(records)``.
        """
        n = len(records)
        for name, arr in [
            ("avatar_outputs", avatar_outputs),
            ("aide_outputs", aide_outputs),
            ("observations", observations),
            ("scenarios", scenarios),
        ]:
            if arr is not None and len(arr) != n:
                raise ValueError(f"{name} length {len(arr)} != records length {n}")

        corpus: List[PairedTrajectoryStep] = []
        for i, rec in enumerate(records):
            corpus.append(
                PairedTrajectoryStep.from_experience_record(
                    rec,
                    avatar_output=avatar_outputs[i] if avatar_outputs else None,
                    aide_output=aide_outputs[i] if aide_outputs else None,
                    observation=observations[i] if observations else None,
                    scenario=scenarios[i] if scenarios else None,
                )
            )
        return corpus

    # -- main entrypoint ---------------------------------------------------

    def fuse_models(
        self,
        avatar: Any,
        aide: Any,
        corpus: List[PairedTrajectoryStep],
        trainer_config: Optional[Dict[str, Any]] = None,
        force: bool = False,
        held_out_corpus: Optional[List[PairedTrajectoryStep]] = None,
    ) -> ModelFusionReport:
        """
        Attempt model-level fusion.

        Args:
            avatar: BaseAvatar (carries avatar_id, experience_memory, etc.)
            aide: BaseAide (carries aide_id, strategy metrics, etc.)
            corpus: paired trajectory steps for distillation
            trainer_config: forwarded to ``StudentTrainer.train``
            force: if True, skip eligibility gate
            held_out_corpus: optional held-out split for acceptance evals;
                defaults to a 20% tail slice of ``corpus``.

        Returns:
            ModelFusionReport with success/failure and, on success,
            a FusionResult bearing ``model_checkpoint``.
        """
        avatar_id = getattr(avatar, "avatar_id", "unknown_avatar")
        aide_id = getattr(aide, "aide_id", "unknown_aide")
        report = ModelFusionReport(avatar_model_id=str(avatar_id), aide_model_id=str(aide_id))

        # 0. Eligibility gate (symbolic)
        self._emit(SignalType.FUSION_READINESS_CHECK, {"avatar_id": str(avatar_id), "aide_id": str(aide_id)})
        readiness = self._assessor.assess(avatar, aide)
        report.readiness = readiness
        if not readiness.ready and not force:
            report.failure_reason = (
                f"Not eligible. Blocking: {[d.name for d in readiness.blocking_dimensions]}. "
                f"Overall {readiness.overall_score:.2f} < {self._assessor.OVERALL_THRESHOLD}"
            )
            self._emit(SignalType.FUSION_FAILED, {"reason": report.failure_reason})
            self._history.append(report)
            return report

        if not corpus:
            report.failure_reason = "Empty corpus: need at least 1 PairedTrajectoryStep"
            self._emit(SignalType.FUSION_FAILED, {"reason": report.failure_reason})
            self._history.append(report)
            return report

        self._emit(SignalType.FUSION_STARTED, {"avatar_id": str(avatar_id), "aide_id": str(aide_id)})

        # 1. Gold generation
        gold = self._teacher.route_corpus(corpus)

        # 2. Student training (injectable)
        train_result = self._trainer.train(corpus, gold, trainer_config or {})
        checkpoint_id: str = train_result.get("checkpoint_id") or f"advocate_ckpt_{uuid.uuid4().hex[:8]}"
        report.model_checkpoint = checkpoint_id

        # 3. Acceptance evals
        eval_corpus = held_out_corpus if held_out_corpus is not None else self._held_out_split(corpus)
        evals = self._run_acceptance_evals(corpus, eval_corpus, gold, readiness)
        report.model_evals = evals

        blocking_evals = [e for e in evals if not e.passed]
        if blocking_evals and not force:
            report.failure_reason = f"Acceptance evals failed: {[e.eval_name for e in blocking_evals]}"
            self._emit(SignalType.FUSION_FAILED, {"reason": report.failure_reason, "evals": [e.to_dict() for e in evals]})
            self._history.append(report)
            return report
        if blocking_evals:
            # force=True: surface warning but allow success
            pass

        # 4. Build FusionResult (reuse symbolic quality + attach checkpoint)
        # Import here to avoid cycles at module import time
        from .fusion_engine import FusionEngine as SymbolicEngine

        sym = SymbolicEngine(event_bus=self.event_bus)
        # Reuse symbolic engine's capability/quality derivation for consistency
        # but call its internals via the public fuse(force=True) path on a lightweight report
        # to avoid duplicating logic. Instead, derive directly for the model path:
        sym_report = sym.fuse(avatar, aide, force=True)
        base_result = sym_report.fusion_result
        if base_result is None:
            # Fallback: should not happen with force=True, but handle defensively
            report.failure_reason = "Symbolic fusion failed even with force=True"
            self._emit(SignalType.FUSION_FAILED, {"reason": report.failure_reason})
            self._history.append(report)
            return report

        # Attach model checkpoint + evals to the result
        base_result.model_checkpoint = checkpoint_id
        base_result.model_evals = [e.to_dict() for e in evals]
        if blocking_evals:
            base_result.fusion_notes.append("WARNING: acceptance evals overridden via force=True")

        report.fusion_result = base_result
        report.success = True
        self._emit(
            SignalType.FUSION_COMPLETED,
            {"advocate_id": base_result.advocate_id, "model_checkpoint": checkpoint_id},
        )
        self._history.append(report)
        return report

    # -- evals -------------------------------------------------------------

    def _run_acceptance_evals(
        self,
        corpus: List[PairedTrajectoryStep],
        held_out: List[PairedTrajectoryStep],
        gold: List[Dict[str, Any]],
        readiness: FusionReadiness,
    ) -> List[ModelEvalResult]:
        """
        Lightweight acceptance evals for the harness layer.

        Real model evals (empathy AUROC, coaching replay success, etc.)
        are heavier and live in training infra; these checks ensure the
        fusion harness itself is not producing degenerate outputs and that
        readiness-derived signals are sane on the corpus.
        """
        evals: List[ModelEvalResult] = []

        # 1. Corpus non-degeneracy: at least one success in training corpus
        success_rate = sum(1 for s in corpus if s.outcome.get("outcome_success")) / max(len(corpus), 1)
        evals.append(
            ModelEvalResult(
                eval_name="corpus_has_successes",
                passed=success_rate > 0.0,
                score=success_rate,
                threshold=0.0,
                detail={"success_rate": success_rate},
            )
        )

        # 2. Teacher produces valid modes
        valid_modes = {m.value for m in AdvocateMode}
        gold_modes = [g.get("mode") for g in gold]
        valid_ratio = sum(1 for m in gold_modes if m in valid_modes) / max(len(gold_modes), 1)
        evals.append(
            ModelEvalResult(
                eval_name="teacher_mode_validity",
                passed=valid_ratio == 1.0,
                score=valid_ratio,
                threshold=1.0,
                detail={"valid_ratio": valid_ratio},
            )
        )

        # 3. Readiness parity: readiness overall should not be degenerate
        evals.append(
            ModelEvalResult(
                eval_name="readiness_sanity",
                passed=readiness.overall_score >= 0.0,
                score=readiness.overall_score,
                threshold=0.0,
                detail={"overall_score": readiness.overall_score},
            )
        )

        # 4. Held-out non-empty
        evals.append(
            ModelEvalResult(
                eval_name="held_out_non_empty",
                passed=len(held_out) > 0,
                score=float(len(held_out)),
                threshold=1.0,
                detail={"held_out_size": len(held_out), "corpus_size": len(corpus)},
            )
        )

        # 5. Burnout safety proxy: avg stress in corpus not critical
        avg_stress = sum(
            float(s.observation.get("stress_level", s.avatar_output.get("stress_peak", 0.5)) or 0.5)
            for s in corpus
        ) / max(len(corpus), 1)
        evals.append(
            ModelEvalResult(
                eval_name="burnout_safety_proxy",
                passed=avg_stress < 0.9,
                score=1.0 - avg_stress,
                threshold=0.1,
                detail={"avg_stress": avg_stress},
            )
        )

        return evals

    @staticmethod
    def _held_out_split(corpus: List[PairedTrajectoryStep]) -> List[PairedTrajectoryStep]:
        if len(corpus) < 2:
            return list(corpus)
        k = max(1, len(corpus) // 5)
        return corpus[-k:]

    # -- history + events --------------------------------------------------

    @property
    def history(self) -> List[ModelFusionReport]:
        return list(self._history)

    def _emit(self, signal_type: SignalType, data: Dict[str, Any]) -> None:
        self.event_bus.emit(
            Signal(signal_type=signal_type, source_id="model_fusion_engine", source_type="engine", data=data)
        )
