"""
Pipeline V2 Source-Native Extracted Record Models.

Represents un-normalized, raw structured records extracted directly from
external genuine sources (FoodOn, USDA FDC, PubChem, Codex GSFA) before
entity resolution or normalization in Phase 3.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class ExtractionStatus(str, Enum):
    EXTRACTED = "EXTRACTED"
    REJECTED = "REJECTED"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"


class SourceRecord(BaseModel):
    """
    Standardized container for raw extracted source-native records.
    Adheres strictly to the Section 5 Extractor Output Contract.
    """
    source_id: str = Field(..., description="Unique source identifier (e.g. SRC-FOODON)")
    dataset_id: str = Field(..., description="Dataset release snapshot identifier")
    source_record_id: str = Field(..., description="Native primary identifier in original source")
    source_entity_type: str = Field(..., description="Source-native entity type (e.g. OWL_CLASS, FOOD_ITEM)")
    original_identifier: str = Field(..., description="Exact raw identifier as reported by source")
    original_name: str = Field(..., description="Exact raw label or description")
    original_fields: Dict[str, Any] = Field(default_factory=dict, description="Raw source key-value payload")
    raw_asset_id: str = Field(..., description="Foreign key to source_assets.asset_id in manifest")
    source_location: str = Field(..., description="Exact URI, line, row, or table reference in raw file")
    extraction_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    extraction_status: ExtractionStatus = Field(default=ExtractionStatus.EXTRACTED)
    rejection_reason: Optional[str] = Field(None, description="Detailed explanation if record was rejected")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ExtractionBatchResult(BaseModel):
    """Summary of an extractor execution batch."""
    source_id: str
    dataset_id: str
    asset_id: str
    total_records_discovered: int = 0
    total_records_extracted: int = 0
    total_records_rejected: int = 0
    total_records_review: int = 0
    records: List[SourceRecord] = Field(default_factory=list)
    rejected_records: List[SourceRecord] = Field(default_factory=list)
    errors: List[Dict[str, Any]] = Field(default_factory=list)
