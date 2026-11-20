"""
Feature Engineering Subsystem for Food Formulation Platform
Provides versioned, leakage-free feature extraction combining quantitative
macronutrient ratios and sub-word character n-gram TF-IDF representations.
Zero text-based regex binary indicators to prevent target leakage.
"""
from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from scipy.sparse import hstack

# Quantitative nutritional composition features
NUMERIC_FEATURE_NAMES = [
    "protein",
    "fat",
    "carbs",
    "calories",
    "protein_ratio",
    "fat_ratio",
    "carb_ratio",
    "caloric_density",
    "macro_dominance",
    "energy_per_gram"
]

def extract_numeric_features(record: Dict[str, Any]) -> List[float]:
    """
    Extracts strictly quantitative feature vector from an ingredient's nutritional composition.
    Protects against missing values, division by zero, and numerical out-of-range artifacts.
    """
    protein = float(record.get("protein", 0.0) or 0.0)
    fat = float(record.get("fat", 0.0) or 0.0)
    carbs = float(record.get("carbs", 0.0) or 0.0)
    calories = float(record.get("calories", 0.0) or 0.0)

    # Physical validity bounding
    protein = max(0.0, min(100.0, protein))
    fat = max(0.0, min(100.0, fat))
    carbs = max(0.0, min(100.0, carbs))
    calories = max(0.0, calories)

    total_macro = protein + fat + carbs + 1e-6
    
    protein_ratio = protein / total_macro
    fat_ratio = fat / total_macro
    carb_ratio = carbs / total_macro
    caloric_density = calories / (total_macro + 1.0)
    macro_dominance = max(protein, fat, carbs) / total_macro
    energy_per_gram = calories / 100.0

    return [
        protein,
        fat,
        carbs,
        calories,
        protein_ratio,
        fat_ratio,
        carb_ratio,
        caloric_density,
        macro_dominance,
        energy_per_gram
    ]

def extract_numeric_matrix(df: pd.DataFrame) -> np.ndarray:
    """Batch extracts numeric feature matrix from a DataFrame."""
    rows = [extract_numeric_features(r) for r in df.to_dict(orient="records")]
    return np.array(rows, dtype=np.float32)

class HybridIngredientFeatureExtractor:
    """
    Hybrid feature pipeline combining standard-scaled macronutrient ratios
    with a character n-gram TF-IDF vectorizer fit exclusively on training data.
    """
    def __init__(self, max_tfidf_features: int = 150):
        self.max_tfidf_features = max_tfidf_features
        self.scaler = StandardScaler()
        self.tfidf = TfidfVectorizer(
            ngram_range=(3, 5),
            analyzer="char_wb",
            max_features=max_tfidf_features,
            sublinear_tf=True
        )
        self.is_fitted = False

    def fit(self, df: pd.DataFrame) -> "HybridIngredientFeatureExtractor":
        """Fits scaler on numeric features and TF-IDF on names strictly on training split."""
        num_feats = extract_numeric_matrix(df)
        self.scaler.fit(num_feats)
        
        names = df["name"].astype(str).tolist()
        self.tfidf.fit(names)
        self.is_fitted = True
        return self

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """Transforms DataFrame into combined dense feature matrix."""
        if not self.is_fitted:
            raise RuntimeError("HybridIngredientFeatureExtractor must be fitted before transform.")
        
        num_feats = extract_numeric_matrix(df)
        num_scaled = self.scaler.transform(num_feats)
        
        names = df["name"].astype(str).tolist()
        tfidf_feats = self.tfidf.transform(names)
        
        return hstack([num_scaled, tfidf_feats]).toarray()

    def transform_single(self, record: Dict[str, Any]) -> np.ndarray:
        """Transforms a single ingredient record for inference."""
        if not self.is_fitted:
            raise RuntimeError("HybridIngredientFeatureExtractor must be fitted before transform.")
            
        num_feats = np.array([extract_numeric_features(record)], dtype=np.float32)
        num_scaled = self.scaler.transform(num_feats)
        
        name = str(record.get("name", ""))
        tfidf_feats = self.tfidf.transform([name])
        
        return hstack([num_scaled, tfidf_feats]).toarray()
