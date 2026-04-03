"""Tests for fusion package exports."""


def test_fusion_package_exports():
    from src.fusion import (  # local import verifies package wiring
        FusionEngine,
        ReadinessAssessor,
        DimensionScore,
        FusionDimension,
        FusionReadiness,
    )

    assert FusionEngine is not None
    assert ReadinessAssessor is not None
    assert DimensionScore is not None
    assert FusionDimension is not None
    assert FusionReadiness is not None
