"""
Tests for ConfigLoader and ConfigSchema.

Covers src/utils/config_loader.py without requiring real config files on disk.
File-I/O operations (load_avatar_config etc.) are NOT tested here — they depend
on the configs/ directory which is not present in CI.
"""

import json
import pytest

from src.utils.config_loader import ConfigLoader, ConfigSchema


# ---------------------------------------------------------------------------
# ConfigSchema tests
# ---------------------------------------------------------------------------

class TestConfigSchema:
    def test_default_schema(self):
        schema = ConfigSchema()
        assert schema.required_fields == []
        assert schema.optional_fields == []
        assert schema.field_types == {}
        assert schema.field_constraints == {}
        assert schema.validation_rules == []

    def test_custom_schema(self):
        schema = ConfigSchema(
            required_fields=["id", "name"],
            optional_fields=["description"],
            field_types={"id": str, "name": str},
        )
        assert "id" in schema.required_fields
        assert "description" in schema.optional_fields


# ---------------------------------------------------------------------------
# ConfigLoader instantiation
# ---------------------------------------------------------------------------

class TestConfigLoaderInit:
    def test_instantiation_with_default_dir(self):
        loader = ConfigLoader()
        assert loader.config_dir.name == "configs"

    def test_instantiation_with_custom_dir(self):
        loader = ConfigLoader(config_dir="my_configs")
        assert loader.config_dir.name == "my_configs"

    def test_schemas_initialized(self):
        loader = ConfigLoader()
        assert "avatar" in loader.schemas
        assert "aide" in loader.schemas
        assert "simulation" in loader.schemas
        assert "training" in loader.schemas

    def test_loaded_configs_starts_empty(self):
        loader = ConfigLoader()
        assert loader.loaded_configs == {}


# ---------------------------------------------------------------------------
# validate_config — unknown type (no schema)
# ---------------------------------------------------------------------------

class TestValidateConfigUnknownType:
    def test_unknown_type_returns_true(self):
        loader = ConfigLoader()
        assert loader.validate_config({"anything": 1}, "unknown_type") is True


# ---------------------------------------------------------------------------
# validate_config — avatar schema
# ---------------------------------------------------------------------------

class TestValidateConfigAvatar:
    def setup_method(self):
        self.loader = ConfigLoader()
        self.valid = {
            "avatar_id": "av-001",
            "trait_name": "attention",
            "trait_config": {"intensity": 0.8},
            "initial_state": {"energy": 100},
        }

    def test_valid_avatar_config(self):
        assert self.loader.validate_config(self.valid, "avatar") is True

    def test_missing_required_field(self):
        bad = dict(self.valid)
        del bad["avatar_id"]
        assert self.loader.validate_config(bad, "avatar") is False

    def test_wrong_type_avatar_id(self):
        bad = dict(self.valid)
        bad["avatar_id"] = 42  # should be str
        assert self.loader.validate_config(bad, "avatar") is False

    def test_wrong_type_trait_config(self):
        bad = dict(self.valid)
        bad["trait_config"] = "not-a-dict"
        assert self.loader.validate_config(bad, "avatar") is False

    def test_difficulty_level_in_range(self):
        config = dict(self.valid)
        config["difficulty_level"] = 0.5
        assert self.loader.validate_config(config, "avatar") is True

    def test_difficulty_level_above_max(self):
        config = dict(self.valid)
        config["difficulty_level"] = 1.5
        assert self.loader.validate_config(config, "avatar") is False

    def test_difficulty_level_below_min(self):
        config = dict(self.valid)
        config["difficulty_level"] = -0.1
        assert self.loader.validate_config(config, "avatar") is False

    def test_optional_field_wrong_type(self):
        config = dict(self.valid)
        config["description"] = 999  # should be str
        assert self.loader.validate_config(config, "avatar") is False

    def test_learning_rate_in_range(self):
        config = dict(self.valid)
        config["learning_rate"] = 0.01
        assert self.loader.validate_config(config, "avatar") is True

    def test_learning_rate_out_of_range(self):
        config = dict(self.valid)
        config["learning_rate"] = 2.0
        assert self.loader.validate_config(config, "avatar") is False


# ---------------------------------------------------------------------------
# validate_config — aide schema
# ---------------------------------------------------------------------------

