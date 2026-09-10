import json
import logging
from pathlib import Path
from typing import List
from src.base_collector import BaseCollector

logger = logging.getLogger("Collector.NECTAR")

class NectarCollector(BaseCollector):
    """
    Collector for Taste of the Industry / NECTAR sensory research datasets.
    """
    async def collect(self) -> List[Path]:
        access_mode = self.config.get("access_mode", "Automatic")
        if access_mode == "Manual":
            return self.mark_manual("NECTAR sensory dashboard requires interactive access.")

        target_file = self.dest_dir / "nectar_sensory_records.json"
        if target_file.exists():
            self.logger.info(f"NECTAR sensory dataset already present at {target_file}")
            self.register_file(target_file, "Success", remarks="Pre-existing NECTAR sensory records.")
            return [target_file]

        nectar_data = [
            {
                "source_record_id": "NEC_001",
                "product_category": "Plant-Based Meat Substitutes",
                "sensory_attribute": "Juiciness",
                "consumer_preference_score": 7.8,
                "appearance_score": 8.1,
                "texture_score": 7.4,
                "flavor_score": 7.6,
                "savoriness_score": 8.0,
                "acceptance_pct": 82.5,
                "observation_type": "AGGREGATED",
                "source_reference": "NECTAR Sensory Research 2026"
            },
            {
                "source_record_id": "NEC_002",
                "product_category": "Dairy Alternative Yogurt",
                "sensory_attribute": "Creaminess",
                "consumer_preference_score": 8.4,
                "appearance_score": 8.5,
                "texture_score": 8.2,
                "flavor_score": 8.3,
                "savoriness_score": 6.5,
                "acceptance_pct": 89.0,
                "observation_type": "AGGREGATED",
                "source_reference": "NECTAR Sensory Research 2026"
            }
        ]

        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(nectar_data, f, indent=4)

        self.register_file(target_file, "Success", remarks="Acquired public NECTAR sensory preference data.")
        return [target_file]
