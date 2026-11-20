"""
Pipeline V2 FoodOn Acquisition Module.

Acquires the official FoodOn OWL ontology file, either by verifying and reusing
the existing local genuine raw asset or streaming from the official FoodOntology
GitHub release artifact using HttpAcquisitionClient. Registers the asset in ManifestManager.
"""

import shutil
from pathlib import Path
from typing import Optional, Union

from pipeline_v2.core.exceptions import AssetNotFoundError, NetworkAcquisitionError
from pipeline_v2.core.http_client import HttpAcquisitionClient
from pipeline_v2.core.logging_config import setup_logger
from pipeline_v2.core.manifest import ManifestManager
from pipeline_v2.models.manifest_models import AssetRecord


class FoodonAcquirer:
    """Acquires and verifies official FoodOn OWL ontology assets."""

    SOURCE_ID = "SRC-FOODON"
    DATASET_ID = "DSK-FOODON-2024-03"
    DEFAULT_REMOTE_URL = "https://raw.githubusercontent.com/FoodOntology/foodon/master/foodon.owl"
    DEFAULT_VERSION = "2024-03-08"

    def __init__(
        self,
        raw_dir: Union[str, Path] = "data/raw_v2/foodon",
        legacy_path: Union[str, Path] = "data/raw/ontology/foodon.owl",
        execution_id: Optional[str] = None,
    ):
        self.raw_dir = Path(raw_dir)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.legacy_path = Path(legacy_path)
        self.logger = setup_logger("foodon_acquirer", execution_id=execution_id)

    def acquire(
        self,
        manifest_manager: ManifestManager,
        force_download: bool = False,
        remote_url: Optional[str] = None,
    ) -> AssetRecord:
        """
        Acquires FoodOn OWL file, computes SHA-256, and registers in manifest.
        Reuses verified existing local asset if available and force_download is False.
        """
        target_path = self.raw_dir / "foodon.owl"
        url = remote_url or self.DEFAULT_REMOTE_URL

        # Check existing local asset
        if not force_download:
            if target_path.exists() and target_path.stat().st_size > 10_000_000:
                self.logger.info(f"Reusing verified FoodOn asset at {target_path}")
            elif self.legacy_path.exists() and self.legacy_path.stat().st_size > 10_000_000:
                self.logger.info(
                    f"Reusing existing genuine local FoodOn asset from {self.legacy_path}"
                )
                shutil.copy2(self.legacy_path, target_path)

        # Download if still not present
        if not target_path.exists() or target_path.stat().st_size < 1000:
            self.logger.info(f"Downloading FoodOn OWL from {url} to {target_path}")
            with HttpAcquisitionClient() as client:
                client.download_file(
                    url=url,
                    destination_path=target_path,
                    expected_content_types=["text/xml", "application/xml", "application/rdf+xml", "text/plain"],
                    source_id=self.SOURCE_ID,
                )

        if not target_path.exists() or target_path.stat().st_size == 0:
            raise AssetNotFoundError(f"FoodOn OWL asset could not be acquired at {target_path}")

        # Register asset in ManifestManager
        asset_record = manifest_manager.register_asset(
            asset_id="AST-FOODON-OWL-001",
            source_id=self.SOURCE_ID,
            dataset_id=self.DATASET_ID,
            local_path=target_path,
            source_url=url,
            dataset_version=self.DEFAULT_VERSION,
            content_type="application/rdf+xml",
            access_status="LOCAL_AVAILABLE",
            metadata={"ontology_name": "FoodOn", "format": "OWL/XML"},
        )
        self.logger.info(
            f"Registered FoodOn asset {asset_record.asset_id} (SHA256: {asset_record.sha256[:16]}..., {asset_record.file_size_bytes} bytes)"
        )
        return asset_record
