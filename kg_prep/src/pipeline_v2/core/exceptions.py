"""
Pipeline V2 Structured Exceptions Hierarchy.

All domain-specific exceptions raised by registry, manifest, http_client,
storage, and normalization modules inherit from PipelineError.
"""

from typing import Optional, Dict, Any


class PipelineError(Exception):
    """Base exception for all Knowledge Graph Pipeline V2 errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


# Configuration & Registry Exceptions
class ConfigurationError(PipelineError):
    """Raised when configuration files are missing, malformed, or invalid."""
    pass


class SourceRegistryError(ConfigurationError):
    """Raised when source definitions are invalid or violate registry rules."""
    pass


class SchemaValidationError(ConfigurationError):
    """Raised when node or relationship schema definitions fail structural validation."""
    pass


class ReferentialIntegrityError(SchemaValidationError):
    """Raised when relationship endpoints refer to nonexistent or incompatible node types."""
    pass


# Manifest & File Integrity Exceptions
class ManifestError(PipelineError):
    """Base exception for manifest and asset tracking errors."""
    pass


class AssetNotFoundError(ManifestError):
    """Raised when an asset registered in the manifest does not exist on disk."""
    pass


class ChecksumMismatchError(ManifestError):
    """Raised when an asset's computed SHA-256 does not match the registered/expected hash."""
    pass


class CorruptedAssetError(ManifestError):
    """Raised when an asset is unreadable, empty when unexpected, or truncated."""
    pass


# HTTP Client & Acquisition Exceptions
class NetworkAcquisitionError(PipelineError):
    """Base exception for network and download failures."""
    pass


class HTTPStatusError(NetworkAcquisitionError):
    """Raised when an HTTP request returns an error status (4xx, 5xx)."""

    def __init__(self, message: str, status_code: int, url: str, details: Optional[Dict[str, Any]] = None):
        details = details or {}
        details.update({"status_code": status_code, "url": url})
        super().__init__(message, details=details)
        self.status_code = status_code
        self.url = url


class RateLimitExceededError(HTTPStatusError):
    """Raised when an HTTP 429 Too Many Requests response is received and retries exhausted."""
    pass


class DownloadTimeoutError(NetworkAcquisitionError):
    """Raised when an HTTP download times out during connection or reading."""
    pass


class ContentTypeError(NetworkAcquisitionError):
    """Raised when the received Content-Type does not match the expected format (e.g. HTML error page)."""
    pass


class InterruptedDownloadError(NetworkAcquisitionError):
    """Raised when a download terminates prematurely before all bytes are received."""
    pass


# Storage & DuckDB Exceptions
class StorageError(PipelineError):
    """Base exception for database and persistence errors."""
    pass


class DatabaseInitializationError(StorageError):
    """Raised when DuckDB fails to initialize or create required schema tables."""
    pass


class DuplicateRecordError(StorageError):
    """Raised when a record violates a primary key or unique constraint."""
    pass


class TransactionError(StorageError):
    """Raised when a database transaction fails or rollback is triggered."""
    pass


class ProvenanceTrackingError(StorageError):
    """Raised when mandatory provenance or lineage metadata cannot be recorded."""
    pass


# Data Normalization Exceptions
class NormalizationError(PipelineError):
    """Base exception for data normalization failures."""
    pass


class UnsupportedUnitError(NormalizationError):
    """Raised when an unknown or unconvertible unit is encountered."""
    pass


class IncompatibleDimensionError(NormalizationError):
    """Raised when attempting an impossible unit conversion (e.g., mass to temperature)."""
    pass
