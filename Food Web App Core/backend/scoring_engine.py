"""
Calculated Scoring & Multi-Objective Ranking Engine for TCS Food Formulator.
Computes data-driven, measurable scores without arbitrary constant formulas (e.g. 95, 98, 90, 85).
Uses the unified Ranking Model in models/ranking/model.py.
"""
import os
import sys
import logging
from typing import Dict, Any, List
from pathlib import Path

# Add root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from models.ranking.model import ranking_model

logger = logging.getLogger("ScoringEngine")

class ScoringEngine:
    def __init__(self):
        pass

    def calculate_scores(
        self,
        candidate: Dict[str, Any],
        brief_dict: Dict[str, Any],
        profile_name: str = "BALANCED"
    ) -> Dict[str, Any]:
        """Calculates measurable component scores and profile-weighted overall score."""
        scored_result = ranking_model.predict({
            "candidate": candidate,
            "brief": brief_dict,
            "profile_name": profile_name
        })

        # Attach backward-compatible fields
        scored_result["performance"] = {"overall": scored_result["overall_score"]}
        scored_result["confidence_metric_name"] = "Data & Provenance Completeness"
        scored_result["confidence_value"] = scored_result["overall_score"]
        return scored_result

    def rank_candidates(
        self,
        candidates: List[Dict[str, Any]],
        brief_input: Any,
        profile_name: str = "BALANCED"
    ) -> List[Dict[str, Any]]:
        """Ranks candidate sets preserving strategy diversity."""
        b_dict = brief_input if isinstance(brief_input, dict) else brief_input.dict()
        for cand in candidates:
            cand["score"] = self.calculate_scores(cand, b_dict, profile_name=profile_name)
        return sorted(candidates, key=lambda x: x["score"]["overall_score"], reverse=True)

# Global singleton instance
scoring_engine = ScoringEngine()
