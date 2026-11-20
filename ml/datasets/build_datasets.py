"""
Reproducible Data Pipeline for Food Formulation Platform
Reads raw food ingredient datasets and Knowledge Graph nodes, cleans data,
removes non-food artifacts, maps into standardized functional classes,
downsamples majority imputation bias, and creates strictly separated
train (70%), validation (15%), and test (15%) splits with zero leakage.
"""
import os
import json
import shutil
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

RANDOM_SEED = 42
PREPROCESSING_VERSION = "v2.0.0"
DATASET_VERSION = "2026.11.04"

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
FEATURES_DIR = DATA_DIR / "features"
TRAINING_DIR = DATA_DIR / "training"
VAL_DIR = DATA_DIR / "validation"
TEST_DIR = DATA_DIR / "test"

for d in [RAW_DIR, PROCESSED_DIR, FEATURES_DIR, TRAINING_DIR, VAL_DIR, TEST_DIR]:
    d.mkdir(parents=True, exist_ok=True)

import sys
sys.path.insert(0, str(ROOT_DIR / "Food Web App Core" / "backend"))
import repository

def map_canonical_role(role_raw: str, name_raw: str, protein: float, fat: float, carbs: float) -> str:
    """Standardizes heterogeneous raw roles into 8 canonical food formulation roles."""
    r = str(role_raw).lower()
    n = str(name_raw).lower()
    
    if "protein" in r or ("isolate" in n and protein >= 40) or (protein >= 25 and carbs < 45):
        return "Protein Source"
    if "lipid" in r or "fats & oils" in r or fat >= 30:
        return "Lipid Source"
    if "sweetener" in r or any(s in n for s in ["sugar", "allulose", "erythritol", "stevia", "monk", "syrup"]):
        return "Sweetener"
    if any(e in r for e in ["emulsifier", "surfactant"]) or any(e in n for e in ["lecithin", "phosphatide", "pgpr", "glyceride"]):
        return "Emulsifier"
    if any(s in r for s in ["stabilizer", "thickener", "gelling", "hydrocolloid"]) or any(s in n for s in ["gum", "pectin", "agar", "alginate", "carrageenan"]):
        return "Hydrocolloid & Stabilizer"
    if any(a in r for a in ["acidity", "acid", "preservat", "antioxidant"]) or any(a in n for a in ["citric", "sorbate", "benzoate", "tocopherol"]):
        return "Acidity & Preservation"
    if any(f in r for f in ["flavor", "cocoa", "salt"]) or any(f in n for f in ["vanilla", "cocoa powder", "salt", "extract"]):
        return "Flavor System"
    return "Bulking Agent"

def build_data_pipeline():
    print("[DataPipeline] Starting reproducible dataset preparation...")
    
    # 1. Locate raw ingredient dataset
    source_csv = ROOT_DIR / "Food Web App Core" / "backend" / "food_ingredients_clean.csv"
    if not source_csv.exists():
        raise FileNotFoundError(f"Source ingredient dataset not found at {source_csv}")

    # Copy raw snapshot
    target_raw = RAW_DIR / "food_ingredients_raw.csv"
    shutil.copyfile(source_csv, target_raw)
    print(f"[DataPipeline] Copied raw snapshot to {target_raw}")

    raw_df = pd.read_csv(target_raw)
    
    # 2. Filter out non-food ontological artifacts
    noise_patterns = [
        "extrusion", "casing", "obsolete", "cultivar", "mackerel", "cockle",
        "hazard", "formula for", "dietary use", "waterfly", "non-carbonated water", "wax pepper"
    ]
    is_noise = raw_df["name"].astype(str).str.lower().str.contains("|".join(noise_patterns))
    clean_df = raw_df[~is_noise].copy()
    
    # Numeric sanitization
    for col in ["protein", "fat", "carbs", "calories"]:
        clean_df[col] = pd.to_numeric(clean_df[col], errors="coerce").fillna(0.0).clip(lower=0.0)

    # 3. Canonical Role Mapping
    clean_df["functional_role"] = [
        map_canonical_role(row["functional_role"], row["name"], row["protein"], row["fat"], row["carbs"])
        for _, row in clean_df.iterrows()
    ]

    # 4. Integrate 58 curated industrial seed ingredients from repository
    seed_rows = []
    for s in repository.SEED_INGREDIENTS:
        seed_rows.append({
            "name": s["name"],
            "category": s["category"],
            "protein": float(s.get("protein", 0.0)),
            "fat": float(s.get("fat", 0.0)),
            "carbs": float(s.get("carbs", 0.0)),
            "calories": float(s.get("energy", 0.0)),
            "functional_role": map_canonical_role(s["functional_role"], s["name"], s.get("protein", 0), s.get("fat", 0), s.get("carbs", 0)),
            "allergen": str(s.get("allergens", "None"))
        })
    seeds_df = pd.DataFrame(seed_rows)
    
    # Combine seeds with non-bulking and downsampled bulking
    non_bulking = clean_df[clean_df["functional_role"] != "Bulking Agent"]
    bulking = clean_df[clean_df["functional_role"] == "Bulking Agent"].sample(n=1000, random_state=RANDOM_SEED)

    curated_df = pd.concat([seeds_df, non_bulking, bulking], ignore_index=True)
    # Deduplicate by ingredient name
    curated_df = curated_df.drop_duplicates(subset=["name"]).reset_index(drop=True)
    
    # Save processed
    processed_path = PROCESSED_DIR / "food_ingredients_processed.csv"
    curated_df.to_csv(processed_path, index=False)
    print(f"[DataPipeline] Curated dataset size: {len(curated_df)} rows")
    print(f"[DataPipeline] Class distribution:\n{curated_df['functional_role'].value_counts()}")

    # 5. Strict Stratified Train (70%) / Validation (15%) / Test (15%) Separation
    y = curated_df["functional_role"]
    
    # Stratified split 1: 85% train+val, 15% untouched test
    train_val_df, test_df = train_test_split(
        curated_df,
        test_size=0.15,
        stratify=y,
        random_state=RANDOM_SEED
    )
    
    # Stratified split 2: 70% train, 15% validation (0.15 / 0.85 = ~0.1765)
    train_df, val_df = train_test_split(
        train_val_df,
        test_size=0.17647,
        stratify=train_val_df["functional_role"],
        random_state=RANDOM_SEED
    )

    # Persist splits
    train_path = TRAINING_DIR / "train.csv"
    val_path = VAL_DIR / "val.csv"
    test_path = TEST_DIR / "test.csv"

    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path, index=False)
    test_df.to_csv(test_path, index=False)

    metadata = {
        "dataset_version": DATASET_VERSION,
        "preprocessing_version": PREPROCESSING_VERSION,
        "total_curated_samples": len(curated_df),
        "train_samples": len(train_df),
        "validation_samples": len(val_df),
        "test_samples": len(test_df),
        "random_seed": RANDOM_SEED,
        "classes": sorted(curated_df["functional_role"].unique().tolist()),
        "class_counts": curated_df["functional_role"].value_counts().to_dict()
    }
    with open(FEATURES_DIR / "dataset_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"[DataPipeline] Dataset split complete:")
    print(f"   - Train:      {len(train_df)} samples ({train_path})")
    print(f"   - Validation: {len(val_df)} samples ({val_path})")
    print(f"   - Test:       {len(test_df)} samples ({test_path})")

if __name__ == "__main__":
    build_data_pipeline()
