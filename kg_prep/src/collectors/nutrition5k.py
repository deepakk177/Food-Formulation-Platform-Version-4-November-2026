from pathlib import Path
from typing import List
from src.base_collector import BaseCollector

class Nutrition5KCollector(BaseCollector):
    """
    Nutrition5K Collector: Since Nutrition5K contains large datasets (images + video features)
    hosted on Google Cloud Storage via GitHub, it requires manual downloading or specialized
    CLI commands to copy objects. This registers the source in Manual Mode.
    """
    async def collect(self) -> List[Path]:
        remarks = (
            "Manual Download Required: Nutrition5K dataset contains large-scale video features "
            "and food images. Please follow the download instructions at the official repo: "
            "https://github.com/google-research-datasets/Nutrition5k. "
            "Once downloaded, place the metadata CSVs (e.g., dish_metadata_cafe1.csv, "
            f"dish_metadata_cafe2.csv) and JSON structures under: {self.dest_dir}"
        )
        return self.mark_manual(remarks=remarks)
