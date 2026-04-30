"""
Fusion Engine

Orchestrates the actual fusion of an Avatar + Aide into an Advocate.

Fusion is the culmination of the experiential learning process:
1. Assess readiness across multiple dimensions
2. Extract experiential knowledge from Avatar's memory
3. Extract proven strategies from Aide's effectiveness records
4. Combine into a unified Advocate capability profile
5. Validate the fused Advocate meets quality standards
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

from ..core.events import EventBus, Signal, SignalType
from ..avatars.base_avatar import BaseAvatar
from ..aides.base_aide import BaseAide
from ..advocates.base_advocate import (
    BaseAdvocate,
    AdvocateCapabilities,
    AdvocateMode,
    EmpathyLevel,
    FusionResult,
)
from .readiness_assessor import (
    ReadinessAssessor,
    FusionReadiness,
    FusionDimension,
)


@dataclass
class FusionReport:
    """Detailed report of a fusion attempt."""
    fusion_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    avatar_id: str = ""
    aide_id: str = ""
    readiness: Optional[FusionReadiness] = None
    success: bool = False
    fusion_result: Optional[FusionResult] = None
    failure_reason: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fusion_id": self.fusion_id,
            "avatar_id": self.avatar_id,
            "aide_id": self.aide_id,
            "success": self.success,
            "readiness": self.readiness.to_dict() if self.readiness else None,
            "fusion_result": self.fusion_result.to_dict() if self.fusion_result else None,
            "failure_reason": self.failure_reason,
            "timestamp": self.timestamp.isoformat(),
        }


class FusionEngine:
    """
    Manages the Avatar + Aide -> Advocate fusion process.

    The engine:
    1. Checks readiness via ReadinessAssessor
    2. Extracts Avatar experiences and Aide expertise
    3. Determines empathy level based on experiential depth
    4. Builds the AdvocateCapabilities profile
    5. Produces a FusionResult that a BaseAdvocate subclass consumes
    """

    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self.event_bus = event_bus or EventBus()
        self._assessor = ReadinessAssessor()
        self._fusion_history: List[FusionReport] = []

    def check_readiness(self, avatar: BaseAvatar, aide: BaseAide) -> FusionReadiness:
        """Assess whether a pair is ready to fuse."""
        return self._assessor.assess(avatar, aide)

    def fuse(
        self,
        avatar: BaseAvatar,
        aide: BaseAide,
        force: bool = False,
    ) -> FusionReport:
        """
        Attempt to fuse an Avatar and Aide into an Advocate.

        Args:
            avatar: The Avatar with experiential knowledge.
            aide: The Aide with proven coaching expertise.
            force: If True, skip readiness check (for testing).

        Returns:
            FusionReport with success/failure details.
        """
        report = FusionReport(avatar_id=avatar.avatar_id, aide_id=aide.aide_id)

        self._emit(SignalType.FUSION_READINESS_CHECK, {
            "avatar_id": avatar.avatar_id,
            "aide_id": aide.aide_id,
        })

        # 1. Check readiness
        readiness = self._assessor.assess(avatar, aide)
        report.readiness = readiness

        if not readiness.ready and not force:
            report.failure_reason = (
                f"Not ready. Blocking dimensions: "
                f"{[d.name for d in readiness.blocking_dimensions]}. "
                f"Overall score: {readiness.overall_score:.2f}"
            )
            self._emit(SignalType.FUSION_FAILED, {
                "reason": report.failure_reason,
                "readiness": readiness.to_dict(),
            })
            self._fusion_history.append(report)
            return report

        self._emit(SignalType.FUSION_STARTED, {
            "avatar_id": avatar.avatar_id,
            "aide_id": aide.aide_id,
            "readiness_score": readiness.overall_score,
        })

        # 2. Extract experiential knowledge
        experiential_knowledge = self._extract_avatar_experience(avatar)

        # 3. Extract aide expertise
        aide_expertise = self._extract_aide_expertise(aide)

        # 4. Determine empathy level
        empathy_level = self._determine_empathy_level(readiness)

        # 5. Build capabilities
        capabilities = self._build_capabilities(
            avatar, aide, readiness, empathy_level
        )

        # 6. Compute fusion quality
        quality_score = self._compute_fusion_quality(readiness, capabilities)

        # 7. Validate
        validation = self._validate_fusion(capabilities, quality_score)

        # 8. Build result
        advocate_id = f"advocate_{avatar.trait_name}_{str(uuid.uuid4())[:8]}"
        fusion_result = FusionResult(
            fusion_id=report.fusion_id,
            avatar_id=avatar.avatar_id,
            aide_id=aide.aide_id,
            advocate_id=advocate_id,
            fusion_timestamp=datetime.now(),
            fusion_quality_score=quality_score,
            capabilities=capabilities,
            validation_results=validation,
            fusion_notes=[
                f"Experiential depth: {experiential_knowledge['total_experiences']} experiences",
                f"Aide effectiveness: {aide_expertise['success_rate']:.1%}",
                f"Empathy level: {empathy_level.value}",
                f"Fusion quality: {quality_score:.2f}",
            ],
            avatar_experience_summary=experiential_knowledge,
            aide_expertise_summary=aide_expertise,
        )

        if not validation['all_passed'] and not force:
            report.failure_reason = (
                f"Validation failed: {[k for k, v in validation['checks'].items() if not v]}"
            )
            self._emit(SignalType.FUSION_FAILED, {
                'reason': report.failure_reason,
                'validation': validation,
            })
            self._fusion_history.append(report)
            return report

        # If forced but validation failed, still mark but add warning note
        if not validation['all_passed']:
            fusion_result.fusion_notes.append("WARNING: Validation overridden via force=True")

        report.success = True
        report.fusion_result = fusion_result

        self._emit(SignalType.FUSION_COMPLETED, {
            "advocate_id": advocate_id,
            "quality_score": quality_score,
            "empathy_level": empathy_level.value,
        })

        self._fusion_history.append(report)
        return report

    # ------------------------------------------------------------------
    # Knowledge extraction
    # ------------------------------------------------------------------

    def _extract_avatar_experience(self, avatar: BaseAvatar) -> Dict[str, Any]:
        """Extract structured experiential knowledge from the Avatar."""
        memory = avatar.experience_memory
        return {
            "total_experiences": memory.total_experiences,
            "success_rate": memory.success_rate,
            "recurring_struggles": memory.get_recurring_struggles(),
            "effective_strategies": memory.get_effective_strategies(),
            "independence_trajectory": memory.get_independence_trajectory(),
            "learning_progress": {
                k: {
                    "attempts": v.attempts,
                    "success_rate": v.success_rate,
                    "independence": v.current_independence_level,
                }
                for k, v in avatar.learning_progress.items()
            },
        }

    def _extract_aide_expertise(self, aide: BaseAide) -> Dict[str, Any]:
        """Extract proven expertise from the Aide."""
        metrics = aide.get_coaching_effectiveness_metrics()
        return {
            "expertise_area": aide.expertise_area,
            "success_rate": metrics["success_rate"],
            "total_interventions": metrics["total_interventions"],
            "strategy_effectiveness": metrics["strategy_effectiveness"],
            "crisis_interventions": metrics["crisis_interventions"],
            "independence_achievements": metrics["independence_achievements"],
        }

    # ------------------------------------------------------------------
    # Fusion logic
    # ------------------------------------------------------------------

    def _determine_empathy_level(self, readiness: FusionReadiness) -> EmpathyLevel:
        """Map experiential depth to empathy level."""
        exp_score = readiness.dimension_scores.get(FusionDimension.EXPERIENTIAL_DEPTH)
        if exp_score is None:
            return EmpathyLevel.THEORETICAL

        if exp_score.score >= 0.9:
            return EmpathyLevel.DEEP_EXPERIENTIAL
        elif exp_score.score >= 0.7:
            return EmpathyLevel.EXPERIENTIAL
        elif exp_score.score >= 0.4:
            return EmpathyLevel.OBSERVATIONAL
        else:
            return EmpathyLevel.THEORETICAL

    def _build_capabilities(
        self,
        avatar: BaseAvatar,
        aide: BaseAide,
        readiness: FusionReadiness,
        empathy_level: EmpathyLevel,
    ) -> AdvocateCapabilities:
        """Construct the capability profile for the fused Advocate."""
        # Expertise areas from the Aide
        expertise_areas = [aide.expertise_area]

        # Coaching strategies that proved effective
        effective = aide.get_strategy_effectiveness_summary()
        strategies = [
            name for name, info in effective.items()
            if info.get("effectiveness", 0) > 0.5
        ]
        if not strategies:
            strategies = [aide.expertise_area]

        # Determine capability flags
        crisis_capable = aide.crisis_interventions > 0
        independence_capable = aide.independence_achievements > 0

        # Burnout prevention from readiness
        burnout_dim = readiness.dimension_scores.get(FusionDimension.BURNOUT_MANAGEMENT)
        burnout_capable = burnout_dim is not None and burnout_dim.passes

        # Real-world applicability from strategy internalisation
        strat_dim = readiness.dimension_scores.get(FusionDimension.STRATEGY_INTERNALISATION)
        real_world = strat_dim.score if strat_dim else 0.5

        # Clinical validation from coaching effectiveness
        coach_dim = readiness.dimension_scores.get(FusionDimension.COACHING_EFFECTIVENESS)
        clinical = coach_dim.score if coach_dim else 0.5

        return AdvocateCapabilities(
            empathy_level=empathy_level,
            expertise_areas=expertise_areas,
            coaching_strategies=strategies,
            crisis_intervention=crisis_capable,
            independence_building=independence_capable,
            burnout_prevention=burnout_capable,
            real_world_applicability=real_world,
            clinical_validation=clinical,
        )

    def _compute_fusion_quality(
        self, readiness: FusionReadiness, capabilities: AdvocateCapabilities
    ) -> float:
        """Compute an overall quality score for the fusion."""
        # Weighted average of readiness + capability richness
        readiness_weight = 0.6
        capability_weight = 0.4

        cap_flags = [
            capabilities.crisis_intervention,
            capabilities.independence_building,
            capabilities.burnout_prevention,
        ]
        cap_score = sum(cap_flags) / len(cap_flags)

        return (
            readiness.overall_score * readiness_weight
            + cap_score * capability_weight
        )

    def _validate_fusion(
        self, capabilities: AdvocateCapabilities, quality: float
    ) -> Dict[str, Any]:
        """Run validation checks on the fusion output."""
        checks = {
            "has_empathy": capabilities.empathy_level != EmpathyLevel.THEORETICAL,
            "has_expertise": len(capabilities.expertise_areas) > 0,
            "has_strategies": len(capabilities.coaching_strategies) > 0,
            "quality_above_minimum": quality >= 0.3,
        }
        return {
            "checks": checks,
            "all_passed": all(checks.values()),
            "quality_score": quality,
        }

    # ------------------------------------------------------------------
    # Event emission
    # ------------------------------------------------------------------

    def _emit(self, signal_type: SignalType, data: Dict[str, Any]) -> None:
        self.event_bus.emit(Signal(
            signal_type=signal_type,
            source_id="fusion_engine",
            source_type="engine",
            data=data,
        ))
