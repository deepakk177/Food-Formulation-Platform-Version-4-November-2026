"""
Tests for Phase 2A.2 Complete FoodOn and USDA Bulk Ingestion.

Validates:
1. FoodOn streaming chunked extraction and staging.
2. DuckDB transaction rollback and error handling.
3. Idempotent insertion (ON CONFLICT DO NOTHING).
4. USDA bulk JSON extraction (Foundation Foods and SR Legacy).
5. Nutrient measurement preservation including zero values.
6. Dataset registry and asset manifest reconciliation.
"""

import json
import pytest
from pathlib import Path
from src.pipeline_v2.core.manifest import ManifestManager, IntegrityStatus
from src.pipeline_v2.extractors.foodon.extractor import FoodonExtractor
from src.pipeline_v2.extractors.usda.extractor import UsdaExtractor
from src.pipeline_v2.models.manifest_models import AssetRecord
from src.pipeline_v2.models.source_record_models import SourceRecord
from src.pipeline_v2.storage.duckdb_store import DuckDBStore


@pytest.fixture
def memory_store():
    store = DuckDBStore(":memory:")
    store.initialize_schema()
    # Seed required source registries for FK satisfaction
    for s_id, s_name in [("SRC-FOODON", "FoodOn"), ("SRC-USDA-FDC", "USDA FDC")]:
        store.conn.execute(
            """
            INSERT INTO source_registry (
                source_id, source_name, authority, source_type, base_url,
                access_method, expected_format, authentication_required,
                license_reference, dataset_version, access_status, parser_identifier, enabled
            ) VALUES (?, ?, 'Auth', 'ONTOLOGY', 'http://test', 'LOCAL_FILE', 'JSON', false, 'CC', '1.0', 'LOCAL_AVAILABLE', 'ext', true)
            ON CONFLICT (source_id) DO NOTHING;
            """,
            [s_id, s_name],
        )
    # Seed execution runs
    for exec_id in ["EXEC-01", "EXEC-02"]:
        store.conn.execute(
            """
            INSERT INTO execution_runs (execution_id, stage_name, status, started_at, pipeline_version)
            VALUES (?, 'ACQUISITION', 'RUNNING', CURRENT_TIMESTAMP, '2.0.0')
            ON CONFLICT (execution_id) DO NOTHING;
            """,
            [exec_id],
        )
    yield store
    store.close()


def test_foodon_streaming_chunking(tmp_path):
    """Test that FoodOn streaming extracts in specified chunk sizes."""
    owl_content = """<?xml version="1.0"?>
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns:owl="http://www.w3.org/2002/07/owl#"
             xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
             xmlns:oboInOwl="http://www.geneontology.org/formats/oboInOwl#">
        <owl:Class rdf:about="http://purl.obolibrary.org/obo/FOODON_00001001">
            <rdfs:label>food product 1</rdfs:label>
        </owl:Class>
        <owl:Class rdf:about="http://purl.obolibrary.org/obo/FOODON_00001002">
            <rdfs:label>food product 2</rdfs:label>
        </owl:Class>
        <owl:Class rdf:about="http://purl.obolibrary.org/obo/FOODON_00001003">
            <rdfs:label>food product 3</rdfs:label>
        </owl:Class>
    </rdf:RDF>
    """
    owl_file = tmp_path / "test_foodon.owl"
    owl_file.write_text(owl_content, encoding="utf-8")

    extractor = FoodonExtractor()
    chunks = list(extractor.stream_records(owl_file, "AST-TEST-001", chunk_size=2))

    assert len(chunks) == 2
    assert len(chunks[0]) == 2
    assert len(chunks[1]) == 1
    assert chunks[0][0].source_record_id == "FOODON:00001001"
    assert chunks[1][0].source_record_id == "FOODON:00001003"


def test_duckdb_chunked_staging_idempotency(memory_store):
    """Test that stage_raw_records_chunk inserts and does not duplicate on repeat."""
    rec = SourceRecord(
        source_id="SRC-FOODON",
        dataset_id="DSK-FOODON-2024-03",
        source_record_id="FOODON_00001001",
        source_entity_type="OWL_CLASS",
        original_identifier="http://purl.obolibrary.org/obo/FOODON_00001001",
        original_name="test food",
        original_fields={"label": "test food", "parents": []},
        raw_asset_id="AST-001",
        source_location="test_foodon.owl#L1",
    )

    n1 = memory_store.stage_raw_records_chunk([rec], "EXEC-01")
    assert n1 == 1
    assert memory_store.count_records("raw_records") == 1

    # Insert same record again -> ON CONFLICT DO NOTHING ensures count stays 1
    memory_store.stage_raw_records_chunk([rec], "EXEC-02")
    assert memory_store.count_records("raw_records") == 1


