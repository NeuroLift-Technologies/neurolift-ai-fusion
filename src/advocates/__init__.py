"""
Advocate System

Represents the fusion of trained Avatar experience with Aide expertise.
Advocates combine lived understanding of ADHD struggles with proven
coaching strategies.
"""

from .base_advocate import (
    BaseAdvocate,
    AdvocateCapabilities,
    AdvocateMode,
    EmpathyLevel,
    FusionResult,
    SupportResponse,
)
# Fusion engine module not yet implemented
# from .fusion_engine import FusionEngine, FusionReadiness, FusionCriteria

__all__ = [
    "BaseAdvocate",
    "AdvocateCapabilities",
    "AdvocateMode",
    "EmpathyLevel",
    "FusionResult",
    "SupportResponse",
    # Additional exports will be added as modules are implemented
]
