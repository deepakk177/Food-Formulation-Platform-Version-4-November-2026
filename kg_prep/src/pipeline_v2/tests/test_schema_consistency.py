"""
Unit Tests for Pipeline V2 Schema Consistency and Structural Guarantees.

Validates that all frozen schemas, relationship endpoints, output filenames,
and provenance rules adhere strictly to the Phase 0.2 architecture.
"""

import re
from pathlib import Path
import pytest

from pipeline_v2.core.registry import PipelineRegistry


@pytest.fixture(scope="module")
def registry():
    """Loads and validates the complete production config_v2 directory."""
    pkg_dir = Path(__file__).resolve().parent.parent.parent.parent
    config_dir = pkg_dir / "config_v2"
    r = PipelineRegistry(str(config_dir))
    r.load_all()
    return r


def test_frozen_node_count(registry):
    """Verifies all 41 frozen canonical and reified node entities are defined."""
    assert len(registry.nodes) == 41


def test_frozen_relationship_count(registry):
    """Verifies all 38 canonical relationship contracts are defined."""
    assert len(registry.relationships) == 38


def test_frozen_source_count(registry):
    """Verifies all 12 approved source integrations are defined."""
    assert len(registry.sources) == 12


def test_all_output_filenames_unique_and_valid_format(registry):
    """Verifies every node output filename is unique and follows 'Nodes/<Name>.csv'."""
    seen_filenames = set()
    for node_type, schema in registry.nodes.items():
        assert schema.output_filename.startswith("Nodes/")
        assert schema.output_filename.endswith(".csv")
        assert (
            schema.output_filename not in seen_filenames
        ), f"Filename collision on {schema.output_filename}"
        seen_filenames.add(schema.output_filename)


def test_all_relationship_endpoints_referentially_valid(registry):
    """Verifies every relationship contract has valid, existing source and target node types."""
    valid_node_types = set(registry.nodes.keys())

    for rel_name, rel in registry.relationships.items():
        sources = (
            [rel.source_node_type]
            if isinstance(rel.source_node_type, str)
            else rel.source_node_type
        )
        targets = (
            [rel.target_node_type]
            if isinstance(rel.target_node_type, str)
            else rel.target_node_type
        )

        for s in sources:
            assert (
                s in valid_node_types
            ), f"Relationship {rel_name} has invalid source_node_type: {s}"

        for t in targets:
            assert (
                t in valid_node_types
            ), f"Relationship {rel_name} has invalid target_node_type: {t}"


def test_canonical_snake_case_fields(registry):
    """Verifies that all field names across node schemas follow lowercase snake_case."""
    snake_case_pattern = re.compile(r"^[a-z][a-z0-9_]*$")

    for node_type, schema in registry.nodes.items():
        all_fields = schema.required_fields + schema.optional_fields
        for field in all_fields:
            assert snake_case_pattern.match(
                field
            ), f"Node '{node_type}' field '{field}' is not lowercase snake_case."


def test_provenance_requirements_defined(registry):
    """Verifies every node schema specifies provenance requirements."""
    for node_type, schema in registry.nodes.items():
        assert (
            len(schema.provenance_requirements) > 0
        ), f"Node '{node_type}' missing provenance_requirements"


def test_standard_relationship_header_conformance():
    """Verifies the standard lower_snake_case relationship header contract."""
    from pipeline_v2.core.registry import PipelineRegistry

    pkg_dir = Path(__file__).resolve().parent.parent.parent.parent
    config_dir = pkg_dir / "config_v2"
    r = PipelineRegistry(str(config_dir))
    rel_data = r._read_yaml("relationship_schemas.yaml")

    expected_header = [
        "relationship_id",
        "source_id",
        "source_type",
        "relationship_type",
        "target_id",
        "target_type",
        "source_dataset_id",
        "source_record_id",
        "extraction_confidence",
        "evidence_id",
        "verification_status",
    ]

    assert rel_data.get("standard_header") == expected_header
