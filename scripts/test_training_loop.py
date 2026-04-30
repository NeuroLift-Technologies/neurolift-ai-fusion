#!/usr/bin/env python3
"""
Test Training Loop - Demonstrates complete Avatar-Aide training session

This script:
1. Creates a StayAlert Avatar
2. Creates a StayAlertAide
3. Runs a training session with a workplace scenario
4. Displays results and metrics
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.avatars.adhd_traits.stay_alert_avatar import StayAlertAvatar
from src.aides.coaching.stay_alert_aide import StayAlertAide
from src.simulation.environment.scenarios import ScenarioLibrary, ScenarioCategory
from src.simulation.training_session import TrainingSession
from src.database.supabase_client import SupabaseClient
import uuid


def initialize_avatar_and_aide():
    """Create and initialize Avatar and Aide instances"""
    print("\n" + "="*60)
    print("INITIALIZING AVATAR AND AIDE")
    print("="*60 + "\n")

    avatar_id = f"avatar_stay_alert_{uuid.uuid4().hex[:8]}"
    aide_id = f"aide_attention_{uuid.uuid4().hex[:8]}"

    avatar_config = {
        "trait_name": "StayAlert",
        "attention_duration": 15,
        "drift_probability": 0.3,
        "hyperfocus_tendency": 0.2,
    }

    aide_config = {
        "expertise_area": "sustained_attention",
    }

    avatar = StayAlertAvatar(avatar_id, avatar_config)
    aide = StayAlertAide(aide_id, aide_config)

    print(f"Avatar Created:")
    print(f"  - ID: {avatar_id}")
    print(f"  - Trait: {avatar.trait_name}")
    print(f"  - State: {avatar.current_state.value}")

    print(f"\nAide Created:")
    print(f"  - ID: {aide_id}")
    print(f"  - Expertise: {aide.expertise_area}")

    try:
        db_client = SupabaseClient()
        avatar_record = db_client.create_avatar(avatar_id, avatar.trait_name, avatar_config)
        aide_record = db_client.create_aide(aide_id, aide.expertise_area, aide_config)

        if avatar_record and aide_record:
            print("\n✓ Successfully saved to Supabase")
        else:
            print("\n⚠ Partial database save")
    except Exception as e:
        print(f"\n⚠ Could not save to Supabase: {e}")
        print("  (Continuing with local session...)")

    return avatar, aide


def select_scenario():
    """Select a scenario for training"""
    print("\n" + "="*60)
    print("SELECTING SCENARIO")
    print("="*60 + "\n")

    scenarios = ScenarioLibrary.get_scenarios_by_category(ScenarioCategory.WORKPLACE)

    print("Available Scenarios:")
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario.name}")
        print(f"   Description: {scenario.description}")
        print(f"   Duration: {scenario.expected_duration.total_seconds() / 60:.0f} minutes")
        print(f"   Complexity: {scenario.complexity}")
        print(f"   Aversiveness: {scenario.aversiveness:.1f}")
        print(f"   Requires Sustained Focus: {scenario.requires_sustained_focus}")

    choice = scenarios[0]
    print(f"\nSelected: {choice.name}")
    return choice


def run_training_session(avatar, aide, scenario):
    """Execute the training session"""
    print("\n" + "="*60)
    print("RUNNING TRAINING SESSION")
    print("="*60)

    session = TrainingSession(avatar, aide, scenario)
    results = session.run()

    return results


def display_results(results):
    """Display comprehensive session results"""
    print("\n" + "="*60)
    print("SESSION RESULTS")
    print("="*60 + "\n")

    print(f"Avatar: {results['avatar']}")
    print(f"Scenario: {results['scenario']}")
    print(f"Status: {'✓ SUCCESS' if results['successful'] else '✗ FAILED'}")
    print(f"\nAttempts: {results['successful_attempts']}/{results['attempts']}")
    print(f"Average Quality Score: {results['average_quality_score']:.2f}")
    print(f"Coaching Interventions: {results['coaching_interventions']}")
    print(f"Duration: {results['duration_seconds']} seconds")

    print(f"\n--- Avatar Final State ---")
    avatar_state = results['avatar_final_state']
    print(f"Current State: {avatar_state['current_state']}")
    print(f"Emotional State: {avatar_state['emotional_state']}")
    print(f"Cognitive Load: {avatar_state['cognitive_load']:.2f}")
    print(f"Stress Level: {avatar_state['stress_level']:.2f}")
    print(f"Overall Independence: {avatar_state['overall_independence']:.2f}")
    print(f"Success Rate: {avatar_state['success_rate']:.2f}")
    print(f"Total Tasks Completed: {avatar_state['total_tasks_completed']}")

    print(f"\n--- Aide Metrics ---")
    aide_metrics = results['aide_metrics']
    print(f"Total Interventions: {aide_metrics['total_interventions']}")
    print(f"Successful Interventions: {aide_metrics['successful_interventions']}")
    print(f"Success Rate: {aide_metrics['success_rate']:.2f}")
    print(f"Crisis Interventions: {aide_metrics['crisis_interventions']}")


def main():
    """Main test execution"""
    print("\n" + "="*80)
    print("NEUROLIT TECHNOLOGIES - TRAINING LOOP TEST")
    print("="*80)

    try:
        avatar, aide = initialize_avatar_and_aide()
        scenario = select_scenario()
        results = run_training_session(avatar, aide, scenario)
        display_results(results)

        print("\n" + "="*80)
        print("TEST COMPLETED SUCCESSFULLY")
        print("="*80 + "\n")

        return 0

    except Exception as e:
        print(f"\n✗ Error during test execution: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
