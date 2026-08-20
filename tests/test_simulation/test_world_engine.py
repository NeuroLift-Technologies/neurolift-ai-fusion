import pytest
from datetime import timedelta
from src.simulation.environment.ecs import Entity, Position, Interactable, AgentController, System
from src.simulation.environment.world_engine import WorldEngine, SimulationState, WorldEngineConfig
from src.simulation.environment.world_map import GridManager
from src.simulation.environment.agent_interface import AgentInterface
from src.simulation.environment.time_manager import TimeManager, TimeSpeed, TimeChangeEvent

class DummyMovementSystem(System):
    """A simple system to test ECS updates."""
    def update(self, delta_time: float) -> None:
        entities = self.registry.get_entities_with(Position, AgentController)
        for entity in entities:
            pos = self.registry.get_component(entity, Position)
            controller = self.registry.get_component(entity, AgentController)
            
            # Very simple fake movement based on intent
            if controller.current_intent and controller.current_intent["type"] == "move":
                target = controller.current_intent["data"]
                # Move 1 step towards target
                if pos.x < target["x"]: pos.x += 1
                elif pos.x > target["x"]: pos.x -= 1
                elif pos.y < target["y"]: pos.y += 1
                elif pos.y > target["y"]: pos.y -= 1
                
                if pos.x == target["x"] and pos.y == target["y"]:
                    controller.current_intent = None # Finished

def test_ecs_basic_operations():
    engine = WorldEngine()
    entity = engine.spawn_entity()
    
    pos = Position(1, 2, 0)
    engine.registry.add_component(entity, pos)
    
    assert engine.registry.has_component(entity, Position)
    retrieved_pos = engine.registry.get_component(entity, Position)
    assert retrieved_pos.x == 1
    assert retrieved_pos.y == 2
    
    engine.remove_entity(entity)
    assert not engine.registry.has_component(entity, Position)

def test_spatial_grid_queries():
    engine = WorldEngine()
    
    e1 = engine.spawn_entity()
    engine.registry.add_component(e1, Position(5, 5, 0))
    
    e2 = engine.spawn_entity()
    engine.registry.add_component(e2, Position(5, 6, 0))
    
    e3 = engine.spawn_entity()
    engine.registry.add_component(e3, Position(20, 20, 0))
    
    # Radius 2 from (5,5) should catch e1 and e2, but not e3
    nearby = engine.grid.get_entities_in_radius(5, 5, 2)
    assert e1 in nearby
    assert e2 in nearby
    assert e3 not in nearby

def test_pathfinding():
    engine = WorldEngine()
    
    # Put a solid object at (2, 2)
    wall = engine.spawn_entity()
    engine.registry.add_component(wall, Position(2, 2, 0))
    engine.registry.add_component(wall, Interactable(["examine"])) # Interactable acts as solid
    
    assert not engine.grid.is_walkable(2, 2)
    assert engine.grid.is_walkable(2, 3)
    
    # Path from (1, 2) to (3, 2) should go around the wall at (2, 2)
    path = engine.grid.find_path(1, 2, 3, 2)
    
    assert len(path) > 0
    assert (2, 2) not in path # Must not step on the wall

def test_engine_tick_and_agent_interface():
    engine = WorldEngine()
    engine.registry.register_system(DummyMovementSystem())
    
    agent = AgentInterface(engine, "agent_1")
    # Agent starts at (0,0) by default
    
    agent.submit_intent("move", data={"x": 3, "y": 0})
    
    assert agent.check_intent_status() is not None
    
    # Tick 1: moves to (1, 0)
    engine.run_simulation_step()
    pos = engine.registry.get_component(agent.entity, Position)
    assert pos.x == 1
    assert pos.y == 0
    
    # Tick 2: moves to (2, 0)
    engine.run_simulation_step()
    
    # Tick 3: moves to (3, 0)
    engine.run_simulation_step()
    pos = engine.registry.get_component(agent.entity, Position)
    assert pos.x == 3
    assert pos.y == 0
    
    # Intent should be cleared by DummyMovementSystem
    assert agent.check_intent_status() is None


