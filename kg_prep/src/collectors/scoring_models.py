import json
import logging
from pathlib import Path
from typing import List
from src.base_collector import BaseCollector

logger = logging.getLogger("Collector.ScoringModels")

class ScoringModelsCollector(BaseCollector):
    """
    Collector for Dietary and Nutrition Scoring Methodologies:
    1. Food Patterns Equivalents Database (FPED)
    2. Healthy Eating Index (HEI)
    3. Nutri-Score Algorithm Rules
    4. Health Star Rating (HSR) Algorithm Rules
    """
    async def collect(self) -> List[Path]:
        target_file = self.dest_dir / "scoring_model_definitions.json"
        if target_file.exists():
            self.logger.info(f"Scoring models dataset already present at {target_file}")
            self.register_file(target_file, "Success", remarks="Pre-existing scoring model definitions.")
            return [target_file]

        scoring_definitions = [
            {
                "source_record_id": "FPED_2020",
                "model_name": "Food Patterns Equivalents Database (FPED)",
                "provider": "USDA ARS",
                "model_type": "DIETARY_EQUIVALENTS",
                "components": ["Fruit_Cup_Eq", "Vegetable_Cup_Eq", "Grain_Oz_Eq", "Dairy_Cup_Eq", "Protein_Oz_Eq"],
                "version": "2019-2020",
                "source_reference": "USDA Agricultural Research Service FPED"
            },
            {
                "source_record_id": "HEI_2020",
                "model_name": "Healthy Eating Index (HEI)",
                "provider": "USDA CNPP / NCI",
                "model_type": "DIET_QUALITY_SCORE",
                "components": ["Total Fruit", "Whole Fruit", "Total Vegetables", "Greens and Beans", "Whole Grains", "Dairy", "Total Protein", "Seafood and Plant Proteins", "Fatty Acids"],
                "max_score": 100,
                "version": "HEI-2020",
                "source_reference": "USDA CNPP Healthy Eating Index"
            },
            {
                "source_record_id": "NUTRI_SCORE_2023",
                "model_name": "Nutri-Score",
                "provider": "Santé Publique France",
                "model_type": "FRONT_OF_PACK_NUTRITION_SCORE",
                "negative_components": ["Energy (kJ)", "Saturated Fatty Acids (g)", "Sugars (g)", "Sodium (mg)"],
                "positive_components": ["Fruits/Vegetables/Legumes/Nuts (%)", "Fibre (g)", "Protein (g)"],
                "rating_categories": ["A", "B", "C", "D", "E"],
                "version": "2023 Revision",
                "source_reference": "Official Nutri-Score Governance"
            },
            {
                "source_record_id": "HSR_2022",
                "model_name": "Health Star Rating",
                "provider": "Australian / New Zealand Food Regulation Standing Committee",
                "model_type": "STAR_RATING_SCORE",
                "components": ["Risk Component (Energy, SatFat, Sugars, Sodium)", "Positive Component (FVNL, Fibre, Protein)"],
                "rating_range": [0.5, 5.0],
                "version": "2022 Guide",
                "source_reference": "Health Star Rating System Implementation Guide"
            }
        ]

        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(scoring_definitions, f, indent=4)

        self.register_file(target_file, "Success", remarks="Acquired FPED, HEI, Nutri-Score, and HSR scoring methodologies.")
        return [target_file]
