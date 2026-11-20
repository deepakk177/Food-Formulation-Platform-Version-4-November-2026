"""
Pipeline V2 Registry Module.

Responsible for loading, parsing, and strictly validating all configuration files:
- source_registry.yaml
- node_schemas.yaml
- relationship_schemas.yaml
- normalizer_rules.yaml

Enforces fail-fast referential integrity:
- Every relationship endpoint must match an existing node type.
- Every node output filename must be unique.
- No duplicate source_ids, node_types, or relationship_names.
- Required fields and type annotations must be valid.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
import yaml
from pydantic import ValidationError

from pipeline_v2.core.exceptions import (
    ConfigurationError,
    SourceRegistryError,
    SchemaValidationError,
    ReferentialIntegrityError,
)
from pipeline_v2.models.source_models import (
    SourceIntegrationModel,
    NodeSchemaModel,
    RelationshipSchemaModel,
    NormalizerConfigModel,
)


class PipelineRegistry:
    """Central registry holding validated configurations for Pipeline V2."""

    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir) if config_dir else self._default_config_dir()
        self.sources: Dict[str, SourceIntegrationModel] = {}
        self.nodes: Dict[str, NodeSchemaModel] = {}
        self.relationships: Dict[str, RelationshipSchemaModel] = {}
        self.normalizer_rules: Optional[Dict[str, Any]] = None
        self.config_versions: Dict[str, str] = {}
        self.is_loaded: bool = False

    @staticmethod
    def _default_config_dir() -> Path:
        # Defaults to kg_prep/config_v2 relative to workspace
        current_file = Path(__file__).resolve()
        # pipeline_v2/core/registry.py -> up 3 levels to kg_prep -> config_v2
        return current_file.parent.parent.parent / "config_v2"

    def load_all(self) -> "PipelineRegistry":
        """Loads and validates all four configuration files."""
        if not self.config_dir.exists():
            raise ConfigurationError(
                f"Configuration directory does not exist: {self.config_dir}"
            )

        self.load_sources()
        self.load_nodes()
        self.load_relationships()
        self.load_normalizer_rules()
        self.validate_cross_references()
        self.is_loaded = True
        return self

    def _read_yaml(self, filename: str) -> Dict[str, Any]:
        file_path = self.config_dir / filename
        if not file_path.exists():
            raise ConfigurationError(f"Missing configuration file: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if not isinstance(data, dict):
                raise ConfigurationError(
                    f"Configuration file {filename} must contain a YAML mapping (dict)."
                )
            return data
        except yaml.YAMLError as e:
            raise ConfigurationError(f"YAML parsing error in {filename}: {e}")

    def load_sources(self) -> Dict[str, SourceIntegrationModel]:
        """Loads and validates source_registry.yaml."""
        data = self._read_yaml("source_registry.yaml")
        self.config_versions["source_registry"] = data.get("version", "UNKNOWN")

        raw_sources = data.get("sources")
        if not isinstance(raw_sources, list):
            raise SourceRegistryError("source_registry.yaml missing 'sources' list.")

        loaded_sources: Dict[str, SourceIntegrationModel] = {}
        for entry in raw_sources:
            try:
                model = SourceIntegrationModel(**entry)
                if model.source_id in loaded_sources:
                    raise SourceRegistryError(
                        f"Duplicate source_id detected: '{model.source_id}'."
                    )
                loaded_sources[model.source_id] = model
            except ValidationError as ve:
                raise SourceRegistryError(
                    f"Validation error in source definition '{entry.get('source_id', 'UNKNOWN')}': {ve}"
                )

        self.sources = loaded_sources
        return self.sources

    def load_nodes(self) -> Dict[str, NodeSchemaModel]:
        """Loads and validates node_schemas.yaml."""
        data = self._read_yaml("node_schemas.yaml")
        self.config_versions["node_schemas"] = data.get("version", "UNKNOWN")

        raw_nodes = data.get("nodes")
        if not isinstance(raw_nodes, list):
            raise SchemaValidationError("node_schemas.yaml missing 'nodes' list.")

        loaded_nodes: Dict[str, NodeSchemaModel] = {}
        filenames_seen: Dict[str, str] = {}

        for entry in raw_nodes:
            try:
                model = NodeSchemaModel(**entry)
                if model.node_type in loaded_nodes:
                    raise SchemaValidationError(
                        f"Duplicate node_type detected: '{model.node_type}'."
                    )
                if model.output_filename in filenames_seen:
                    prev_node = filenames_seen[model.output_filename]
                    raise SchemaValidationError(
                        f"Duplicate output_filename collision: '{model.output_filename}' used by both "
                        f"'{prev_node}' and '{model.node_type}'."
                    )
                filenames_seen[model.output_filename] = model.node_type
                loaded_nodes[model.node_type] = model
            except ValidationError as ve:
                raise SchemaValidationError(
                    f"Validation error in node schema '{entry.get('node_type', 'UNKNOWN')}': {ve}"
                )

        self.nodes = loaded_nodes
        return self.nodes

    def load_relationships(self) -> Dict[str, RelationshipSchemaModel]:
        """Loads and validates relationship_schemas.yaml."""
        data = self._read_yaml("relationship_schemas.yaml")
        self.config_versions["relationship_schemas"] = data.get("version", "UNKNOWN")

        raw_rels = data.get("relationships")
        if not isinstance(raw_rels, list):
            raise SchemaValidationError("relationship_schemas.yaml missing 'relationships' list.")

        loaded_rels: Dict[str, RelationshipSchemaModel] = {}
        for entry in raw_rels:
            try:
                model = RelationshipSchemaModel(**entry)
                if model.relationship_name in loaded_rels:
                    raise SchemaValidationError(
                        f"Duplicate relationship_name detected: '{model.relationship_name}'."
                    )
                loaded_rels[model.relationship_name] = model
            except ValidationError as ve:
                raise SchemaValidationError(
                    f"Validation error in relationship contract '{entry.get('relationship_name', 'UNKNOWN')}': {ve}"
                )

        self.relationships = loaded_rels
        return self.relationships

    def load_normalizer_rules(self) -> Dict[str, Any]:
        """Loads and validates normalizer_rules.yaml."""
        data = self._read_yaml("normalizer_rules.yaml")
        self.config_versions["normalizer_rules"] = data.get("version", "UNKNOWN")

        required_sections = [
            "canonical_namespaces",
            "physical_dimensions",
            "conversion_factors",
            "percentage_bases",
            "supported_currencies",
            "text_normalization",
        ]
        for sec in required_sections:
            if sec not in data:
                raise ConfigurationError(
                    f"normalizer_rules.yaml missing required section '{sec}'."
                )

        self.normalizer_rules = data
        return self.normalizer_rules

    def validate_cross_references(self) -> None:
        """
        Validates cross-file referential integrity:
        1. Every relationship source_node_type must exist in self.nodes.
        2. Every relationship target_node_type must exist in self.nodes.
        3. Every supported_node_type in sources must exist in self.nodes.
        4. Every supported_relationship_type in sources must exist in self.relationships (by relationship_type).
        """
        valid_node_types = set(self.nodes.keys())
        valid_rel_types = {rel.relationship_type for rel in self.relationships.values()}

        # 1 & 2: Relationship Endpoints Referential Integrity
        for rel_name, rel in self.relationships.items():
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
                if s not in valid_node_types:
                    raise ReferentialIntegrityError(
                        f"Relationship '{rel_name}' references undefined source_node_type '{s}'. "
                        f"Available node types: {sorted(list(valid_node_types))}"
                    )

            for t in targets:
                if t not in valid_node_types:
                    raise ReferentialIntegrityError(
                        f"Relationship '{rel_name}' references undefined target_node_type '{t}'. "
                        f"Available node types: {sorted(list(valid_node_types))}"
                    )

        # 3 & 4: Source Registry References
        for source_id, src in self.sources.items():
            for nt in src.supported_node_types:
                if nt not in valid_node_types:
                    raise ReferentialIntegrityError(
                        f"Source '{source_id}' lists unsupported node_type '{nt}'."
                    )
            for rt in src.supported_relationship_types:
                if rt not in valid_rel_types:
                    raise ReferentialIntegrityError(
                        f"Source '{source_id}' lists unsupported relationship_type '{rt}'."
                    )

    def get_source(self, source_id: str) -> SourceIntegrationModel:
        if source_id not in self.sources:
            raise SourceRegistryError(f"Source '{source_id}' not found in registry.")
        return self.sources[source_id]

    def get_node_schema(self, node_type: str) -> NodeSchemaModel:
        if node_type not in self.nodes:
            raise SchemaValidationError(f"Node schema for '{node_type}' not found.")
        return self.nodes[node_type]

    def get_relationship_schema(self, relationship_name: str) -> RelationshipSchemaModel:
        if relationship_name not in self.relationships:
            raise SchemaValidationError(
                f"Relationship contract for '{relationship_name}' not found."
            )
        return self.relationships[relationship_name]
