"""
Time Manager

Manages a 24-hour in-simulation day with configurable acceleration.
Tracks day number, hour (0-23), minute (0-59), and day/night status.
Emits time change events via callbacks.
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional
from enum import Enum


class TimeSpeed(Enum):
    """Preset speed multipliers for the simulation."""
    REALTIME = 1
    FAST = 5
    ULTRA = 20
    HYPER = 100


@dataclass
class TimeChangeEvent:
    """Event data emitted when time changes."""
    day: int
    hour: int
    minute: int
    is_daytime: bool
    total_minutes_elapsed: int


class TimeManager:
    """
    Manages the simulation time with a 24-hour day cycle.
    
    Default speed: 1 real second = 1 sim minute (24h sim day = 24 real minutes).
    Supports acceleration via speed multiplier.
    """

    DAY_START_HOUR = 6  # 6:00 AM = day starts
    DAY_END_HOUR = 20   # 8:00 PM = night starts
    MINUTES_PER_HOUR = 60
    HOURS_PER_DAY = 24
    MINUTES_PER_DAY = HOURS_PER_DAY * MINUTES_PER_HOUR

    def __init__(
        self,
        start_day: int = 1,
        start_hour: int = 6,
        start_minute: int = 0,
        speed_multiplier: float = 1.0,
    ):
        self._total_minutes = start_day * self.MINUTES_PER_DAY + start_hour * self.MINUTES_PER_HOUR + start_minute
        self._speed_multiplier = speed_multiplier
        self._listeners: List[Callable[[TimeChangeEvent], None]] = []

    @property
    def day(self) -> int:
        return self._total_minutes // self.MINUTES_PER_DAY

    @property
    def hour(self) -> int:
        return (self._total_minutes % self.MINUTES_PER_DAY) // self.MINUTES_PER_HOUR

    @property
    def minute(self) -> int:
        return self._total_minutes % self.MINUTES_PER_HOUR

    @property
    def is_daytime(self) -> bool:
        return self.DAY_START_HOUR <= self.hour < self.DAY_END_HOUR

    @property
    def total_minutes_elapsed(self) -> int:
        return self._total_minutes

    @property
    def speed_multiplier(self) -> float:
        return self._speed_multiplier

    @speed_multiplier.setter
    def speed_multiplier(self, value: float) -> None:
        self._speed_multiplier = max(0.1, value)

    def advance(self, minutes: float) -> None:
        """Advance simulation time by the given number of minutes."""
        old_day = self.day
        old_hour = self.hour
        old_minute = self.minute
        old_is_daytime = self.is_daytime

        self._total_minutes += int(minutes)
        self._total_minutes = max(0, self._total_minutes)

        if (
            self.day != old_day
            or self.hour != old_hour
            or self.minute != old_minute
            or self.is_daytime != old_is_daytime
        ):
            self._emit_event()

    def set_time(self, hour: int, minute: int = 0) -> None:
        """Set the simulation time to a specific hour and minute on the current day."""
        old_day = self.day
        old_hour = self.hour
        old_minute = self.minute
        old_is_daytime = self.is_daytime

        self._total_minutes = self.day * self.MINUTES_PER_DAY + hour * self.MINUTES_PER_HOUR + minute

        if (
            self.hour != old_hour
            or self.minute != old_minute
            or self.is_daytime != old_is_daytime
        ):
            self._emit_event()

    def advance_by_tick(self, seconds_per_tick: float) -> None:
        """
        Advance time by one simulation tick.
        
        Calculates sim minutes elapsed as: seconds_per_tick * speed_multiplier.
        """
        sim_minutes = seconds_per_tick * self._speed_multiplier
        self.advance(sim_minutes)

    def add_listener(self, callback: Callable[[TimeChangeEvent], None]) -> None:
        """Register a callback to be invoked on time change events."""
        self._listeners.append(callback)

    def remove_listener(self, callback: Callable[[TimeChangeEvent], None]) -> None:
        """Unregister a previously registered callback."""
        if callback in self._listeners:
            self._listeners.remove(callback)

    def _emit_event(self) -> None:
        """Notify all registered listeners of the time change."""
        event = TimeChangeEvent(
            day=self.day,
            hour=self.hour,
            minute=self.minute,
            is_daytime=self.is_daytime,
            total_minutes_elapsed=self.total_minutes_elapsed,
        )
        for callback in self._listeners:
            try:
                callback(event)
            except Exception:
                pass

    def to_dict(self) -> Dict:
        """Serialize state to a dictionary."""
        return {
            "total_minutes": self._total_minutes,
            "speed_multiplier": self._speed_multiplier,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "TimeManager":
        """Deserialize state from a dictionary."""
        total_minutes = data.get("total_minutes", 0)
        speed_multiplier = data.get("speed_multiplier", 1.0)
        day = total_minutes // cls.MINUTES_PER_DAY
        hour = (total_minutes % cls.MINUTES_PER_DAY) // cls.MINUTES_PER_HOUR
        minute = total_minutes % cls.MINUTES_PER_HOUR
        return cls(
            start_day=day,
            start_hour=hour,
            start_minute=minute,
            speed_multiplier=speed_multiplier,
        )
