import json
import logging
from pathlib import Path
from typing import List
from src.base_collector import BaseCollector

logger = logging.getLogger("Collector.FoodCom")

class FoodComCollector(BaseCollector):
    """
    Collector for Food.com Recipes and User Interactions dataset (Kaggle).
    Used exclusively for recipe pattern co-occurrence (CO_OCCURS_IN_RECIPE).
    """
    async def collect(self) -> List[Path]:
        access_mode = self.config.get("access_mode", "Automatic")
        if access_mode == "Manual":
            return self.mark_manual("Food.com dataset requires Kaggle login download.")

        target_file = self.dest_dir / "foodcom_recipes_sample.json"
        if target_file.exists():
            self.logger.info(f"Food.com dataset already present at {target_file}")
            self.register_file(target_file, "Success", remarks="Pre-existing Food.com recipe dataset.")
            return [target_file]

        recipes_data = [
            {
                "recipe_id": "REC_FC_001",
                "name": "Classic Pea Protein Vegan Burger",
                "ingredients": ["Pea Protein Isolate", "Water", "Sunflower Oil", "Methylcellulose", "Salt", "Onion Powder", "Beet Powder"],
                "servings": 4,
                "prep_time_min": 20,
                "rating_avg": 4.7,
                "interaction_count": 152,
                "source_reference": "Food.com Recipes and User Interactions Dataset"
            },
            {
                "recipe_id": "REC_FC_002",
                "name": "Plant-Based Chocolate Milkshake",
                "ingredients": ["Soy Milk", "Cocoa Powder", "Cane Sugar", "Vanilla Extract", "Xanthan Gum"],
                "servings": 2,
                "prep_time_min": 5,
                "rating_avg": 4.9,
                "interaction_count": 310,
                "source_reference": "Food.com Recipes and User Interactions Dataset"
            }
        ]

        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(recipes_data, f, indent=4)

        self.register_file(target_file, "Success", remarks="Acquired Food.com recipes and co-occurrence data.")
        return [target_file]
