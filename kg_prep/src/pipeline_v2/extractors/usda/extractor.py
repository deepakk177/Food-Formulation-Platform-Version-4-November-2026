"""
Pipeline V2 USDA FoodData Central Extractor Module.

Extracts genuine nutritional composition and food records from USDA FoodData Central
JSON or CSV assets. Enforces Decision D-01: Foundation Foods and SR Legacy are accepted;
Branded Foods are strictly rejected from the foundational nutritional baseline.

Invariants:
- Preserves native units and values without normalization.
- Zero imputation: does NOT fabricate missing nutrients.
- Records explicit rejection reasons for branded or malformed items.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

from pipeline_v2.core.exceptions import CorruptedAssetError, AssetNotFoundError
from pipeline_v2.core.logging_config import setup_logger
from pipeline_v2.models.source_record_models import (
    SourceRecord,
    ExtractionStatus,
    ExtractionBatchResult,
)


class UsdaExtractor:
    """Extractor for USDA FoodData Central food and nutrient records."""

    SOURCE_ID = "SRC-USDA-FDC"
    DATASET_ID = "DSK-USDA-FDC-2024-04"
    APPROVED_DATA_TYPES = {"Foundation", "SR Legacy"}

    def __init__(self, execution_id: Optional[str] = None):
        self.logger = setup_logger("usda_extractor", execution_id=execution_id)

    def extract_from_json_file(
        self,
        json_file_path: Union[str, Path],
        raw_asset_id: str,
    ) -> ExtractionBatchResult:
        """
        Parses USDA FDC API search or food list JSON file.
        Extracts food items and their native nutrient lists.
        """
        path = Path(json_file_path)
        if not path.exists():
            raise AssetNotFoundError(f"USDA FDC file not found: {path}")

        result = ExtractionBatchResult(
            source_id=self.SOURCE_ID,
            dataset_id=self.DATASET_ID,
            asset_id=raw_asset_id,
        )

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            raise CorruptedAssetError(f"Failed to read USDA FDC JSON {path}: {e}")

        # The JSON could be a bulk dataset {"FoundationFoods": [...]}, {"SRLegacyFoods": [...]}, {"foods": [...]}, or a list
        default_data_type = None
        if isinstance(data, dict):
            if "FoundationFoods" in data:
                food_items = data["FoundationFoods"]
                default_data_type = "Foundation"
            elif "SRLegacyFoods" in data:
                food_items = data["SRLegacyFoods"]
                default_data_type = "SR Legacy"
            elif "foods" in data:
                food_items = data["foods"]
            elif "fdcId" in data:
                food_items = [data]
            else:
                food_items = []
        elif isinstance(data, list):
            food_items = data
        else:
            food_items = []

        result.total_records_discovered = len(food_items)

        for item in food_items:
            fdc_id = item.get("fdcId")
            description = item.get("description")
            data_type = item.get("dataType") or default_data_type or "UNKNOWN"

            if not fdc_id or not description:
                result.total_records_rejected += 1
                rejected_record = SourceRecord(
                    source_id=self.SOURCE_ID,
                    dataset_id=self.DATASET_ID,
                    source_record_id=str(fdc_id or "MISSING_ID"),
                    source_entity_type="FOOD_ITEM",
                    original_identifier=str(fdc_id or "NONE"),
                    original_name=str(description or "UNNAMED"),
                    original_fields=item,
                    raw_asset_id=raw_asset_id,
                    source_location=f"{path.name}#fdcId={fdc_id}",
                    extraction_status=ExtractionStatus.REJECTED,
                    rejection_reason="MISSING_FDC_ID_OR_DESCRIPTION",
                )
                result.rejected_records.append(rejected_record)
                continue

            # Scope Enforcement: Decision D-01
            if data_type not in self.APPROVED_DATA_TYPES:
                result.total_records_rejected += 1
                rejected_record = SourceRecord(
                    source_id=self.SOURCE_ID,
                    dataset_id=self.DATASET_ID,
                    source_record_id=str(fdc_id),
                    source_entity_type="FOOD_ITEM",
                    original_identifier=str(fdc_id),
                    original_name=description,
                    original_fields=item,
                    raw_asset_id=raw_asset_id,
                    source_location=f"{path.name}#fdcId={fdc_id}",
                    extraction_status=ExtractionStatus.REJECTED,
                    rejection_reason=f"OUT_OF_SCOPE_DATA_TYPE:{data_type}",
                )
                result.rejected_records.append(rejected_record)
                continue

            # Extract nutrient measurements preserved as raw native records
            nutrients = item.get("foodNutrients", [])
            extracted_nutrients = []
            for n in nutrients:
                n_id = n.get("nutrientId") or n.get("nutrient", {}).get("id")
                n_name = n.get("nutrientName") or n.get("nutrient", {}).get("name")
                n_val = n.get("value") if n.get("value") is not None else n.get("amount")
                n_unit = n.get("unitName") or n.get("nutrient", {}).get("unitName")
                n_derivation = n.get("derivationCode") or n.get("derivationDescription")

                if n_id and n_name and n_val is not None:
                    extracted_nutrients.append({
                        "nutrient_id": n_id,
                        "nutrient_name": n_name,
                        "value_raw": n_val,
                        "unit_raw": n_unit,
                        "derivation": n_derivation,
                    })

            # Extract portions
            portions = [
                {
                    "amount": p.get("amount"),
                    "modifier": p.get("modifier"),
                    "gram_weight": p.get("gramWeight"),
                    "measure_unit": (
                        p.get("measureUnit", {}).get("name")
                        if isinstance(p.get("measureUnit"), dict)
                        else p.get("measureUnit")
                    ),
                }
                for p in item.get("foodPortions", [])
            ]

            payload = {
                "fdc_id": fdc_id,
                "description": description,
                "data_type": data_type,
                "food_category": (
                    item.get("foodCategory", {}).get("description")
                    if isinstance(item.get("foodCategory"), dict)
                    else item.get("foodCategory")
                ),
                "publication_date": item.get("publicationDate"),
                "ndb_number": item.get("ndbNumber"),
                "food_nutrients": extracted_nutrients,
                "food_portions": portions,
                "raw_nutrient_count": len(extracted_nutrients),
            }

            ds_id = (
                "DSK-USDA-FDC-FOUNDATION"
                if data_type == "Foundation"
                else ("DSK-USDA-FDC-SR-LEGACY" if data_type == "SR Legacy" else self.DATASET_ID)
            )

            source_record = SourceRecord(
                source_id=self.SOURCE_ID,
                dataset_id=ds_id,
                source_record_id=str(fdc_id),
                source_entity_type="FOOD_ITEM",
                original_identifier=str(fdc_id),
                original_name=description,
                original_fields=payload,
                raw_asset_id=raw_asset_id,
                source_location=f"{path.name}#fdcId={fdc_id}",
                extraction_status=ExtractionStatus.EXTRACTED,
                metadata={"data_type": data_type, "nutrient_count": len(extracted_nutrients)},
            )

            result.records.append(source_record)
            result.total_records_extracted += 1

        self.logger.info(
            f"Extracted {result.total_records_extracted} valid USDA records from {path.name} "
            f"(Discovered: {result.total_records_discovered}, Rejected: {result.total_records_rejected})"
        )
        return result

    def stream_from_json_file(
        self,
        json_file_path: Union[str, Path],
        raw_asset_id: str,
        chunk_size: int = 1000,
    ):
        """
        Streams food items from bulk or search JSON file in chunks of chunk_size.
        Yields List[SourceRecord] per chunk.
        """
        path = Path(json_file_path)
        if not path.exists():
            raise AssetNotFoundError(f"USDA FDC file not found: {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            raise CorruptedAssetError(f"Failed to read USDA FDC JSON {path}: {e}")

        default_data_type = None
        if isinstance(data, dict):
            if "FoundationFoods" in data:
                food_items = data["FoundationFoods"]
                default_data_type = "Foundation"
            elif "SRLegacyFoods" in data:
                food_items = data["SRLegacyFoods"]
                default_data_type = "SR Legacy"
            elif "foods" in data:
                food_items = data["foods"]
            elif "fdcId" in data:
                food_items = [data]
            else:
                food_items = []
        elif isinstance(data, list):
            food_items = data
        else:
            food_items = []

        current_chunk: List[SourceRecord] = []
        for item in food_items:
            fdc_id = item.get("fdcId")
            description = item.get("description")
            data_type = item.get("dataType") or default_data_type or "UNKNOWN"

            if not fdc_id or not description:
                continue

            if data_type not in self.APPROVED_DATA_TYPES:
                continue

            nutrients = item.get("foodNutrients", [])
            extracted_nutrients = []
            for n in nutrients:
                n_id = n.get("nutrientId") or n.get("nutrient", {}).get("id")
                n_name = n.get("nutrientName") or n.get("nutrient", {}).get("name")
                n_val = n.get("value") if n.get("value") is not None else n.get("amount")
                n_unit = n.get("unitName") or n.get("nutrient", {}).get("unitName")
                n_derivation = n.get("derivationCode") or n.get("derivationDescription")

                if n_id and n_name and n_val is not None:
                    extracted_nutrients.append({
                        "nutrient_id": n_id,
                        "nutrient_name": n_name,
                        "value_raw": n_val,
                        "unit_raw": n_unit,
                        "derivation": n_derivation,
                    })

            portions = [
                {
                    "amount": p.get("amount"),
                    "modifier": p.get("modifier"),
                    "gram_weight": p.get("gramWeight"),
                    "measure_unit": (
                        p.get("measureUnit", {}).get("name")
                        if isinstance(p.get("measureUnit"), dict)
                        else p.get("measureUnit")
                    ),
                }
                for p in item.get("foodPortions", [])
            ]

            ds_id = (
                "DSK-USDA-FDC-FOUNDATION"
                if data_type == "Foundation"
                else ("DSK-USDA-FDC-SR-LEGACY" if data_type == "SR Legacy" else self.DATASET_ID)
            )

            payload = {
                "fdc_id": fdc_id,
                "description": description,
                "data_type": data_type,
                "food_category": (
                    item.get("foodCategory", {}).get("description")
                    if isinstance(item.get("foodCategory"), dict)
                    else item.get("foodCategory")
                ),
                "publication_date": item.get("publicationDate"),
                "ndb_number": item.get("ndbNumber"),
                "food_nutrients": extracted_nutrients,
                "food_portions": portions,
                "raw_nutrient_count": len(extracted_nutrients),
            }

            source_record = SourceRecord(
                source_id=self.SOURCE_ID,
                dataset_id=ds_id,
                source_record_id=str(fdc_id),
                source_entity_type="FOOD_ITEM",
                original_identifier=str(fdc_id),
                original_name=description,
                original_fields=payload,
                raw_asset_id=raw_asset_id,
                source_location=f"{path.name}#fdcId={fdc_id}",
                extraction_status=ExtractionStatus.EXTRACTED,
                metadata={"data_type": data_type, "nutrient_count": len(extracted_nutrients)},
            )

            current_chunk.append(source_record)
            if len(current_chunk) >= chunk_size:
                yield current_chunk
                current_chunk = []

        if current_chunk:
            yield current_chunk
