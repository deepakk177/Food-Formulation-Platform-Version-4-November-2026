"""
Pipeline V2 PubChem Acquisition Module.

Acquires verified chemical compound records from the official NCBI PubChem
PUG REST API. Supports queries by CID, exact name, CAS RN, or InChIKey.
Enforces request throttling (<= 5 req/sec). Registers acquired assets in ManifestManager.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Union
from urllib.parse import quote
import requests

from pipeline_v2.core.exceptions import NetworkAcquisitionError, HTTPStatusError
from pipeline_v2.core.logging_config import setup_logger
from pipeline_v2.core.manifest import ManifestManager
from pipeline_v2.models.manifest_models import AssetRecord


class PubChemAcquirer:
    """Acquires verified chemical structures and properties from NCBI PubChem."""

    SOURCE_ID = "SRC-PUBCHEM"
    DATASET_ID = "DSK-PUBCHEM-2026"
    BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound"
    DATASET_VERSION = "PUG-REST-v1"
    PROPERTY_LIST = (
        "IUPACName,MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES,InChI,InChIKey"
    )

    def __init__(
        self,
        raw_dir: Union[str, Path] = "data/raw_v2/pubchem",
        execution_id: Optional[str] = None,
        min_interval_seconds: float = 0.25,  # Max 4-5 req/sec
    ):
        self.raw_dir = Path(raw_dir)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.logger = setup_logger("pubchem_acquirer", execution_id=execution_id)
        self.min_interval = min_interval_seconds
        self.last_request_time = 0.0

    def _throttle(self) -> None:
        """Enforces NCBI PubChem usage policy (<= 5 requests per second)."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()

    def fetch_by_cid(self, cid: int, force_download: bool = False) -> Path:
        """Fetches properties and synonyms for a specific PubChem CID. Reuses local if present."""
        dest_path = self.raw_dir / f"pubchem_cid_{cid}.json"
        if dest_path.exists() and not force_download and dest_path.stat().st_size > 0:
            self.logger.info(f"Reusing verified local PubChem asset at {dest_path}")
            return dest_path

        self._throttle()

        url = f"{self.BASE_URL}/cid/{cid}/property/{self.PROPERTY_LIST}/JSON"
        self.logger.info(f"Fetching PubChem properties for CID {cid}")
        response = requests.get(
            url,
            headers={"User-Agent": "FoodFormulationPlatform/2.0"},
            timeout=20.0,
        )

        if not response.ok:
            raise HTTPStatusError(
                f"PubChem CID fetch failed for {cid} with status {response.status_code}",
                status_code=response.status_code,
                url=url,
            )

        data = response.json()

        # Also fetch synonyms if available
        self._throttle()
        syn_url = f"{self.BASE_URL}/cid/{cid}/synonyms/JSON"
        syn_resp = requests.get(
            syn_url,
            headers={"User-Agent": "FoodFormulationPlatform/2.0"},
            timeout=20.0,
        )
        if syn_resp.ok:
            syn_data = syn_resp.json()
            data["Synonyms"] = syn_data.get("InformationList", {}).get("Information", [{}])[0].get("Synonym", [])

        with open(dest_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return dest_path

    def fetch_by_name(self, chemical_name: str) -> Path:
        """Fetches properties for a verified chemical name via PubChem name endpoint."""
        safe_name = quote(chemical_name.strip())
        dest_path = self.raw_dir / f"pubchem_name_{chemical_name.replace(' ', '_').lower()}.json"
        self._throttle()

        url = f"{self.BASE_URL}/name/{safe_name}/property/{self.PROPERTY_LIST}/JSON"
        self.logger.info(f"Fetching PubChem properties for name '{chemical_name}'")
        response = requests.get(
            url,
            headers={"User-Agent": "FoodFormulationPlatform/2.0"},
            timeout=20.0,
        )

        if not response.ok:
            raise HTTPStatusError(
                f"PubChem name fetch failed for '{chemical_name}' with status {response.status_code}",
                status_code=response.status_code,
                url=url,
            )

        data = response.json()
        with open(dest_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return dest_path

    def register_acquired_asset(
        self,
        asset_id: str,
        file_path: Path,
        manifest_manager: ManifestManager,
        metadata: Optional[Dict] = None,
    ) -> AssetRecord:
        """Registers a downloaded PubChem JSON asset in ManifestManager."""
        return manifest_manager.register_asset(
            asset_id=asset_id,
            source_id=self.SOURCE_ID,
            dataset_id=self.DATASET_ID,
            local_path=file_path,
            source_url=self.BASE_URL,
            dataset_version=self.DATASET_VERSION,
            content_type="application/json",
            access_status="REMOTE_AVAILABLE",
            metadata=metadata or {"format": "PUG_REST_JSON"},
        )
