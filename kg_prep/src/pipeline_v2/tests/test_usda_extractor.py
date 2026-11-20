"""
Unit Tests for Pipeline V2 USDA FoodData Central Extractor Module.
"""

import json
import tempfile
from pathlib import Path
import pytest

from pipeline_v2.extractors.usda.extractor import UsdaExtractor
from pipeline_v2.core.exceptions import CorruptedAssetError, AssetNotFoundError
from pipeline_v2.models.source_record_models import ExtractionStatus


@pytest.fixture
def genuine_usda_sample_json():
    """Provides a temporary genuine USDA FDC sample JSON fixture."""
    data = {
        "foods": [
            {
                "fdcId": 167512,
                "description": "Milk, whole, 3.25% milkfat",
                "dataType": "Foundation",
                "publicationDate": "2020-10-30",
                "foodCategory": "Dairy and Egg Products",
                "foodNutrients": [
                    {
                        "nutrientId": 1003,
                        "nutrientName": "Protein",
                        "value": 3.15,
                        "unitName": "G",
                        "derivationCode": "A",
                    },
                    {
                        "nutrientId": 1004,
                        "nutrientName": "Total lipid (fat)",
                        "value": 3.25,
                        "unitName": "G",
                        "derivationCode": "A",
                    },
                ],
                "foodPortions": [
                    {"amount": 1.0, "modifier": "cup", "gramWeight": 244.0}
                ],
            },
            {
                "fdcId": 174980,
                "description": "Crackers, milk",
                "dataType": "SR Legacy",
                "publicationDate": "2019-04-01",
                "foodNutrients": [
                    {"nutrientId": 1008, "nutrientName": "Energy", "value": 433.0, "unitName": "KCAL"}
                ],
            },
            {
                "fdcId": 2428039,
                "description": "BRANDED CHEDDAR CHEESE",
                "dataType": "Branded",
                "publicationDate": "2023-01-15",
                "foodNutrients": [{"nutrientId": 1003, "nutrientName": "Protein", "value": 25.0}],
            },
        ]
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
        json.dump(data, tmp)
        tmp_path = Path(tmp.name)
    yield tmp_path
    if tmp_path.exists():
        tmp_path.unlink()


def test_extract_valid_foundation_and_sr_legacy(genuine_usda_sample_json):
    """Verifies that Foundation and SR Legacy foods are extracted and Branded foods are rejected."""
    extractor = UsdaExtractor()
    batch = extractor.extract_from_json_file(
        json_file_path=genuine_usda_sample_json,
        raw_asset_id="AST-USDA-TEST",
    )

    assert batch.source_id == "SRC-USDA-FDC"
    assert batch.total_records_discovered == 3
    assert batch.total_records_extracted == 2
    assert batch.total_records_rejected == 1

    # Verify extracted records (Milk & Crackers)
    extracted_ids = [r.source_record_id for r in batch.records]
    assert "167512" in extracted_ids
    assert "174980" in extracted_ids

    # Verify rejected record (Branded Cheddar)
    assert len(batch.rejected_records) == 1
    rejected = batch.rejected_records[0]
    assert rejected.source_record_id == "2428039"
    assert "OUT_OF_SCOPE_DATA_TYPE:Branded" in rejected.rejection_reason


def test_usda_nutrient_preservation(genuine_usda_sample_json):
    """Verifies that nutrient lists retain native values, units, and derivations without alteration."""
    extractor = UsdaExtractor()
    batch = extractor.extract_from_json_file(genuine_usda_sample_json, "AST-USDA-TEST")

    milk_rec = [r for r in batch.records if r.source_record_id == "167512"][0]
    nutrients = milk_rec.original_fields["food_nutrients"]
    assert len(nutrients) == 2

    protein = [n for n in nutrients if n["nutrient_id"] == 1003][0]
    assert protein["nutrient_name"] == "Protein"
    assert protein["value_raw"] == 3.15
    assert protein["unit_raw"] == "G"


def test_usda_missing_file():
    """Verifies AssetNotFoundError on missing file."""
    extractor = UsdaExtractor()
    with pytest.raises(AssetNotFoundError):
        extractor.extract_from_json_file("data/non_existent.json", "AST-FAIL")


def test_usda_corrupted_json():
    """Verifies CorruptedAssetError on malformed JSON file."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
        tmp.write("{malformed_json: true, unquoted")
        tmp_path = Path(tmp.name)

    try:
        extractor = UsdaExtractor()
        with pytest.raises(CorruptedAssetError):
            extractor.extract_from_json_file(tmp_path, "AST-CORRUPT")
    finally:
        if tmp_path.exists():
            tmp_path.unlink()
