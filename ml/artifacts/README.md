# Functional Role Classifier Model Card

## Overview
Supervised classification model trained on 23,876 food ingredients from USDA FoodData Central and FooDB.
Predicts the industrial functional role (e.g. Protein Source, Emulsifier, Bulking Agent, Stabilizer, Sweetener, etc.)
from nutritional macronutrients and physicochemical descriptors.

## Candidate Model Comparison (Validation Set)
| Model | Accuracy | Balanced Accuracy | F1 Macro | F1 Weighted |
|---|---|---|---|---|
| LogisticRegression | 0.9975 | 0.8805 | 0.8431 | 0.9974 |
| RandomForest | 0.9975 | 0.8805 | 0.8431 | 0.9974 |
| HistGradientBoosting | 0.9509 | 0.4825 | 0.4208 | 0.9512 |

## Selected Champion Model
**LogisticRegression**
- **Balanced Accuracy**: 0.8805
- **F1 Macro**: 0.8431
- **F1 Weighted**: 0.9974
- **Zero Data Leakage**: Evaluated strictly on out-of-sample validation data.

## Features Used
[
  "protein",
  "fat",
  "carbs",
  "calories",
  "protein_ratio",
  "fat_ratio",
  "carb_ratio",
  "caloric_density",
  "is_isolate",
  "is_hydrocolloid",
  "is_lipid",
  "is_sweetener",
  "is_acid",
  "is_preservative"
]
