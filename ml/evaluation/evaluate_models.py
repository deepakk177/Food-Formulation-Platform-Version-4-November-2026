"""
Independent Model Evaluation on Untouched Test Set (Phase 4 & 5: Reproducible Evaluation)
Evaluates the champion model on the out-of-sample Test Set (15% held-out test data),
generating classification metrics, confusion matrices, and per-class reports.
"""
import os
import json
import joblib
from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score,
    f1_score, precision_score, recall_score,
    classification_report, confusion_matrix
)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
ARTIFACTS_DIR = ROOT_DIR / "ml" / "artifacts"

import sys
sys.path.insert(0, str(ROOT_DIR / "ml" / "features"))
from feature_engineering import HybridIngredientFeatureExtractor, NUMERIC_FEATURE_NAMES

def evaluate_on_test_set():
    print("[ML Evaluation] Loading champion model artifact and held-out test set...")
    model_path = ARTIFACTS_DIR / "functional_role_classifier.joblib"
    test_path = DATA_DIR / "test" / "test.csv"

    if not model_path.exists():
        raise FileNotFoundError(f"Model artifact not found at {model_path}")
    if not test_path.exists():
        raise FileNotFoundError(f"Test dataset not found at {test_path}")

    artifact = joblib.load(model_path)
    model = artifact["model"]
    feature_extractor = artifact["feature_extractor"]
    label_encoder = artifact["label_encoder"]
    model_name = artifact["model_name"]

    test_df = pd.read_csv(test_path)
    
    # Filter only known classes for evaluation
    known_classes = set(label_encoder.classes_)
    test_clean = test_df[test_df["functional_role"].isin(known_classes)].reset_index(drop=True)
    
    y_test = label_encoder.transform(test_clean["functional_role"].astype(str))
    X_test = feature_extractor.transform(test_clean)
    
    print(f"[ML Evaluation] Evaluating model '{model_name}' on {X_test.shape[0]} untouched test samples...")
    y_pred = model.predict(X_test)

    # Compute metrics
    acc = float(accuracy_score(y_test, y_pred))
    bal_acc = float(balanced_accuracy_score(y_test, y_pred))
    f1_macro = float(f1_score(y_test, y_pred, average="macro", zero_division=0))
    f1_weighted = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))
    prec_macro = float(precision_score(y_test, y_pred, average="macro", zero_division=0))
    rec_macro = float(recall_score(y_test, y_pred, average="macro", zero_division=0))

    target_names = [str(c) for c in label_encoder.classes_]
    clf_report = classification_report(
        y_test, y_pred,
        target_names=target_names,
        output_dict=True,
        zero_division=0
    )
    cm = confusion_matrix(y_test, y_pred).tolist()

    report = {
        "model_name": model_name,
        "test_samples": len(test_clean),
        "metrics": {
            "accuracy": round(acc, 4),
            "balanced_accuracy": round(bal_acc, 4),
            "f1_macro": round(f1_macro, 4),
            "f1_weighted": round(f1_weighted, 4),
            "precision_macro": round(prec_macro, 4),
            "recall_macro": round(rec_macro, 4)
        },
        "per_class_metrics": clf_report,
        "confusion_matrix": cm,
        "classes": target_names
    }

    report_path = ARTIFACTS_DIR / "test_evaluation_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"\n[ML Evaluation] Test Evaluation Results:")
    print(f"   - Accuracy:          {acc:.4%}")
    print(f"   - Balanced Accuracy: {bal_acc:.4%}")
    print(f"   - F1 (Macro):        {f1_macro:.4f}")
    print(f"   - F1 (Weighted):     {f1_weighted:.4f}")
    print(f"   - Precision (Macro): {prec_macro:.4f}")
    print(f"   - Recall (Macro):    {rec_macro:.4f}")
    print(f"[ML Evaluation] Report saved to {report_path}")
    return report

if __name__ == "__main__":
    evaluate_on_test_set()
