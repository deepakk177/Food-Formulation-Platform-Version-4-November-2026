"""
Unit Tests for Pipeline V2 Manifest Module.
"""

import hashlib
import os
import tempfile
from pathlib import Path
import pytest

from pipeline_v2.core.manifest import ManifestManager
from pipeline_v2.core.exceptions import (
    AssetNotFoundError,
    ChecksumMismatchError,
    CorruptedAssetError,
    ManifestError,
)
from pipeline_v2.models.manifest_models import IntegrityStatus


def test_compute_sha256_known_content():
    """Verifies that compute_sha256 produces exact lowercase SHA-256 hash."""
    with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
        payload = b"Food Formulation Knowledge Graph Ground Truth 2026"
        tmp.write(payload)
        tmp_path = Path(tmp.name)

    try:
        expected_hash = hashlib.sha256(payload).hexdigest().lower()
        computed_hash = ManifestManager.compute_sha256(tmp_path)
        assert computed_hash == expected_hash
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def test_missing_file_detection():
    """Verifies that non-existent paths raise AssetNotFoundError."""
    with pytest.raises(AssetNotFoundError):
        ManifestManager.compute_sha256("/non/existent/file.csv")

    with pytest.raises(AssetNotFoundError):
        ManifestManager.get_file_size_bytes("/non/existent/file.csv")


def test_register_asset_and_checksum_verification():
    """Registers an asset and verifies correct metadata and integrity status."""
    with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
        payload = b"Genuine food data content"
        tmp.write(payload)
        tmp_path = Path(tmp.name)

    try:
        expected_hash = hashlib.sha256(payload).hexdigest().lower()
        manager = ManifestManager()

        record = manager.register_asset(
            asset_id="AST-001",
            source_id="SRC-FOODON",
            dataset_id="DSK-FOODON-01",
            local_path=tmp_path,
            source_url="https://example.com/foodon.owl",
            dataset_version="2024-03-08",
            content_type="application/rdf+xml",
            expected_sha256=expected_hash,
        )

        assert record.sha256 == expected_hash
        assert record.file_size_bytes == len(payload)
        assert record.integrity_status == IntegrityStatus.VERIFIED
        assert manager.verify_asset("AST-001") is True
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def test_checksum_mismatch():
    """Verifies that registering with an incorrect expected hash raises ChecksumMismatchError."""
    with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
        tmp.write(b"Original content")
        tmp_path = Path(tmp.name)

    try:
        manager = ManifestManager()
        wrong_hash = "0" * 64
        with pytest.raises(ChecksumMismatchError, match="Checksum mismatch"):
            manager.register_asset(
                asset_id="AST-FAIL",
                source_id="SRC-TEST",
                dataset_id="DSK-TEST",
                local_path=tmp_path,
                source_url="https://example.com/test",
                dataset_version="1.0",
                content_type="text/plain",
                expected_sha256=wrong_hash,
            )
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def test_detect_file_tampering_or_mutation():
    """Verifies that modifying a registered file on disk is caught during verification."""
    with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
        tmp.write(b"Original pristine data")
        tmp_path = Path(tmp.name)

    try:
        manager = ManifestManager()
        manager.register_asset(
            asset_id="AST-TAMPER",
            source_id="SRC-TEST",
            dataset_id="DSK-TEST",
            local_path=tmp_path,
            source_url="https://example.com/test",
            dataset_version="1.0",
            content_type="text/plain",
        )

        # Mutate the file on disk
        with open(tmp_path, "wb") as f:
            f.write(b"Tampered data with different length and bytes")

        with pytest.raises((CorruptedAssetError, ChecksumMismatchError)):
            manager.verify_asset("AST-TAMPER")
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def test_duplicate_file_detection():
    """Verifies that duplicate content across multiple assets is detected."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_dir = Path(tmpdir)
        file1 = tmp_dir / "file1.dat"
        file2 = tmp_dir / "file2.dat"

        shared_bytes = b"Identical dataset content in two places"
        file1.write_bytes(shared_bytes)
        file2.write_bytes(shared_bytes)

        manager = ManifestManager()
        manager.register_asset(
            asset_id="AST-DUP-1",
            source_id="SRC-A",
            dataset_id="DSK-A",
            local_path=file1,
            source_url="https://a.com/file",
            dataset_version="1.0",
            content_type="text/plain",
        )
        manager.register_asset(
            asset_id="AST-DUP-2",
            source_id="SRC-B",
            dataset_id="DSK-B",
            local_path=file2,
            source_url="https://b.com/file",
            dataset_version="1.0",
            content_type="text/plain",
        )

        duplicates = manager.find_duplicate_hashes()
        expected_hash = hashlib.sha256(shared_bytes).hexdigest().lower()
        assert expected_hash in duplicates
        assert set(duplicates[expected_hash]) == {"AST-DUP-1", "AST-DUP-2"}


def test_manifest_serialization_json_and_csv():
    """Verifies export and round-trip reloading of JSON and CSV manifest formats."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_dir = Path(tmpdir)
        test_file = tmp_dir / "test.csv"
        test_file.write_bytes(b"col1,col2\nval1,val2\n")

        manager = ManifestManager(manifest_id="MANIFEST-TEST-001")
        manager.register_asset(
            asset_id="AST-SER-1",
            source_id="SRC-FOODON",
            dataset_id="DSK-FOODON",
            local_path=test_file,
            source_url="https://example.com/test.csv",
            dataset_version="1.0",
            content_type="text/csv",
        )

        json_out = tmp_dir / "manifest.json"
        csv_out = tmp_dir / "manifest.csv"

        manager.save_json(json_out)
        manager.export_csv(csv_out)

        assert json_out.exists()
        assert csv_out.exists()

        # Reload from JSON
        loaded_manager = ManifestManager.load_json(json_out)
        assert loaded_manager.manifest_id == "MANIFEST-TEST-001"
        assert "AST-SER-1" in loaded_manager.assets
        assert loaded_manager.assets["AST-SER-1"].file_size_bytes == test_file.stat().st_size