class TestTimeManager:
    def test_initial_state(self):
        tm = TimeManager()
        assert tm.day == 1
        assert tm.hour == 6
        assert tm.minute == 0
        assert tm.is_daytime is True

    def test_advance_minutes(self):
        tm = TimeManager(start_day=1, start_hour=6, start_minute=0)
        tm.advance(120)
        assert tm.hour == 8
        assert tm.minute == 0
        assert tm.is_daytime is True

    def test_advance_crosses_hour(self):
        tm = TimeManager(start_day=1, start_hour=6, start_minute=30)
        tm.advance(45)
        assert tm.hour == 7
        assert tm.minute == 15

    def test_advance_crosses_day(self):
        tm = TimeManager(start_day=1, start_hour=23, start_minute=30)
        tm.advance(90)
        assert tm.day == 2
        assert tm.hour == 1
        assert tm.minute == 0
        assert tm.is_daytime is False

    def test_set_time(self):
        tm = TimeManager(start_day=1, start_hour=6, start_minute=0)
        tm.set_time(23, 30)
        assert tm.hour == 23
        assert tm.minute == 30
        assert tm.is_daytime is False

    def test_is_daytime(self):
        tm_day = TimeManager(start_day=1, start_hour=10, start_minute=0)
        assert tm_day.is_daytime is True
        tm_night = TimeManager(start_day=1, start_hour=22, start_minute=0)
        assert tm_night.is_daytime is False

    def test_speed_multiplier(self):
        tm = TimeManager(speed_multiplier=5.0)
        assert tm.speed_multiplier == 5.0

    def test_listeners(self):
        tm = TimeManager()
        events = []

        def on_event(event):
            events.append(event)

        tm.add_listener(on_event)
        tm.advance(60)
        assert len(events) == 1
        assert events[0].hour == 7
        assert events[0].minute == 0
        tm.remove_listener(on_event)
        tm.advance(60)
        assert len(events) == 1  # No new event

    def test_advance_by_tick(self):
        tm = TimeManager(speed_multiplier=1.0)
        tm.advance_by_tick(1.0)
        assert tm.minute == 1
        tm.advance_by_tick(1.0)
        assert tm.minute == 2

    def test_to_from_dict(self):
        tm = TimeManager(start_day=3, start_hour=14, start_minute=30, speed_multiplier=20.0)
        data = tm.to_dict()
        tm2 = TimeManager.from_dict(data)
        assert tm2.day == 3
        assert tm2.hour == 14
        assert tm2.minute == 30
        assert tm2.speed_multiplier == 20.0


class TestWorldEngineConfig:
    def test_defaults(self):
        config = WorldEngineConfig()
        assert config.grid_width == 100
        assert config.grid_height == 100
        assert config.seconds_per_tick == 1.0
        assert config.time_speed_multiplier == 1.0

    def test_custom_values(self):
        config = WorldEngineConfig(grid_width=50, grid_height=50, seconds_per_tick=0.5, time_speed_multiplier=10.0)
        assert config.grid_width == 50
        assert config.grid_height == 50
        assert config.seconds_per_tick == 0.5
        assert config.time_speed_multiplier == 10.0


class TestWorldEngineTimeAndSerialization:
    def test_backward_compat_none_config(self):
        engine = WorldEngine(config=None)
        assert engine.time_manager is not None
        assert engine.time_manager.day == 1

    def test_backward_compat_dict_config(self):
        engine = WorldEngine(config={"grid_width": 20, "grid_height": 20})
        assert engine.grid.width == 20
        assert engine.grid.height == 20

    def test_config_dataclass(self):
        config = WorldEngineConfig(grid_width=10, grid_height=10, seconds_per_tick=0.1, time_speed_multiplier=2.0)
        engine = WorldEngine(config=config)
        assert engine.grid.width == 10
        assert engine.grid.height == 10
        assert engine.time_manager.speed_multiplier == 2.0

    def test_time_advances_on_tick(self):
        engine = WorldEngine()
        initial_hour = engine.time_manager.hour
        engine.run_simulation_step()
        assert engine.time_manager.hour >= initial_hour

    def test_save_state_returns_json(self):
        engine = WorldEngine()
        entity = engine.spawn_entity()
        engine.registry.add_component(entity, Position(5, 5, 0))
        json_str = engine.save_state()
        assert isinstance(json_str, str)
        data = pytest.importorskip("json").loads(json_str)
        assert "entities" in data
        assert "time_manager" in data
        assert "config" in data
        assert len(data["entities"]) == 1

    def test_load_state_restores_world(self):
        engine1 = WorldEngine()
        e = engine1.spawn_entity()
        engine1.registry.add_component(e, Position(7, 3, 0))
        engine1.run_simulation_step()
        state_json = engine1.save_state()

        engine2 = WorldEngine()
        engine2.load_state(state_json)
        assert engine2.tick_count == engine1.tick_count
        assert engine2.time_manager.day == engine1.time_manager.day
        assert engine2.time_manager.hour == engine1.time_manager.hour
        entities = list(engine2.registry._entities)
        assert len(entities) == 1
        pos = engine2.registry.get_component(entities[0], Position)
        assert pos.x == 7
        assert pos.y == 3

    def test_save_state_contains_time_manager(self):
        engine = WorldEngine()
        engine.run_simulation_step()
        json_str = engine.save_state()
        data = pytest.importorskip("json").loads(json_str)
        assert "total_minutes" in data["time_manager"]
        assert "speed_multiplier" in data["time_manager"]

    def test_load_state_restores_time_manager(self):
        engine1 = WorldEngine(config=WorldEngineConfig(seconds_per_tick=0.5, time_speed_multiplier=10.0))
        for _ in range(100):
            engine1.run_simulation_step()
        state_json = engine1.save_state()

        engine2 = WorldEngine()
        engine2.load_state(state_json)
        assert engine2.time_manager.day == engine1.time_manager.day
        assert engine2.time_manager.hour == engine1.time_manager.hour
        assert engine2.time_manager.minute == engine1.time_manager.minute
        assert engine2.time_manager.speed_multiplier == engine1.time_manager.speed_multiplier

