import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

try:
    import duckdb
except ImportError:
    duckdb = None

logger = logging.getLogger("GroundedDB")

class GroundedDatabaseEngine:
    """
    Analytical Grounded Database engine using DuckDB.
    Maintains immutable raw payloads, normalized records, field-level provenance,
    conflict logs, rejection logs, and pipeline execution manifests.
    """
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path).resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None

    def connect(self):
        if duckdb is None:
            logger.warning("DuckDB is not installed. Grounded DB operations falling back to memory/JSON mode.")
            return False
        try:
            self.conn = duckdb.connect(str(self.db_path))
            try:
                self.conn.execute("SET max_memory = '1GB'")
            except Exception:
                pass
            self._init_schema()
            logger.info(f"Connected to Grounded DuckDB at {self.db_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to DuckDB at {self.db_path}: {e}")
            return False

    def close(self):
        if self.conn:
            try:
                self.conn.execute("CHECKPOINT")
            except Exception:
                pass
            self.conn.close()
            self.conn = None
            logger.info("Closed Grounded DuckDB connection.")

    def _init_schema(self):
        """Initializes tables for grounded data validation, audit, and traceability."""
        if not self.conn:
            return

        tables = {
            "datasets": """
                CREATE TABLE IF NOT EXISTS datasets (
                    dataset_id VARCHAR PRIMARY KEY,
                    dataset_name VARCHAR,
                    provider VARCHAR,
                    version VARCHAR,
                    release_date VARCHAR,
                    source_url VARCHAR,
                    download_url VARCHAR,
                    license VARCHAR,
                    acquired_at VARCHAR,
                    sha256 VARCHAR,
                    record_count INTEGER,
                    status VARCHAR
                )
            """,
            "source_files": """
                CREATE TABLE IF NOT EXISTS source_files (
                    file_id VARCHAR PRIMARY KEY,
                    dataset_id VARCHAR,
                    filename VARCHAR,
                    relative_path VARCHAR,
                    file_format VARCHAR,
                    file_size BIGINT,
                    sha256 VARCHAR,
                    download_timestamp VARCHAR
                )
            """,
            "raw_records": """
                CREATE TABLE IF NOT EXISTS raw_records (
                    raw_record_id VARCHAR PRIMARY KEY,
                    dataset_id VARCHAR,
                    file_id VARCHAR,
                    source_record_id VARCHAR,
                    raw_payload VARCHAR,
                    record_hash VARCHAR
                )
            """,
            "normalized_records": """
                CREATE TABLE IF NOT EXISTS normalized_records (
                    normalized_record_id VARCHAR PRIMARY KEY,
                    raw_record_id VARCHAR,
                    entity_type VARCHAR,
                    canonical_id VARCHAR,
                    normalized_payload VARCHAR,
                    normalization_version VARCHAR
                )
            """,
            "entity_mappings": """
                CREATE TABLE IF NOT EXISTS entity_mappings (
                    mapping_id VARCHAR PRIMARY KEY,
                    source_dataset_id VARCHAR,
                    source_record_id VARCHAR,
                    canonical_id VARCHAR,
                    matching_method VARCHAR,
                    matching_score DOUBLE,
                    validation_status VARCHAR,
                    evidence VARCHAR
                )
            """,
            "relationships": """
                CREATE TABLE IF NOT EXISTS relationships (
                    relationship_id VARCHAR PRIMARY KEY,
                    source_id VARCHAR,
                    relationship_type VARCHAR,
                    target_id VARCHAR,
                    dataset_id VARCHAR,
                    source_record_id VARCHAR,
                    relationship_classification VARCHAR,
                    evidence VARCHAR
                )
            """,
            "provenance": """
                CREATE TABLE IF NOT EXISTS provenance (
                    provenance_id VARCHAR PRIMARY KEY,
                    entity_id VARCHAR,
                    field_name VARCHAR,
                    source_dataset_id VARCHAR,
                    source_record_id VARCHAR,
                    source_file VARCHAR,
                    source_location VARCHAR,
                    transformation VARCHAR,
                    transformation_version VARCHAR
                )
            """,
            "conflicts": """
                CREATE TABLE IF NOT EXISTS conflicts (
                    conflict_id VARCHAR PRIMARY KEY,
                    entity_id VARCHAR,
                    field_name VARCHAR,
                    source_dataset_a VARCHAR,
                    value_a VARCHAR,
                    source_dataset_b VARCHAR,
                    value_b VARCHAR,
                    conflict_type VARCHAR,
                    resolution_status VARCHAR
                )
            """,
            "rejected_records": """
                CREATE TABLE IF NOT EXISTS rejected_records (
                    rejection_id VARCHAR PRIMARY KEY,
                    dataset_id VARCHAR,
                    source_record_id VARCHAR,
                    rejection_reason VARCHAR,
                    raw_payload VARCHAR,
                    timestamp VARCHAR
                )
            """,
            "pipeline_runs": """
                CREATE TABLE IF NOT EXISTS pipeline_runs (
                    run_id VARCHAR PRIMARY KEY,
                    timestamp VARCHAR,
                    git_commit VARCHAR,
                    pipeline_version VARCHAR,
                    dataset_versions VARCHAR,
                    files_processed INTEGER,
                    records_processed INTEGER,
                    records_rejected INTEGER,
                    nodes_created INTEGER,
                    relationships_created INTEGER,
                    validation_status VARCHAR
                )
            """
        }

        for table_name, create_sql in tables.items():
            self.conn.execute(create_sql)

    def register_dataset(self, data: Dict[str, Any]):
        if not self.conn:
            return
        sql = """
            INSERT OR REPLACE INTO datasets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.conn.execute(sql, [
            data.get("dataset_id"),
            data.get("dataset_name"),
            data.get("provider"),
            data.get("version"),
            data.get("release_date"),
            data.get("source_url"),
            data.get("download_url"),
            data.get("license"),
            data.get("acquired_at"),
            data.get("sha256"),
            data.get("record_count", 0),
            data.get("status", "ACTIVE")
        ])

    def insert_raw_records(self, records: List[Dict[str, Any]], batch_size: int = 2000):
        if not self.conn or not records:
            return
        for i in range(0, len(records), batch_size):
            chunk = records[i:i + batch_size]
            rows = [
                (
                    r.get("raw_record_id"),
                    r.get("dataset_id"),
                    r.get("file_id"),
                    r.get("source_record_id"),
                    json.dumps(r.get("raw_payload", {})) if isinstance(r.get("raw_payload"), (dict, list)) else str(r.get("raw_payload", "")),
                    r.get("record_hash")
                ) for r in chunk
            ]
            self.conn.executemany("INSERT OR REPLACE INTO raw_records VALUES (?, ?, ?, ?, ?, ?)", rows)

    def insert_normalized_records(self, records: List[Dict[str, Any]], batch_size: int = 2000):
        if not self.conn or not records:
            return
        for i in range(0, len(records), batch_size):
            chunk = records[i:i + batch_size]
            rows = [
                (
                    r.get("normalized_record_id"),
                    r.get("raw_record_id"),
                    r.get("entity_type"),
                    r.get("canonical_id"),
                    json.dumps(r.get("normalized_payload", {})) if isinstance(r.get("normalized_payload"), (dict, list)) else str(r.get("normalized_payload", "")),
                    r.get("normalization_version", "1.0")
                ) for r in chunk
            ]
            self.conn.executemany("INSERT OR REPLACE INTO normalized_records VALUES (?, ?, ?, ?, ?, ?)", rows)

    def insert_field_provenance(self, records: List[Dict[str, Any]], batch_size: int = 2000):
        if not self.conn or not records:
            return
        for i in range(0, len(records), batch_size):
            chunk = records[i:i + batch_size]
            rows = [
                (
                    r.get("provenance_id"),
                    r.get("entity_id"),
                    r.get("field_name"),
                    r.get("source_dataset_id"),
                    r.get("source_record_id"),
                    r.get("source_file"),
                    r.get("source_location"),
                    r.get("transformation", "EXACT_MAP"),
                    r.get("transformation_version", "1.0")
                ) for r in chunk
            ]
            self.conn.executemany("INSERT OR REPLACE INTO provenance VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)

    def insert_relationships(self, records: List[Dict[str, Any]], batch_size: int = 2000):
        if not self.conn or not records:
            return
        for i in range(0, len(records), batch_size):
            chunk = records[i:i + batch_size]
            rows = [
                (
                    r.get("relationship_id"),
                    r.get("source_id"),
                    r.get("relationship_type"),
                    r.get("target_id"),
                    r.get("dataset_id"),
                    r.get("source_record_id"),
                    r.get("relationship_classification"),
                    json.dumps(r.get("evidence", {})) if isinstance(r.get("evidence"), (dict, list)) else str(r.get("evidence", ""))
                ) for r in chunk
            ]
            self.conn.executemany("INSERT OR REPLACE INTO relationships VALUES (?, ?, ?, ?, ?, ?, ?, ?)", rows)


    def log_conflict(self, data: Dict[str, Any]):
        if not self.conn:
            return
        sql = "INSERT OR REPLACE INTO conflicts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.conn.execute(sql, [
            data.get("conflict_id"),
            data.get("entity_id"),
            data.get("field_name"),
            data.get("source_dataset_a"),
            str(data.get("value_a")),
            data.get("source_dataset_b"),
            str(data.get("value_b")),
            data.get("conflict_type", "VALUE_MISMATCH"),
            data.get("resolution_status", "UNRESOLVED")
        ])

    def log_rejected_record(self, data: Dict[str, Any]):
        if not self.conn:
            return
        sql = "INSERT OR REPLACE INTO rejected_records VALUES (?, ?, ?, ?, ?, ?)"
        self.conn.execute(sql, [
            data.get("rejection_id"),
            data.get("dataset_id"),
            data.get("source_record_id"),
            data.get("rejection_reason"),
            json.dumps(data.get("raw_payload", {})) if isinstance(data.get("raw_payload"), (dict, list)) else str(data.get("raw_payload", "")),
            data.get("timestamp")
        ])

    def log_pipeline_run(self, data: Dict[str, Any]):
        if not self.conn:
            return
        sql = "INSERT OR REPLACE INTO pipeline_runs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.conn.execute(sql, [
            data.get("run_id"),
            data.get("timestamp"),
            data.get("git_commit", "HEAD"),
            data.get("pipeline_version", "1.0.0"),
            data.get("dataset_versions", "v1.0"),
            data.get("files_processed", 0),
            data.get("records_processed", 0),
            data.get("records_rejected", 0),
            data.get("nodes_created", 0),
            data.get("relationships_created", 0),
            data.get("validation_status", "PASSED")
        ])

    def export_table_to_dataframe(self, table_name: str) -> pd.DataFrame:
        if not self.conn:
            return pd.DataFrame()
        return self.conn.execute(f"SELECT * FROM {table_name}").df()
