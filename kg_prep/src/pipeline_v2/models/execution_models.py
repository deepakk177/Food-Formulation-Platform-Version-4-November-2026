"""
Pipeline V2 Execution, Provenance, and Error Models.

Defines schemas for execution runs, stage telemetry, field-level provenance,
relationship-level provenance, and structured error tracking.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class ExecutionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ABORTED = "ABORTED"


class ProcessingStage(str, Enum):
    ACQUISITION = "ACQUISITION"
    EXTRACTION = "EXTRACTION"
    NORMALIZATION = "NORMALIZATION"
    RESOLUTION = "RESOLUTION"
    GRAPH_SYNTHESIS = "GRAPH_SYNTHESIS"
    VALIDATION = "VALIDATION"
    EXPORT = "EXPORT"


class ExecutionRunRecord(BaseModel):
    """Execution run telemetry record stored in DuckDB execution_runs."""
    execution_id: str = Field(..., description="Unique run UUID or timestamp-based ID")
    stage_name: ProcessingStage
    status: ExecutionStatus = Field(default=ExecutionStatus.PENDING)
    started_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None
    total_records_processed: int = Field(default=0)
    total_records_failed: int = Field(default=0)
    pipeline_version: str = Field(default="2.0.0")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    summary_metrics: Dict[str, Any] = Field(default_factory=dict)


class ExecutionErrorRecord(BaseModel):
    """Structured failure record stored in DuckDB execution_errors."""
    error_id: str = Field(..., description="Unique error identifier")
    execution_id: str = Field(..., description="Foreign key to execution_runs")
    stage_name: ProcessingStage
    source_id: Optional[str] = None
    record_identifier: Optional[str] = None
    error_type: str = Field(..., description="Class name of exception")
    error_message: str = Field(..., description="Human-readable exception message")
    error_details: Dict[str, Any] = Field(default_factory=dict)
    occurred_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class FieldProvenanceRecord(BaseModel):
    """Field-level lineage tracking record stored in DuckDB field_provenance."""
    provenance_id: str = Field(..., description="Unique provenance entry ID")
    execution_id: str = Field(..., description="Execution run ID")
    target_table: str = Field(..., description="Canonical node table name (e.g. Ingredients)")
    target_entity_id: str = Field(..., description="Primary key value of the node")
    target_field_name: str = Field(..., description="Attribute name populated")
    source_id: str = Field(..., description="Source system ID (e.g. SRC-FOODON)")
    source_dataset_id: str = Field(..., description="Dataset release ID")
    source_record_id: str = Field(..., description="Native record ID in original source")
    source_field_name: str = Field(..., description="Native attribute name in original source")
    raw_value: Optional[str] = None
    normalized_value: Optional[str] = None
    transformation_rule: Optional[str] = None
    extraction_confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class RelationshipProvenanceRecord(BaseModel):
    """Relationship-level lineage tracking record stored in DuckDB relationship_provenance."""
    relationship_id: str = Field(..., description="Unique relationship ID")
    execution_id: str = Field(..., description="Execution run ID")
    relationship_type: str = Field(..., description="Edge label (e.g. BELONGS_TO_CATEGORY)")
    source_node_id: str = Field(..., description="Source node primary key")
    source_node_type: str = Field(..., description="Source node label")
    target_node_id: str = Field(..., description="Target node primary key")
    target_node_type: str = Field(..., description="Target node label")
    source_dataset_id: str = Field(..., description="Origin dataset ID")
    source_record_id: str = Field(..., description="Native source record identifier")
    extraction_confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    evidence_id: Optional[str] = None
    verification_status: str = Field(default="SOURCE_VERIFIED")
    is_derived: bool = Field(default=False)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
