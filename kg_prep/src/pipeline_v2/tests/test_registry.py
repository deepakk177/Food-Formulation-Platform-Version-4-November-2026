"""
Unit Tests for Pipeline V2 Registry Module.
"""

import os
import tempfile
from pathlib import Path
import pytest
import yaml

from pipeline_v2.core.registry import PipelineRegistry
from pipeline_v2.core.exceptions import (
    ConfigurationError,
    SourceRegistryError,
    SchemaValidationError,
    ReferentialIntegrityError,
)


@pytest.fixture
def valid_config_dir():
    """Returns path to the production config_v2 directory."""
    pkg_dir = Path(__file__).resolve().parent.parent.parent.parent
    return pkg_dir / "config_v2"


def test_valid_yaml_loading(valid_config_dir):
    """Verifies that the frozen configurations load and validate cleanly."""
    registry = PipelineRegistry(str(valid_config_dir))
    registry.load_all()

    assert registry.is_loaded is True
    assert len(registry.sources) == 12
    assert len(registry.nodes) == 41
    assert len(registry.relationships) == 38
    assert "canonical_namespaces" in registry.normalizer_rules
    assert "conversion_factors" in registry.normalizer_rules


def test_missing_config_directory():
    """Verifies that non-existent directory raises ConfigurationError."""
    registry = PipelineRegistry("/non/existent/config/path/12345")
    with pytest.raises(ConfigurationError, match="does not exist"):
        registry.load_all()


def test_missing_config_file():
    """Verifies that a missing YAML file raises ConfigurationError."""
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = PipelineRegistry(tmpdir)
        with pytest.raises(ConfigurationError, match="Missing configuration file"):
            registry.load_all()


def test_duplicate_source_id():
    """Verifies fail-fast rejection of duplicate source IDs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        source_yaml = {
            "version": "2.0.0",
            "sources": [
                {
                    "source_id": "SRC-TEST-1",
                    "source_name": "Test 1",
                    "authority": "Auth",
                    "source_type": "DATABASE",
                    "base_url": "https://example.com",
                    "endpoint": "NOT_VERIFIED",
                    "access_method": "LOCAL_FILE",
                    "expected_format": "JSON",
                    "authentication_required": False,
                    "license_reference": "Open",
                    "dataset_version": "1.0",
                    "access_status": "LOCAL_AVAILABLE",
                    "parser_identifier": "test_parser",
                },
                {
                    "source_id": "SRC-TEST-1",
                    "source_name": "Test 1 Duplicate",
                    "authority": "Auth",
                    "source_type": "DATABASE",
                    "base_url": "https://example.com",
                    "endpoint": "NOT_VERIFIED",
                    "access_method": "LOCAL_FILE",
                    "expected_format": "JSON",
                    "authentication_required": False,
                    "license_reference": "Open",
                    "dataset_version": "1.0",
                    "access_status": "LOCAL_AVAILABLE",
                    "parser_identifier": "test_parser",
                },
            ],
        }
        with open(tmp_path / "source_registry.yaml", "w", encoding="utf-8") as f:
            yaml.dump(source_yaml, f)

        registry = PipelineRegistry(tmpdir)
        with pytest.raises(SourceRegistryError, match="Duplicate source_id detected"):
            registry.load_sources()


def test_duplicate_output_filename():
    """Verifies rejection of output CSV filename collisions across node schemas."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        node_yaml = {
            "version": "2.0.0",
            "nodes": [
                {
                    "node_type": "IngredientA",
                    "output_filename": "Nodes/CollidingFile.csv",
                    "primary_key": "id_a",
                    "required_fields": ["id_a"],
                    "field_types": {"id_a": "string"},
                    "nullability": {"id_a": False},
                },
                {
                    "node_type": "IngredientB",
                    "output_filename": "Nodes/CollidingFile.csv",
                    "primary_key": "id_b",
                    "required_fields": ["id_b"],
                    "field_types": {"id_b": "string"},
                    "nullability": {"id_b": False},
                },
            ],
        }
        with open(tmp_path / "node_schemas.yaml", "w", encoding="utf-8") as f:
            yaml.dump(node_yaml, f)

        registry = PipelineRegistry(tmpdir)
        with pytest.raises(SchemaValidationError, match="output_filename collision"):
            registry.load_nodes()


def test_invalid_relationship_endpoints():
    """Verifies that an edge referencing a nonexistent node type raises ReferentialIntegrityError."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        # Create minimal valid node schema
        node_yaml = {
            "version": "2.0.0",
            "nodes": [
                {
                    "node_type": "Ingredient",
                    "output_filename": "Nodes/Ingredients.csv",
                    "primary_key": "ingredient_id",
                    "required_fields": ["ingredient_id"],
                    "field_types": {"ingredient_id": "string"},
                    "nullability": {"ingredient_id": False},
                }
            ],
        }
        with open(tmp_path / "node_schemas.yaml", "w", encoding="utf-8") as f:
            yaml.dump(node_yaml, f)

        # Relationship pointing to undefined NonExistentCategory node
        rel_yaml = {
            "version": "2.0.0",
            "relationships": [
                {
                    "relationship_name": "bad_rel",
                    "relationship_type": "TEST_REL",
                    "source_node_type": "Ingredient",
                    "target_node_type": "NonExistentCategory",
                    "direction": "OUTGOING",
                    "provenance_requirement": "Test",
                    "evidence_requirement": "Test",
                }
            ],
        }
        with open(tmp_path / "relationship_schemas.yaml", "w", encoding="utf-8") as f:
            yaml.dump(rel_yaml, f)

        registry = PipelineRegistry(tmpdir)
        registry.load_nodes()
        registry.load_relationships()

        with pytest.raises(ReferentialIntegrityError, match="undefined target_node_type 'NonExistentCategory'"):
            registry.validate_cross_references()


def test_required_field_marked_nullable():
    """Verifies schema validation failure when a required field is marked nullable=True."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        node_yaml = {
            "version": "2.0.0",
            "nodes": [
                {
                    "node_type": "BadNode",
                    "output_filename": "Nodes/Bad.csv",
                    "primary_key": "id",
                    "required_fields": ["id", "mandatory_field"],
                    "field_types": {"id": "string", "mandatory_field": "string"},
                    "nullability": {"id": False, "mandatory_field": True},
                }
            ],
        }
        with open(tmp_path / "node_schemas.yaml", "w", encoding="utf-8") as f:
            yaml.dump(node_yaml, f)

        registry = PipelineRegistry(tmpdir)
        with pytest.raises(SchemaValidationError, match="Required field 'mandatory_field' cannot be marked nullable=True"):
            registry.load_nodes()
