"""
Base Advocate Class

The foundation for all fused Advocates. Combines Avatar's experiential
understanding of ADHD struggles with Aide's proven expertise and coaching
strategies.

Architecture notes
------------------
* An Advocate is created by the FusionEngine, which produces a FusionResult
  containing the AdvocateCapabilities profile.
* The Advocate draws on the Avatar's ExperienceMemory to provide empathic
  understanding and on the Aide's strategy effectiveness data to provide
  expert guidance.
* Operating modes (PROACTIVE, REACTIVE, CRISIS, etc.) are selected
  automatically based on user context assessment.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime

from ..core.events import EventBus, Signal, SignalType
from ..core.protocols import ExperienceMemory


# ---------------------------------------------------------------------------
# Severity assessment thresholds
# ---------------------------------------------------------------------------

CRITICAL_STRESS_THRESHOLD = 0.8
CRITICAL_LOAD_THRESHOLD = 0.9
HIGH_STRESS_THRESHOLD = 0.6
HIGH_LOAD_THRESHOLD = 0.7
MEDIUM_STRESS_THRESHOLD = 0.4


# ---------------------------------------------------------------------------
# Enums and data classes
# ---------------------------------------------------------------------------

class AdvocateMode(Enum):
    """Operating modes for Advocates."""
    PROACTIVE = "proactive"
    REACTIVE = "reactive"
    CRISIS = "crisis"
    RECOVERY = "recovery"
    INDEPENDENCE_BUILDING = "independence_building"


class EmpathyLevel(Enum):
    """Levels of empathetic understanding, determined by fusion depth."""
    THEORETICAL = "theoretical"
    OBSERVATIONAL = "observational"
    EXPERIENTIAL = "experiential"
    DEEP_EXPERIENTIAL = "deep_experiential"


@dataclass
class AdvocateCapabilities:
    """Capabilities of a fused Advocate."""
    empathy_level: EmpathyLevel
    expertise_areas: List[str]
    coaching_strategies: List[str]
    crisis_intervention: bool
    independence_building: bool
    burnout_prevention: bool
    real_world_applicability: float  # 0.0 to 1.0
    clinical_validation: float  # 0.0 to 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "empathy_level": self.empathy_level.value,
            "expertise_areas": self.expertise_areas,
            "coaching_strategies": self.coaching_strategies,
            "crisis_intervention": self.crisis_intervention,
            "independence_building": self.independence_building,
            "burnout_prevention": self.burnout_prevention,
            "real_world_applicability": self.real_world_applicability,
            "clinical_validation": self.clinical_validation,
        }


@dataclass
class FusionResult:
    """Result of Avatar-Aide fusion process."""
    fusion_id: str
    avatar_id: str
    aide_id: str
    advocate_id: str
    fusion_timestamp: datetime
    fusion_quality_score: float  # 0.0 to 1.0
    capabilities: AdvocateCapabilities
    validation_results: Dict[str, Any]
    fusion_notes: List[str]

    # Carried forward from fusion for the Advocate to reference
    avatar_experience_summary: Dict[str, Any] = field(default_factory=dict)
    aide_expertise_summary: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fusion_id": self.fusion_id,
            "avatar_id": self.avatar_id,
            "aide_id": self.aide_id,
            "advocate_id": self.advocate_id,
            "fusion_timestamp": self.fusion_timestamp.isoformat(),
            "fusion_quality_score": self.fusion_quality_score,
            "capabilities": self.capabilities.to_dict(),
            "validation_results": self.validation_results,
            "fusion_notes": self.fusion_notes,
        }


@dataclass
class SupportResponse:
    """Structured response from an Advocate to a user."""
    mode: AdvocateMode
    empathic_understanding: Dict[str, Any]
    expert_guidance: Dict[str, Any]
    actionable_steps: List[str]
    encouragement: str
    follow_up: Optional[str] = None
    success: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mode": self.mode.value,
            "empathic_understanding": self.empathic_understanding,
            "expert_guidance": self.expert_guidance,
            "actionable_steps": self.actionable_steps,
            "encouragement": self.encouragement,
            "follow_up": self.follow_up,
            "success": self.success,
        }


# ---------------------------------------------------------------------------
# BaseAdvocate
# ---------------------------------------------------------------------------

class BaseAdvocate(ABC):
    """
    Base class for all fused Advocates.

    An Advocate has *both* lived experience (from the Avatar) and
    proven expertise (from the Aide).  It is the entity that
    eventually faces real users.
    """

    def __init__(
        self,
        advocate_id: str,
        fusion_result: FusionResult,
        avatar_experience: Optional[ExperienceMemory] = None,
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self.advocate_id = advocate_id
        self.fusion_result = fusion_result
        self.capabilities = fusion_result.capabilities

        # Carried-forward knowledge stores
        self.avatar_experience = avatar_experience  # may be None until wired
        self.aide_expertise: Dict[str, Any] = fusion_result.aide_expertise_summary

        # Operating state
        self.current_mode = AdvocateMode.PROACTIVE
        self.empathy_level = fusion_result.capabilities.empathy_level
        self.expertise_areas = fusion_result.capabilities.expertise_areas

        # Performance tracking
        self.interactions_count: int = 0
        self.successful_interactions: int = 0
        self.crisis_interventions: int = 0
        self.independence_achievements: int = 0

        # Event bus
        self.event_bus = event_bus or EventBus()

        # Timestamps
        self.created_at = fusion_result.fusion_timestamp
        self.last_interaction = datetime.now()

    # ------------------------------------------------------------------
    # Abstract interface — each Advocate specialisation implements these
    # ------------------------------------------------------------------

    @abstractmethod
    def provide_empathic_support(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide empathic support drawn from the Avatar's lived experience.

        The implementation should reference the Avatar's experience memory
        to find relatable struggles and communicate genuine understanding.
        """

    @abstractmethod
    def provide_expert_guidance(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide expert guidance drawn from the Aide's proven strategies.

        The implementation should reference the Aide's effectiveness data
        to recommend strategies with evidence of success.
        """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def assess_user_situation(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Holistic assessment combining experience-based pattern recognition
        with expert severity evaluation.
        """
        struggles = self._identify_struggles_from_experience(user_context)
        severity = self._assess_severity_with_expertise(user_context)
        recommended_mode = self._determine_mode(user_context, severity)

        return {
            "struggle_identification": struggles,
            "severity_assessment": severity,
            "recommended_mode": recommended_mode,
            "intervention_priority": self._assess_priority(severity),
        }

    def provide_comprehensive_support(
        self, user_context: Dict[str, Any]
    ) -> SupportResponse:
        """
        Full support response combining empathy and expertise.

        This is the primary user-facing method.
        """
        self.interactions_count += 1
        self.last_interaction = datetime.now()

        assessment = self.assess_user_situation(user_context)
        mode = assessment["recommended_mode"]
        self.current_mode = mode

        empathic = self.provide_empathic_support(user_context)
        expert = self.provide_expert_guidance(user_context)

        # Build actionable steps from expert guidance
        steps = expert.get("recommended_steps", [])
        if not steps:
            steps = expert.get("techniques", [])

        encouragement = self._build_encouragement(user_context, mode)

        response = SupportResponse(
            mode=mode,
            empathic_understanding=empathic,
            expert_guidance=expert,
            actionable_steps=steps[:5],  # cap at 5
            encouragement=encouragement,
            follow_up=self._suggest_follow_up(mode),
        )

        if response.success:
            self.successful_interactions += 1

        if mode == AdvocateMode.CRISIS:
            self.crisis_interventions += 1
        elif mode == AdvocateMode.INDEPENDENCE_BUILDING:
            self.independence_achievements += 1

        return response

    def activate_rrt_mode(self, user_context: Dict[str, Any]) -> SupportResponse:
        """Activate Rapid Response Team mode for crisis situations."""
        if not self.capabilities.crisis_intervention:
            return SupportResponse(
                mode=AdvocateMode.CRISIS,
                empathic_understanding={"error": "No crisis capability"},
                expert_guidance={},
                actionable_steps=[],
                encouragement="",
                success=False,
            )

        self.current_mode = AdvocateMode.CRISIS
        self.crisis_interventions += 1

        empathic = self._provide_crisis_empathy(user_context)
        expert = self._provide_crisis_expertise(user_context)

        return SupportResponse(
            mode=AdvocateMode.CRISIS,
            empathic_understanding=empathic,
            expert_guidance=expert,
            actionable_steps=[
                "Assess immediate safety and stability",
                "Apply stress reduction techniques",
                "Simplify or remove current task pressure",
                "Establish a short recovery plan",
            ],
            encouragement=(
                "I understand how overwhelming this feels — I've been through "
                "similar moments. Let's take this one small step at a time."
            ),
            follow_up="Check in within the next hour",
        )

    def get_advocate_metrics(self) -> Dict[str, Any]:
        total = max(self.interactions_count, 1)
        return {
            "advocate_id": self.advocate_id,
            "fusion_quality_score": self.fusion_result.fusion_quality_score,
            "empathy_level": self.empathy_level.value,
            "expertise_areas": self.expertise_areas,
            "current_mode": self.current_mode.value,
            "total_interactions": self.interactions_count,
            "successful_interactions": self.successful_interactions,
            "success_rate": self.successful_interactions / total,
            "crisis_interventions": self.crisis_interventions,
            "independence_achievements": self.independence_achievements,
            "capabilities": self.capabilities.to_dict(),
            "last_interaction": self.last_interaction.isoformat(),
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _identify_struggles_from_experience(
        self, user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Use Avatar memory to recognise familiar struggle patterns."""
        if self.avatar_experience is None:
            return {"identified_struggles": [], "source": "no_experience_data"}

        described_struggles = user_context.get("struggles", [])
        matches: List[str] = []
        for struggle in described_struggles:
            past = self.avatar_experience.recall_struggles(struggle, limit=5)
            if past:
                matches.append(struggle)

        recurring = self.avatar_experience.get_recurring_struggles()
        return {
            "identified_struggles": matches,
            "recurring_patterns_known": list(recurring.keys()),
            "empathy_connections": len(matches),
            "source": "experiential_memory",
        }

    def _assess_severity_with_expertise(
        self, user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Use Aide expertise to gauge severity."""
        stress = user_context.get("stress_level", 0.5)
        cognitive_load = user_context.get("cognitive_load", 0.5)

        if stress > CRITICAL_STRESS_THRESHOLD or cognitive_load > CRITICAL_LOAD_THRESHOLD:
            level = "critical"
        elif stress > HIGH_STRESS_THRESHOLD or cognitive_load > HIGH_LOAD_THRESHOLD:
            level = "high"
        elif stress > MEDIUM_STRESS_THRESHOLD:
            level = "medium"
        else:
            level = "low"

        return {
            "severity_level": level,
            "stress_indicator": stress,
            "cognitive_load_indicator": cognitive_load,
        }

    def _determine_mode(
        self, user_context: Dict[str, Any], severity: Dict[str, Any]
    ) -> AdvocateMode:
        level = severity.get("severity_level", "medium")
        if level == "critical":
            return AdvocateMode.CRISIS
        if level == "high":
            return AdvocateMode.REACTIVE
        if user_context.get("building_independence", False):
            return AdvocateMode.INDEPENDENCE_BUILDING
        return AdvocateMode.PROACTIVE

    def _assess_priority(self, severity: Dict[str, Any]) -> str:
        level = severity.get("severity_level", "medium")
        return {"critical": "immediate", "high": "high", "medium": "normal", "low": "low"}.get(level, "normal")

    def _build_encouragement(
        self, user_context: Dict[str, Any], mode: AdvocateMode
    ) -> str:
        if mode == AdvocateMode.CRISIS:
            return "You're not alone in this. Let's stabilise things together."
        if mode == AdvocateMode.INDEPENDENCE_BUILDING:
            return "You've been making real progress. Trust the strategies you've built."
        return "Every step forward counts, even the small ones."

    def _suggest_follow_up(self, mode: AdvocateMode) -> Optional[str]:
        if mode == AdvocateMode.CRISIS:
            return "Let's check in again within the hour."
        if mode == AdvocateMode.REACTIVE:
            return "Let's revisit this after your next attempt."
        return None

    def _provide_crisis_empathy(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "understanding": "I know how this feels — the overwhelm is real.",
            "validation": "Your response makes complete sense given what you're facing.",
            "hope": "I've been through similar moments and found a way through.",
        }

    def _provide_crisis_expertise(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "immediate_techniques": [
                "Box breathing (4-4-4-4 pattern)",
                "Grounding: name 5 things you can see",
                "Reduce stimulus — step away if possible",
            ],
            "next_steps": [
                "Simplify your current task list to one item",
                "Set a 15-minute recovery timer",
            ],
        }
