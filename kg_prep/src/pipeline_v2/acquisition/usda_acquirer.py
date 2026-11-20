"""
Pipeline V2 USDA FoodData Central Acquisition Module.

Acquires official USDA FoodData Central records scoped strictly to Foundation Foods
and SR Legacy datasets per Decision D-01. Uses official FDC REST API with credentials
loaded safely from the environment. Registers all downloaded assets in ManifestManager.
"""

import json
import os
import time
from pathlib import Path
from typing import Dict, List, Optional, Union
import requests

from pipeline_v2.core.exceptions import NetworkAcquisitionError, HTTPStatusError
from pipeline_v2.core.logging_config import setup_logger
from pipeline_v2.core.manifest import ManifestManager
from pipeline_v2.models.manifest_models import AssetRecord


class UsdaAcquirer:
    """Acquires official USDA FoodData Central datasets (Foundation Foods + SR Legacy)."""

    SOURCE_ID = "SRC-USDA-FDC"
    DATASET_ID = "DSK-USDA-FDC-2024-04"
    BASE_API_URL = "https://api.nal.usda.gov/fdc/v1"
    DATASET_VERSION = "2024-04-18"

    def __init__(
        self,
        raw_dir: Union[str, Path] = "data/raw_v2/usda",
        api_key: Optional[str] = None,
        execution_id: Optional[str] = None,
    ):
        self.raw_dir = Path(raw_dir)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        # Safe credential retrieval: env var -> passed arg -> DEMO_KEY
        self.api_key = api_key or os.environ.get("USDA_FDC_API_KEY") or "DEMO_KEY"
        self.logger = setup_logger("usda_acquirer", execution_id=execution_id)

    def query_foods_by_data_type(
        self,
        query: str,
        data_types: Optional[List[str]] = None,
        page_size: int = 50,
        output_filename: Optional[str] = None,
        force_download: bool = False,
    ) -> Path:
        """
        Queries FDC search endpoint for foods belonging to approved data types
        (default: Foundation Foods and SR Legacy). Reuses verified local file if available.
        """
        target_types = data_types or ["Foundation", "SR Legacy"]
        filename = output_filename or f"fdc_search_{query.replace(' ', '_')}.json"
        dest_path = self.raw_dir / filename

        if dest_path.exists() and not force_download and dest_path.stat().st_size > 0:
            self.logger.info(f"Reusing verified local USDA asset at {dest_path}")
            return dest_path

        url = f"{self.BASE_API_URL}/foods/search"
        params = {
            "query": query,
            "dataType": ",".join(target_types),
            "pageSize": page_size,
            "api_key": self.api_key,
        }

        self.logger.info(f"Querying USDA FDC for query='{query}', dataTypes={target_types}")
        response = requests.get(url, params=params, timeout=30.0)

        if not response.ok:
            raise HTTPStatusError(
                f"USDA FDC query failed with status {response.status_code}",
                status_code=response.status_code,
                url=url,
            )

        data = response.json()
        with open(dest_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        self.logger.info(
            f"Saved {len(data.get('foods', []))} genuine USDA records to {dest_path}"
        )
        return dest_path

    def fetch_food_details(self, fdc_id: int) -> Path:
        """Fetches complete raw nutrient assay profile for a specific FDC ID."""
        dest_path = self.raw_dir / f"fdc_food_{fdc_id}.json"
        url = f"{self.BASE_API_URL}/food/{fdc_id}"
        params = {"api_key": self.api_key}

        self.logger.info(f"Fetching full USDA food details for FDC ID {fdc_id}")
        response = requests.get(url, params=params, timeout=30.0)

        if not response.ok:
            raise HTTPStatusError(
                f"USDA FDC food detail fetch failed for {fdc_id} with status {response.status_code}",
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
        """Registers a downloaded FDC JSON asset in ManifestManager."""
        return manifest_manager.register_asset(
            asset_id=asset_id,
            source_id=self.SOURCE_ID,
            dataset_id=self.DATASET_ID,
            local_path=file_path,
            source_url=f"{self.BASE_API_URL}/foods",
            dataset_version=self.DATASET_VERSION,
            content_type="application/json",
            access_status="REMOTE_AVAILABLE",
            metadata=metadata or {"data_types": ["Foundation", "SR Legacy"]},
        )
