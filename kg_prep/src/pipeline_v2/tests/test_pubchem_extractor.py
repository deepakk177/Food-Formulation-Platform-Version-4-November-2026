"""
Unit Tests for Pipeline V2 PubChem Extractor Module.
"""

import json
import tempfile
from pathlib import Path
import pytest

from pipeline_v2.extractors.pubchem.extractor import PubChemExtractor
from pipeline_v2.core.exceptions import CorruptedAssetError, AssetNotFoundError
from pipeline_v2.models.source_record_models import ExtractionStatus


@pytest.fixture
def genuine_pubchem_sample_json():
    """Provides a temporary genuine PubChem compound payload fixture (Vanillin & Caffeine)."""
    data = {
        "PropertyTable": {
            "Properties": [
                {
                    "CID": 1183,
                    "MolecularFormula": "C8H8O3",
                    "MolecularWeight": "152.15",
                    "CanonicalSMILES": "COC1=C(C=CC(=C1)C=O)O",
                    "InChI": "InChI=1S/C8H8O3/c1-11-8-4-6(5-9)2-3-7(8)10/h2-5,10H,1H3",
                    "InChIKey": "MWOOGOJBHIARFG-UHFFFAOYSA-N",
                    "IUPACName": "4-hydroxy-3-methoxybenzaldehyde",
                },
                {
                    "CID": 2519,
                    "MolecularFormula": "C8H10N4O2",
                    "MolecularWeight": "194.19",
                    "CanonicalSMILES": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
                    "InChIKey": "RYYVLZVUVIJVGH-UHFFFAOYSA-N",
                    "IUPACName": "1,3,7-trimethylpurine-2,6-dione",
                },
                {
                    "IUPACName": "Invalid Missing CID Compound",
                },
            ]
        },
        "Synonyms": ["Vanillin", "Vanilla", "4-Hydroxy-3-methoxybenzaldehyde"],
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
        json.dump(data, tmp)
        tmp_path = Path(tmp.name)
    yield tmp_path
    if tmp_path.exists():
        tmp_path.unlink()


def test_extract_valid_pubchem_compounds(genuine_pubchem_sample_json):
    """Verifies extraction of genuine PubChem compounds and properties."""
    extractor = PubChemExtractor()
    batch = extractor.extract_from_json_file(
        json_file_path=genuine_pubchem_sample_json,
        raw_asset_id="AST-PUBCHEM-TEST",
    )

    assert batch.source_id == "SRC-PUBCHEM"
    assert batch.total_records_discovered == 3
    assert batch.total_records_extracted == 2
    assert batch.total_records_rejected == 1

    # Verify Vanillin
    vanillin = [r for r in batch.records if r.source_record_id == "1183"][0]
    assert vanillin.source_entity_type == "COMPOUND"
    assert vanillin.original_name == "4-hydroxy-3-methoxybenzaldehyde"
    assert vanillin.original_fields["molecular_formula"] == "C8H8O3"
    assert vanillin.original_fields["molecular_weight"] == "152.15"
    assert vanillin.original_fields["inchi_key"] == "MWOOGOJBHIARFG-UHFFFAOYSA-N"
    assert "Vanillin" in vanillin.original_fields["synonyms"]

    # Verify Rejected (missing CID)
    assert len(batch.rejected_records) == 1
    rejected = batch.rejected_records[0]
    assert rejected.rejection_reason == "MISSING_PUBCHEM_CID"


def test_pubchem_missing_file():
    """Verifies AssetNotFoundError on missing file."""
    extractor = PubChemExtractor()
    with pytest.raises(AssetNotFoundError):
        extractor.extract_from_json_file("data/non_existent.json", "AST-FAIL")


def test_pubchem_corrupted_json():
    """Verifies CorruptedAssetError on corrupted JSON payload."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
        tmp.write("invalid json stream")
        tmp_path = Path(tmp.name)

    try:
        extractor = PubChemExtractor()
        with pytest.raises(CorruptedAssetError):
            extractor.extract_from_json_file(tmp_path, "AST-CORRUPT")
    finally:
        if tmp_path.exists():
            tmp_path.unlink()
