"""
Pipeline V2 Core Package.
"""

from .exceptions import (
    PipelineError,
    ConfigurationError,
    SourceRegistryError,
    SchemaValidationError,
    ReferentialIntegrityError,
    ManifestError,
    AssetNotFoundError,
    ChecksumMismatchError,
    CorruptedAssetError,
    NetworkAcquisitionError,
    HTTPStatusError,
    RateLimitExceededError,
    DownloadTimeoutError,
    ContentTypeError,
    InterruptedDownloadError,
    StorageError,
    DatabaseInitializationError,
    DuplicateRecordError,
    TransactionError,
    ProvenanceTrackingError,
    NormalizationError,
    UnsupportedUnitError,
    IncompatibleDimensionError,
)
from .logging_config import setup_logger
from .registry import PipelineRegistry
from .manifest import ManifestManager
from .http_client import HttpAcquisitionClient

__all__ = [
    "PipelineError",
    "ConfigurationError",
    "SourceRegistryError",
    "SchemaValidationError",
    "ReferentialIntegrityError",
    "ManifestError",
    "AssetNotFoundError",
    "ChecksumMismatchError",
    "CorruptedAssetError",
    "NetworkAcquisitionError",
    "HTTPStatusError",
    "RateLimitExceededError",
    "DownloadTimeoutError",
    "ContentTypeError",
    "InterruptedDownloadError",
    "StorageError",
    "DatabaseInitializationError",
    "DuplicateRecordError",
    "TransactionError",
    "ProvenanceTrackingError",
    "NormalizationError",
    "UnsupportedUnitError",
    "IncompatibleDimensionError",
    "setup_logger",
    "PipelineRegistry",
    "ManifestManager",
    "HttpAcquisitionClient",
]
