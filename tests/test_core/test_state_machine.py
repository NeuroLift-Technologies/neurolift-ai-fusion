"""Tests for the StateMachine."""

import pytest
from enum import Enum
from src.core.state_machine import StateMachine, InvalidTransitionError


class Light(Enum):
    OFF = "off"
    ON = "on"
    DIMMED = "dimmed"


class TestStateMachine:
    def test_initial_state(self):
        sm = StateMachine(Light, Light.OFF)
        assert sm.current_state == Light.OFF

    def test_valid_transition(self):
        sm = StateMachine(Light, Light.OFF)
        sm.add_transition(Light.OFF, Light.ON)
        t = sm.transition_to(Light.ON, trigger="switch")
        assert sm.current_state == Light.ON
        assert t.from_state == Light.OFF
        assert t.to_state == Light.ON

    def test_invalid_transition_raises(self):
        sm = StateMachine(Light, Light.OFF)
        sm.add_transition(Light.OFF, Light.ON)
        with pytest.raises(InvalidTransitionError):
            sm.transition_to(Light.DIMMED)

    def test_add_transitions_bulk(self):
        sm = StateMachine(Light, Light.OFF)
        sm.add_transitions(Light.OFF, [Light.ON, Light.DIMMED])
        assert sm.can_transition_to(Light.ON)
        assert sm.can_transition_to(Light.DIMMED)

    def test_guard_blocks_transition(self):
        sm = StateMachine(Light, Light.OFF)
        sm.add_transition(Light.OFF, Light.ON)
        sm.add_guard(Light.OFF, Light.ON, lambda f, t, m: False)

        with pytest.raises(InvalidTransitionError):
            sm.transition_to(Light.ON)

    def test_guard_allows_transition(self):
        sm = StateMachine(Light, Light.OFF)
        sm.add_transition(Light.OFF, Light.ON)
        sm.add_guard(Light.OFF, Light.ON, lambda f, t, m: True)
        sm.transition_to(Light.ON)
        assert sm.current_state == Light.ON

    def test_on_enter_callback(self):
        sm = StateMachine(Light, Light.OFF)
        sm.add_transition(Light.OFF, Light.ON)
        entered = []
        sm.on_enter(Light.ON, lambda f, t, m: entered.append((f, t)))
        sm.transition_to(Light.ON)
        assert entered == [(Light.OFF, Light.ON)]

    def test_on_exit_callback(self):
        sm = StateMachine(Light, Light.OFF)
        sm.add_transition(Light.OFF, Light.ON)
        exited = []
        sm.on_exit(Light.OFF, lambda f, t, m: exited.append((f, t)))
        sm.transition_to(Light.ON)
        assert exited == [(Light.OFF, Light.ON)]

    def test_history(self):
        sm = StateMachine(Light, Light.OFF)
        sm.add_transition(Light.OFF, Light.ON)
        sm.add_transition(Light.ON, Light.DIMMED)
        sm.transition_to(Light.ON)
        sm.transition_to(Light.DIMMED)
        assert len(sm.history) == 2

    def test_get_available_transitions(self):
        sm = StateMachine(Light, Light.OFF)
        sm.add_transitions(Light.OFF, [Light.ON, Light.DIMMED])
        available = sm.get_available_transitions()
        assert available == {Light.ON, Light.DIMMED}

    def test_reset(self):
        sm = StateMachine(Light, Light.OFF)
        sm.add_transition(Light.OFF, Light.ON)
        sm.transition_to(Light.ON)
        sm.reset(Light.OFF)
        assert sm.current_state == Light.OFF
        assert len(sm.history) == 0
