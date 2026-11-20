"""
Pipeline V2 Source and Schema Configuration Models.

Defines typed Pydantic models for sources, datasets, node schemas,
relationship contracts, and normalization rules.
"""

from enum import Enum
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel, Field, field_validator, model_validator


class AccessStatus(str, Enum):
    LOCAL_AVAILABLE = "LOCAL_AVAILABLE"
    LOCAL_PARTIAL = "LOCAL_PARTIAL"
    REMOTE_AVAILABLE = "REMOTE_AVAILABLE"
    BLOCKED_REQUIRES_REGISTRATION = "BLOCKED_REQUIRES_REGISTRATION"
    BLOCKED_REQUIRES_LICENSE = "BLOCKED_REQUIRES_LICENSE"
    UNAVAILABLE = "UNAVAILABLE"


class AccessMethod(str, Enum):
    LOCAL_FILE = "LOCAL_FILE"
    BULK_DOWNLOAD = "BULK_DOWNLOAD"
    REST_API = "REST_API"
    WEB_SCRAPING = "WEB_SCRAPING"
    MANUAL_DOWNLOAD = "MANUAL_DOWNLOAD"
    GATED_API = "GATED_API"


class SourceIntegrationModel(BaseModel):
    """Declarative specification for an approved data source."""
    source_id: str = Field(..., description="Unique source identifier (e.g. SRC-FOODON)")
    source_name: str = Field(..., description="Full canonical name of the source")
    authority: str = Field(..., description="Governing body or publishing organization")
    source_type: str = Field(..., description="ONTOLOGY, DATABASE, REGULATION, REPOSITORY, etc.")
    base_url: str = Field(..., description="Official base URL")
    endpoint: str = Field(..., description="Specific download endpoint or query URL; NOT_VERIFIED if unconfirmed")
    access_method: AccessMethod = Field(..., description="Operational access protocol")
    expected_format: str = Field(..., description="Expected serialization format (OWL, JSON, CSV, PDF, HTML)")
    authentication_required: bool = Field(default=False)
    environment_variable_name: Optional[str] = Field(None, description="Environment variable holding secret if applicable")
    license_reference: str = Field(..., description="Legal license or copyright terms")
    update_frequency: str = Field(default="UNKNOWN")
    dataset_version: str = Field(..., description="Authoritative version code or release date")
    supported_node_types: List[str] = Field(default_factory=list)
    supported_relationship_types: List[str] = Field(default_factory=list)
    enabled: bool = Field(default=True)
    access_status: AccessStatus = Field(..., description="Operational availability status")
    parser_identifier: str = Field(..., description="Extractor module or class identifier")
    notes: str = Field(default="")
    source_limitations: str = Field(default="")

    @field_validator("source_id")
    @classmethod
    def validate_source_id(cls, v: str) -> str:
        if not v.startswith("SRC-"):
            raise ValueError(f"source_id must begin with 'SRC-', got '{v}'")
        return v


class NodeSchemaModel(BaseModel):
    """Declarative specification for a canonical or reified node entity."""
    node_type: str = Field(..., description="Canonical node label (e.g. Ingredient, FoodCategory)")
    output_filename: str = Field(..., description="Exact CSV filename (e.g. Nodes/Ingredients.csv)")
    primary_key: str = Field(..., description="Unique identifier field name")
    required_fields: List[str] = Field(..., description="Fields that must be non-null in every valid row")
    optional_fields: List[str] = Field(default_factory=list)
    field_types: Dict[str, str] = Field(..., description="Data types for all fields (string, float, integer, boolean, iso_datetime)")
    uniqueness_constraints: List[str] = Field(default_factory=list)
    nullability: Dict[str, bool] = Field(..., description="Mapping of field_name -> is_nullable")
    provenance_requirements: List[str] = Field(default_factory=list)

    @field_validator("output_filename")
    @classmethod
    def validate_output_filename(cls, v: str) -> str:
        if not v.startswith("Nodes/") or not v.endswith(".csv"):
            raise ValueError(f"output_filename must follow 'Nodes/<Name>.csv' pattern, got '{v}'")
        return v

    @model_validator(mode="after")
    def validate_keys_and_types(self) -> "NodeSchemaModel":
        all_fields = set(self.required_fields + self.optional_fields)
        # Check that primary key is in required fields
        if self.primary_key not in self.required_fields:
            raise ValueError(f"primary_key '{self.primary_key}' must be included in required_fields")
        # Check that every field has a type defined
        for f in all_fields:
            if f not in self.field_types:
                raise ValueError(f"Field '{f}' in node '{self.node_type}' missing entry in field_types")
            if f not in self.nullability:
                raise ValueError(f"Field '{f}' in node '{self.node_type}' missing entry in nullability")
        # Required fields must not be nullable
        for req in self.required_fields:
            if self.nullability.get(req, False) is True:
                raise ValueError(f"Required field '{req}' cannot be marked nullable=True")
        return self


class RelationshipSchemaModel(BaseModel):
    """Declarative specification for a frozen relationship contract."""
    relationship_name: str = Field(..., description="Canonical relationship identifier (e.g. ingredient_belongs_to_category)")
    relationship_type: str = Field(..., description="Uppercase graph edge label (e.g. BELONGS_TO_CATEGORY)")
    source_node_type: Union[str, List[str]] = Field(..., description="Valid source node label(s)")
    target_node_type: Union[str, List[str]] = Field(..., description="Valid target node label(s)")
    direction: str = Field(default="OUTGOING", description="Relationship direction (always OUTGOING source->target)")
    required_properties: List[str] = Field(default_factory=list)
    optional_properties: List[str] = Field(default_factory=list)
    provenance_requirement: str = Field(..., description="Mandatory provenance rule")
    evidence_requirement: str = Field(..., description="Mandatory citation/evidence rule")
    allowed_assertion_status: List[str] = Field(default_factory=list)
    uniqueness_constraints: List[str] = Field(default_factory=list)
    is_derived: bool = Field(default=False)

    @field_validator("relationship_type")
    @classmethod
    def validate_rel_type(cls, v: str) -> str:
        if not v.isupper():
            raise ValueError(f"relationship_type must be UPPERCASE, got '{v}'")
        return v


class NormalizerConfigModel(BaseModel):
    """Declarative specification for unit systems and conversion rules."""
    version: str
    unit_systems: Dict[str, Any]
    conversion_factors: Dict[str, Any]
    physical_dimensions: Dict[str, Any]
    canonical_namespaces: Dict[str, str]
    text_normalization: Dict[str, Any]
