"""
Production Inference Engine for Functional Role Prediction
Loads champion joblib artifact, applies hybrid feature extraction,
and returns prediction with class probability and confidence uncertainty.
"""
import os
import joblib
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, List
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ARTIFACT_PATH = ROOT_DIR / "ml" / "artifacts" / "functional_role_classifier.joblib"

import sys
sys.path.insert(0, str(ROOT_DIR / "ml" / "features"))
from feature_engineering import HybridIngredientFeatureExtractor, NUMERIC_FEATURE_NAMES

class FunctionalRolePredictor:
    def __init__(self, artifact_path: Optional[Path] = None):
        self.artifact_path = artifact_path or ARTIFACT_PATH
        self.artifact = None
        self.model = None
        self.feature_extractor = None
        self.label_encoder = None
        self.classes: List[str] = []
        self._cache = {}
        self._load_model()

    def _load_model(self):
        if self.artifact_path.exists():
            try:
                self.artifact = joblib.load(self.artifact_path)
                self.model = self.artifact["model"]
                if hasattr(self.model, "n_jobs"):
                    self.model.n_jobs = 1  # Optimize for low-latency single item inference
                self.feature_extractor = self.artifact.get("feature_extractor")
                self.label_encoder = self.artifact["label_encoder"]
                self.classes = list(self.label_encoder.classes_)
            except Exception as e:
                print(f"[FunctionalRolePredictor] Warning loading model: {e}")

    def predict(self, ingredient_dict: Dict[str, Any]) -> str:
        """Predicts the most probable functional role for an ingredient."""
        pred, _ = self.predict_with_uncertainty(ingredient_dict)
        return pred

    def predict_with_uncertainty(self, ingredient_dict: Dict[str, Any]) -> Tuple[str, float]:
        """
        Predicts the functional role and returns (prediction, confidence_probability).
        Falls back to provided role or 'Bulking Agent' if model is not loaded.
        """
        if not self.model or not self.feature_extractor:
            return ingredient_dict.get("functional_role", "Bulking Agent"), 0.50

        cache_key = (
            str(ingredient_dict.get("name", "")).strip().lower(),
            str(ingredient_dict.get("category", "")).strip().lower()
        )
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            X = self.feature_extractor.transform_single(ingredient_dict)
            if hasattr(self.model, "predict_proba"):
                probs = self.model.predict_proba(X)[0]
                top_idx = int(np.argmax(probs))
                confidence = float(probs[top_idx])
                pred_class = self.label_encoder.inverse_transform([top_idx])[0]
            else:
                pred_idx = self.model.predict(X)[0]
                pred_class = self.label_encoder.inverse_transform([pred_idx])[0]
                confidence = 1.0

            res = (str(pred_class), round(confidence, 4))
            self._cache[cache_key] = res
            return res
        except Exception as e:
            print(f"[FunctionalRolePredictor] Prediction fallback due to error: {e}")
            return ingredient_dict.get("functional_role", "Bulking Agent"), 0.50

    def metadata(self) -> Dict[str, Any]:
        return {
            "model_name": self.artifact.get("model_name", "Unknown") if self.artifact else "None",
            "classes": self.classes,
            "version": "2.0.0",
            "status": "LOADED" if self.model else "UNAVAILABLE"
        }

# Global singleton
functional_predictor = FunctionalRolePredictor()
