import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.metadata_manager import MetadataManager
from src.utils.http_client import HTTPClient
from src.utils.checksum import calculate_sha256

class BaseCollector(ABC):
    """
    Abstract base collector class for FoodKG raw data acquisition.
    """
    def __init__(
        self,
        config: Dict[str, Any],
        system_config: Dict[str, Any],
        metadata_manager: MetadataManager,
        http_client: HTTPClient,
        project_root: Path
    ):
        self.config = config
        self.system_config = system_config
        self.metadata_manager = metadata_manager
        self.http_client = http_client
        self.project_root = project_root
        
        # Configure output paths: e.g. project_root / data / structured / foodb
        self.dest_dir = (self.project_root / "data" / self.config["path"]).resolve()
        self.dest_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger(f"Collector.{self.config['id']}")
        self.logger.info(f"Initialized collector '{self.config['name']}' in directory '{self.dest_dir}'")

    @abstractmethod
    async def collect(self) -> List[Path]:
        """
        Executes the acquisition routine for this data source.
        Returns a list of local file Paths that were downloaded, scraped, or tracked.
        """
        pass

    def mark_manual(self, remarks: str = "") -> List[Path]:
        """
        Registers this source in manual download mode.
        """
        self.logger.info(f"Marking dataset '{self.config['name']}' as MANUAL DOWNLOAD REQUIRED.")
        
        # Determine relative path from project root
        try:
            rel_path = str(self.dest_dir.relative_to(self.project_root)).replace("\\", "/")
        except ValueError:
            rel_path = str(self.dest_dir).replace("\\", "/")

        self.metadata_manager.register_dataset(
            name=self.config["name"],
            official_source=self.config["official_source"],
            download_url=self.config.get("download_url", ""),
            access_mode="Manual",
            license_str=self.config["license"],
            raw_file_type=self.config["file_type"],
            local_path=rel_path,
            status="Manual Download Required",
            filename="N/A",
            size_str="N/A",
            remarks=remarks or f"Requires manual download. Official URL: {self.config['official_source']}"
        )
        return []

    def register_file(self, file_path: Path, status: str, size_str: str = "", remarks: str = "") -> None:
        """
        Registers a downloaded or scraped file in the metadata catalog and download log.
        """
        if not file_path.exists():
            self.logger.warning(f"File {file_path} does not exist. Cannot register.")
            return

        size_bytes = file_path.stat().st_size
        if not size_str:
            size_str = self._format_size(size_bytes)
            
        try:
            checksum = calculate_sha256(file_path)
            checksum_remark = f"SHA256: {checksum}. {remarks}"
        except Exception as e:
            checksum_remark = f"Checksum computation failed: {e}. {remarks}"

        # Determine relative path from project root
        try:
            rel_path = str(file_path.relative_to(self.project_root)).replace("\\", "/")
        except ValueError:
            rel_path = str(file_path).replace("\\", "/")

        self.metadata_manager.register_dataset(
            name=self.config["name"],
            official_source=self.config["official_source"],
            download_url=self.config.get("download_url", ""),
            access_mode=self.config["access_mode"],
            license_str=self.config["license"],
            raw_file_type=self.config["file_type"],
            local_path=rel_path,
            status=status,
            filename=file_path.name,
            size_str=size_str,
            remarks=checksum_remark
        )
        self.logger.info(f"Registered file: {file_path.name} (Status: {status})")

    def _format_size(self, size_bytes: int) -> str:
        """Formats bytes into human readable sizes."""
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"
