"""
Configuration Loader

Handles loading and validation of configuration files for Avatars, Aides, and
simulation environments. Ensures all configurations meet required schemas.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
import json
import yaml
import re
from pathlib import Path
from datetime import datetime


@dataclass
class ConfigSchema:
    """Schema definition for configuration validation"""
    required_fields: List[str] = field(default_factory=list)
    optional_fields: List[str] = field(default_factory=list)
    field_types: Dict[str, type] = field(default_factory=dict)
    field_constraints: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    validation_rules: List[callable] = field(default_factory=list)


class ConfigLoader:
    """
    Configuration loader with validation and schema support.
    """
    
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.loaded_configs: Dict[str, Dict[str, Any]] = {}
        self.schemas: Dict[str, ConfigSchema] = {}
        
        # Initialize default schemas
        self._initialize_default_schemas()
    
    def load_avatar_config(self, avatar_name: str) -> Dict[str, Any]:
        """
        Load Avatar configuration.
        
        Args:
            avatar_name: Name of the Avatar configuration to load
            
        Returns:
            Avatar configuration dictionary
        """
        config_path = self.config_dir / "avatars" / f"{avatar_name}.json"
        return self._load_config(config_path, "avatar")
    
    def load_aide_config(self, aide_name: str) -> Dict[str, Any]:
        """
        Load Aide configuration.
        
        Args:
            aide_name: Name of the Aide configuration to load
            
        Returns:
            Aide configuration dictionary
        """
        config_path = self.config_dir / "aides" / f"{aide_name}.json"
        return self._load_config(config_path, "aide")
    
    def load_simulation_config(self, config_name: str = "simulation") -> Dict[str, Any]:
        """
        Load simulation configuration.
        
        Args:
            config_name: Name of the simulation configuration to load
            
        Returns:
            Simulation configuration dictionary
        """
        config_path = self.config_dir / f"{config_name}.yaml"
        return self._load_config(config_path, "simulation")
    
    def load_training_config(self, config_name: str = "training") -> Dict[str, Any]:
        """
        Load training configuration.
        
        Args:
            config_name: Name of the training configuration to load
            
        Returns:
            Training configuration dictionary
        """
        config_path = self.config_dir / f"{config_name}.yaml"
        return self._load_config(config_path, "training")
    
    def validate_config(self, config: Dict[str, Any], config_type: str) -> bool:
        """
        Validate configuration against schema.
        
        Args:
            config: Configuration to validate
            config_type: Type of configuration (avatar, aide, etc.)
            
        Returns:
            True if valid, False otherwise
        """
        if config_type not in self.schemas:
            return True  # No schema defined, assume valid
        
        schema = self.schemas[config_type]
        
        # Check required fields
        for field in schema.required_fields:
            if field not in config:
                return False
        
        # Check field types
        for field, expected_type in schema.field_types.items():
            if field in config and not isinstance(config[field], expected_type):
                return False
        
        # Check field constraints
        for field, constraints in schema.field_constraints.items():
            if field in config:
                if not self._check_constraints(config[field], constraints):
                    return False
        
        # Run validation rules
        for rule in schema.validation_rules:
            if not rule(config):
                return False
        
        return True
    
    def save_config(self, config: Dict[str, Any], config_path: str, 
                   config_type: str = "generic") -> bool:
        """
        Save configuration to file.
        
        Args:
            config: Configuration to save
            config_path: Path to save configuration
            config_type: Type of configuration for validation
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Validate before saving
            if not self.validate_config(config, config_type):
                return False
            
            # Determine file format
            path = Path(config_path)
            if path.suffix.lower() in ['.yaml', '.yml']:
                with open(path, 'w') as f:
                    yaml.dump(config, f, default_flow_style=False)
            else:
                with open(path, 'w') as f:
                    json.dump(config, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Failed to save config: {e}")
            return False
    
    def _load_config(self, config_path: Path, config_type: str) -> Dict[str, Any]:
        """Load configuration from file"""
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            if config_path.suffix.lower() in ['.yaml', '.yml']:
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
            else:
                with open(config_path, 'r') as f:
                    config = json.load(f)
            
            # Validate configuration
            if not self.validate_config(config, config_type):
                raise ValueError(f"Invalid configuration: {config_path}")
            
            # Cache the configuration
            self.loaded_configs[str(config_path)] = config
            
            return config
            
        except Exception as e:
            print(f"Failed to load config {config_path}: {e}")
            raise
    
    def _check_constraints(self, value: Any, constraints: Dict[str, Any]) -> bool:
        """Check value against constraints"""
        for constraint_type, constraint_value in constraints.items():
            if constraint_type == "min" and value < constraint_value:
                return False
            elif constraint_type == "max" and value > constraint_value:
                return False
            elif constraint_type == "choices" and value not in constraint_value:
                return False
            elif constraint_type == "pattern" and not re.match(constraint_value, str(value)):
                return False
        
        return True
    
    def _initialize_default_schemas(self) -> None:
        """Initialize default configuration schemas"""
        
        # Avatar schema
        self.schemas["avatar"] = ConfigSchema(
            required_fields=[
                "avatar_id",
                "trait_name",
                "trait_config",
                "initial_state",
            ],
            optional_fields=[
                "description",
                "difficulty_level",
                "learning_rate",
                "burnout_threshold",
            ],
            field_types={
                "avatar_id": str,
                "trait_name": str,
                "trait_config": dict,
                "initial_state": dict,
                "description": str,
                "difficulty_level": (int, float),
                "learning_rate": (int, float),
                "burnout_threshold": (int, float),
            },
            field_constraints={
                "difficulty_level": {"min": 0, "max": 1},
                "learning_rate": {"min": 0, "max": 1},
                "burnout_threshold": {"min": 0, "max": 1},
            },
        )
        
        # Aide schema
        self.schemas["aide"] = ConfigSchema(
            required_fields=[
                "aide_id",
                "expertise_area",
                "expertise_config",
                "rrt_config",
            ],
            optional_fields=[
                "description",
                "coaching_style",
                "intervention_threshold",
                "success_metrics",
            ],
            field_types={
                "aide_id": str,
                "expertise_area": str,
                "expertise_config": dict,
                "rrt_config": dict,
                "description": str,
                "coaching_style": str,
                "intervention_threshold": (int, float),
                "success_metrics": dict,
            },
            field_constraints={
                "intervention_threshold": {"min": 0, "max": 1},
            },
        )
        
        # Simulation schema
        self.schemas["simulation"] = ConfigSchema(
            required_fields=[
                "simulation_id",
                "world_config",
                "time_config",
                "consequence_config",
            ],
            optional_fields=[
                "description",
                "difficulty_scaling",
                "random_events",
                "performance_metrics",
            ],
            field_types={
                "simulation_id": str,
                "world_config": dict,
                "time_config": dict,
                "consequence_config": dict,
                "description": str,
                "difficulty_scaling": dict,
                "random_events": dict,
                "performance_metrics": dict,
            },
        )
        
        # Training schema
        self.schemas["training"] = ConfigSchema(
            required_fields=[
                "training_id",
                "avatar_config",
                "aide_config",
                "scenario_config",
            ],
            optional_fields=[
                "description",
                "duration",
                "success_criteria",
                "evaluation_metrics",
            ],
            field_types={
                "training_id": str,
                "avatar_config": dict,
                "aide_config": dict,
                "scenario_config": dict,
                "description": str,
                "duration": (int, str),
                "success_criteria": dict,
                "evaluation_metrics": dict,
            },
        )