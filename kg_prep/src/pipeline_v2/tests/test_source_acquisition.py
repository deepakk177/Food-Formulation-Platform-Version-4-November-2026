"""
Unit Tests for Pipeline V2 Source Acquisition Modules.
"""

import tempfile
from pathlib import Path
import pytest

from pipeline_v2.acquisition.foodon_acquirer import FoodonAcquirer
from pipeline_v2.acquisition.gsfa_acquirer import GsfaAcquirer
from pipeline_v2.acquisition.usda_acquirer import UsdaAcquirer
from pipeline_v2.acquisition.pubchem_acquirer import PubChemAcquirer
from pipeline_v2.core.manifest import ManifestManager
from pipeline_v2.models.manifest_models import IntegrityStatus


def test_foodon_acquisition_local_reuse():
    """Verifies FoodOn acquirer reuses existing genuine raw asset and registers it."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = ManifestManager()
        acquirer = FoodonAcquirer(raw_dir=tmpdir)

        asset = acquirer.acquire(manifest_manager=manager, force_download=False)

        assert asset.source_id == "SRC-FOODON"
        assert asset.asset_id == "AST-FOODON-OWL-001"
        assert asset.integrity_status == IntegrityStatus.VERIFIED
        assert asset.file_size_bytes > 10_000_000
        assert len(asset.sha256) == 64
        assert Path(asset.local_path).exists()


def test_gsfa_acquisition_local_reuse():
    """Verifies GSFA acquirer reuses existing genuine additive HTML and registers it."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = ManifestManager()
        acquirer = GsfaAcquirer(raw_dir=tmpdir)

        asset = acquirer.acquire_additive_index(manifest_manager=manager)

        assert asset.source_id == "SRC-CODEX-GSFA"
        assert asset.asset_id == "AST-CODEX-GSFA-ADDITIVES-001"
        assert asset.integrity_status == IntegrityStatus.VERIFIED
        assert asset.file_size_bytes > 40_000
        assert len(asset.sha256) == 64


def test_gsfa_online_cloudflare_detection():
    """Verifies that GsfaAcquirer detects Cloudflare anti-bot gate gracefully."""
    acquirer = GsfaAcquirer()
    result = acquirer.probe_online_category_provision("01.0")

    assert result["category_code"] == "01.0"
    assert result["status"] in ("BLOCKED_BY_CLOUDFLARE", "CONNECTION_FAILED", "ACCESSIBLE")
    if result["status"] == "BLOCKED_BY_CLOUDFLARE":
        assert result["http_code"] == 403


def test_usda_acquirer_local_registration():
    """Verifies UsdaAcquirer registration of acquired JSON files in manifest."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / "test_usda.json"
        tmp_path.write_bytes(b'{"foods": []}')

        manager = ManifestManager()
        acquirer = UsdaAcquirer(raw_dir=tmpdir)
        asset = acquirer.register_acquired_asset("AST-USDA-01", tmp_path, manager)

        assert asset.source_id == "SRC-USDA-FDC"
        assert asset.asset_id == "AST-USDA-01"
        assert asset.integrity_status == IntegrityStatus.VERIFIED
        assert asset.file_size_bytes == len(b'{"foods": []}')


def test_pubchem_acquirer_local_registration():
    """Verifies PubChemAcquirer registration of acquired compound JSON in manifest."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / "test_pubchem.json"
        tmp_path.write_bytes(b'{"PropertyTable": {"Properties": []}}')

        manager = ManifestManager()
        acquirer = PubChemAcquirer(raw_dir=tmpdir)
        asset = acquirer.register_acquired_asset("AST-PUBCHEM-01", tmp_path, manager)

        assert asset.source_id == "SRC-PUBCHEM"
        assert asset.asset_id == "AST-PUBCHEM-01"
        assert asset.integrity_status == IntegrityStatus.VERIFIED
        assert asset.file_size_bytes == len(b'{"PropertyTable": {"Properties": []}}')
