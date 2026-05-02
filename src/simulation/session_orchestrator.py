"""
Session Orchestrator

Coordinates a complete training session: pairs an Avatar with an Aide,
runs them through a sequence of Scenarios, manages the observe-coach-retry
loop, tracks progress, and determines when the pair is ready for fusion.

This is the "game loop" of the experiential learning system.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

from ..core.events import EventBus, Signal, SignalType
from ..avatars.base_avatar import BaseAvatar, TaskResult
from ..aides.base_aide import BaseAide
from ..fusion.readiness_assessor import ReadinessAssessor, FusionReadiness


class SessionPhase(Enum):
    """Phases of a training session."""
    SETUP = auto()
    TRAINING = auto()
    COOLDOWN = auto()
    ASSESSMENT = auto()
    COMPLETED = auto()


@dataclass
class SessionConfig:
    """Configuration for a training session."""
    max_attempts_per_scenario: int = 10
    max_coaching_per_attempt: int = 3
    min_attempts_for_success_check: int = 3
    independence_target: float = 0.8
    success_rate_target: float = 0.7
    burnout_abort_threshold: float = 0.85
    check_fusion_readiness: bool = True


@dataclass
class ScenarioResult:
    """Aggregated result for one scenario within a session."""
    scenario_name: str
    total_attempts: int = 0
    successes: int = 0
    coaching_interventions: int = 0
    independence_level: float = 0.0
    burnout_risk_peak: float = 0.0
    aborted: bool = False
    abort_reason: Optional[str] = None


@dataclass
class SessionResult:
    """Complete result of a training session."""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    avatar_id: str = ""
    aide_id: str = ""
    phase: SessionPhase = SessionPhase.COMPLETED
    scenario_results: List[ScenarioResult] = field(default_factory=list)
    total_attempts: int = 0
    total_successes: int = 0
    total_coaching: int = 0
    final_independence: float = 0.0
    fusion_readiness: Optional[FusionReadiness] = None
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    @property
    def success_rate(self) -> float:
        return self.total_successes / max(self.total_attempts, 1)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "avatar_id": self.avatar_id,
            "aide_id": self.aide_id,
            "phase": self.phase.name,
            "total_attempts": self.total_attempts,
            "total_successes": self.total_successes,
            "total_coaching": self.total_coaching,
            "success_rate": round(self.success_rate, 3),
            "final_independence": round(self.final_independence, 3),
            "fusion_ready": (
                self.fusion_readiness.ready if self.fusion_readiness else False
            ),
            "scenarios": [
                {
                    "name": sr.scenario_name,
                    "attempts": sr.total_attempts,
                    "successes": sr.successes,
                    "coaching": sr.coaching_interventions,
                    "independence": round(sr.independence_level, 3),
                    "aborted": sr.aborted,
                }
                for sr in self.scenario_results
            ],
            "started_at": self.started_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
        }


class SessionOrchestrator:
    """
    Runs the training loop for one Avatar-Aide pair.

    Usage:
        orchestrator = SessionOrchestrator(avatar, aide, config)
        result = orchestrator.run_session(scenarios)
    """

    def __init__(
        self,
        avatar: BaseAvatar,
        aide: BaseAide,
        config: Optional[SessionConfig] = None,
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self.avatar = avatar
        self.aide = aide
        self.config = config or SessionConfig()

        # Share or create event bus
        self.event_bus = event_bus or avatar.event_bus
        if aide.event_bus is not self.event_bus:
            aide.event_bus = self.event_bus

        # Bind Aide to Avatar
        self.channel = aide.bind_to_avatar(avatar)

        self._readiness_assessor = ReadinessAssessor()
        self._session_result = SessionResult(
            avatar_id=avatar.avatar_id,
            aide_id=aide.aide_id,
        )

    def run_session(
        self,
        scenarios: List[Dict[str, Any]],
    ) -> SessionResult:
        """
        Run a complete training session through a list of scenarios.

        Each scenario is a dict with at least:
            name, task_type, base_success_rate, cognitive_demand
        """
        self._session_result.phase = SessionPhase.TRAINING
        self._emit(SignalType.SESSION_STARTED, {
            "avatar_id": self.avatar.avatar_id,
            "aide_id": self.aide.aide_id,
            "scenario_count": len(scenarios),
        })

        for scenario in scenarios:
            scenario_result = self._run_scenario(scenario)
            self._session_result.scenario_results.append(scenario_result)
            self._session_result.total_attempts += scenario_result.total_attempts
            self._session_result.total_successes += scenario_result.successes
            self._session_result.total_coaching += scenario_result.coaching_interventions

            # Return Avatar to idle between scenarios
            self.avatar.return_to_idle()

        # Cooldown & assessment
        self._session_result.phase = SessionPhase.ASSESSMENT
        self._session_result.final_independence = self.avatar.get_independence_level()

        if self.config.check_fusion_readiness:
            self._session_result.fusion_readiness = self._readiness_assessor.assess(
                self.avatar, self.aide
            )

        self._session_result.phase = SessionPhase.COMPLETED
        self._session_result.completed_at = datetime.now()

        self._emit(SignalType.SESSION_COMPLETED, self._session_result.to_dict())
        return self._session_result

    def run_single_attempt(
        self, task_context: Dict[str, Any]
    ) -> TaskResult:
        """
        Run one attempt-observe-coach cycle.

        Useful for step-by-step control from external callers.
        """
        # Avatar attempts
        result = self.avatar.attempt_task(task_context)

        # Aide observes and optionally coaches
        if not result.success:
            coaching = self.aide.observe_and_coach(task_context)
            if coaching:
                self.aide.track_intervention_effectiveness(coaching, result)

        return result

    # ------------------------------------------------------------------
    # Private scenario runner
    # ------------------------------------------------------------------

    def _run_scenario(self, scenario: Dict[str, Any]) -> ScenarioResult:
        """Run one scenario with the attempt-coach-retry loop."""
        name = scenario.get("name", "unnamed")
        sr = ScenarioResult(scenario_name=name)

        while sr.total_attempts < self.config.max_attempts_per_scenario:
            # Check burnout abort
            burnout = self.avatar.assess_burnout_risk()
            sr.burnout_risk_peak = max(sr.burnout_risk_peak, burnout["risk_score"])
            if burnout["risk_score"] >= self.config.burnout_abort_threshold:
                sr.aborted = True
                sr.abort_reason = "burnout_risk_exceeded"
                break

            # Attempt
            result = self.avatar.attempt_task(scenario)
            sr.total_attempts += 1
            scenario_complete = False

            if result.success:
                sr.successes += 1

                # Check if we've hit target success rate
                scenario_complete = self._meets_success_target(sr)
            else:
                # Aide coaching loop
                coaching_count = 0
                while (
                    coaching_count < self.config.max_coaching_per_attempt
                    and sr.total_attempts < self.config.max_attempts_per_scenario
                ):
                    coaching = self.aide.observe_and_coach(scenario)
                    if coaching is None:
                        break
                    sr.coaching_interventions += 1
                    coaching_count += 1

                    # Retry after coaching
                    retry = self.avatar.attempt_task(scenario)
                    sr.total_attempts += 1
                    # Always track outcomes (including failed retries) so strategy
                    # effectiveness reflects both wins and losses.
                    self.aide.track_intervention_effectiveness(coaching, retry)
                    if retry.success:
                        sr.successes += 1
                        scenario_complete = self._meets_success_target(sr)
                        break

            # Return to idle between attempts
            self.avatar.return_to_idle()
            if scenario_complete:
                break

        sr.independence_level = self.avatar.get_independence_level(
            scenario.get("task_type", "unknown")
        )
        return sr

    def _meets_success_target(self, scenario_result: ScenarioResult) -> bool:
        """Check if scenario has met success criteria."""
        current_rate = scenario_result.successes / max(scenario_result.total_attempts, 1)
        return (
            current_rate >= self.config.success_rate_target
            and scenario_result.total_attempts >= self.config.min_attempts_for_success_check
        )

    # ------------------------------------------------------------------
    # Event emission
    # ------------------------------------------------------------------

    def _emit(self, signal_type: SignalType, data: Dict[str, Any]) -> None:
        self.event_bus.emit(Signal(
            signal_type=signal_type,
            source_id="session_orchestrator",
            source_type="engine",
            data=data,
        ))
