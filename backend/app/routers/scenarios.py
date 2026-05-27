"""
Scenarios Router
Expose the ScenarioLibrary to the frontend and mobile apps.
"""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException

router = APIRouter()

# ---------------------------------------------------------------------------
# Static scenario catalogue (mirrors ScenarioLibrary in src/simulation)
# ---------------------------------------------------------------------------
SCENARIOS: List[Dict[str, Any]] = [
    # Workplace
    {
        "scenario_id": "workplace_email_overload",
        "name": "Email Overload",
        "category": "workplace",
        "task_type": "email_management",
        "complexity": "medium",
        "aversiveness": 0.5,
        "requires_sustained_focus": True,
        "cognitive_demand": 0.6,
        "base_success_rate": 0.6,
        "description": "Process 47 unread emails and action the urgent ones within 30 minutes.",
    },
    {
        "scenario_id": "workplace_meeting_prep",
        "name": "Last-Minute Meeting Preparation",
        "category": "workplace",
        "task_type": "meeting_preparation",
        "complexity": "high",
        "aversiveness": 0.7,
        "requires_sustained_focus": True,
        "cognitive_demand": 0.75,
        "base_success_rate": 0.55,
        "description": "Prepare and present a project status update with 15 minutes' notice.",
    },
    {
        "scenario_id": "workplace_report_writing",
        "name": "Quarterly Report Writing",
        "category": "workplace",
        "task_type": "report_writing",
        "complexity": "high",
        "aversiveness": 0.6,
        "requires_sustained_focus": True,
        "cognitive_demand": 0.8,
        "base_success_rate": 0.5,
        "description": "Write a 2,000-word quarterly performance report under deadline pressure.",
    },
    # Personal
    {
        "scenario_id": "personal_bill_payment",
        "name": "Bill Payment Chaos",
        "category": "personal",
        "task_type": "financial_management",
        "complexity": "medium",
        "aversiveness": 0.8,
        "requires_sustained_focus": False,
        "cognitive_demand": 0.5,
        "base_success_rate": 0.65,
        "description": "Locate and pay three overdue bills before late fees are applied.",
    },
    {
        "scenario_id": "personal_household_tasks",
        "name": "Household Task Spiral",
        "category": "personal",
        "task_type": "household_management",
        "complexity": "medium",
        "aversiveness": 0.5,
        "requires_sustained_focus": False,
        "cognitive_demand": 0.4,
        "base_success_rate": 0.7,
        "description": "Complete a list of five household chores without getting sidetracked.",
    },
    # Social
    {
        "scenario_id": "social_rejection_sensitivity",
        "name": "Perceived Social Rejection",
        "category": "social",
        "task_type": "emotional_regulation",
        "complexity": "high",
        "aversiveness": 0.9,
        "requires_sustained_focus": False,
        "cognitive_demand": 0.7,
        "base_success_rate": 0.45,
        "description": "Navigate a social situation where a colleague's short reply triggers rejection-sensitive dysphoria.",
    },
    {
        "scenario_id": "social_group_project",
        "name": "Group Project Coordination",
        "category": "social",
        "task_type": "collaboration",
        "complexity": "high",
        "aversiveness": 0.65,
        "requires_sustained_focus": True,
        "cognitive_demand": 0.7,
        "base_success_rate": 0.55,
        "description": "Coordinate a group project where teammates have conflicting schedules and communication styles.",
    },
]

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/", summary="List all scenarios")
async def list_scenarios(category: Optional[str] = None):
    if category:
        return [s for s in SCENARIOS if s["category"] == category]
    return SCENARIOS


@router.get("/categories", summary="List scenario categories")
async def list_categories():
    cats = sorted(set(s["category"] for s in SCENARIOS))
    return {"categories": cats}


@router.get("/{scenario_id}", summary="Get scenario by ID")
async def get_scenario(scenario_id: str):
    for s in SCENARIOS:
        if s["scenario_id"] == scenario_id:
            return s
    raise HTTPException(status_code=404, detail="Scenario not found")
