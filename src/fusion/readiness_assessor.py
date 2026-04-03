"""
Fusion Readiness Assessor

Evaluates whether an Avatar-Aide pair is ready for fusion across
multiple dimensions.  Fusion is not a binary gate — it produces a
multi-dimensional readiness profile that determines fusion quality.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional
from datetime import datetime

from ..avatars.base_avatar import BaseAvatar
from ..aides.base_aide import BaseAide


class FusionDimension(Enum):
    """Dimensions along which fusion readiness is assessed."""
    EXPERIENTIAL_DEPTH = auto()       # How deeply has the Avatar lived the struggle?
    COACHING_EFFECTIVENESS = auto()   # How effective was the Aide's coaching?
    INDEPENDENCE_LEVEL = auto()       # Can the Avatar manage without the Aide?
    EMOTIONAL_RESILIENCE = auto()     # Has the Avatar built emotional coping skills?
    STRATEGY_INTERNALISATION = auto() # Has the Avatar adopted strategies as its own?
    BURNOUT_MANAGEMENT = auto()       # Can the pair manage burnout risk?


@dataclass
class DimensionScore:
    """Score for a single fusion dimension."""
    dimension: FusionDimension
    score: float  # 0.0 to 1.0
    evidence: List[str] = field(default_factory=list)
    threshold: float = 0.6  # minimum to pass

    @property
    def passes(self) -> bool:
        return self.score >= self.threshold


@dataclass
class FusionReadiness:
    """Complete fusion readiness assessment."""
    avatar_id: str
    aide_id: str
    dimension_scores: Dict[FusionDimension, DimensionScore] = field(default_factory=dict)
    overall_score: float = 0.0
    ready: bool = False
    blocking_dimensions: List[FusionDimension] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "avatar_id": self.avatar_id,
            "aide_id": self.aide_id,
            "overall_score": round(self.overall_score, 3),
            "ready": self.ready,
            "dimensions": {
                d.name: {"score": round(s.score, 3), "passes": s.passes}
                for d, s in self.dimension_scores.items()
            },
            "blocking_dimensions": [d.name for d in self.blocking_dimensions],
            "recommendations": self.recommendations,
            "timestamp": self.timestamp.isoformat(),
        }


class ReadinessAssessor:
    """
    Assesses fusion readiness for an Avatar-Aide pair.

    Each dimension is scored independently, then combined into an
    overall readiness verdict.  The pair is "ready" when all
    dimensions pass their individual thresholds AND the overall
    score exceeds 0.65.
    """

    OVERALL_THRESHOLD = 0.65
    EXPERIENCE_VOLUME_TARGET = 50
    EXPERIENCE_VARIETY_TARGET = 3
    EXPERIENCE_VOLUME_WEIGHT = 0.6
    EXPERIENCE_VARIETY_WEIGHT = 0.4
    COACHING_CONFIDENCE_TARGET = 20
    INDEPENDENCE_LEVEL_WEIGHT = 0.7
    INDEPENDENT_TASK_RATIO_WEIGHT = 0.3
    NEGATIVE_EMOTIONAL_STATES = {"frustrated", "disappointed", "overwhelmed"}
    RESILIENCE_RECOVERY_WEIGHT = 0.6
    RESILIENCE_STRESS_WEIGHT = 0.4
    INTERNALISATION_STRATEGY_BONUS = 0.05
    CRISIS_INTERVENTION_PENALTY = 0.05
    CRISIS_INTERVENTION_PENALTY_CAP = 0.3

    def assess(self, avatar: BaseAvatar, aide: BaseAide) -> FusionReadiness:
        """Run the full readiness assessment."""
        scores: Dict[FusionDimension, DimensionScore] = {}

        scores[FusionDimension.EXPERIENTIAL_DEPTH] = self._assess_experiential_depth(avatar)
        scores[FusionDimension.COACHING_EFFECTIVENESS] = self._assess_coaching_effectiveness(aide)
        scores[FusionDimension.INDEPENDENCE_LEVEL] = self._assess_independence(avatar)
        scores[FusionDimension.EMOTIONAL_RESILIENCE] = self._assess_emotional_resilience(avatar)
        scores[FusionDimension.STRATEGY_INTERNALISATION] = self._assess_strategy_internalisation(avatar, aide)
        scores[FusionDimension.BURNOUT_MANAGEMENT] = self._assess_burnout_management(avatar, aide)

        blocking = [d for d, s in scores.items() if not s.passes]
        overall = sum(s.score for s in scores.values()) / len(scores) if scores else 0.0
        ready = overall >= self.OVERALL_THRESHOLD and len(blocking) == 0

        recommendations = self._generate_recommendations(scores, blocking)

        return FusionReadiness(
            avatar_id=avatar.avatar_id,
            aide_id=aide.aide_id,
            dimension_scores=scores,
            overall_score=overall,
            ready=ready,
            blocking_dimensions=blocking,
            recommendations=recommendations,
        )

    # ------------------------------------------------------------------
    # Dimension assessors
    # ------------------------------------------------------------------

    def _assess_experiential_depth(self, avatar: BaseAvatar) -> DimensionScore:
        """Has the Avatar accumulated enough lived experience?"""
        total = avatar.experience_memory.total_experiences
        recurring = avatar.experience_memory.get_recurring_struggles()

        # Score based on volume and variety of experiences
        volume_score = min(1.0, total / self.EXPERIENCE_VOLUME_TARGET)
        variety_score = min(1.0, len(recurring) / self.EXPERIENCE_VARIETY_TARGET)
        score = (
            volume_score * self.EXPERIENCE_VOLUME_WEIGHT
            + variety_score * self.EXPERIENCE_VARIETY_WEIGHT
        )

        evidence = [
            f"Total experiences: {total}",
            f"Recurring struggle types: {len(recurring)}",
        ]
        return DimensionScore(
            dimension=FusionDimension.EXPERIENTIAL_DEPTH,
            score=score,
            evidence=evidence,
        )

    def _assess_coaching_effectiveness(self, aide: BaseAide) -> DimensionScore:
        """Has the Aide been effective in its coaching?"""
        metrics = aide.get_coaching_effectiveness_metrics()
        success_rate = metrics.get("success_rate", 0.0)
        total = metrics.get("total_interventions", 0)

        # Need enough interventions to have a meaningful rate
        confidence = min(1.0, total / self.COACHING_CONFIDENCE_TARGET)
        score = success_rate * confidence

        evidence = [
            f"Coaching success rate: {success_rate:.1%}",
            f"Total interventions: {total}",
        ]
        return DimensionScore(
            dimension=FusionDimension.COACHING_EFFECTIVENESS,
            score=score,
            evidence=evidence,
        )

    def _assess_independence(self, avatar: BaseAvatar) -> DimensionScore:
        """Can the Avatar manage tasks independently?"""
        independence = avatar.get_independence_level()
        progress_items = avatar.learning_progress.values()
        independent_tasks = sum(1 for p in progress_items if p.is_independent)
        total_tasks = len(avatar.learning_progress) or 1

        score = (
            independence * self.INDEPENDENCE_LEVEL_WEIGHT
            + (independent_tasks / total_tasks) * self.INDEPENDENT_TASK_RATIO_WEIGHT
        )

        evidence = [
            f"Overall independence: {independence:.1%}",
            f"Independent task types: {independent_tasks}/{total_tasks}",
        ]
        return DimensionScore(
            dimension=FusionDimension.INDEPENDENCE_LEVEL,
            score=score,
            evidence=evidence,
        )

    def _assess_emotional_resilience(self, avatar: BaseAvatar) -> DimensionScore:
        """Has the Avatar built emotional coping capacity?"""
        # Look at emotional journey in experiences
        records = avatar.experience_memory.get_records()
        if not records:
            return DimensionScore(
                dimension=FusionDimension.EMOTIONAL_RESILIENCE,
                score=0.0,
                evidence=["No experiences recorded yet"],
            )

        # Count recovery from negative states
        recoveries = 0
        negative_episodes = 0
        for i, r in enumerate(records):
            if any(s in self.NEGATIVE_EMOTIONAL_STATES for s in r.emotional_journey):
                negative_episodes += 1
                # Check if next experience shows recovery
                if i + 1 < len(records):
                    next_emotions = records[i + 1].emotional_journey
                    if any(s not in self.NEGATIVE_EMOTIONAL_STATES for s in next_emotions):
                        recoveries += 1

        recovery_rate = recoveries / max(negative_episodes, 1)
        current_stress = avatar.stress_level
        resilience_bonus = max(0.0, 1.0 - current_stress)

        score = (
            recovery_rate * self.RESILIENCE_RECOVERY_WEIGHT
            + resilience_bonus * self.RESILIENCE_STRESS_WEIGHT
        )

        evidence = [
            f"Emotional recovery rate: {recovery_rate:.1%}",
            f"Current stress: {current_stress:.1%}",
        ]
        return DimensionScore(
            dimension=FusionDimension.EMOTIONAL_RESILIENCE,
            score=score,
            evidence=evidence,
        )

    def _assess_strategy_internalisation(
        self, avatar: BaseAvatar, aide: BaseAide
    ) -> DimensionScore:
        """Has the Avatar adopted coaching strategies as its own?"""
        effective = avatar.experience_memory.get_effective_strategies()
        aide_strategies = aide.get_strategy_effectiveness_summary()

        # Overlap: strategies the Aide taught that the Avatar now uses independently
        internalised = set(effective.keys()) & set(aide_strategies.keys())
        total_taught = len(aide_strategies) or 1
        internalisation_rate = len(internalised) / total_taught

        score = min(
            1.0,
            internalisation_rate + len(effective) * self.INTERNALISATION_STRATEGY_BONUS,
        )

        evidence = [
            f"Strategies internalised: {len(internalised)}",
            f"Aide strategies taught: {len(aide_strategies)}",
            f"Avatar effective strategies: {len(effective)}",
        ]
        return DimensionScore(
            dimension=FusionDimension.STRATEGY_INTERNALISATION,
            score=score,
            evidence=evidence,
        )

    def _assess_burnout_management(
        self, avatar: BaseAvatar, aide: BaseAide
    ) -> DimensionScore:
        """Can the pair manage burnout risk effectively?"""
        burnout = avatar.assess_burnout_risk()
        crisis_count = aide.crisis_interventions

        # Low burnout risk + few crises = good management
        risk_score = 1.0 - burnout["risk_score"]
        crisis_penalty = min(
            self.CRISIS_INTERVENTION_PENALTY_CAP,
            crisis_count * self.CRISIS_INTERVENTION_PENALTY,
        )
        score = max(0.0, risk_score - crisis_penalty)

        evidence = [
            f"Current burnout risk: {burnout['risk_level']}",
            f"Crisis interventions needed: {crisis_count}",
        ]
        return DimensionScore(
            dimension=FusionDimension.BURNOUT_MANAGEMENT,
            score=score,
            evidence=evidence,
        )

    # ------------------------------------------------------------------
    # Recommendations
    # ------------------------------------------------------------------

    def _generate_recommendations(
        self,
        scores: Dict[FusionDimension, DimensionScore],
        blocking: List[FusionDimension],
    ) -> List[str]:
        recs: List[str] = []
        for dim in blocking:
            ds = scores[dim]
            if dim == FusionDimension.EXPERIENTIAL_DEPTH:
                recs.append(f"Need more experiences (current: {ds.score:.0%}, target: {ds.threshold:.0%})")
            elif dim == FusionDimension.COACHING_EFFECTIVENESS:
                recs.append("Improve coaching strategy selection and delivery")
            elif dim == FusionDimension.INDEPENDENCE_LEVEL:
                recs.append("Avatar needs more independent task completions")
            elif dim == FusionDimension.EMOTIONAL_RESILIENCE:
                recs.append("Build Avatar's emotional coping through gradual challenge increase")
            elif dim == FusionDimension.STRATEGY_INTERNALISATION:
                recs.append("Avatar should practice coached strategies without Aide prompting")
            elif dim == FusionDimension.BURNOUT_MANAGEMENT:
                recs.append("Reduce burnout risk before fusion")
        return recs
