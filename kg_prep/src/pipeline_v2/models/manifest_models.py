"""
Pipeline V2 Manifest and Asset Models.

Defines data models for tracking raw downloaded assets, computing cryptographic hashes,
and maintaining reproducible asset manifests.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class IntegrityStatus(str, Enum):
    VERIFIED = "VERIFIED"
    CHECKSUM_MISMATCH = "CHECKSUM_MISMATCH"
    FILE_MISSING = "FILE_MISSING"
    CORRUPTED = "CORRUPTED"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"


class AssetRecord(BaseModel):
    """Represents a single acquired raw asset file tracked by the pipeline."""
    asset_id: str = Field(..., description="Unique asset ID, e.g. AST-USDA-001")
    source_id: str = Field(..., description="Foreign key to source_registry.source_id")
    dataset_id: str = Field(..., description="Dataset release identifier, e.g. DSK-USDA-SRLEGACY-2024")
    original_filename: str = Field(..., description="Original remote or local file name")
    local_path: str = Field(..., description="Relative or absolute path in data/raw_v2/")
    source_url: str = Field(..., description="Remote URL or local provenance URI")
    dataset_version: str = Field(..., description="Release version code or date string")
    downloaded_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    file_size_bytes: int = Field(..., ge=0, description="Size in bytes on disk")
    sha256: str = Field(..., min_length=64, max_length=64, description="Hex-encoded SHA-256 hash")
    content_type: str = Field(..., description="MIME content type or format description")
    access_status: str = Field(default="LOCAL_AVAILABLE")
    integrity_status: IntegrityStatus = Field(default=IntegrityStatus.PENDING_VERIFICATION)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("sha256")
    @classmethod
    def validate_sha256_format(cls, v: str) -> str:
        v = v.lower()
        if not all(c in "0123456789abcdef" for c in v):
            raise ValueError(f"sha256 must be a 64-character lowercase hex string, got '{v}'")
        return v


class ManifestDocument(BaseModel):
    """Collection of assets forming a coherent snapshot of the raw data lake."""
    manifest_id: str = Field(..., description="Unique manifest release identifier, e.g. MANIFEST-2026-11-16")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    pipeline_version: str = Field(default="2.0.0")
    total_assets: int = Field(default=0)
    total_bytes: int = Field(default=0)
    assets: List[AssetRecord] = Field(default_factory=list)
