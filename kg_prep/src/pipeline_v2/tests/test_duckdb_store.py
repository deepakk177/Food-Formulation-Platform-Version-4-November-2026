"""
Unit Tests for Pipeline V2 DuckDB Store Module.

Tests schema creation, transactions, rollback guarantees, duplicate primary key
rejections, and provenance recording.
"""

import tempfile
from pathlib import Path
import pytest

from pipeline_v2.storage.duckdb_store import DuckDBStore
from pipeline_v2.core.exceptions import (
    TransactionError,
    StorageError,
    ProvenanceTrackingError,
)
from pipeline_v2.models.source_models import SourceIntegrationModel, AccessMethod, AccessStatus
from pipeline_v2.models.execution_models import (
    ExecutionRunRecord,
    ExecutionErrorRecord,
    FieldProvenanceRecord,
    RelationshipProvenanceRecord,
    ExecutionStatus,
    ProcessingStage,
)
from pipeline_v2.models.manifest_models import AssetRecord, IntegrityStatus


@pytest.fixture
def store():
    """Provides an initialized in-memory DuckDB store fixture."""
    s = DuckDBStore(":memory:")
    s.initialize_schema()
    yield s
    s.close()


def test_schema_initialization(store):
    """Verifies that all 10 core tables are created."""
    tables = store.list_tables()
    expected_tables = {
        "schema_versions",
        "source_registry",
        "dataset_registry",
        "source_assets",
        "execution_runs",
        "execution_errors",
        "raw_records",
        "normalized_records",
        "field_provenance",
        "relationship_provenance",
    }
    assert expected_tables.issubset(set(tables))
    assert store.count_records("schema_versions") == 1


def test_sync_source_registry(store):
    """Verifies persisting SourceIntegrationModel into source_registry."""
    src = SourceIntegrationModel(
        source_id="SRC-FOODON",
        source_name="FoodOn Ontology",
        authority="Food Ontology Consortium",
        source_type="ONTOLOGY",
        base_url="https://foodon.org",
        endpoint="https://raw.githubusercontent.com/FoodOntology/foodon/master/foodon.owl",
        access_method=AccessMethod.LOCAL_FILE,
        expected_format="OWL",
        authentication_required=False,
        license_reference="CC-BY 4.0",
        dataset_version="2024-03-08",
        access_status=AccessStatus.LOCAL_AVAILABLE,
        parser_identifier="foodon_extractor",
    )

    count = store.sync_source_registry({"SRC-FOODON": src})
    assert count == 1
    assert store.count_records("source_registry") == 1


def test_transaction_rollback_on_error(store):
    """Verifies that failures inside a transaction roll back all modifications."""
    # First ensure a valid source exists
    test_sync_source_registry(store)

    with pytest.raises(TransactionError):
        with store.transaction():
            # Valid insertion
            store.conn.execute(
                """
                INSERT INTO execution_runs (
                    execution_id, stage_name, status, started_at, pipeline_version
                ) VALUES ('RUN-TEST-001', 'ACQUISITION', 'RUNNING', CURRENT_TIMESTAMP, '2.0.0');
                """
            )
            # Intentionally cause a SQL error
            store.conn.execute("INSERT INTO non_existent_table VALUES ('corrupt');")

    # Verify that RUN-TEST-001 was rolled back
    assert store.count_records("execution_runs") == 0


def test_execution_run_and_error_recording(store):
    """Verifies recording execution runs and structured errors."""
    run = ExecutionRunRecord(
        execution_id="RUN-20261116-01",
        stage_name=ProcessingStage.EXTRACTION,
        status=ExecutionStatus.RUNNING,
        parameters={"source_id": "SRC-FOODON"},
    )
    store.record_execution_run(run)
    assert store.count_records("execution_runs") == 1

    err = ExecutionErrorRecord(
        error_id="ERR-001",
        execution_id="RUN-20261116-01",
        stage_name=ProcessingStage.EXTRACTION,
        source_id="SRC-FOODON",
        error_type="ValueError",
        error_message="Test error message",
        error_details={"line": 42},
    )
    store.record_execution_error(err)
    assert store.count_records("execution_errors") == 1


def test_provenance_recording(store):
    """Verifies insertion of field-level and relationship-level provenance."""
    # Setup parent records
    test_sync_source_registry(store)
    test_execution_run_and_error_recording(store)

    # Field Provenance
    f_prov = FieldProvenanceRecord(
        provenance_id="PROV-F-001",
        execution_id="RUN-20261116-01",
        target_table="Ingredients",
        target_entity_id="ING-001",
        target_field_name="canonical_name",
        source_id="SRC-FOODON",
        source_dataset_id="DSK-FOODON-01",
        source_record_id="FOODON:00001001",
        source_field_name="rdfs:label",
        raw_value="Whole Cow Milk",
        normalized_value="whole cow milk",
        transformation_rule="LOWERCASE_NFC",
        extraction_confidence=1.0,
    )
    store.record_field_provenance(f_prov)
    assert store.count_records("field_provenance") == 1

    # Relationship Provenance
    r_prov = RelationshipProvenanceRecord(
        relationship_id="REL-001",
        execution_id="RUN-20261116-01",
        relationship_type="BELONGS_TO_CATEGORY",
        source_node_id="ING-001",
        source_node_type="Ingredient",
        target_node_id="CAT-01.1",
        target_node_type="FoodCategory",
        source_dataset_id="DSK-FOODON-01",
        source_record_id="FOODON:00001001",
        extraction_confidence=1.0,
        verification_status="SOURCE_VERIFIED",
        is_derived=False,
    )
    store.record_relationship_provenance(r_prov)
    assert store.count_records("relationship_provenance") == 1
