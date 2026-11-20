"""
Pipeline V2 Codex GSFA Acquisition Module.

Acquires official Codex General Standard for Food Additives (CXS 192-1995) assets.
Reuses verified local genuine additive index (data/raw/semi_structured/gsfa_html/gsfa_additives.html)
and registers it in ManifestManager.
Handles live provision endpoints; when blocked by Cloudflare, records BLOCKED status without
synthesizing fake data.
"""

import shutil
from pathlib import Path
from typing import Dict, List, Optional, Union
import requests

from pipeline_v2.core.exceptions import AssetNotFoundError, NetworkAcquisitionError, ContentTypeError
from pipeline_v2.core.logging_config import setup_logger
from pipeline_v2.core.manifest import ManifestManager
from pipeline_v2.models.manifest_models import AssetRecord


class GsfaAcquirer:
    """Acquires official Codex GSFA regulatory data and provisions."""

    SOURCE_ID = "SRC-CODEX-GSFA"
    DATASET_ID = "DSK-CODEX-GSFA-2023"
    DATASET_VERSION = "CXS 192-1995 (Rev. 2023)"
    ONLINE_BASE_URL = "https://www.fao.org/gsfaonline"

    # Targeted Initial Category Scope
    CORE_CATEGORIES = {
        "01.0": "Dairy products and analogues",
        "02.0": "Fats and oils, and fat emulsions",
        "05.0": "Confectionery",
        "06.0": "Cereals and cereal based products",
        "07.0": "Bakery wares",
        "14.0": "Beverages",
    }

    def __init__(
        self,
        raw_dir: Union[str, Path] = "data/raw_v2/codex_gsfa",
        legacy_html_path: Union[str, Path] = "data/raw/semi_structured/gsfa_html/gsfa_additives.html",
        execution_id: Optional[str] = None,
    ):
        self.raw_dir = Path(raw_dir)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.legacy_html = Path(legacy_html_path)
        self.logger = setup_logger("gsfa_acquirer", execution_id=execution_id)

    def acquire_additive_index(
        self,
        manifest_manager: ManifestManager,
    ) -> AssetRecord:
        """
        Reuses and verifies genuine local GSFA additives index HTML.
        Computes SHA-256 and registers into ManifestManager.
        """
        dest_path = self.raw_dir / "gsfa_additives.html"

        if not dest_path.exists() and self.legacy_html.exists():
            self.logger.info(f"Copying verified genuine GSFA additive index from {self.legacy_html}")
            shutil.copy2(self.legacy_html, dest_path)

        if not dest_path.exists() or dest_path.stat().st_size == 0:
            raise AssetNotFoundError(f"GSFA additive index asset missing at {dest_path}")

        return manifest_manager.register_asset(
            asset_id="AST-CODEX-GSFA-ADDITIVES-001",
            source_id=self.SOURCE_ID,
            dataset_id=self.DATASET_ID,
            local_path=dest_path,
            source_url=f"{self.ONLINE_BASE_URL}/additives/index.html",
            dataset_version=self.DATASET_VERSION,
            content_type="text/html",
            access_status="LOCAL_AVAILABLE",
            metadata={"description": "Official Codex GSFA Food Additive Index HTML table"},
        )

    def probe_online_category_provision(self, category_code: str) -> Dict[str, Union[str, int]]:
        """
        Probes official GSFA online portal for a specific food category provision.
        Detects Cloudflare challenge or gateway blocks and records status without faking data.
        """
        url = f"{self.ONLINE_BASE_URL}/foods/details.html?id={category_code.replace('.0', '')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

        try:
            resp = requests.get(url, headers=headers, timeout=10.0)
            if resp.status_code == 403 or "Just a moment..." in resp.text:
                self.logger.warning(
                    f"Codex GSFA online endpoint {url} is gated by Cloudflare anti-bot challenge. Status: BLOCKED_BY_CLOUDFLARE"
                )
                return {
                    "category_code": category_code,
                    "status": "BLOCKED_BY_CLOUDFLARE",
                    "http_code": resp.status_code,
                    "url": url,
                }
            return {
                "category_code": category_code,
                "status": "ACCESSIBLE",
                "http_code": resp.status_code,
                "url": url,
            }
        except Exception as e:
            self.logger.warning(f"Error connecting to GSFA online: {e}")
            return {
                "category_code": category_code,
                "status": "CONNECTION_FAILED",
                "http_code": 0,
                "url": url,
                "error": str(e),
            }
