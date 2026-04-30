"""
World Engine

Core simulation engine that manages the virtual world.
Now powered by a hybrid Entity-Component System (ECS) to efficiently
handle thousands of objects, spatial queries, and ticking mechanics.
"""

from enum import Enum
from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime, timedelta

from .ecs import Registry, Entity, System, Position
from .world_map import GridManager


class SimulationState(Enum):
    """Current state of the simulation"""
    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"


class EventType(Enum):
    """Types of events emitted by the simulation engine"""
    TICK = "tick"
    ENTITY_ADDED = "entity_added"
    ENTITY_REMOVED = "entity_removed"
    ENTITY_MOVED = "entity_moved"
    INTERACTION_STARTED = "interaction_started"
    INTERACTION_COMPLETED = "interaction_completed"


class WorldEngine:
    """
    The main driver for the ECS and spatial grid.
    Advances time, runs systems, and emits global events.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.simulation_id = str(uuid.uuid4())
        
        # State
        self.current_state = SimulationState.INITIALIZING
        
        # Time
        self.simulation_time = datetime.now()
        self.tick_count = 0
        self.time_per_tick = timedelta(seconds=self.config.get("seconds_per_tick", 1.0))
        
        # Architecture
        self.registry = Registry()
        
        # We start with a 100x100 grid by default
        grid_width = self.config.get("grid_width", 100)
        grid_height = self.config.get("grid_height", 100)
        self.grid = GridManager(width=grid_width, height=grid_height, registry=self.registry)
        
        # Event Bus
        self.event_listeners: Dict[EventType, List[Any]] = {e: [] for e in EventType}
        
        self.initialize()
        
    def initialize(self) -> None:
        """Set up initial systems and state."""
        self.current_state = SimulationState.RUNNING
        
        # Register Core Systems here. E.g.:
        # self.registry.register_system(MovementSystem())
        # self.registry.register_system(InteractionSystem())
        
    def spawn_entity(self) -> Entity:
        """Create and register a new entity."""
        entity = Entity()
        self.registry.add_entity(entity)
        self.emit_event(EventType.ENTITY_ADDED, {"entity_id": entity.entity_id})
        return entity
        
    def remove_entity(self, entity: Entity) -> None:
        """Remove an entity from the world."""
        self.registry.remove_entity(entity)
        self.emit_event(EventType.ENTITY_REMOVED, {"entity_id": entity.entity_id})

    def run_simulation_step(self) -> bool:
        """
        Run one 'tick' of the simulation.
        Processes all ECS systems, updates time, and fires events.
        """
        if self.current_state != SimulationState.RUNNING:
            return False
            
        try:
            # Time delta for systems is usually seconds
            dt = self.time_per_tick.total_seconds()
            
            # 1. Run ECS Systems
            self.registry.tick(dt)
            
            # 2. Update Time
            self.simulation_time += self.time_per_tick
            self.tick_count += 1
            
            # 3. Emit global tick event
            self.emit_event(EventType.TICK, {
                "tick_count": self.tick_count,
                "simulation_time": self.simulation_time.isoformat()
            })
            
            return True
            
        except Exception as e:
            self.current_state = SimulationState.ERROR
            print(f"Simulation tick failed: {e}")
            return False

    def emit_event(self, event_type: EventType, data: Dict[str, Any]) -> None:
        """Simple pub/sub for engine events."""
        listeners = self.event_listeners.get(event_type, [])
        for listener in listeners:
            try:
                # Expecting a callable listener: listener(event_type, data)
                listener(event_type, data)
            except Exception as e:
                print(f"Error in event listener: {e}")

    def subscribe(self, event_type: EventType, listener: Any) -> None:
        """Subscribe to engine events."""
        if event_type in self.event_listeners:
            self.event_listeners[event_type].append(listener)