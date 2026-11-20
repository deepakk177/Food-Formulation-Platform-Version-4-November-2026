"""
Unit Tests for Pipeline V2 Codex GSFA Extractor Module.
"""

import tempfile
from pathlib import Path
import pytest

from pipeline_v2.extractors.gsfa.extractor import GsfaExtractor
from pipeline_v2.core.exceptions import CorruptedAssetError, AssetNotFoundError
from pipeline_v2.models.source_record_models import ExtractionStatus


@pytest.fixture
def gsfa_html_path():
    """Returns path to genuine local gsfa_additives.html file."""
    p = Path("data/raw/semi_structured/gsfa_html/gsfa_additives.html")
    if not p.exists():
        pytest.skip("gsfa_additives.html not found in local workspace")
    return p


def test_extract_additives_from_genuine_gsfa_index(gsfa_html_path):
    """Verifies parsing of authentic Codex GSFA additive index."""
    extractor = GsfaExtractor()
    batch = extractor.extract_from_html_index(
        html_file_path=gsfa_html_path,
        raw_asset_id="AST-CODEX-TEST",
    )

    assert batch.source_id == "SRC-CODEX-GSFA"
    assert batch.total_records_discovered > 200
    assert batch.total_records_extracted > 200
    assert len(batch.records) > 200

    # Find Acesulfame potassium (INS 950, GSFA ID 104)
    acesulfame = [r for r in batch.records if r.source_record_id == "GSFA:104"]
    assert len(acesulfame) == 1
    ace = acesulfame[0]
    assert ace.source_entity_type == "FOOD_ADDITIVE"
    assert "Acesulfame potassium" in ace.original_name
    assert ace.original_fields["ins_number"] == "950"
    assert ace.original_fields["regulatory_standard"] == "CXS 192-1995"
    assert ace.extraction_status == ExtractionStatus.EXTRACTED

    # Invariant Verification: Zero modulo-assigned categories or fake max levels in raw records
    for rec in batch.records:
        assert "food_category_code" not in rec.original_fields
        assert "max_use_level" not in rec.original_fields


def test_gsfa_missing_file():
    """Verifies AssetNotFoundError on missing HTML file."""
    extractor = GsfaExtractor()
    with pytest.raises(AssetNotFoundError):
        extractor.extract_from_html_index("data/non_existent.html", "AST-FAIL")


def test_gsfa_synthetic_content_handling():
    """Verifies parsing on small controlled HTML snippet."""
    sample_html = """
    <html><body>
    <table>
      <tr><td><a href="details.html?id=999">Test Additive Alpha (1001)</a></td></tr>
      <tr><td><a href="details.html?id=999">Duplicate Additive (1001)</a></td></tr>
    </table>
    </body></html>
    """
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(sample_html)
        tmp_path = Path(tmp.name)

    try:
        extractor = GsfaExtractor()
        batch = extractor.extract_from_html_index(tmp_path, "AST-SNIPPET")
        # Should deduplicate id=999
        assert batch.total_records_extracted == 1
        rec = batch.records[0]
        assert rec.source_record_id == "GSFA:999"
        assert rec.original_fields["ins_number"] == "1001"
        assert rec.original_name == "Test Additive Alpha"
    finally:
        if tmp_path.exists():
            tmp_path.unlink()
