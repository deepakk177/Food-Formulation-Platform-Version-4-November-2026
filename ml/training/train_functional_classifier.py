"""
Supervised Model Training Pipeline for Ingredient Functional Role Classification
Trains and compares baseline model candidates on strictly separated training data,
evaluates on validation data using Balanced Accuracy and Macro F1, selects the champion model,
and persists versioned artifacts to ml/artifacts/.
"""
import os
import json
import joblib
from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score,
    f1_score, precision_score, recall_score,
    classification_report
)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
ARTIFACTS_DIR = ROOT_DIR / "ml" / "artifacts"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

import sys
sys.path.insert(0, str(ROOT_DIR / "ml" / "features"))
from feature_engineering import HybridIngredientFeatureExtractor, NUMERIC_FEATURE_NAMES

RANDOM_SEED = 42

def train_and_compare_models():
    print("[ML Training] Loading train and validation datasets...")
    train_path = DATA_DIR / "training" / "train.csv"
    val_path = DATA_DIR / "validation" / "val.csv"
    
    if not train_path.exists() or not val_path.exists():
        raise FileNotFoundError(f"Train/Val files not found at {train_path} or {val_path}")

    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)

    # Encode target labels
    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(train_df["functional_role"].astype(str))
    
    # Handle unseen validation labels safely
    known_classes = set(label_encoder.classes_)
    val_clean = val_df[val_df["functional_role"].isin(known_classes)].reset_index(drop=True)
    y_val = label_encoder.transform(val_clean["functional_role"].astype(str))

    # Fit feature extractor strictly on training split
    print("[ML Training] Fitting HybridIngredientFeatureExtractor (Nutritional Ratios + Character TF-IDF)...")
    feature_extractor = HybridIngredientFeatureExtractor(max_tfidf_features=150)
    feature_extractor.fit(train_df)

    X_train = feature_extractor.transform(train_df)
    X_val = feature_extractor.transform(val_clean)

    print(f"[ML Training] Training samples: {X_train.shape[0]}, Features: {X_train.shape[1]}")
    print(f"[ML Training] Validation samples: {X_val.shape[0]}")
    print(f"[ML Training] Target classes ({len(label_encoder.classes_)}): {list(label_encoder.classes_)}")

    # Model Candidates & Baselines
    candidates = {
        "Baseline_StratifiedDummy": DummyClassifier(
            strategy="stratified",
            random_state=RANDOM_SEED
        ),
        "Baseline_MostFrequentDummy": DummyClassifier(
            strategy="most_frequent"
        ),
        "LogisticRegression_Balanced": LogisticRegression(
            C=2.0,
            max_iter=1500,
            class_weight="balanced",
            random_state=RANDOM_SEED
        ),
        "RandomForest_Balanced": RandomForestClassifier(
            n_estimators=150,
            max_depth=14,
            class_weight="balanced",
            random_state=RANDOM_SEED,
            n_jobs=-1
        ),
        "HistGradientBoosting": HistGradientBoostingClassifier(
            max_iter=150,
            random_state=RANDOM_SEED
        )
    }

    results = {}
    fitted_models = {}

    for name, model in candidates.items():
        print(f"\n[ML Training] Fitting candidate model: {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)

        acc = float(accuracy_score(y_val, y_pred))
        bal_acc = float(balanced_accuracy_score(y_val, y_pred))
        f1_macro = float(f1_score(y_val, y_pred, average="macro", zero_division=0))
        f1_weighted = float(f1_score(y_val, y_pred, average="weighted", zero_division=0))
        prec_macro = float(precision_score(y_val, y_pred, average="macro", zero_division=0))
        rec_macro = float(recall_score(y_val, y_pred, average="macro", zero_division=0))

        results[name] = {
            "accuracy": round(acc, 4),
            "balanced_accuracy": round(bal_acc, 4),
            "f1_macro": round(f1_macro, 4),
            "f1_weighted": round(f1_weighted, 4),
            "precision_macro": round(prec_macro, 4),
            "recall_macro": round(rec_macro, 4)
        }
        fitted_models[name] = model

        print(f"   -> Accuracy:          {acc:.4%}")
        print(f"   -> Balanced Accuracy: {bal_acc:.4%}")
        print(f"   -> Macro F1:          {f1_macro:.4f}")
        print(f"   -> Weighted F1:       {f1_weighted:.4f}")

    # Model Selection: Champion has highest Macro F1 on validation set (excluding dummies)
    non_dummy_candidates = [k for k in candidates.keys() if "Dummy" not in k]
    best_candidate_name = max(non_dummy_candidates, key=lambda k: results[k]["f1_macro"])
    best_model = fitted_models[best_candidate_name]
    best_metrics = results[best_candidate_name]

    print(f"\n[ML Training] Selected Champion Model: {best_candidate_name}")
    print(f"   -> Champion Validation Macro F1: {best_metrics['f1_macro']:.4f}")
    print(f"   -> Champion Balanced Accuracy:   {best_metrics['balanced_accuracy']:.4%}")

    # Persist Champion Artifact
    artifact = {
        "model_name": best_candidate_name,
        "model": best_model,
        "feature_extractor": feature_extractor,
        "label_encoder": label_encoder,
        "classes": list(label_encoder.classes_),
        "numeric_features": NUMERIC_FEATURE_NAMES,
        "version": "2.0.0",
        "validation_metrics": best_metrics
    }

    artifact_path = ARTIFACTS_DIR / "functional_role_classifier.joblib"
    joblib.dump(artifact, artifact_path)
    print(f"[ML Training] Champion artifact saved to: {artifact_path}")

    # Persist Metrics Report
    metrics_path = ARTIFACTS_DIR / "metrics.json"
    metrics_data = {
        "best_model": best_candidate_name,
        "validation_metrics": best_metrics,
        "all_candidates": results,
        "feature_schema": NUMERIC_FEATURE_NAMES,
        "classes": list(label_encoder.classes_)
    }
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=2)
    print(f"[ML Training] Metrics report saved to: {metrics_path}")

    return artifact

if __name__ == "__main__":
    train_and_compare_models()
