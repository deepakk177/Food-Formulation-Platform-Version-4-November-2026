import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict

class DatasetMetadata(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    dataset_name: str = Field(..., serialization_alias="Dataset Name")
    official_source: str = Field(..., serialization_alias="Official Source")
    download_url: str = Field(..., serialization_alias="Download URL")
    access_mode: str = Field(..., serialization_alias="Access Mode")
    license: str = Field(..., serialization_alias="License")
    raw_file_type: str = Field(..., serialization_alias="Raw File Type")
    download_timestamp: str = Field(..., serialization_alias="Download Timestamp")
    local_path: str = Field(..., serialization_alias="Local Path")
    status: str = Field(..., serialization_alias="Status")

class MetadataManager:
    """
    Manages loading, updating, and saving of raw data collection metadata.
    Updates metadata.json and appends entries to download_log.csv.
    """
    def __init__(self, metadata_path: Path, log_path: Path):
        self.metadata_path = Path(metadata_path)
        self.log_path = Path(log_path)
        
        # Ensure directories exist
        self.metadata_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize metadata.json if it doesn't exist
        if not self.metadata_path.exists():
            self._save_metadata([])

        # Initialize download_log.csv with headers if it doesn't exist
        if not self.log_path.exists():
            self._init_log_csv()

    def _load_metadata(self) -> List[Dict[str, Any]]:
        try:
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_metadata(self, data: List[Dict[str, Any]]) -> None:
        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _init_log_csv(self) -> None:
        headers = [
            "Dataset", "Official URL", "Download URL", "Filename", 
            "Timestamp", "Status", "Mode", "Size", "Remarks"
        ]
        with open(self.log_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    def register_dataset(
        self,
        name: str,
        official_source: str,
        download_url: str,
        access_mode: str,
        license_str: str,
        raw_file_type: str,
        local_path: str,
        status: str,
        filename: str = "",
        size_str: str = "N/A",
        remarks: str = ""
    ) -> None:
        """Registers/updates a dataset in metadata.json and logs the entry in download_log.csv."""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        meta = DatasetMetadata(
            dataset_name=name,
            official_source=official_source,
            download_url=download_url,
            access_mode=access_mode,
            license=license_str,
            raw_file_type=raw_file_type,
            download_timestamp=timestamp,
            local_path=str(local_path).replace("\\", "/"),
            status=status
        )

        # Update metadata.json (replace duplicate by name or path if existing, otherwise append)
        metadata_list = self._load_metadata()
        updated_list = []
        replaced = False
        
        # We serialize using the aliases so they match the requested format exactly
        meta_dict = meta.model_dump(by_alias=True)
        
        for item in metadata_list:
            if item.get("Dataset Name") == name:
                updated_list.append(meta_dict)
                replaced = True
            else:
                updated_list.append(item)
                
        if not replaced:
            updated_list.append(meta_dict)
            
        self._save_metadata(updated_list)

        # Log entry in download_log.csv
        with open(self.log_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                name,
                official_source,
                download_url,
                filename or Path(local_path).name,
                timestamp,
                status,
                access_mode,
                size_str,
                remarks
            ])
