"""
Pipeline V2 Manifest Management Module.

Tracks acquired raw assets, computes reproducible SHA-256 cryptographic hashes
from actual file bytes, verifies file integrity, detects duplicates, and exports
manifest documents to JSON and CSV.
"""

import csv
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Union

from pipeline_v2.core.exceptions import (
    ManifestError,
    AssetNotFoundError,
    ChecksumMismatchError,
    CorruptedAssetError,
)
from pipeline_v2.models.manifest_models import (
    AssetRecord,
    ManifestDocument,
    IntegrityStatus,
)


class ManifestManager:
    """Manages raw asset manifests and cryptographic integrity checks."""

    CHUNK_SIZE = 65536  # 64 KB read buffer for streaming hash calculation

    def __init__(self, manifest_id: Optional[str] = None):
        self.manifest_id = (
            manifest_id
            or f"MANIFEST-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        )
        self.assets: Dict[str, AssetRecord] = {}  # asset_id -> AssetRecord

    @classmethod
    def compute_sha256(cls, file_path: Union[str, Path]) -> str:
        """Computes lowercase hex-encoded SHA-256 checksum from actual file bytes."""
        path = Path(file_path)
        if not path.exists():
            raise AssetNotFoundError(f"File not found for hash calculation: {path}")
        if not path.is_file():
            raise CorruptedAssetError(f"Target path is not a regular file: {path}")

        hasher = hashlib.sha256()
        try:
            with open(path, "rb") as f:
                while chunk := f.read(cls.CHUNK_SIZE):
                    hasher.update(chunk)
            return hasher.hexdigest().lower()
        except OSError as e:
            raise CorruptedAssetError(f"Failed to read file bytes from {path}: {e}")

    @classmethod
    def get_file_size_bytes(cls, file_path: Union[str, Path]) -> int:
        """Returns the file size in bytes."""
        path = Path(file_path)
        if not path.exists():
            raise AssetNotFoundError(f"File not found: {path}")
        return path.stat().st_size

    def register_asset(
        self,
        asset_id: str,
        source_id: str,
        dataset_id: str,
        local_path: Union[str, Path],
        source_url: str,
        dataset_version: str,
        content_type: str,
        original_filename: Optional[str] = None,
        access_status: str = "LOCAL_AVAILABLE",
        expected_sha256: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ) -> AssetRecord:
        """
        Registers an asset file, computes its SHA-256 and size from disk,
        and verifies integrity against expected checksum if supplied.
        """
        path = Path(local_path)
        if not path.exists():
            raise AssetNotFoundError(
                f"Cannot register asset '{asset_id}': path '{path}' does not exist."
            )

        if asset_id in self.assets:
            raise ManifestError(f"Asset with ID '{asset_id}' is already registered.")

        # Compute hash and size from actual file bytes
        computed_sha256 = self.compute_sha256(path)
        file_size = self.get_file_size_bytes(path)
        filename = original_filename or path.name

        integrity = IntegrityStatus.VERIFIED
        if expected_sha256:
            expected_lower = expected_sha256.strip().lower()
            if computed_sha256 != expected_lower:
                integrity = IntegrityStatus.CHECKSUM_MISMATCH
                raise ChecksumMismatchError(
                    f"Checksum mismatch for asset '{asset_id}' ({filename}): "
                    f"expected '{expected_lower}', computed '{computed_sha256}'."
                )

        record = AssetRecord(
            asset_id=asset_id,
            source_id=source_id,
            dataset_id=dataset_id,
            original_filename=filename,
            local_path=str(path.as_posix()),
            source_url=source_url,
            dataset_version=dataset_version,
            downloaded_at=datetime.now(timezone.utc).isoformat(),
            file_size_bytes=file_size,
            sha256=computed_sha256,
            content_type=content_type,
            access_status=access_status,
            integrity_status=integrity,
            metadata=metadata or {},
        )

        self.assets[asset_id] = record
        return record

    def verify_asset(self, asset_id: str) -> bool:
        """
        Re-verifies an existing asset on disk:
        Checks existence, readability, size consistency, and recomputes SHA-256.
        """
        if asset_id not in self.assets:
            raise AssetNotFoundError(f"Asset '{asset_id}' not found in manifest.")

        record = self.assets[asset_id]
        path = Path(record.local_path)

        if not path.exists():
            record.integrity_status = IntegrityStatus.FILE_MISSING
            raise AssetNotFoundError(f"Asset file missing on disk: {path}")

        current_size = path.stat().st_size
        if current_size != record.file_size_bytes:
            record.integrity_status = IntegrityStatus.CORRUPTED
            raise CorruptedAssetError(
                f"Asset '{asset_id}' size mismatch: registered {record.file_size_bytes} bytes, "
                f"found {current_size} bytes."
            )

        current_hash = self.compute_sha256(path)
        if current_hash != record.sha256:
            record.integrity_status = IntegrityStatus.CHECKSUM_MISMATCH
            raise ChecksumMismatchError(
                f"Asset '{asset_id}' hash changed on disk! Recorded {record.sha256}, "
                f"computed {current_hash}."
            )

        record.integrity_status = IntegrityStatus.VERIFIED
        return True

    def find_duplicate_hashes(self) -> Dict[str, List[str]]:
        """Identifies duplicate files in the manifest based on identical SHA-256."""
        hash_map: Dict[str, List[str]] = {}
        for asset in self.assets.values():
            hash_map.setdefault(asset.sha256, []).append(asset.asset_id)
        return {h: ids for h, ids in hash_map.items() if len(ids) > 1}

    def to_manifest_document(self) -> ManifestDocument:
        """Creates a snapshot ManifestDocument."""
        asset_list = list(self.assets.values())
        total_bytes = sum(a.file_size_bytes for a in asset_list)
        return ManifestDocument(
            manifest_id=self.manifest_id,
            total_assets=len(asset_list),
            total_bytes=total_bytes,
            assets=asset_list,
        )

    def save_json(self, output_path: Union[str, Path]) -> Path:
        """Serializes the manifest to a formatted JSON file."""
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        doc = self.to_manifest_document()
        with open(out, "w", encoding="utf-8") as f:
            f.write(doc.model_dump_json(indent=2))
        return out

    @classmethod
    def load_json(cls, input_path: Union[str, Path]) -> "ManifestManager":
        """Loads a ManifestManager instance from a previously serialized JSON manifest."""
        in_path = Path(input_path)
        if not in_path.exists():
            raise ManifestError(f"Manifest file not found: {in_path}")
        with open(in_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        doc = ManifestDocument(**data)
        manager = cls(manifest_id=doc.manifest_id)
        for asset in doc.assets:
            manager.assets[asset.asset_id] = asset
        return manager

    def export_csv(self, output_path: Union[str, Path]) -> Path:
        """Exports tabular asset metadata to a standard CSV file."""
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "asset_id",
            "source_id",
            "dataset_id",
            "original_filename",
            "local_path",
            "source_url",
            "dataset_version",
            "downloaded_at",
            "file_size_bytes",
            "sha256",
            "content_type",
            "access_status",
            "integrity_status",
        ]

        with open(out, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for a in self.assets.values():
                row = {fn: getattr(a, fn) for fn in fieldnames}
                writer.writerow(row)
        return out
