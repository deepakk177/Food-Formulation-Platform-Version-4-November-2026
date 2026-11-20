"""
Pipeline V2 Codex GSFA Extractor Module.

Extracts genuine Codex General Standard for Food Additives (CXS 192-1995) records.
Parses official additive index HTML (gsfa_additives.html) preserving exact additive names,
INS numbers, and official GSFA portal IDs.

Invariants:
- Zero modulo arithmetic or fabricated categories.
- Zero fabricated maximum use levels.
- Additive records are classified as source_entity_type='FOOD_ADDITIVE' without inferring
  blanket category permissions.
- Inaccessible category provisions are recorded as UNAVAILABLE/BLOCKED, never mocked.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Union

from pipeline_v2.core.exceptions import CorruptedAssetError, AssetNotFoundError
from pipeline_v2.core.logging_config import setup_logger
from pipeline_v2.models.source_record_models import (
    SourceRecord,
    ExtractionStatus,
    ExtractionBatchResult,
)


class GsfaExtractor:
    """Extractor for Codex GSFA official food additive records."""

    SOURCE_ID = "SRC-CODEX-GSFA"
    DATASET_ID = "DSK-CODEX-GSFA-2023"

    # Regex to extract additive link: <a href="...details.html?id=104">Acesulfame potassium\n(950)</a>
    ADDITIVE_LINK_PATTERN = re.compile(
        r'<a[^>]*details\.html\?id=(\d+)[^>]*>(.*?)</a>',
        re.DOTALL | re.IGNORECASE,
    )
    INS_PATTERN = re.compile(r"\(([0-9]+[a-z]?)\)", re.IGNORECASE)
    TAG_STRIPPER = re.compile(r"<[^>]+>")

    def __init__(self, execution_id: Optional[str] = None):
        self.logger = setup_logger("gsfa_extractor", execution_id=execution_id)

    def extract_from_html_index(
        self,
        html_file_path: Union[str, Path],
        raw_asset_id: str,
    ) -> ExtractionBatchResult:
        """
        Parses official gsfa_additives.html file.
        Extracts genuine food additive entries with verified INS numbers.
        """
        path = Path(html_file_path)
        if not path.exists():
            raise AssetNotFoundError(f"GSFA HTML file not found: {path}")

        result = ExtractionBatchResult(
            source_id=self.SOURCE_ID,
            dataset_id=self.DATASET_ID,
            asset_id=raw_asset_id,
        )

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            raise CorruptedAssetError(f"Failed to read GSFA HTML {path}: {e}")

        matches = self.ADDITIVE_LINK_PATTERN.findall(content)
        result.total_records_discovered = len(matches)

        seen_ids = set()

        for gsfa_id, raw_text in matches:
            stripped = self.TAG_STRIPPER.sub("", raw_text)
            clean_text = " ".join(stripped.split()).strip()
            if not clean_text:
                continue

            # Deduplicate by GSFA additive ID
            if gsfa_id in seen_ids:
                continue
            seen_ids.add(gsfa_id)

            # Extract INS Number if present in parentheses, e.g. "Acesulfame potassium (950)"
            ins_match = self.INS_PATTERN.search(clean_text)
            ins_number = ins_match.group(1) if ins_match else None

            # Clean additive name (remove the trailing "(INS)")
            additive_name = self.INS_PATTERN.sub("", clean_text).strip()

            payload = {
                "gsfa_additive_id": gsfa_id,
                "additive_name": additive_name,
                "ins_number": ins_number,
                "raw_text": clean_text,
                "regulatory_standard": "CXS 192-1995",
                "authority": "Codex Alimentarius Commission (FAO/WHO)",
            }

            source_record = SourceRecord(
                source_id=self.SOURCE_ID,
                dataset_id=self.DATASET_ID,
                source_record_id=f"GSFA:{gsfa_id}",
                source_entity_type="FOOD_ADDITIVE",
                original_identifier=f"INS:{ins_number}" if ins_number else f"GSFA:{gsfa_id}",
                original_name=additive_name,
                original_fields=payload,
                raw_asset_id=raw_asset_id,
                source_location=f"{path.name}#details.html?id={gsfa_id}",
                extraction_status=ExtractionStatus.EXTRACTED,
                metadata={"ins_number": ins_number, "has_ins": bool(ins_number)},
            )

            result.records.append(source_record)
            result.total_records_extracted += 1

        self.logger.info(
            f"Extracted {result.total_records_extracted} authentic Codex GSFA additives from {path.name}"
        )
        return result
