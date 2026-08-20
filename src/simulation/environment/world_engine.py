"""
World Engine

Core simulation engine that manages the virtual world.
Powered by a hybrid Entity-Component System (ECS) to efficiently
handle thousands of objects, spatial queries, and ticking mechanics.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional, Union
import uuid
import json
import importlib
from datetime import datetime, timedelta

from .ecs import Registry, Entity, System, Position, Component, UnknownComponent, AgentController, Interactable
from .world_map import GridManager
from .time_manager import TimeManager, TimeChangeEvent


@dataclass
class WorldEngineConfig:
    """Configuration for the WorldEngine."""
    grid_width: int = 100
    grid_height: int = 100
    seconds_per_tick: float = 1.0
    time_speed_multiplier: float = 1.0


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
    TIME_CHANGED = "time_changed"
    RELATIONSHIP_ADDED = "relationship_added"
    RELATIONSHIP_UPDATED = "relationship_updated"
    SOCIAL_INTERACTION = "social_interaction"


class WorldEngine:
    """
    The main driver for the ECS and spatial grid.
    Advances time, runs systems, and emits global events.
    """

    def __init__(
        self,
        config: Optional[Union[Dict[str, Any], WorldEngineConfig]] = None,
        time_manager: Optional[TimeManager] = None,
    ):
        if isinstance(config, WorldEngineConfig):
            self.config = config
        else:
            config = config or {}
            self.config = WorldEngineConfig(
                grid_width=config.get("grid_width", 100),
                grid_height=config.get("grid_height", 100),
                seconds_per_tick=config.get("seconds_per_tick", 1.0),
                time_speed_multiplier=config.get("time_speed_multiplier", 1.0),
            )

        self.simulation_id = str(uuid.uuid4())

        # State
        self.current_state = SimulationState.INITIALIZING

        # Time
        self.time_manager = time_manager or TimeManager(
            start_day=1,
            start_hour=6,
            start_minute=0,
            speed_multiplier=self.config.time_speed_multiplier,
        )
        self.tick_count = 0
        self.time_per_tick = timedelta(seconds=self.config.seconds_per_tick)

        # Architecture
        self.registry = Registry()

        # Grid
        self.grid = GridManager(
            width=self.config.grid_width,
            height=self.config.grid_height,
            registry=self.registry,
        )

        # Event Bus
        self.event_listeners: Dict[EventType, List[Any]] = {e: [] for e in EventType}

        # Forward time events from TimeManager to engine event bus
        self.time_manager.add_listener(self._on_time_changed)

        # Relationship system (social dynamics between Sims).
        # Imported lazily to avoid a circular import with the relationships module.
        from .relationships import RelationshipManager
        self.relationship_manager = RelationshipManager(
            registry=self.registry,
            on_event=self.emit_event,
        )

        self.initialize()

    def _on_time_changed(self, event: TimeChangeEvent) -> None:
        """Forward time change events from TimeManager to the engine event bus."""
        self.emit_event(EventType.TIME_CHANGED, {
            "day": event.day,
            "hour": event.hour,
            "minute": event.minute,
            "is_daytime": event.is_daytime,
            "total_minutes_elapsed": event.total_minutes_elapsed,
        })

    def initialize(self) -> None:
        """Set up initial systems and state."""
        self.current_state = SimulationState.RUNNING
        self._register_core_systems()

    def _register_core_systems(self) -> None:
        """Register the core ECS systems onto the current registry."""
        # Imported lazily to avoid a circular import with the relationships module.
        from .relationships import RelationshipSystem
        self.registry.register_system(
            RelationshipSystem(self.relationship_manager, self.time_manager)
        )

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
            self.time_manager.advance_by_tick(self.config.seconds_per_tick)
            self.tick_count += 1

            # 3. Emit global tick event
            self.emit_event(EventType.TICK, {
                "tick_count": self.tick_count,
                "day": self.time_manager.day,
                "hour": self.time_manager.hour,
                "minute": self.time_manager.minute,
                "is_daytime": self.time_manager.is_daytime,
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

    def save_state(self) -> str:
        """
        Serialize the full world state to JSON.
        
        Returns a JSON string containing entities, components, time manager state,
        and engine configuration.
        """
        entities_data = []
        for entity in self.registry.get_entities():
            entity_data = {
                "entity_id": entity.entity_id,
                "components": {},
            }
            for comp_type in self.registry.get_component_types():
                comp = self.registry.get_component(entity, comp_type)
                if comp is not None:
                    entity_data["components"][comp_type.__name__] = self._serialize_component(comp)
            entities_data.append(entity_data)

        state = {
            "simulation_id": self.simulation_id,
            "tick_count": self.tick_count,
            "current_state": self.current_state.value,
            "config": {
                "grid_width": self.config.grid_width,
                "grid_height": self.config.grid_height,
                "seconds_per_tick": self.config.seconds_per_tick,
                "time_speed_multiplier": self.config.time_speed_multiplier,
            },
            "time_manager": self.time_manager.to_dict(),
            "entities": entities_data,
        }
        return json.dumps(state, indent=2)

    def load_state(self, json_data: str) -> None:
        """
        Deserialize the world state from JSON and restore the engine.
        
        Args:
            json_data: JSON string previously produced by save_state().
        
        Raises:
            ValueError: If the JSON data is malformed or missing required keys.
        """
        try:
            state = json.loads(json_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Malformed JSON: {e}") from e

        try:
            self.simulation_id = state.get("simulation_id", str(uuid.uuid4()))
            self.tick_count = state.get("tick_count", 0)
            current_state_value = state.get("current_state", SimulationState.RUNNING.value)
            self.current_state = SimulationState(current_state_value)

            config_data = state.get("config", {})
            self.config = WorldEngineConfig(
                grid_width=config_data.get("grid_width", 100),
                grid_height=config_data.get("grid_height", 100),
                seconds_per_tick=config_data.get("seconds_per_tick", 1.0),
                time_speed_multiplier=config_data.get("time_speed_multiplier", 1.0),
            )
            self.time_per_tick = timedelta(seconds=self.config.seconds_per_tick)

            # Restore time manager state
            time_manager_data = state.get("time_manager", {})
            self.time_manager = TimeManager.from_dict(time_manager_data)

            # Re-bind time manager listener
            self.time_manager.add_listener(self._on_time_changed)

            # Restore entities and components
            self.registry = Registry()
            entities_data = state.get("entities", [])
            for entity_data in entities_data:
                entity = Entity(entity_id=entity_data["entity_id"])
                self.registry.add_entity(entity)
                components = entity_data.get("components", {})
                for comp_name, comp_data in components.items():
                    component = self._deserialize_component(comp_name, comp_data)
                    if component is not None:
                        self.registry.add_component(entity, component)

            # Rebuild grid
            self.grid = GridManager(
                width=self.config.grid_width,
                height=self.config.grid_height,
                registry=self.registry,
            )

            # Rebind the relationship manager to the rebuilt registry and
            # re-register core systems (the registry was recreated above).
            self.relationship_manager.registry = self.registry
            self.relationship_manager._index = {}
            self._register_core_systems()
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f"Invalid world state data: {e}") from e

    def _serialize_component(self, component: Component) -> Dict[str, Any]:
        """Serialize a component to a plain dictionary."""
        if hasattr(component, "to_dict"):
            return component.to_dict()
        data = {}
        for attr in vars(component):
            if not attr.startswith("_"):
                val = getattr(component, attr)
                if hasattr(val, "to_dict"):
                    data[attr] = val.to_dict()
                elif isinstance(val, dict):
                    data[attr] = {
                        k: (v.to_dict() if hasattr(v, "to_dict") else v)
                        for k, v in val.items()
                    }
                else:
                    data[attr] = val
        return data

    def _deserialize_component(self, comp_name: str, data: Dict[str, Any]) -> Optional[Component]:
        """Deserialize a component from a plain dictionary."""
        if comp_name == "Position":
            return Position(
                x=data.get("x", 0),
                y=data.get("y", 0),
                z=data.get("z", 0),
            )
        elif comp_name == "Interactable":
            return Interactable(affordances=data.get("affordances", []))
        elif comp_name == "AgentController":
            ctrl = AgentController(agent_id=data.get("agent_id", ""))
            ctrl.current_intent = data.get("current_intent")
            ctrl.intent_progress = data.get("intent_progress", 0.0)
            return ctrl

        component = self._try_import_component(comp_name, data)
        if component is not None:
            return component

        return UnknownComponent(component_type=comp_name, data=data)

    def _try_import_component(self, comp_name: str, data: Dict[str, Any]) -> Optional[Component]:
        """Attempt to dynamically import and instantiate a component by class name."""
        modules_to_try = [
            "src.simulation.environment.ecs",
            "src.simulation.environment.needs",
            "src.simulation.environment.rooms",
            "src.simulation.environment.relationships",
        ]
        for module_name in modules_to_try:
            try:
                module = importlib.import_module(module_name)
                comp_cls = getattr(module, comp_name, None)
                if comp_cls is not None and isinstance(comp_cls, type) and issubclass(comp_cls, Component):
                    try:
                        return comp_cls(**data)
                    except TypeError:
                        return UnknownComponent(component_type=comp_name, data=data)
            except ImportError:
                continue
        return None
