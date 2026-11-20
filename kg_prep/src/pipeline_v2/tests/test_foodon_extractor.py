"""
Unit Tests for Pipeline V2 FoodOn Extractor Module.
"""

import tempfile
from pathlib import Path
import pytest

from pipeline_v2.extractors.foodon.extractor import FoodonExtractor
from pipeline_v2.core.exceptions import CorruptedAssetError, AssetNotFoundError
from pipeline_v2.models.source_record_models import ExtractionStatus


@pytest.fixture
def foodon_owl_path():
    """Returns path to genuine local foodon.owl file."""
    p = Path("data/raw/ontology/foodon.owl")
    if not p.exists():
        pytest.skip("foodon.owl not found in local workspace")
    return p


def test_extract_records_from_genuine_foodon_sample(foodon_owl_path):
    """Tests streaming extraction on genuine FoodOn OWL ontology."""
    extractor = FoodonExtractor()
    batch = extractor.extract_records(
        owl_file_path=foodon_owl_path,
        raw_asset_id="AST-FOODON-TEST",
        max_records=50,
    )

    assert batch.source_id == "SRC-FOODON"
    assert len(batch.records) == 50
    assert batch.total_records_discovered >= 50
    assert batch.total_records_extracted > 0

    # Inspect first extracted record
    rec = batch.records[0]
    assert rec.source_id == "SRC-FOODON"
    assert rec.source_entity_type == "OWL_CLASS"
    assert rec.source_record_id.startswith("FOODON:") or ":" in rec.source_record_id
    assert "curie" in rec.original_fields
    assert "parent_iris" in rec.original_fields
    assert isinstance(rec.original_fields["parent_iris"], list)


def test_foodon_missing_file():
    """Verifies AssetNotFoundError when OWL file is missing."""
    extractor = FoodonExtractor()
    with pytest.raises(AssetNotFoundError):
        extractor.extract_records("data/non_existent.owl", raw_asset_id="AST-FAIL")


def test_foodon_corrupted_xml():
    """Verifies CorruptedAssetError on malformed XML content."""
    with tempfile.NamedTemporaryFile("w", suffix=".owl", delete=False, encoding="utf-8") as tmp:
        tmp.write("<?xml version='1.0'?><rdf:RDF><owl:Class>Unclosed tags")
        tmp_path = Path(tmp.name)

    try:
        extractor = FoodonExtractor()
        with pytest.raises(CorruptedAssetError):
            extractor.extract_records(tmp_path, raw_asset_id="AST-CORRUPT")
    finally:
        if tmp_path.exists():
            tmp_path.unlink()
