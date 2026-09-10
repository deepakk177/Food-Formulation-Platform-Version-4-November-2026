from pathlib import Path
import pandas as pd
import logging
import zipfile
from typing import Dict, Any

from src.core.base_profiler import BaseProfiler
from src.core.quality_assessor import audit_tabular_data

logger = logging.getLogger("structured.profiler")

class StructuredProfiler(BaseProfiler):
    def __init__(self, config_path: Path):
        super().__init__(config_path, "structured")

    def detect_schema(self, file_path: Path, mime_type: str) -> Dict[str, Any]:
        """Infer columns, types, primary keys, and shape from structured files."""
        suffix = file_path.suffix.lower()
        schema = {"columns": [], "nested_fields": [], "type": "Structured", "primary_key_candidates": []}

        if suffix in [".csv", ".tsv"]:
            try:
                sep = "\t" if suffix == ".tsv" else ","
                # Read header and a sample of rows
                df_sample = pd.read_csv(file_path, sep=sep, nrows=100)
                schema["columns"] = list(df_sample.columns)
                schema["column_types"] = {col: str(dtype) for col, dtype in df_sample.dtypes.items()}
                
                # Check for Primary Key candidates
                pk_candidates = []
                for col in df_sample.columns:
                    non_nulls = df_sample[col].dropna()
                    if len(non_nulls) == len(df_sample) and non_nulls.is_unique:
                        pk_candidates.append(col)
                schema["primary_key_candidates"] = pk_candidates
                schema["type"] = "CSV/TSV Table"
            except Exception as e:
                logger.error(f"Error reading CSV header for {file_path}: {e}")
                
        elif suffix == ".zip":
            # If it's a zipped archive, inspect nested files
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    file_list = zip_ref.namelist()
                    schema["nested_files"] = file_list
                    schema["type"] = "Zipped Archive"
                    # Try to extract the first CSV inside and profile its headers
                    for f in file_list:
                        if f.endswith(".csv"):
                            with zip_ref.open(f) as zf:
                                df_sample = pd.read_csv(zf, nrows=5)
                                schema["columns"] = list(df_sample.columns)
                                schema["type"] = "ZIP containing CSV"
                                break
            except Exception as e:
                logger.error(f"Error reading ZIP contents for {file_path}: {e}")
                
        return schema

    def assess_quality(self, file_path: Path, mime_type: str) -> Dict[str, Any]:
        """Audit tabular quality (completeness, duplicates, Readiness Score)."""
        suffix = file_path.suffix.lower()
        if suffix in [".csv", ".tsv"]:
            try:
                sep = "\t" if suffix == ".tsv" else ","
                df = pd.read_csv(file_path, sep=sep)
                audit = audit_tabular_data(df)
                audit["total_records"] = len(df)
                return audit
            except Exception as e:
                logger.error(f"Failed to audit quality for {file_path}: {e}")
                return {
                    "valid_utf8": False,
                    "broken_format": True,
                    "completeness": 0.0,
                    "consistency": 0.0,
                    "duplicate_records": 0,
                    "readiness_score": 0.0,
                    "total_records": 0
                }
        elif suffix == ".zip":
            # Extract first CSV inside and audit it
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    for f in zip_ref.namelist():
                        if f.endswith(".csv"):
                            with zip_ref.open(f) as zf:
                                df = pd.read_csv(zf)
                                audit = audit_tabular_data(df)
                                audit["total_records"] = len(df)
                                return audit
            except Exception:
                pass
        
        return super().assess_quality(file_path, mime_type)