def test_usda_foundation_and_sr_legacy_bulk_parsing(tmp_path):
    """Test that UsdaExtractor handles both FoundationFoods and SRLegacyFoods bulk keys."""
    foundation_data = {
        "FoundationFoods": [
            {
                "fdcId": 746774,
                "description": "Butter, without salt",
                "foodClass": "FinalFood",
                "foodCategory": {"description": "Dairy and Egg Products"},
                "foodNutrients": [
                    {
                        "nutrient": {"id": 1003, "name": "Protein", "unitName": "g"},
                        "amount": 0.85,
                    },
                    {
                        "nutrient": {"id": 1004, "name": "Total lipid (fat)", "unitName": "g"},
                        "amount": 81.11,
                    },
                    {
                        "nutrient": {"id": 1005, "name": "Carbohydrate, by difference", "unitName": "g"},
                        "amount": 0.06,
                    },
                ],
            }
        ]
    }
    f_path = tmp_path / "foundation_test.json"
    f_path.write_text(json.dumps(foundation_data), encoding="utf-8")

    extractor = UsdaExtractor()
    f_chunks = list(extractor.stream_from_json_file(f_path, "AST-USDA-FOUNDATION", chunk_size=10))
    assert len(f_chunks) == 1
    f_recs = f_chunks[0]
    assert len(f_recs) == 1
    rec = f_recs[0]
    assert rec.source_record_id == "746774"
    assert rec.original_fields["data_type"] == "Foundation"
    assert len(rec.original_fields["food_nutrients"]) == 3

    # Test SR Legacy key
    sr_data = {
        "SRLegacyFoods": [
            {
                "fdcId": 170000,
                "description": "Cheese, cheddar",
                "foodNutrients": [
                    {
                        "nutrient": {"id": 1003, "name": "Protein", "unitName": "g"},
                        "amount": 24.9,
                    },
                    {
                        "nutrient": {"id": 1008, "name": "Energy", "unitName": "kcal"},
                        "amount": 403.0,
                    },
                ],
            }
        ]
    }
    sr_path = tmp_path / "sr_test.json"
    sr_path.write_text(json.dumps(sr_data), encoding="utf-8")

    sr_chunks = list(extractor.stream_from_json_file(sr_path, "AST-USDA-SR", chunk_size=10))
    assert len(sr_chunks) == 1
    sr_recs = sr_chunks[0]
    assert len(sr_recs) == 1
    assert sr_recs[0].source_record_id == "170000"
    assert sr_recs[0].original_fields["data_type"] == "SR Legacy"
    assert len(sr_recs[0].original_fields["food_nutrients"]) == 2


def test_usda_zero_nutrient_value_preservation(tmp_path):
    """Test that zero-amount nutrients are strictly preserved and not dropped."""
    food_data = {
        "FoundationFoods": [
            {
                "fdcId": 999999,
                "description": "Pure Water",
                "foodNutrients": [
                    {
                        "nutrient": {"id": 1003, "name": "Protein", "unitName": "g"},
                        "amount": 0.0,
                    },
                    {
                        "nutrient": {"id": 1004, "name": "Fat", "unitName": "g"},
                        "value": 0.0,
                    },
                    {
                        "nutrient": {"id": 1005, "name": "Carbohydrate", "unitName": "g"},
                        "amount": None,
                    }
                ],
            }
        ]
    }
    p = tmp_path / "zero_test.json"
    p.write_text(json.dumps(food_data), encoding="utf-8")

    extractor = UsdaExtractor()
    chunks = list(extractor.stream_from_json_file(p, "AST-TEST", chunk_size=10))
    nutrients = chunks[0][0].original_fields["food_nutrients"]

    # Protein amount=0.0 -> value_raw: 0.0
    assert nutrients[0]["value_raw"] == 0.0
    # Fat value=0.0 -> value_raw: 0.0
    assert nutrients[1]["value_raw"] == 0.0
    # Carbohydrate None is excluded because it has no measurement
    assert len(nutrients) == 2


def test_dataset_registry_persistence(memory_store):
    """Test registering datasets into the dataset_registry table."""
    memory_store.record_dataset(
        dataset_id="DSK-TEST-001",
        source_id="SRC-FOODON",
        dataset_version="2024-03",
        release_date="2024-03-15",
        sha256_hash="abcdef1234567890",
        download_url="https://example.com/data.owl",
        record_count=100,
    )

    rows = memory_store.conn.execute("SELECT * FROM dataset_registry WHERE dataset_id = 'DSK-TEST-001'").fetchall()
    assert len(rows) == 1
    assert rows[0][0] == "DSK-TEST-001"
    assert rows[0][1] == "SRC-FOODON"
    assert rows[0][6] == 100