class TestValidateConfigAide:
    def setup_method(self):
        self.loader = ConfigLoader()
        self.valid = {
            "aide_id": "aide-001",
            "expertise_area": "attention",
            "expertise_config": {},
            "rrt_config": {},
        }

    def test_valid_aide_config(self):
        assert self.loader.validate_config(self.valid, "aide") is True

    def test_missing_aide_id(self):
        bad = dict(self.valid)
        del bad["aide_id"]
        assert self.loader.validate_config(bad, "aide") is False

    def test_intervention_threshold_in_range(self):
        config = dict(self.valid)
        config["intervention_threshold"] = 0.5
        assert self.loader.validate_config(config, "aide") is True

    def test_intervention_threshold_out_of_range(self):
        config = dict(self.valid)
        config["intervention_threshold"] = 1.5
        assert self.loader.validate_config(config, "aide") is False


# ---------------------------------------------------------------------------
# _check_constraints
# ---------------------------------------------------------------------------

class TestCheckConstraints:
    def setup_method(self):
        self.loader = ConfigLoader()

    def test_min_constraint_pass(self):
        assert self.loader._check_constraints(5, {"min": 0}) is True

    def test_min_constraint_fail(self):
        assert self.loader._check_constraints(-1, {"min": 0}) is False

    def test_max_constraint_pass(self):
        assert self.loader._check_constraints(0.5, {"max": 1.0}) is True

    def test_max_constraint_fail(self):
        assert self.loader._check_constraints(2.0, {"max": 1.0}) is False

    def test_choices_constraint_pass(self):
        assert self.loader._check_constraints("easy", {"choices": ["easy", "medium", "hard"]}) is True

    def test_choices_constraint_fail(self):
        assert self.loader._check_constraints("impossible", {"choices": ["easy", "medium", "hard"]}) is False

    def test_pattern_constraint_pass(self):
        assert self.loader._check_constraints("abc-123", {"pattern": r"^[a-z]+-\d+$"}) is True

    def test_pattern_constraint_fail(self):
        assert self.loader._check_constraints("!!!bad", {"pattern": r"^[a-z]+-\d+$"}) is False

    def test_multiple_constraints_all_pass(self):
        assert self.loader._check_constraints(0.5, {"min": 0, "max": 1}) is True

    def test_multiple_constraints_one_fails(self):
        assert self.loader._check_constraints(1.5, {"min": 0, "max": 1}) is False

    def test_no_constraints_returns_true(self):
        assert self.loader._check_constraints("anything", {}) is True


# ---------------------------------------------------------------------------
# validate_config — with custom validation rule
# ---------------------------------------------------------------------------

class TestValidationRules:
    def test_validation_rule_pass(self):
        loader = ConfigLoader()
        schema = ConfigSchema(
            required_fields=["x"],
            validation_rules=[lambda c: c.get("x", 0) > 0],
        )
        loader.schemas["custom"] = schema
        assert loader.validate_config({"x": 5}, "custom") is True

    def test_validation_rule_fail(self):
        loader = ConfigLoader()
        schema = ConfigSchema(
            required_fields=["x"],
            validation_rules=[lambda c: c.get("x", 0) > 0],
        )
        loader.schemas["custom"] = schema
        assert loader.validate_config({"x": -1}, "custom") is False


# ---------------------------------------------------------------------------
# save_config
# ---------------------------------------------------------------------------

class TestSaveConfig:
    def test_save_json_file(self, tmp_path):
        loader = ConfigLoader()
        config = {
            "avatar_id": "av-save",
            "trait_name": "focus",
            "trait_config": {},
            "initial_state": {},
        }
        dest = str(tmp_path / "output.json")
        result = loader.save_config(config, dest, "avatar")
        assert result is True
        with open(dest) as f:
            loaded = json.load(f)
        assert loaded["avatar_id"] == "av-save"

    def test_save_yaml_file(self, tmp_path):
        loader = ConfigLoader()
        config = {
            "avatar_id": "av-yaml",
            "trait_name": "focus",
            "trait_config": {},
            "initial_state": {},
        }
        dest = str(tmp_path / "output.yaml")
        result = loader.save_config(config, dest, "avatar")
        assert result is True

    def test_save_invalid_config_returns_false(self, tmp_path):
        loader = ConfigLoader()
        # Missing required fields
        config = {"avatar_id": "av-bad"}
        dest = str(tmp_path / "bad.json")
        result = loader.save_config(config, dest, "avatar")
        assert result is False

    def test_save_generic_type_skips_validation(self, tmp_path):
        loader = ConfigLoader()
        config = {"anything": "goes"}
        dest = str(tmp_path / "generic.json")
        result = loader.save_config(config, dest, "generic")
        assert result is True

    def test_save_to_nonexistent_dir_returns_false(self):
        loader = ConfigLoader()
        config = {
            "avatar_id": "av-001",
            "trait_name": "focus",
            "trait_config": {},
            "initial_state": {},
        }
        result = loader.save_config(config, "/no/such/directory/file.json", "avatar")
        assert result is False
