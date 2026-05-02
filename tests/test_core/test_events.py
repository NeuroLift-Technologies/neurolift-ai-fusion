"""Tests for the EventBus and Signal system."""

import pytest
from src.core.events import EventBus, Signal, SignalType


class TestSignal:
    def test_signal_creation(self):
        signal = Signal(
            signal_type=SignalType.AVATAR_TASK_STARTED,
            source_id="avatar_001",
            source_type="avatar",
            data={"task": "focus"},
        )
        assert signal.signal_type == SignalType.AVATAR_TASK_STARTED
        assert signal.source_id == "avatar_001"
        assert signal.signal_id  # auto-generated

    def test_signal_to_dict(self):
        signal = Signal(signal_type=SignalType.AVATAR_STRUGGLING, source_id="a1")
        d = signal.to_dict()
        assert d["signal_type"] == "AVATAR_STRUGGLING"
        assert d["source_id"] == "a1"


class TestEventBus:
    def test_subscribe_and_emit(self):
        bus = EventBus()
        received = []
        bus.subscribe(SignalType.AVATAR_TASK_STARTED, lambda s: received.append(s))

        signal = Signal(signal_type=SignalType.AVATAR_TASK_STARTED, source_id="a1")
        count = bus.emit(signal)

        assert count == 1
        assert len(received) == 1
        assert received[0].source_id == "a1"

    def test_source_filter(self):
        bus = EventBus()
        received = []
        bus.subscribe(
            SignalType.AVATAR_STRUGGLING,
            lambda s: received.append(s),
            source_filter="avatar_A",
        )

        # Signal from matching source
        bus.emit(Signal(signal_type=SignalType.AVATAR_STRUGGLING, source_id="avatar_A"))
        # Signal from different source — should be filtered
        bus.emit(Signal(signal_type=SignalType.AVATAR_STRUGGLING, source_id="avatar_B"))

        assert len(received) == 1
        assert received[0].source_id == "avatar_A"

    def test_unsubscribe(self):
        bus = EventBus()
        received = []
        sub_id = bus.subscribe(
            SignalType.SESSION_STARTED, lambda s: received.append(s)
        )

        bus.emit(Signal(signal_type=SignalType.SESSION_STARTED))
        assert len(received) == 1

        assert bus.unsubscribe(sub_id) is True
        bus.emit(Signal(signal_type=SignalType.SESSION_STARTED))
        assert len(received) == 1  # no new event

    def test_unsubscribe_nonexistent(self):
        bus = EventBus()
        assert bus.unsubscribe("fake_id") is False

    def test_history(self):
        bus = EventBus()
        bus.emit(Signal(signal_type=SignalType.AVATAR_TASK_STARTED, source_id="a1"))
        bus.emit(Signal(signal_type=SignalType.AVATAR_TASK_COMPLETED, source_id="a1"))
        bus.emit(Signal(signal_type=SignalType.AIDE_COACHING_DELIVERED, source_id="aide1"))

        assert len(bus.get_history()) == 3
        assert len(bus.get_history(signal_type=SignalType.AVATAR_TASK_STARTED)) == 1
        assert len(bus.get_history(source_id="aide1")) == 1

    def test_handler_exception_does_not_break_bus(self):
        bus = EventBus()
        good_received = []

        def bad_handler(s):
            raise ValueError("boom")

        bus.subscribe(SignalType.SESSION_STARTED, bad_handler)
        bus.subscribe(SignalType.SESSION_STARTED, lambda s: good_received.append(s))

        count = bus.emit(Signal(signal_type=SignalType.SESSION_STARTED))
        # Both handlers called, one failed gracefully
        assert count == 2
        assert len(good_received) == 1
