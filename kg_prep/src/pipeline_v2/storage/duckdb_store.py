"""
Pipeline V2 DuckDB Provenance and Relational Storage Module.

Provides relational staging, execution tracking, and fine-grained field-level and
relationship-level provenance tracking using DuckDB.

Supports:
- ACID transactions with explicit commit and rollback
- 10 versioned core staging and provenance tables
- Primary key constraints and indexing
- Zero synthetic data generation
"""

import json
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Generator

import duckdb

from pipeline_v2.core.exceptions import (
    DatabaseInitializationError,
    StorageError,
    DuplicateRecordError,
    TransactionError,
    ProvenanceTrackingError,
)
from pipeline_v2.models.execution_models import (
    ExecutionRunRecord,
    ExecutionErrorRecord,
    FieldProvenanceRecord,
    RelationshipProvenanceRecord,
    ExecutionStatus,
    ProcessingStage,
)
from pipeline_v2.models.manifest_models import AssetRecord
from pipeline_v2.models.source_models import SourceIntegrationModel


class DuckDBStore:
    """Manages DuckDB connection, table creation, and provenance persistence."""

    SCHEMA_VERSION = "2.0.0"

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        if db_path != ":memory:":
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        try:
            self.conn = duckdb.connect(self.db_path)
        except Exception as e:
            raise DatabaseInitializationError(f"Failed to connect to DuckDB at {db_path}: {e}")

    def initialize_schema(self) -> None:
        """Initializes all 10 core relational tables and indices."""
        try:
            with self.transaction():
                # 1. Schema Versions
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS schema_versions (
                        version_id VARCHAR PRIMARY KEY,
                        installed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        description VARCHAR
                    );
                """)

                # 2. Source Registry
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS source_registry (
                        source_id VARCHAR PRIMARY KEY,
                        source_name VARCHAR NOT NULL,
                        authority VARCHAR NOT NULL,
                        source_type VARCHAR NOT NULL,
                        base_url VARCHAR NOT NULL,
                        endpoint VARCHAR,
                        access_method VARCHAR NOT NULL,
                        expected_format VARCHAR NOT NULL,
                        authentication_required BOOLEAN NOT NULL,
                        license_reference VARCHAR NOT NULL,
                        dataset_version VARCHAR,
                        enabled BOOLEAN NOT NULL,
                        access_status VARCHAR NOT NULL,
                        parser_identifier VARCHAR NOT NULL,
                        notes VARCHAR,
                        registered_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # 3. Dataset Registry
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS dataset_registry (
                        dataset_id VARCHAR PRIMARY KEY,
                        source_id VARCHAR NOT NULL REFERENCES source_registry(source_id),
                        dataset_version VARCHAR NOT NULL,
                        release_date VARCHAR,
                        sha256_hash VARCHAR,
                        download_url VARCHAR,
                        record_count BIGINT,
                        registered_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # 4. Source Assets
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS source_assets (
                        asset_id VARCHAR PRIMARY KEY,
                        source_id VARCHAR NOT NULL REFERENCES source_registry(source_id),
                        dataset_id VARCHAR NOT NULL,
                        original_filename VARCHAR NOT NULL,
                        local_path VARCHAR NOT NULL,
                        source_url VARCHAR NOT NULL,
                        dataset_version VARCHAR NOT NULL,
                        downloaded_at TIMESTAMP WITH TIME ZONE NOT NULL,
                        file_size_bytes BIGINT NOT NULL,
                        sha256 VARCHAR(64) NOT NULL,
                        content_type VARCHAR NOT NULL,
                        access_status VARCHAR NOT NULL,
                        integrity_status VARCHAR NOT NULL,
                        metadata_json JSON
                    );
                """)

                # 5. Execution Runs
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS execution_runs (
                        execution_id VARCHAR PRIMARY KEY,
                        stage_name VARCHAR NOT NULL,
                        status VARCHAR NOT NULL,
                        started_at TIMESTAMP WITH TIME ZONE NOT NULL,
                        completed_at TIMESTAMP WITH TIME ZONE,
                        total_records_processed BIGINT DEFAULT 0,
                        total_records_failed BIGINT DEFAULT 0,
                        pipeline_version VARCHAR NOT NULL,
                        parameters_json JSON,
                        summary_metrics_json JSON
                    );
                """)

                # 6. Execution Errors
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS execution_errors (
                        error_id VARCHAR PRIMARY KEY,
                        execution_id VARCHAR NOT NULL REFERENCES execution_runs(execution_id),
                        stage_name VARCHAR NOT NULL,
                        source_id VARCHAR,
                        record_identifier VARCHAR,
                        error_type VARCHAR NOT NULL,
                        error_message VARCHAR NOT NULL,
                        error_details_json JSON,
                        occurred_at TIMESTAMP WITH TIME ZONE NOT NULL
                    );
                """)

                # 7. Raw Records (Staging)
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS raw_records (
                        raw_record_id VARCHAR PRIMARY KEY,
                        source_id VARCHAR NOT NULL REFERENCES source_registry(source_id),
                        dataset_id VARCHAR NOT NULL,
                        native_record_id VARCHAR NOT NULL,
                        asset_id VARCHAR NOT NULL,
                        payload_json JSON NOT NULL,
                        extracted_at TIMESTAMP WITH TIME ZONE NOT NULL,
                        execution_id VARCHAR NOT NULL REFERENCES execution_runs(execution_id)
                    );
                """)

                # 8. Normalized Records (Intermediate)
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS normalized_records (
                        normalized_record_id VARCHAR PRIMARY KEY,
                        raw_record_id VARCHAR NOT NULL REFERENCES raw_records(raw_record_id),
                        target_entity_type VARCHAR NOT NULL,
                        canonical_entity_id VARCHAR NOT NULL,
                        normalized_payload_json JSON NOT NULL,
                        normalization_status VARCHAR NOT NULL,
                        normalized_at TIMESTAMP WITH TIME ZONE NOT NULL,
                        execution_id VARCHAR NOT NULL REFERENCES execution_runs(execution_id)
                    );
                """)

                # 9. Field Provenance
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS field_provenance (
                        provenance_id VARCHAR PRIMARY KEY,
                        execution_id VARCHAR NOT NULL REFERENCES execution_runs(execution_id),
                        target_table VARCHAR NOT NULL,
                        target_entity_id VARCHAR NOT NULL,
                        target_field_name VARCHAR NOT NULL,
                        source_id VARCHAR NOT NULL REFERENCES source_registry(source_id),
                        source_dataset_id VARCHAR NOT NULL,
                        source_record_id VARCHAR NOT NULL,
                        source_field_name VARCHAR NOT NULL,
                        raw_value VARCHAR,
                        normalized_value VARCHAR,
                        transformation_rule VARCHAR,
                        extraction_confidence DOUBLE NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE NOT NULL
                    );
                """)

                # 10. Relationship Provenance
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS relationship_provenance (
                        relationship_id VARCHAR PRIMARY KEY,
                        execution_id VARCHAR NOT NULL REFERENCES execution_runs(execution_id),
                        relationship_type VARCHAR NOT NULL,
                        source_node_id VARCHAR NOT NULL,
                        source_node_type VARCHAR NOT NULL,
                        target_node_id VARCHAR NOT NULL,
                        target_node_type VARCHAR NOT NULL,
                        source_dataset_id VARCHAR NOT NULL,
                        source_record_id VARCHAR NOT NULL,
                        extraction_confidence DOUBLE NOT NULL,
                        evidence_id VARCHAR,
                        verification_status VARCHAR NOT NULL,
                        is_derived BOOLEAN NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE NOT NULL
                    );
                """)

                # Register Schema Version
                self.conn.execute(
                    """
                    INSERT INTO schema_versions (version_id, installed_at, description)
                    VALUES (?, CURRENT_TIMESTAMP, ?)
                    ON CONFLICT (version_id) DO NOTHING;
                    """,
                    [self.SCHEMA_VERSION, "Pipeline V2 Initial Relational Schema"],
                )
        except Exception as e:
            raise DatabaseInitializationError(f"Database schema initialization failed: {e}")

    @contextmanager
    def transaction(self) -> Generator[duckdb.DuckDBPyConnection, None, None]:
        """Provides transaction management with automatic rollback on error."""
        self.conn.execute("BEGIN TRANSACTION;")
        try:
            yield self.conn
            self.conn.execute("COMMIT;")
        except Exception as e:
            self.conn.execute("ROLLBACK;")
            raise TransactionError(f"Transaction aborted and rolled back: {e}")

    # --------------------------------------------------------------------------
    # Registry Synchronization
    # --------------------------------------------------------------------------
    def sync_source_registry(self, sources: Dict[str, SourceIntegrationModel]) -> int:
        """Synchronizes declarative source definitions into the database."""
        count = 0
        with self.transaction():
            for src in sources.values():
                self.conn.execute(
                    """
                    INSERT INTO source_registry (
                        source_id, source_name, authority, source_type, base_url,
                        endpoint, access_method, expected_format, authentication_required,
                        license_reference, dataset_version, enabled, access_status,
                        parser_identifier, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT (source_id) DO UPDATE SET
                        source_name = EXCLUDED.source_name,
                        authority = EXCLUDED.authority,
                        base_url = EXCLUDED.base_url,
                        endpoint = EXCLUDED.endpoint,
                        access_method = EXCLUDED.access_method,
                        expected_format = EXCLUDED.expected_format,
                        authentication_required = EXCLUDED.authentication_required,
                        license_reference = EXCLUDED.license_reference,
                        dataset_version = EXCLUDED.dataset_version,
                        enabled = EXCLUDED.enabled,
                        access_status = EXCLUDED.access_status,
                        parser_identifier = EXCLUDED.parser_identifier,
                        notes = EXCLUDED.notes;
                    """,
                    [
                        src.source_id,
                        src.source_name,
                        src.authority,
                        src.source_type,
                        src.base_url,
                        src.endpoint,
                        src.access_method.value,
                        src.expected_format,
                        src.authentication_required,
                        src.license_reference,
                        src.dataset_version,
                        src.enabled,
                        src.access_status.value,
                        src.parser_identifier,
                        src.notes,
                    ],
                )
                count += 1
        return count

    def record_dataset(
        self,
        dataset_id: str,
        source_id: str,
        dataset_version: str,
        release_date: Optional[str] = None,
        sha256_hash: Optional[str] = None,
        download_url: Optional[str] = None,
        record_count: Optional[int] = None,
    ) -> None:
        """Stores or updates a dataset registration record."""
        try:
            self.conn.execute(
                """
                INSERT INTO dataset_registry (
                    dataset_id, source_id, dataset_version, release_date,
                    sha256_hash, download_url, record_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (dataset_id) DO UPDATE SET
                    dataset_version = EXCLUDED.dataset_version,
                    release_date = EXCLUDED.release_date,
                    sha256_hash = EXCLUDED.sha256_hash,
                    download_url = EXCLUDED.download_url,
                    record_count = EXCLUDED.record_count;
                """,
                [dataset_id, source_id, dataset_version, release_date, sha256_hash, download_url, record_count],
            )
        except Exception as e:
            raise StorageError(f"Failed to record dataset '{dataset_id}': {e}")

    # --------------------------------------------------------------------------
    # Asset Management
    # --------------------------------------------------------------------------
    def record_asset(self, asset: AssetRecord) -> None:
        """Stores or updates an acquired asset record."""
        try:
            self.conn.execute(
                """
                INSERT INTO source_assets (
                    asset_id, source_id, dataset_id, original_filename, local_path,
                    source_url, dataset_version, downloaded_at, file_size_bytes,
                    sha256, content_type, access_status, integrity_status, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (asset_id) DO UPDATE SET
                    integrity_status = EXCLUDED.integrity_status,
                    file_size_bytes = EXCLUDED.file_size_bytes,
                    sha256 = EXCLUDED.sha256,
                    metadata_json = EXCLUDED.metadata_json;
                """,
                [
                    asset.asset_id,
                    asset.source_id,
                    asset.dataset_id,
                    asset.original_filename,
                    asset.local_path,
                    asset.source_url,
                    asset.dataset_version,
                    asset.downloaded_at,
                    asset.file_size_bytes,
                    asset.sha256,
                    asset.content_type,
                    asset.access_status,
                    asset.integrity_status.value,
                    json.dumps(asset.metadata),
                ],
            )
        except Exception as e:
            raise StorageError(f"Failed to record asset '{asset.asset_id}': {e}")

    # --------------------------------------------------------------------------
    # Execution Tracking
    # --------------------------------------------------------------------------
    def record_execution_run(self, run: ExecutionRunRecord) -> None:
        """Records the start or update of an execution run."""
        try:
            self.conn.execute(
                """
                INSERT INTO execution_runs (
                    execution_id, stage_name, status, started_at, completed_at,
                    total_records_processed, total_records_failed, pipeline_version,
                    parameters_json, summary_metrics_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (execution_id) DO UPDATE SET
                    status = EXCLUDED.status,
                    completed_at = EXCLUDED.completed_at,
                    total_records_processed = EXCLUDED.total_records_processed,
                    total_records_failed = EXCLUDED.total_records_failed,
                    summary_metrics_json = EXCLUDED.summary_metrics_json;
                """,
                [
                    run.execution_id,
                    run.stage_name.value,
                    run.status.value,
                    run.started_at,
                    run.completed_at,
                    run.total_records_processed,
                    run.total_records_failed,
                    run.pipeline_version,
                    json.dumps(run.parameters),
                    json.dumps(run.summary_metrics),
                ],
            )
        except Exception as e:
            raise StorageError(f"Failed to record execution run '{run.execution_id}': {e}")

    def record_execution_error(self, err: ExecutionErrorRecord) -> None:
        """Records a structured error during execution."""
        try:
            self.conn.execute(
                """
                INSERT INTO execution_errors (
                    error_id, execution_id, stage_name, source_id, record_identifier,
                    error_type, error_message, error_details_json, occurred_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (error_id) DO NOTHING;
                """,
                [
                    err.error_id,
                    err.execution_id,
                    err.stage_name.value,
                    err.source_id,
                    err.record_identifier,
                    err.error_type,
                    err.error_message,
                    json.dumps(err.error_details),
                    err.occurred_at,
                ],
            )
        except Exception as e:
            raise StorageError(f"Failed to record execution error '{err.error_id}': {e}")

    # --------------------------------------------------------------------------
    # Provenance Tracking
    # --------------------------------------------------------------------------
    def record_field_provenance(self, prov: FieldProvenanceRecord) -> None:
        """Inserts a single field provenance lineage record."""
        try:
            self.conn.execute(
                """
                INSERT INTO field_provenance (
                    provenance_id, execution_id, target_table, target_entity_id,
                    target_field_name, source_id, source_dataset_id, source_record_id,
                    source_field_name, raw_value, normalized_value, transformation_rule,
                    extraction_confidence, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (provenance_id) DO NOTHING;
                """,
                [
                    prov.provenance_id,
                    prov.execution_id,
                    prov.target_table,
                    prov.target_entity_id,
                    prov.target_field_name,
                    prov.source_id,
                    prov.source_dataset_id,
                    prov.source_record_id,
                    prov.source_field_name,
                    prov.raw_value,
                    prov.normalized_value,
                    prov.transformation_rule,
                    prov.extraction_confidence,
                    prov.created_at,
                ],
            )
        except Exception as e:
            raise ProvenanceTrackingError(f"Failed to record field provenance: {e}")

    def record_relationship_provenance(self, rel: RelationshipProvenanceRecord) -> None:
        """Inserts a single relationship provenance record."""
        try:
            self.conn.execute(
                """
                INSERT INTO relationship_provenance (
                    relationship_id, execution_id, relationship_type, source_node_id,
                    source_node_type, target_node_id, target_node_type, source_dataset_id,
                    source_record_id, extraction_confidence, evidence_id, verification_status,
                    is_derived, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (relationship_id) DO NOTHING;
                """,
                [
                    rel.relationship_id,
                    rel.execution_id,
                    rel.relationship_type,
                    rel.source_node_id,
                    rel.source_node_type,
                    rel.target_node_id,
                    rel.target_node_type,
                    rel.source_dataset_id,
                    rel.source_record_id,
                    rel.extraction_confidence,
                    rel.evidence_id,
                    rel.verification_status,
                    rel.is_derived,
                    rel.created_at,
                ],
            )
        except Exception as e:
            raise ProvenanceTrackingError(f"Failed to record relationship provenance: {e}")

    # --------------------------------------------------------------------------
    # Queries & Table Inspection
    # --------------------------------------------------------------------------
    def list_tables(self) -> List[str]:
        """Returns names of all non-system tables in the database."""
        result = self.conn.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='main' ORDER BY table_name;"
        ).fetchall()
        return [row[0] for row in result]

    def count_records(self, table_name: str) -> int:
        """Returns row count for a given table."""
        # Whitelist check against existing tables to prevent injection
        tables = self.list_tables()
        if table_name not in tables:
            raise StorageError(f"Table '{table_name}' does not exist.")
        result = self.conn.execute(f"SELECT COUNT(*) FROM {table_name};").fetchone()
        return result[0] if result else 0

    def stage_raw_records_chunk(
        self,
        records: List[Any],
        execution_id: str,
    ) -> int:
        """
        Stages a chunk of SourceRecord objects into raw_records inside a transaction.
        Idempotent: uses ON CONFLICT (raw_record_id) DO NOTHING.
        Returns the number of records processed.
        """
        if not records:
            return 0

        try:
            import pyarrow as pa
            has_pyarrow = True
        except ImportError:
            has_pyarrow = False

        if has_pyarrow:
            raw_record_ids = [f"{r.source_id}:{r.source_record_id}" for r in records]
            source_ids = [r.source_id for r in records]
            dataset_ids = [r.dataset_id for r in records]
            native_ids = [r.source_record_id for r in records]
            asset_ids = [r.raw_asset_id for r in records]
            payloads = [
                json.dumps(r.original_fields) if isinstance(r.original_fields, dict) else str(r.original_fields)
                for r in records
            ]
            extracted_ats = [r.extraction_timestamp for r in records]
            exec_ids = [execution_id] * len(records)

            arrow_table = pa.Table.from_arrays(
                [
                    pa.array(raw_record_ids),
                    pa.array(source_ids),
                    pa.array(dataset_ids),
                    pa.array(native_ids),
                    pa.array(asset_ids),
                    pa.array(payloads),
                    pa.array(extracted_ats),
                    pa.array(exec_ids),
                ],
                names=[
                    "raw_record_id",
                    "source_id",
                    "dataset_id",
                    "native_record_id",
                    "asset_id",
                    "payload_json",
                    "extracted_at",
                    "execution_id",
                ],
            )

            with self.transaction():
                self.conn.execute(
                    """
                    INSERT INTO raw_records
                    SELECT * FROM arrow_table
                    ON CONFLICT (raw_record_id) DO NOTHING;
                    """
                )
        else:
            tuples = [
                (
                    f"{r.source_id}:{r.source_record_id}",
                    r.source_id,
                    r.dataset_id,
                    r.source_record_id,
                    r.raw_asset_id,
                    json.dumps(r.original_fields),
                    r.extraction_timestamp,
                    execution_id,
                )
                for r in records
            ]

            with self.transaction():
                self.conn.executemany(
                    """
                    INSERT INTO raw_records (
                        raw_record_id, source_id, dataset_id, native_record_id,
                        asset_id, payload_json, extracted_at, execution_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT (raw_record_id) DO NOTHING;
                    """,
                    tuples,
                )
        return len(records)

    def close(self) -> None:
        """Closes the DuckDB connection."""
        self.conn.close()

    def __enter__(self) -> "DuckDBStore":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
