import os
import re
from pathlib import Path
import pandas as pd
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger("core.quality_assessor")

def check_utf8_validity(file_path: Path) -> bool:
    """Check if the file is valid UTF-8."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            f.read(4096)  # Read initial chunk to check encoding
        return True
    except UnicodeDecodeError:
        return False

def check_broken_json(file_path: Path) -> bool:
    """Check if a JSON/JSONL file is malformed."""
    try:
        # If it's a huge file, check a smaller sample, but let's do a basic check
        with open(file_path, "r", encoding="utf-8") as f:
            if file_path.suffix == ".jsonl":
                for line in f:
                    if line.strip():
                        json.loads(line)
            else:
                json.load(f)
        return False  # Not broken
    except Exception:
        return True  # Broken

def check_broken_xml(file_path: Path) -> bool:
    """Check if an XML file is malformed using standard etree."""
    import xml.etree.ElementTree as ET
    try:
        with open(file_path, "rb") as f:
            # Parse only small chunks or use parser to verify
            parser = ET.XMLParser()
            for chunk in iter(lambda: f.read(65536), b""):
                parser.feed(chunk)
            parser.close()
        return False  # Not broken
    except Exception:
        return True  # Broken

def detect_unit_inconsistencies(series: pd.Series) -> List[str]:
    """Find if a text column contains multiple units (e.g. mg and g, or mcg)."""
    if series.dtype != object:
        return []
    
    unique_vals = series.dropna().unique()
    found_units = set()
    
    patterns = {
        "mg": r"\b\d+(\.\d+)?\s*mg\b",
        "g": r"\b\d+(\.\d+)?\s*(g|grams)\b",
        "ug": r"\b\d+(\.\d+)?\s*(ug|mcg|\u03bcg)\b",
        "ml": r"\b\d+(\.\d+)?\s*ml\b",
        "l": r"\b\d+(\.\d+)?\s*l\b",
    }
    
    for val in unique_vals:
        if not isinstance(val, str):
            continue
        val_lower = val.lower()
        for unit, regex in patterns.items():
            if re.search(regex, val_lower):
                found_units.add(unit)
                
    # Return units if multiple are detected
    if len(found_units) > 1:
        return list(found_units)
    return []

def audit_tabular_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Audit tabular data (from CSV/TSV) for schema and value quality."""
    total_records = len(df)
    if total_records == 0:
        return {
            "completeness": 0.0,
            "consistency": 0.0,
            "duplicate_records": 0,
            "duplicate_rate": 0.0,
            "empty_columns": list(df.columns),
            "mixed_type_columns": [],
            "unit_inconsistencies": {},
            "readiness_score": 0.0
        }

    # Completeness (non-null rate across cells)
    null_cells = df.isnull().sum().sum()
    total_cells = df.size
    completeness = 1.0 - (null_cells / total_cells)

    # Duplicates
    dup_rows = df.duplicated().sum()
    duplicate_rate = dup_rows / total_records

    # Empty columns (100% missing)
    empty_cols = [col for col in df.columns if df[col].isnull().all()]

    # Mixed types and unit inconsistencies
    mixed_cols = []
    unit_issues = {}
    
    for col in df.columns:
        if col in empty_cols:
            continue
            
        # Mixed types: check if unique types in non-nulls is > 1
        non_null_types = df[col].dropna().map(type).unique()
        if len(non_null_types) > 1:
            mixed_cols.append(col)
            
        # Unit inconsistencies
        inconsistent_units = detect_unit_inconsistencies(df[col])
        if inconsistent_units:
            unit_issues[col] = inconsistent_units

    # Type consistency score
    type_consistency = 1.0 - (len(mixed_cols) / len(df.columns)) if len(df.columns) > 0 else 1.0

    # Calculate Readiness Score
    # 40% Completeness, 40% Type Consistency, 20% Deduplication rate
    readiness_score = (0.4 * completeness) + (0.4 * type_consistency) + (0.2 * (1.0 - duplicate_rate))

    return {
        "completeness": round(completeness, 4),
        "consistency": round(type_consistency, 4),
        "duplicate_records": int(dup_rows),
        "duplicate_rate": round(duplicate_rate, 4),
        "empty_columns": empty_cols,
        "mixed_type_columns": mixed_cols,
        "unit_inconsistencies": unit_issues,
        "readiness_score": round(max(0.0, min(1.0, readiness_score)), 4)
    }
