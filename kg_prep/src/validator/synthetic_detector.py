import re
import logging
from typing import Dict, Any, Tuple, Optional

logger = logging.getLogger("validator.synthetic_detector")

class SyntheticDetector:
    """
    Automated Synthetic & Placeholder Record Detector.
    Scans candidate records and identifies synthetic names, artificial sequential IDs,
    placeholder keywords, or ungrounded claims.
    """
    def __init__(self):
        # Regex patterns for artificial sequential names or IDs
        self.sequential_patterns = [
            re.compile(r".*(ITEM|INGREDIENT|PRODUCT|FOOD|NUTRIENT|CONSTRAINT|PROCESS|PROPERTY|RECORD)[_\-\s]*[0-9]+.*", re.IGNORECASE),
            re.compile(r"^ING[_\-\s]*[0-9]+$", re.IGNORECASE),
            re.compile(r"^PROD[_\-\s]*[0-9]+$", re.IGNORECASE),
            re.compile(r"^NUT[_\-\s]*[0-9]+$", re.IGNORECASE),
            re.compile(r"^CONST[_\-\s]*[0-9]+$", re.IGNORECASE),
            re.compile(r"^PROC[_\-\s]*[0-9]+$", re.IGNORECASE),
            re.compile(r"^PROP[_\-\s]*[0-9]+$", re.IGNORECASE),
            re.compile(r"^EV[_\-\s]*[0-9]+$", re.IGNORECASE)
        ]

        # Forbidden synthetic & placeholder keywords
        self.placeholder_keywords = [
            "food ingredient item",
            "commercial food product",
            "nutrient component",
            "regulatory constraint limit",
            "food processing operation unit",
            "physicochemical property parameter",
            "industrial food processing equipment unit",
            "scientific evidence document report",
            "specific allergenic epitope sequence",
            "food grade packaging material format",
            "test_ingredient",
            "sample_ingredient",
            "unknown_ingredient",
            "generic_ingredient",
            "placeholder_ingredient",
            "dummy_record",
            "synthetic_record",
            "sample product",
            "unknown food",
            "generic powder"
        ]

    def is_synthetic(self, record: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Evaluates a record against synthetic detection rules.
        Returns (is_synthetic, rejection_reason).
        """
        rec_id = str(record.get("ID", "") or record.get("constraint_id", "") or record.get("ingredient_id", "") or record.get("evidence_id", "") or "").strip()
        rec_name = str(record.get("Name", "") or record.get("canonical_name", "") or record.get("entity_name", "") or record.get("constraint_id", "") or record.get("description", "") or "").strip()
        source_id = str(record.get("Source", "") or record.get("source_id", "") or "").strip()
        source_rec_id = str(record.get("source_record_id", "") or "").strip()

        # Check 1: Empty or missing name
        if not rec_name:
            return True, "MISSING_MANDATORY_ENTITY_NAME"

        # Check 2: Sequential artificial pattern matching in name
        for pattern in self.sequential_patterns:
            if pattern.match(rec_name):
                return True, f"SYNTHETIC_SEQUENTIAL_NAME_PATTERN: '{rec_name}'"

        # Check 3: Placeholder keywords matching in name
        lower_name = rec_name.lower()
        for kw in self.placeholder_keywords:
            if kw in lower_name:
                return True, f"SYNTHETIC_PLACEHOLDER_KEYWORD: '{kw}' in '{rec_name}'"

        # Check 4: Sequential artificial pattern matching in ID (e.g. ing_31, prod_45)
        if re.match(r"^(ing|prod|nut|const|proc|prop|ev|equip|pack|cat)_[0-9]+$", rec_id, re.IGNORECASE):
            # Check if there is a genuine source record ID or FDC ID attached
            if not source_rec_id or source_rec_id.startswith("ing_") or source_rec_id.startswith("prod_"):
                return True, f"SYNTHETIC_SEQUENTIAL_ID_WITHOUT_GROUNDED_SOURCE_ID: '{rec_id}'"

        # Check 5: Lack of verifiable source provenance
        if not source_id or source_id.lower() in ["unknown", "system", "mock", "generated"]:
            if not source_rec_id:
                return True, f"UNGROUNDED_RECORD_WITHOUT_SOURCE_ID: '{rec_name}'"

        return False, None
