import json
import csv
import pytest
import shutil
from pathlib import Path
from src.metadata_manager import MetadataManager, DatasetMetadata
from src.utils.checksum import calculate_sha256
from src.base_collector import BaseCollector

class DummyCollector(BaseCollector):
    """A dummy collector for testing abstract base class methods."""
    async def collect(self):
        return []

@pytest.fixture
def temp_dir(tmp_path):
    yield tmp_path

def test_checksum_calculation(temp_dir):
    test_file = temp_dir / "test.txt"
    test_file.write_text("FoodKG Acquisition Test", encoding="utf-8")
    
    checksum = calculate_sha256(test_file)
    # Expected SHA256 of "FoodKG Acquisition Test"
    assert len(checksum) == 64
    assert isinstance(checksum, str)

def test_metadata_manager_registration(temp_dir):
    meta_json = temp_dir / "metadata.json"
    log_csv = temp_dir / "download_log.csv"
    
    manager = MetadataManager(meta_json, log_csv)
    
    # Register first file
    manager.register_dataset(
        name="Test FooDB",
        official_source="https://example.com/foodb",
        download_url="https://example.com/foodb/dump.zip",
        access_mode="Automatic",
        license_str="ODbL",
        raw_file_type="zip",
        local_path="data/structured/foodb/dump.zip",
        status="Downloaded",
        filename="dump.zip",
        size_str="1.2 MB",
        remarks="Test remark"
    )
    
    # Assert JSON file was created and contains entry
    assert meta_json.exists()
    with open(meta_json, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["Dataset Name"] == "Test FooDB"
        assert data[0]["Status"] == "Downloaded"
        
    # Assert CSV log was created and contains headers + entry
    assert log_csv.exists()
    with open(log_csv, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        assert len(reader) == 2  # header + row
        assert reader[0][0] == "Dataset"
        assert reader[1][0] == "Test FooDB"
        assert reader[1][5] == "Downloaded"

def test_base_collector_manual_marking(temp_dir):
    meta_json = temp_dir / "metadata.json"
    log_csv = temp_dir / "download_log.csv"
    manager = MetadataManager(meta_json, log_csv)
    
    config = {
        "id": "recipe1m",
        "name": "Recipe1M+",
        "domain": "structured",
        "path": "structured/recipe1m",
        "official_source": "http://example.com/recipe1m",
        "license": "Academic",
        "file_type": "json",
        "access_mode": "Manual"
    }
    
    # Instantiate dummy collector
    collector = DummyCollector(
        config=config,
        system_config={"rate_limit_delay": 0.5},
        metadata_manager=manager,
        http_client=None,
        project_root=temp_dir
    )
    
    # Mark as manual
    collector.mark_manual("User registration required")
    
    # Verify metadata registry
    with open(meta_json, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["Dataset Name"] == "Recipe1M+"
        assert data[0]["Status"] == "Manual Download Required"
