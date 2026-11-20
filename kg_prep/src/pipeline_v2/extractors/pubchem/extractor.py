"""
Pipeline V2 PubChem Extractor Module.

Parses official NCBI PubChem PUG REST JSON payloads, extracting chemical compound
properties, stereochemical descriptors, formulas, and synonyms.

Invariants:
- Extracts genuine chemical records only.
- Does NOT perform arbitrary chemical assignments to whole food items.
- Preserves raw values, formulas, and structural strings.
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


class PubChemExtractor:
    """Extractor for NCBI PubChem compound records."""

    SOURCE_ID = "SRC-PUBCHEM"
    DATASET_ID = "DSK-PUBCHEM-2026"

    def __init__(self, execution_id: Optional[str] = None):
        self.logger = setup_logger("pubchem_extractor", execution_id=execution_id)

    def extract_from_json_file(
        self,
        json_file_path: Union[str, Path],
        raw_asset_id: str,
    ) -> ExtractionBatchResult:
        """
        Parses a PubChem PUG REST compound JSON file.
        Extracts CID, IUPACName, MolecularFormula, MolecularWeight, SMILES, InChI, and Synonyms.
        """
        path = Path(json_file_path)
        if not path.exists():
            raise AssetNotFoundError(f"PubChem JSON file not found: {path}")

        result = ExtractionBatchResult(
            source_id=self.SOURCE_ID,
            dataset_id=self.DATASET_ID,
            asset_id=raw_asset_id,
        )

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            raise CorruptedAssetError(f"Failed to read PubChem JSON {path}: {e}")

        # PUG REST structure: {"PropertyTable": {"Properties": [...]}}
        prop_table = data.get("PropertyTable", {})
        compounds = prop_table.get("Properties", [])

        # If data is a direct dict (single compound lookup)
        if not compounds and "CID" in data:
            compounds = [data]

        result.total_records_discovered = len(compounds)

        synonyms = data.get("Synonyms", [])

        for comp in compounds:
            cid = comp.get("CID")
            iupac_name = comp.get("IUPACName")
            formula = comp.get("MolecularFormula")
            mw = comp.get("MolecularWeight")

            if not cid:
                result.total_records_rejected += 1
                rejected_record = SourceRecord(
                    source_id=self.SOURCE_ID,
                    dataset_id=self.DATASET_ID,
                    source_record_id="MISSING_CID",
                    source_entity_type="COMPOUND",
                    original_identifier="NONE",
                    original_name="UNKNOWN_COMPOUND",
                    original_fields=comp,
                    raw_asset_id=raw_asset_id,
                    source_location=f"{path.name}#CID=NONE",
                    extraction_status=ExtractionStatus.REJECTED,
                    rejection_reason="MISSING_PUBCHEM_CID",
                )
                result.rejected_records.append(rejected_record)
                continue

            primary_name = iupac_name or (synonyms[0] if synonyms else f"PubChem CID {cid}")

            payload = {
                "cid": cid,
                "iupac_name": iupac_name,
                "molecular_formula": formula,
                "molecular_weight": mw,
                "canonical_smiles": comp.get("CanonicalSMILES") or comp.get("SMILES"),
                "isomeric_smiles": comp.get("IsomericSMILES"),
                "inchi": comp.get("InChI"),
                "inchi_key": comp.get("InChIKey"),
                "synonyms": synonyms[:20] if synonyms else [],  # Store top 20 verified synonyms
            }

            source_record = SourceRecord(
                source_id=self.SOURCE_ID,
                dataset_id=self.DATASET_ID,
                source_record_id=str(cid),
                source_entity_type="COMPOUND",
                original_identifier=f"CID:{cid}",
                original_name=primary_name,
                original_fields=payload,
                raw_asset_id=raw_asset_id,
                source_location=f"{path.name}#CID={cid}",
                extraction_status=ExtractionStatus.EXTRACTED,
                metadata={"inchi_key": comp.get("InChIKey"), "has_formula": bool(formula)},
            )

            result.records.append(source_record)
            result.total_records_extracted += 1

        self.logger.info(
            f"Extracted {result.total_records_extracted} PubChem compounds from {path.name}"
        )
        return result
