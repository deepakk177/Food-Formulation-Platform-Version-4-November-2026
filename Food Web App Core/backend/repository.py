"""
Repository & SQLite Data Layer for TCS Food Formulator
Manages seed datasets, SQLite tables (ingredients, taxonomy, compatibility, evidence, formulations),
and deterministic data access functions.
"""
import os
import json
import sqlite3
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger("Repository")

DB_PATH = Path(__file__).resolve().parent / "tcs_food_formulator_kg.db"

SEED_INGREDIENTS = [
    # --- PROTEINS ---
    {
        "id": "ing_pea_protein",
        "name": "Pea Protein Isolate (85%)",
        "category": "Proteins",
        "functional_role": "Protein Source",
        "min_inclusion": 2.0, "max_inclusion": 35.0,
        "cost_per_kg": 12.40,
        "protein": 85.0, "fat": 4.0, "saturated_fat": 1.0, "carbs": 2.0, "sugar": 0.0, "fibre": 4.0, "sodium": 1100.0, "energy": 380.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.8, "water_binding": 0.9, "gelation": 0.6, "thickening": 0.7,
        "texture_impact": "Dense, Firm, Smooth", "flavor_profile": "Neutral, Earthy",
        "evidence_claim": "Provides high solubility and non-allergenic protein enrichment.",
        "evidence_source": "USDA FDC / Journal of Food Science 2023"
    },
    {
        "id": "ing_soy_protein",
        "name": "Soy Protein Isolate",
        "category": "Proteins",
        "functional_role": "Protein Source",
        "min_inclusion": 2.0, "max_inclusion": 30.0,
        "cost_per_kg": 10.80,
        "protein": 90.0, "fat": 1.0, "saturated_fat": 0.2, "carbs": 1.0, "sugar": 0.0, "fibre": 1.0, "sodium": 1000.0, "energy": 370.0,
        "allergens": "Soy", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.9, "water_binding": 0.8, "gelation": 0.8, "thickening": 0.7,
        "texture_impact": "Firm, Smooth, Elastic", "flavor_profile": "Beany, Neutral",
        "evidence_claim": "Excellent gelation and emulsification properties in protein matrices.",
        "evidence_source": "Food Chemistry Vol 312"
    },
    {
        "id": "ing_whey_protein",
        "name": "Whey Protein Concentrate 80",
        "category": "Proteins",
        "functional_role": "Protein Source",
        "min_inclusion": 1.0, "max_inclusion": 40.0,
        "cost_per_kg": 15.50,
        "protein": 80.0, "fat": 6.0, "saturated_fat": 4.0, "carbs": 5.0, "sugar": 4.0, "fibre": 0.0, "sodium": 160.0, "energy": 400.0,
        "allergens": "Milk", "vegan": 0, "gluten_free": 1, "dairy_free": 0, "halal": 1, "kosher": 1,
        "emulsification": 0.9, "water_binding": 0.7, "gelation": 0.9, "thickening": 0.6,
        "texture_impact": "Smooth, Soft, Creamy", "flavor_profile": "Dairy, Milky",
        "evidence_claim": "High biological value protein with optimal thermal gelling.",
        "evidence_source": "Dairy Science Review 2022"
    },
    {
        "id": "ing_rice_protein",
        "name": "Organic Brown Rice Protein",
        "category": "Proteins",
        "functional_role": "Protein Source",
        "min_inclusion": 2.0, "max_inclusion": 25.0,
        "cost_per_kg": 11.20,
        "protein": 80.0, "fat": 3.0, "saturated_fat": 0.8, "carbs": 7.0, "sugar": 0.0, "fibre": 5.0, "sodium": 200.0, "energy": 380.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.5, "water_binding": 0.6, "gelation": 0.4, "thickening": 0.5,
        "texture_impact": "Powdery, Dense", "flavor_profile": "Grainy, Sweet",
        "evidence_claim": "Hypoallergenic protein rich in sulfur amino acids.",
        "evidence_source": "Cereal Chemistry 2021"
    },
    {
        "id": "ing_fava_protein",
        "name": "Fava Bean Protein Isolate",
        "category": "Proteins",
        "functional_role": "Protein Source",
        "min_inclusion": 2.0, "max_inclusion": 25.0,
        "cost_per_kg": 13.80,
        "protein": 88.0, "fat": 2.0, "saturated_fat": 0.4, "carbs": 3.0, "sugar": 0.0, "fibre": 2.0, "sodium": 850.0, "energy": 375.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.85, "water_binding": 0.8, "gelation": 0.7, "thickening": 0.6,
        "texture_impact": "Smooth, Soft-gel", "flavor_profile": "Neutral, Mild Nutty",
        "evidence_claim": "High solubility pulse protein with superior foaming and emulsifying capacity.",
        "evidence_source": "Plant Foods for Human Nutrition 2023"
    },
    {
        "id": "ing_pumpkin_protein",
        "name": "Organic Pumpkin Seed Protein",
        "category": "Proteins",
        "functional_role": "Protein Source",
        "min_inclusion": 1.0, "max_inclusion": 20.0,
        "cost_per_kg": 16.50,
        "protein": 60.0, "fat": 12.0, "saturated_fat": 2.5, "carbs": 15.0, "sugar": 1.0, "fibre": 11.0, "sodium": 50.0, "energy": 410.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.6, "water_binding": 0.7, "gelation": 0.5, "thickening": 0.5,
        "texture_impact": "Nutty, Rich, Dense", "flavor_profile": "Earthy, Pumpkin Seed",
        "evidence_claim": "Nutrient-dense seed protein high in magnesium, zinc, and arginine.",
        "evidence_source": "Journal of Agricultural and Food Chemistry 2022"
    },

    # --- FIBERS ---
    {
        "id": "ing_soluble_corn_fiber",
        "name": "Soluble Corn Fiber",
        "category": "Fibres",
        "functional_role": "Fiber",
        "min_inclusion": 2.0, "max_inclusion": 30.0,
        "cost_per_kg": 8.50,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 92.0, "sugar": 2.0, "fibre": 85.0, "sodium": 20.0, "energy": 160.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.1, "water_binding": 0.8, "gelation": 0.2, "thickening": 0.5,
        "texture_impact": "Chewy, Soft, Bulking", "flavor_profile": "Neutral, Clean",
        "evidence_claim": "Low-viscosity soluble fiber ideal for sugar replacement and digestive tolerance.",
        "evidence_source": "Nutrition Research Vol 45"
    },
    {
        "id": "ing_chicory_inulin",
        "name": "Chicory Root Inulin Fibre",
        "category": "Fibres",
        "functional_role": "Fiber",
        "min_inclusion": 1.0, "max_inclusion": 20.0,
        "cost_per_kg": 9.20,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 95.0, "sugar": 8.0, "fibre": 87.0, "sodium": 10.0, "energy": 210.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.2, "water_binding": 0.8, "gelation": 0.5, "thickening": 0.7,
        "texture_impact": "Creamy, Smooth, Fudgy", "flavor_profile": "Mild Sweet",
        "evidence_claim": "Prebiotic soluble fibre supporting digestive health and fat mimetic texture.",
        "evidence_source": "EFSA Journal 2015;13(11):4251"
    },
    {
        "id": "ing_oat_fiber",
        "name": "Organic Oat Fiber (90% Fibre)",
        "category": "Fibres",
        "functional_role": "Fiber",
        "min_inclusion": 1.0, "max_inclusion": 15.0,
        "cost_per_kg": 6.80,
        "protein": 0.5, "fat": 0.2, "saturated_fat": 0.0, "carbs": 93.0, "sugar": 0.0, "fibre": 90.0, "sodium": 5.0, "energy": 20.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.1, "water_binding": 1.0, "gelation": 0.1, "thickening": 0.8,
        "texture_impact": "Moist, Soft, Fibrous", "flavor_profile": "Neutral Oat",
        "evidence_claim": "High insoluble fiber for calorie dilution and moisture retention in baked goods.",
        "evidence_source": "Cereal Foods World 2021"
    },

    # --- FATS & OILS ---
    {
        "id": "ing_almond_butter",
        "name": "Almond Butter (Smooth)",
        "category": "Fats & Oils",
        "functional_role": "Fats & Oils",
        "min_inclusion": 3.0, "max_inclusion": 35.0,
        "cost_per_kg": 14.20,
        "protein": 21.0, "fat": 55.0, "saturated_fat": 4.5, "carbs": 18.0, "sugar": 4.0, "fibre": 10.0, "sodium": 10.0, "energy": 610.0,
        "allergens": "Tree Nuts", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.4, "water_binding": 0.3, "gelation": 0.2, "thickening": 0.7,
        "texture_impact": "Creamy, Fudgy, Rich", "flavor_profile": "Nutty, Roasted Almond",
        "evidence_claim": "Heart-healthy monounsaturated fat base providing rich texture and indulgence.",
        "evidence_source": "USDA FDC / American Journal of Clinical Nutrition"
    },
    {
        "id": "ing_cocoa_butter",
        "name": "Prime Press Cocoa Butter",
        "category": "Fats & Oils",
        "functional_role": "Fats & Oils",
        "min_inclusion": 5.0, "max_inclusion": 45.0,
        "cost_per_kg": 18.50,
        "protein": 0.0, "fat": 100.0, "saturated_fat": 60.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 884.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.1, "water_binding": 0.0, "gelation": 1.0, "thickening": 0.2,
        "texture_impact": "Firm, Snappy, Melt-in-mouth", "flavor_profile": "Mild Cocoa",
        "evidence_claim": "Polymorphic fat matrix providing sharp melt point at 34C body temperature.",
        "evidence_source": "Journal of the American Oil Chemists' Society"
    },
    {
        "id": "ing_mct_powder",
        "name": "Coconut MCT Oil Powder (70%)",
        "category": "Fats & Oils",
        "functional_role": "Fats & Oils",
        "min_inclusion": 1.0, "max_inclusion": 20.0,
        "cost_per_kg": 19.50,
        "protein": 0.0, "fat": 70.0, "saturated_fat": 68.0, "carbs": 25.0, "sugar": 0.0, "fibre": 20.0, "sodium": 30.0, "energy": 670.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.7, "water_binding": 0.4, "gelation": 0.1, "thickening": 0.4,
        "texture_impact": "Creamy, Smooth", "flavor_profile": "Clean, Light Coconut",
        "evidence_claim": "Medium chain triglycerides for rapid ketogenic energy and instant dispersibility.",
        "evidence_source": "Journal of Nutrition and Metabolism 2021"
    },
    {
        "id": "ing_sunflower_oil",
        "name": "High Oleic Sunflower Oil",
        "category": "Fats & Oils",
        "functional_role": "Fats & Oils",
        "min_inclusion": 1.0, "max_inclusion": 25.0,
        "cost_per_kg": 5.40,
        "protein": 0.0, "fat": 100.0, "saturated_fat": 9.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 884.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.1, "water_binding": 0.0, "gelation": 0.0, "thickening": 0.2,
        "texture_impact": "Liquid, Tender, Moist", "flavor_profile": "Neutral",
        "evidence_claim": "High oxidative stability liquid lipid rich in oleic acid.",
        "evidence_source": "JAOCS 2020"
    },

    # --- SWEETENERS ---
    {
        "id": "ing_monk_fruit",
        "name": "Monk Fruit Extract (Mogroside V50)",
        "category": "Sweeteners",
        "functional_role": "Sweetener",
        "min_inclusion": 0.01, "max_inclusion": 0.5,
        "cost_per_kg": 45.00,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 0.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.0, "water_binding": 0.0, "gelation": 0.0, "humectancy": 0.0,
        "texture_impact": "None", "flavor_profile": "High Intensity Sweet, Fruity",
        "evidence_claim": "250x sweetness multiplier derived naturally from Siraitia grosvenorii with zero glycemic impact.",
        "evidence_source": "FDA GRAS Notice GRN 000301"
    },
    {
        "id": "ing_allulose",
        "name": "Rare Sugar Allulose",
        "category": "Sweeteners",
        "functional_role": "Sweetener",
        "min_inclusion": 0.5, "max_inclusion": 15.0,
        "cost_per_kg": 12.50,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 99.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 40.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.0, "water_binding": 0.8, "gelation": 0.0, "humectancy": 0.9,
        "texture_impact": "Smooth, Soft, Melt-in-mouth", "flavor_profile": "Clean Sweet",
        "evidence_claim": "70% sugar sweetness with near-zero caloric metabolism and browning caramelization.",
        "evidence_source": "FDA GRAS Notice No. GRN 000498"
    },
    {
        "id": "ing_stevia_reb_m",
        "name": "Stevia Leaf Extract (Reb M 95%)",
        "category": "Sweeteners",
        "functional_role": "Sweetener",
        "min_inclusion": 0.01, "max_inclusion": 0.2,
        "cost_per_kg": 65.00,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 0.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.0, "water_binding": 0.0, "gelation": 0.0, "humectancy": 0.0,
        "texture_impact": "None", "flavor_profile": "Clean High Sweetness",
        "evidence_claim": "Natural high-intensity sweetener with zero calories and clean sugar-like taste profile.",
        "evidence_source": "JECFA Codex Alimentarius"
    },
    {
        "id": "ing_erythritol",
        "name": "Erythritol Polyol",
        "category": "Sweeteners",
        "functional_role": "Sweetener",
        "min_inclusion": 0.5, "max_inclusion": 12.0,
        "cost_per_kg": 6.20,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 100.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 0.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.0, "water_binding": 0.5, "gelation": 0.0, "humectancy": 0.3,
        "texture_impact": "Crispy, Firm", "flavor_profile": "Cooling Sweet",
        "evidence_claim": "Zero calorie polyol sweetener providing crystalline bulk.",
        "evidence_source": "EFSA Scientific Opinion 2010"
    },

    # --- EMULSIFIERS & STABILIZERS ---
    {
        "id": "ing_sunflower_lecithin",
        "name": "Sunflower Lecithin",
        "category": "Emulsifiers",
        "functional_role": "Emulsifier",
        "min_inclusion": 0.2, "max_inclusion": 2.5,
        "cost_per_kg": 10.50,
        "protein": 0.0, "fat": 90.0, "saturated_fat": 14.0, "carbs": 8.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 720.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 1.0, "water_binding": 0.2, "gelation": 0.0, "humectancy": 0.3,
        "texture_impact": "Smooth, Creamy", "flavor_profile": "Neutral",
        "evidence_claim": "Non-GMO, allergen-free phospholipid emulsifier optimizing fat reduction and mouthfeel.",
        "evidence_source": "EFSA Regulation (EU) No 231/2012"
    },
    {
        "id": "ing_xanthan_gum",
        "name": "Xanthan Gum 200 Mesh",
        "category": "Hydrocolloids",
        "functional_role": "Stabilizer",
        "min_inclusion": 0.05, "max_inclusion": 1.5,
        "cost_per_kg": 14.80,
        "protein": 7.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 80.0, "sugar": 0.0, "fibre": 80.0, "sodium": 3000.0, "energy": 320.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.4, "water_binding": 1.0, "gelation": 0.3, "thickening": 1.0,
        "texture_impact": "Viscous, Gel-like, Soft", "flavor_profile": "Neutral",
        "evidence_claim": "Pseudoplastic rheology modifier preventing syneresis and phase separation.",
        "evidence_source": "FSSAI Food Additives Standard 2011"
    },
    {
        "id": "ing_tapioca_starch",
        "name": "Native Tapioca Starch",
        "category": "Starches",
        "functional_role": "Emulsifier",
        "min_inclusion": 1.0, "max_inclusion": 30.0,
        "cost_per_kg": 3.80,
        "protein": 0.2, "fat": 0.1, "saturated_fat": 0.0, "carbs": 88.0, "sugar": 0.0, "fibre": 0.9, "sodium": 1.0, "energy": 350.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.1, "water_binding": 0.9, "gelation": 0.7, "thickening": 0.9,
        "texture_impact": "Elastic, Chewy, Smooth", "flavor_profile": "Bland",
        "evidence_claim": "Low gelatinization temperature starch providing smooth elasticity.",
        "evidence_source": "Starch/Stärke Journal 2020"
    },
    {
        "id": "ing_guar_gum",
        "name": "Guar Gum 200 Mesh",
        "category": "Hydrocolloids",
        "functional_role": "Stabilizer",
        "min_inclusion": 0.05, "max_inclusion": 1.0,
        "cost_per_kg": 9.80,
        "protein": 5.0, "fat": 0.5, "saturated_fat": 0.0, "carbs": 82.0, "sugar": 0.0, "fibre": 82.0, "sodium": 200.0, "energy": 330.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.3, "water_binding": 1.0, "gelation": 0.2, "thickening": 1.0,
        "texture_impact": "Smooth, Viscous, Creamy", "flavor_profile": "Neutral",
        "evidence_claim": "Cold-water soluble galactomannan providing rapid viscosity build.",
        "evidence_source": "Food Hydrocolloids Journal"
    },

    # --- FLAVOR SYSTEMS & COCOA ---
    {
        "id": "ing_cocoa_powder",
        "name": "Dutch Processed Cocoa Powder 10-12%",
        "category": "Flavoring & Cocoa",
        "functional_role": "Flavor System",
        "min_inclusion": 2.0, "max_inclusion": 25.0,
        "cost_per_kg": 11.50,
        "protein": 20.0, "fat": 11.0, "saturated_fat": 6.8, "carbs": 58.0, "sugar": 1.0, "fibre": 33.0, "sodium": 20.0, "energy": 230.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.3, "water_binding": 0.6, "gelation": 0.2, "thickening": 0.4,
        "texture_impact": "Smooth, Dense, Fudgy", "flavor_profile": "Rich Cocoa, Chocolate",
        "evidence_claim": "Alkalized cocoa providing intense chocolate flavor and dark color.",
        "evidence_source": "USDA FDC"
    },
    {
        "id": "ing_vanilla_extract",
        "name": "Natural Bourbon Vanilla Extract",
        "category": "Flavoring & Cocoa",
        "functional_role": "Flavor System",
        "min_inclusion": 0.1, "max_inclusion": 2.0,
        "cost_per_kg": 38.00,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 12.0, "sugar": 10.0, "fibre": 0.0, "sodium": 10.0, "energy": 288.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.0, "water_binding": 0.1, "gelation": 0.0, "thickening": 0.0,
        "texture_impact": "None", "flavor_profile": "Warm, Aromatic Vanilla",
        "evidence_claim": "Pure Madagascar vanilla extract enriching sweet notes and aroma.",
        "evidence_source": "Flavor and Fragrance Journal 2022"
    },
    {
        "id": "ing_sea_salt",
        "name": "Natural Sea Salt",
        "category": "Minerals",
        "functional_role": "Flavor System",
        "min_inclusion": 0.1, "max_inclusion": 1.5,
        "cost_per_kg": 1.50,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0, "sodium": 38750.0, "energy": 0.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.0, "water_binding": 0.3, "gelation": 0.0, "humectancy": 0.2,
        "texture_impact": "None", "flavor_profile": "Salty",
        "evidence_claim": "Flavor enhancer potentiating sweetness perception and ionic balance.",
        "evidence_source": "USDA FDC"
    },
    # --- INDUSTRIAL FOOD ADDITIVES & MINOR COMPONENTS ---
    {
        "id": "ing_potassium_sorbate",
        "name": "Potassium Sorbate (INS 202)",
        "category": "Food Additives",
        "functional_role": "Preservative",
        "min_inclusion": 0.01, "max_inclusion": 0.20,
        "cost_per_kg": 14.50,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 0.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "ins_number": "INS 202", "cas_number": "24634-61-5", "pubchem_id": "23665582",
        "why_present": "Inhibits mold, yeast, and fungal growth to extend shelf life in intermediate moisture foods.",
        "evidence_claim": "Permitted antimicrobial preservative per Codex GSFA Standard 192-1995.",
        "evidence_source": "FSSAI Schedule II / Codex GSFA"
    },
    {
        "id": "ing_tocopherols",
        "name": "Mixed Tocopherols / Vitamin E (INS 307)",
        "category": "Food Additives",
        "functional_role": "Antioxidant",
        "min_inclusion": 0.005, "max_inclusion": 0.05,
        "cost_per_kg": 42.00,
        "protein": 0.0, "fat": 100.0, "saturated_fat": 10.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 900.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "ins_number": "INS 307", "cas_number": "1406-18-4", "pubchem_id": "14985",
        "why_present": "Prevents lipid oxidation and rancidity in vegetable oils and fat-rich systems.",
        "evidence_claim": "Natural lipophilic antioxidant protecting unsaturated fatty acids.",
        "evidence_source": "EFSA Journal 2015;13(4):4093"
    },
    {
        "id": "ing_citric_acid",
        "name": "Citric Acid Anhydrous (INS 330)",
        "category": "Food Additives",
        "functional_role": "Acidity Regulator",
        "min_inclusion": 0.05, "max_inclusion": 0.80,
        "cost_per_kg": 3.20,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 100.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 247.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "ins_number": "INS 330", "cas_number": "77-92-9", "pubchem_id": "311",
        "why_present": "Controls pH, enhances tart flavor profile, and acts as a chelating synergist for antioxidants.",
        "evidence_claim": "Universal acidulant and pH control agent approved under GMP.",
        "evidence_source": "FSSAI Food Additive Guidelines 2011"
    },
    {
        "id": "ing_sodium_bicarbonate",
        "name": "Sodium Bicarbonate / Baking Soda (INS 500ii)",
        "category": "Food Additives",
        "functional_role": "Raising Agent",
        "min_inclusion": 0.10, "max_inclusion": 1.20,
        "cost_per_kg": 1.80,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0, "sodium": 27360.0, "energy": 0.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "ins_number": "INS 500(ii)", "cas_number": "144-55-8", "pubchem_id": "516892",
        "why_present": "Releases carbon dioxide gas upon thermal activation or acid reaction for product leavening.",
        "evidence_claim": "Standard chemical leavening base providing aeration and crumb structure.",
        "evidence_source": "Cereal Chemistry Vol 88"
    },
    {
        "id": "ing_mono_diglycerides",
        "name": "Mono- and Diglycerides of Fatty Acids (INS 471 / E471)",
        "category": "Emulsifiers",
        "functional_role": "Emulsifier",
        "min_inclusion": 0.10, "max_inclusion": 1.50,
        "cost_per_kg": 8.50,
        "protein": 0.0, "fat": 99.0, "saturated_fat": 90.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 890.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "ins_number": "INS 471", "cas_number": "31566-31-1", "pubchem_id": "92137",
        "why_present": "Stabilizes oil-in-water emulsions, delays starch retrogradation (anti-staling), and improves crumb softness.",
        "evidence_claim": "Primary lipophilic emulsifier providing starch complexation and crumb softening.",
        "evidence_source": "Journal of Agricultural and Food Chemistry"
    },
    {
        "id": "ing_beta_carotene",
        "name": "Natural Beta-Carotene 1% Powder (INS 160a)",
        "category": "Colors",
        "functional_role": "Coloring Agent",
        "min_inclusion": 0.001, "max_inclusion": 0.02,
        "cost_per_kg": 65.00,
        "protein": 0.0, "fat": 1.0, "saturated_fat": 0.0, "carbs": 95.0, "sugar": 0.0, "fibre": 0.0, "sodium": 10.0, "energy": 380.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "ins_number": "INS 160a(i)", "cas_number": "7235-40-7", "pubchem_id": "5280489",
        "why_present": "Provides warm yellow-golden hue while contributing pro-vitamin A activity.",
        "evidence_claim": "Permitted natural carotenoid colorant for bakery and snack systems.",
        "evidence_source": "Codex Alimentarius Standard 192-1995"
    },
    {
        "id": "ing_whole_milk_powder",
        "name": "Full Cream Milk Solids (Whole Milk Powder)",
        "category": "Dairy Solids",
        "functional_role": "Dairy Solids",
        "min_inclusion": 5.0, "max_inclusion": 35.0,
        "cost_per_kg": 4.50,
        "protein": 26.0, "fat": 27.0, "saturated_fat": 17.5, "carbs": 38.0, "sugar": 38.0, "fibre": 0.0, "sodium": 370.0, "energy": 500.0,
        "allergens": "Milk", "vegan": 0, "gluten_free": 1, "dairy_free": 0, "halal": 1, "kosher": 1,
        "emulsification": 0.7, "water_binding": 0.6, "gelation": 0.5, "thickening": 0.5,
        "texture_impact": "Creamy, Smooth, Rich, Melt-in-mouth", "flavor_profile": "Milky, Dairy, Sweet",
        "evidence_claim": "Cadbury benchmark milk solids providing rich dairy mouthfeel, milk fat crystallization, and Maillard flavor.",
        "evidence_source": "Codex Standard 207-1999 for Milk Powders"
    },
    {
        "id": "ing_skim_milk_powder",
        "name": "Skimmed Milk Solids (Powder)",
        "category": "Dairy Solids",
        "functional_role": "Dairy Solids",
        "min_inclusion": 2.0, "max_inclusion": 30.0,
        "cost_per_kg": 4.00,
        "protein": 36.0, "fat": 1.0, "saturated_fat": 0.6, "carbs": 52.0, "sugar": 52.0, "fibre": 0.0, "sodium": 500.0, "energy": 360.0,
        "allergens": "Milk", "vegan": 0, "gluten_free": 1, "dairy_free": 0, "halal": 1, "kosher": 1,
        "emulsification": 0.8, "water_binding": 0.8, "gelation": 0.6, "thickening": 0.6,
        "texture_impact": "Firm, Smooth", "flavor_profile": "Clean Dairy, Milky",
        "evidence_claim": "High-protein dairy solids enhancing hardness and flavor development.",
        "evidence_source": "International Dairy Journal 2022"
    },
    {
        "id": "ing_oat_milk_powder",
        "name": "Oat Milk Powder (Dairy-Free Milk Solids)",
        "category": "Plant-Based Dairy",
        "functional_role": "Dairy Alternative Solids",
        "min_inclusion": 3.0, "max_inclusion": 35.0,
        "cost_per_kg": 6.50,
        "protein": 8.0, "fat": 10.0, "saturated_fat": 2.0, "carbs": 68.0, "sugar": 18.0, "fibre": 6.0, "sodium": 80.0, "energy": 400.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.6, "water_binding": 0.7, "gelation": 0.3, "thickening": 0.6,
        "texture_impact": "Velvety, Creamy, Smooth", "flavor_profile": "Malty, Creamy, Sweet Oat",
        "evidence_claim": "Dairy-free plant milk solids providing clean mouthfeel and opacity for vegan chocolate formulations.",
        "evidence_source": "Plant Foods for Human Nutrition 2023"
    },
    {
        "id": "ing_cane_sugar",
        "name": "Refined Cane Sugar (Granulated)",
        "category": "Sweeteners",
        "functional_role": "Sweetener",
        "min_inclusion": 5.0, "max_inclusion": 60.0,
        "cost_per_kg": 1.20,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 100.0, "sugar": 100.0, "fibre": 0.0, "sodium": 1.0, "energy": 387.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.0, "water_binding": 0.2, "gelation": 0.0, "humectancy": 0.1,
        "texture_impact": "Crystalline, Bulking, Snap", "flavor_profile": "Pure Sweet",
        "evidence_claim": "Standard sucrose sweet bulking agent providing body, snap, and clean sweetness profile.",
        "evidence_source": "Codex Alimentarius Standard 212-1999"
    },
    {
        "id": "ing_coconut_sugar",
        "name": "Organic Coconut Sugar",
        "category": "Sweeteners",
        "functional_role": "Sweetener",
        "min_inclusion": 2.0, "max_inclusion": 40.0,
        "cost_per_kg": 4.80,
        "protein": 1.0, "fat": 0.2, "saturated_fat": 0.0, "carbs": 93.0, "sugar": 85.0, "fibre": 2.5, "sodium": 45.0, "energy": 375.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.0, "water_binding": 0.3, "gelation": 0.0, "humectancy": 0.2,
        "texture_impact": "Granular, Warm", "flavor_profile": "Caramel, Molasses Sweet",
        "evidence_claim": "Low-glycemic unrefined sugar with natural mineral content and caramel notes.",
        "evidence_source": "Food Chemistry 2021"
    },
    {
        "id": "ing_cocoa_mass",
        "name": "Cocoa Solids / Cocoa Liquor (Mass)",
        "category": "Cocoa Solids",
        "functional_role": "Cocoa Solids",
        "min_inclusion": 5.0, "max_inclusion": 40.0,
        "cost_per_kg": 11.50,
        "protein": 13.0, "fat": 53.0, "saturated_fat": 32.0, "carbs": 28.0, "sugar": 1.0, "fibre": 16.0, "sodium": 5.0, "energy": 640.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.3, "water_binding": 0.2, "gelation": 0.8, "thickening": 0.6,
        "texture_impact": "Dense, Fudgy, Snap", "flavor_profile": "Intense Chocolate, Roasted Cocoa, Bitter",
        "evidence_claim": "Pure unadulterated cocoa nib liquor supplying fine cocoa solids and natural polyphenols.",
        "evidence_source": "Codex Standard 87-1981 for Chocolate and Chocolate Products"
    },
    {
        "id": "ing_soy_lecithin",
        "name": "Soy Lecithin (INS 322)",
        "category": "Emulsifiers",
        "functional_role": "Emulsifier",
        "min_inclusion": 0.15, "max_inclusion": 1.0,
        "cost_per_kg": 4.20,
        "protein": 0.0, "fat": 100.0, "saturated_fat": 15.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0, "sodium": 10.0, "energy": 760.0,
        "allergens": "Soy", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 1.0, "water_binding": 0.1, "gelation": 0.0, "humectancy": 0.2,
        "texture_impact": "Smooth, Reduced Viscosity", "flavor_profile": "Neutral",
        "evidence_claim": "Primary phospholipid surfactant reducing plastic viscosity and moisture-induced grittiness in chocolate.",
        "evidence_source": "Codex GSFA INS 322(i)"
    },
    {
        "id": "ing_ammonium_phosphatides",
        "name": "Ammonium Phosphatides (INS 442)",
        "category": "Emulsifiers",
        "functional_role": "Emulsifier",
        "min_inclusion": 0.1, "max_inclusion": 0.7,
        "cost_per_kg": 6.80,
        "protein": 0.0, "fat": 95.0, "saturated_fat": 16.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 850.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "ins_number": "INS 442",
        "emulsification": 1.0, "water_binding": 0.1, "gelation": 0.0, "humectancy": 0.0,
        "texture_impact": "Ultra-smooth, Flowable", "flavor_profile": "Neutral",
        "evidence_claim": "Cadbury benchmark chocolate emulsifier (INS 442) providing viscosity reduction with no off-flavor.",
        "evidence_source": "EFSA Scientific Opinion on Ammonium Phosphatides (E 442) / Codex Stan 87-1981"
    },
    {
        "id": "ing_pgpr",
        "name": "Polyglycerol Polyricinoleate (PGPR / INS 476)",
        "category": "Emulsifiers",
        "functional_role": "Emulsifier",
        "min_inclusion": 0.05, "max_inclusion": 0.5,
        "cost_per_kg": 8.50,
        "protein": 0.0, "fat": 100.0, "saturated_fat": 10.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 900.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "ins_number": "INS 476",
        "emulsification": 1.0, "water_binding": 0.0, "gelation": 0.0, "humectancy": 0.0,
        "texture_impact": "Sharp Yield Stress Reduction, Thin Coating", "flavor_profile": "Neutral",
        "evidence_claim": "Synergistic co-emulsifier with lecithin drastically decreasing Casson yield value for optimal mold filling.",
        "evidence_source": "Journal of Food Engineering / Codex GSFA INS 476"
    },
    {
        "id": "ing_vanilla_flavor",
        "name": "Vanilla Flavour (Nature Identical Vanillin)",
        "category": "Flavoring & Cocoa",
        "functional_role": "Flavor System",
        "min_inclusion": 0.02, "max_inclusion": 0.3,
        "cost_per_kg": 22.00,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 15.0, "sugar": 10.0, "fibre": 0.0, "sodium": 5.0, "energy": 60.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.0, "water_binding": 0.0, "gelation": 0.0, "thickening": 0.0,
        "texture_impact": "None", "flavor_profile": "Sweet Vanilla, Warm, Creamy",
        "evidence_claim": "Standard chocolate vanilla aroma compound balancing cocoa bitterness and dairy notes.",
        "evidence_source": "Flavor and Fragrance Journal"
    },
    # --- PLANT-BASED BEVERAGES ---
    {
        "id": "ing_oat_base",
        "name": "Hydrolyzed Oat Base / Flour",
        "category": "Plant-Based Dairy",
        "functional_role": "Base Raw Material",
        "min_inclusion": 5.0, "max_inclusion": 85.0,
        "cost_per_kg": 3.40,
        "protein": 12.0, "fat": 6.5, "saturated_fat": 1.2, "carbs": 68.0, "sugar": 8.0, "fibre": 8.0, "sodium": 15.0, "energy": 390.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.4, "water_binding": 0.8, "gelation": 0.3, "thickening": 0.6,
        "texture_impact": "Creamy, Smooth, Suspended", "flavor_profile": "Oaty, Naturally Sweet",
        "evidence_claim": "Enzymatically hydrolyzed oat base yielding smooth soluble dispersion and natural sweetness.",
        "evidence_source": "Cereal Foods World 2022"
    },
    {
        "id": "ing_almond_base",
        "name": "Blanched Almond Base Powder",
        "category": "Plant-Based Dairy",
        "functional_role": "Base Raw Material",
        "min_inclusion": 3.0, "max_inclusion": 50.0,
        "cost_per_kg": 9.50,
        "protein": 21.0, "fat": 50.0, "saturated_fat": 3.8, "carbs": 22.0, "sugar": 4.0, "fibre": 12.0, "sodium": 1.0, "energy": 580.0,
        "allergens": "Tree Nuts", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.5, "water_binding": 0.6, "gelation": 0.2, "thickening": 0.4,
        "texture_impact": "Rich, Nutty, Velvety", "flavor_profile": "Nutty, Clean Almond",
        "evidence_claim": "Fine particle milled blanched almond base for high-lipid plant-based emulsions.",
        "evidence_source": "Journal of Agricultural and Food Chemistry"
    },
    {
        "id": "ing_dipotassium_phosphate",
        "name": "Dipotassium Phosphate (INS 340ii)",
        "category": "Food Additives",
        "functional_role": "Acidity Control",
        "min_inclusion": 0.1, "max_inclusion": 0.6,
        "cost_per_kg": 5.20,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 0.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "ins_number": "INS 340(ii)",
        "emulsification": 0.3, "water_binding": 0.2, "gelation": 0.0, "thickening": 0.0,
        "texture_impact": "Stabilizing, Feathering Prevention", "flavor_profile": "Mild Saline",
        "evidence_claim": "Buffering agent preventing protein curdling/feathering when added to hot acidic coffee.",
        "evidence_source": "Codex Alimentarius GSFA Table 3"
    },
    {
        "id": "ing_gellan_gum",
        "name": "Gellan Gum (INS 418)",
        "category": "Hydrocolloids",
        "functional_role": "Stabilizer",
        "min_inclusion": 0.02, "max_inclusion": 0.15,
        "cost_per_kg": 28.00,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 80.0, "sugar": 0.0, "fibre": 75.0, "sodium": 120.0, "energy": 160.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "ins_number": "INS 418",
        "emulsification": 0.2, "water_binding": 0.95, "gelation": 0.9, "thickening": 0.8,
        "texture_impact": "Fluid Gel, Suspension without Clumping", "flavor_profile": "Neutral",
        "evidence_claim": "Forms delicate fluid gel network holding insoluble calcium and cocoa in suspension without high viscosity.",
        "evidence_source": "Food Hydrocolloids Vol 110"
    },
    # --- PLANT-BASED YOGURT / DAIRY ALTERNATIVES ---
    {
        "id": "ing_cultured_coconut_base",
        "name": "Cultured Coconut Cream Base",
        "category": "Plant-Based Dairy",
        "functional_role": "Base Raw Material",
        "min_inclusion": 10.0, "max_inclusion": 85.0,
        "cost_per_kg": 4.60,
        "protein": 3.0, "fat": 24.0, "saturated_fat": 21.0, "carbs": 6.0, "sugar": 3.0, "fibre": 2.0, "sodium": 20.0, "energy": 250.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.6, "water_binding": 0.7, "gelation": 0.5, "thickening": 0.7,
        "texture_impact": "Thick, Decadent, Spoonable", "flavor_profile": "Mild Coconut, Tart",
        "evidence_claim": "Fermented high-lipid coconut cream yielding authentic creamy spoonable yogurt body.",
        "evidence_source": "International Journal of Dairy Technology"
    },
    {
        "id": "ing_vegan_probiotics",
        "name": "Vegan Live Probiotic Cultures",
        "category": "Food Additives",
        "functional_role": "Active Culture",
        "min_inclusion": 0.01, "max_inclusion": 0.1,
        "cost_per_kg": 65.00,
        "protein": 10.0, "fat": 1.0, "saturated_fat": 0.2, "carbs": 70.0, "sugar": 5.0, "fibre": 0.0, "sodium": 50.0, "energy": 330.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.0, "water_binding": 0.1, "gelation": 0.0, "thickening": 0.2,
        "texture_impact": "Acid Coagulation, Soft Curd", "flavor_profile": "Fresh Acidic, Yogurt Tang",
        "evidence_claim": "Traditional symbiotic yogurt cultures (S. thermophilus and L. bulgaricus) producing lactic acid.",
        "evidence_source": "Journal of Functional Foods"
    },
    {
        "id": "ing_pectin_lm",
        "name": "Pectin (Amidated Low Methoxyl, INS 440)",
        "category": "Hydrocolloids",
        "functional_role": "Thickener",
        "min_inclusion": 0.2, "max_inclusion": 1.5,
        "cost_per_kg": 18.50,
        "protein": 0.5, "fat": 0.1, "saturated_fat": 0.0, "carbs": 85.0, "sugar": 15.0, "fibre": 75.0, "sodium": 180.0, "energy": 170.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "ins_number": "INS 440",
        "emulsification": 0.2, "water_binding": 0.9, "gelation": 0.85, "thickening": 0.8,
        "texture_impact": "Smooth Gel, Glossy, Syneresis Prevention", "flavor_profile": "Neutral",
        "evidence_claim": "Calcium-reactive LM pectin stabilizing plant yogurt matrix against whey-off / syneresis.",
        "evidence_source": "Carbohydrate Polymers"
    },
    # --- BAKERY PRODUCTS ---
    {
        "id": "ing_wheat_flour",
        "name": "Organic Enriched Wheat Flour (All-Purpose)",
        "category": "Flour & Grains",
        "functional_role": "Base Raw Material",
        "min_inclusion": 15.0, "max_inclusion": 75.0,
        "cost_per_kg": 1.40,
        "protein": 11.5, "fat": 1.2, "saturated_fat": 0.2, "carbs": 73.0, "sugar": 0.3, "fibre": 3.0, "sodium": 2.0, "energy": 360.0,
        "allergens": "Gluten", "vegan": 1, "gluten_free": 0, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.1, "water_binding": 0.65, "gelation": 0.5, "thickening": 0.7,
        "texture_impact": "Crumb Structure, Elastic Dough, Chew", "flavor_profile": "Mild Wheat",
        "evidence_claim": "Standard hard/soft wheat blend providing gluten network structure for yeast-leavened and chemically-leavened bakery.",
        "evidence_source": "AACC International Approved Methods"
    },
    {
        "id": "ing_gf_oat_flour",
        "name": "Certified Gluten-Free Whole Oat Flour",
        "category": "Flour & Grains",
        "functional_role": "Base Raw Material",
        "min_inclusion": 10.0, "max_inclusion": 70.0,
        "cost_per_kg": 2.60,
        "protein": 13.0, "fat": 6.8, "saturated_fat": 1.3, "carbs": 66.0, "sugar": 1.0, "fibre": 10.0, "sodium": 3.0, "energy": 380.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.2, "water_binding": 0.7, "gelation": 0.4, "thickening": 0.6,
        "texture_impact": "Tender, Soft Crumb, Moist", "flavor_profile": "Nutty, Toasted Oat",
        "evidence_claim": "Purity-protocol whole oat flour supplying soluble beta-glucan fiber in gluten-free bakery matrices.",
        "evidence_source": "Journal of Cereal Science"
    },
    {
        "id": "ing_baking_powder",
        "name": "Double-Acting Baking Powder",
        "category": "Food Additives",
        "functional_role": "Raising Agent",
        "min_inclusion": 0.5, "max_inclusion": 3.0,
        "cost_per_kg": 3.80,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 28.0, "sugar": 0.0, "fibre": 0.0, "sodium": 11000.0, "energy": 110.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.0, "water_binding": 0.1, "gelation": 0.0, "thickening": 0.0,
        "texture_impact": "Porous Crumb, Volume Lift, Aeration", "flavor_profile": "Clean, Neutral",
        "evidence_claim": "Dual leavening release with moisture bench reaction followed by oven heat-activated thermal expansion.",
        "evidence_source": "Baking Science & Technology"
    },
    {
        "id": "ing_shortening",
        "name": "Vegetable Shortening (Non-Hydrogenated Palm)",
        "category": "Fats & Oils",
        "functional_role": "Fats & Oils",
        "min_inclusion": 3.0, "max_inclusion": 30.0,
        "cost_per_kg": 2.80,
        "protein": 0.0, "fat": 100.0, "saturated_fat": 49.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 900.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.3, "water_binding": 0.0, "gelation": 0.0, "thickening": 0.2,
        "texture_impact": "Flaky, Tender, Melt-in-Mouth", "flavor_profile": "Neutral",
        "evidence_claim": "Provides plasticity and tenderizing shortening action by coating starch and protein particles.",
        "evidence_source": "Lipid Technology in Food"
    },
    # --- SAUCES / SPREADS / EMULSIFIED PRODUCTS ---
    {
        "id": "ing_olive_oil",
        "name": "Extra Virgin Olive Oil",
        "category": "Fats & Oils",
        "functional_role": "Fats & Oils",
        "min_inclusion": 5.0, "max_inclusion": 75.0,
        "cost_per_kg": 7.80,
        "protein": 0.0, "fat": 100.0, "saturated_fat": 14.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 884.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.3, "water_binding": 0.0, "gelation": 0.0, "thickening": 0.1,
        "texture_impact": "Silky, Viscous, Smooth", "flavor_profile": "Fruity, Peppery, Rich",
        "evidence_claim": "Cold-pressed monounsaturated fatty acid source providing stable liquid dispersed or continuous phase.",
        "evidence_source": "International Olive Council Standards"
    },
    {
        "id": "ing_canola_oil",
        "name": "Refined Canola Oil (High Smoke Point)",
        "category": "Fats & Oils",
        "functional_role": "Fats & Oils",
        "min_inclusion": 5.0, "max_inclusion": 80.0,
        "cost_per_kg": 2.20,
        "protein": 0.0, "fat": 100.0, "saturated_fat": 7.0, "carbs": 0.0, "sugar": 0.0, "fibre": 0.0, "sodium": 0.0, "energy": 884.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.2, "water_binding": 0.0, "gelation": 0.0, "thickening": 0.1,
        "texture_impact": "Light, Viscous Emulsion Matrix", "flavor_profile": "Neutral",
        "evidence_claim": "Low-saturated lipid standard for stable cold-emulsion mayonnaise and salad dressings.",
        "evidence_source": "Journal of the American Oil Chemists' Society"
    },
    {
        "id": "ing_white_vinegar",
        "name": "Distilled White Vinegar (10% Acidity)",
        "category": "Acids & Vinegars",
        "functional_role": "Acidity Control",
        "min_inclusion": 1.0, "max_inclusion": 15.0,
        "cost_per_kg": 0.85,
        "protein": 0.0, "fat": 0.0, "saturated_fat": 0.0, "carbs": 0.1, "sugar": 0.0, "fibre": 0.0, "sodium": 2.0, "energy": 20.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.0, "water_binding": 0.1, "gelation": 0.0, "thickening": 0.0,
        "texture_impact": "Astringent, Thin", "flavor_profile": "Sharp Acidic, Clean Vinegar",
        "evidence_claim": "Standard microbial fermentation acetic acid acidulant maintaining pH below 4.0 for microbial stability.",
        "evidence_source": "Food Microbiology & Safety"
    },
    {
        "id": "ing_mustard_flour",
        "name": "Yellow Mustard Flour (De-heated)",
        "category": "Spices & Seasonings",
        "functional_role": "Emulsifier",
        "min_inclusion": 0.5, "max_inclusion": 4.0,
        "cost_per_kg": 4.50,
        "protein": 31.0, "fat": 28.0, "saturated_fat": 1.5, "carbs": 25.0, "sugar": 6.0, "fibre": 12.0, "sodium": 5.0, "energy": 470.0,
        "allergens": "Mustard", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.85, "water_binding": 0.75, "gelation": 0.4, "thickening": 0.6,
        "texture_impact": "Cohesive Emulsion, Body, Viscosity", "flavor_profile": "Pungent, Savory, Warm",
        "evidence_claim": "Natural protein and mucilage hydrocolloid complex stabilizing oil-in-water emulsions in plant-based mayo.",
        "evidence_source": "LWT - Food Science and Technology"
    },
    {
        "id": "ing_peanut_butter",
        "name": "Natural Peanut Butter (Creamy)",
        "category": "Fats & Oils",
        "functional_role": "Fats & Oils",
        "min_inclusion": 5.0, "max_inclusion": 50.0,
        "cost_per_kg": 3.90,
        "protein": 25.0, "fat": 50.0, "saturated_fat": 10.0, "carbs": 20.0, "sugar": 6.0, "fibre": 8.0, "sodium": 15.0, "energy": 590.0,
        "allergens": "Peanuts", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.5, "water_binding": 0.6, "gelation": 0.3, "thickening": 0.8,
        "texture_impact": "Dense, Spreadable, Rich", "flavor_profile": "Roasted Peanut, Savory",
        "evidence_claim": "100% dry roasted peanut paste supplying natural lipid emulsion and vegetable protein.",
        "evidence_source": "USDA FoodData Central"
    },
    {
        "id": "ing_date_paste",
        "name": "Medjool Date Paste",
        "category": "Sweeteners",
        "functional_role": "Sweetener",
        "min_inclusion": 5.0, "max_inclusion": 45.0,
        "cost_per_kg": 5.50,
        "protein": 2.2, "fat": 0.4, "saturated_fat": 0.1, "carbs": 75.0, "sugar": 66.0, "fibre": 8.0, "sodium": 3.0, "energy": 280.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.2, "water_binding": 0.85, "gelation": 0.4, "thickening": 0.8,
        "texture_impact": "Chewy, Sticky, Binding Paste", "flavor_profile": "Caramel, Sweet Fruity",
        "evidence_claim": "Whole fruit binding paste providing chewy texture and natural humectancy without refined cane sugar.",
        "evidence_source": "Journal of Food Processing and Preservation"
    },
    {
        "id": "ing_chia_seeds",
        "name": "Organic Chia Seeds",
        "category": "Functional Additives",
        "functional_role": "Thickener",
        "min_inclusion": 1.0, "max_inclusion": 15.0,
        "cost_per_kg": 6.20,
        "protein": 17.0, "fat": 31.0, "saturated_fat": 3.3, "carbs": 42.0, "sugar": 0.0, "fibre": 34.0, "sodium": 16.0, "energy": 486.0,
        "allergens": "None", "vegan": 1, "gluten_free": 1, "dairy_free": 1, "halal": 1, "kosher": 1,
        "emulsification": 0.4, "water_binding": 0.95, "gelation": 0.8, "thickening": 0.85,
        "texture_impact": "Mucilaginous Gel, Crunch", "flavor_profile": "Mild Nutty",
        "evidence_claim": "High alpha-linolenic omega-3 and soluble mucilage seed producing strong hydrogel network.",
        "evidence_source": "Food Chemistry 2021"
    }
]

def init_db():
    """Creates SQLite tables and seeds/upserts master ingredients."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        id TEXT PRIMARY KEY,
        name TEXT,
        category TEXT,
        functional_role TEXT,
        min_inclusion REAL,
        max_inclusion REAL,
        cost_per_kg REAL,
        protein REAL,
        fat REAL,
        saturated_fat REAL,
        carbs REAL,
        sugar REAL,
        fibre REAL,
        sodium REAL,
        energy REAL,
        allergens TEXT,
        vegan INTEGER,
        gluten_free INTEGER,
        dairy_free INTEGER,
        halal INTEGER,
        kosher INTEGER,
        emulsification REAL,
        water_binding REAL,
        gelation REAL,
        thickening REAL,
        texture_impact TEXT,
        flavor_profile TEXT,
        evidence_claim TEXT,
        evidence_source TEXT
    )
    """)

    # Always ensure master SEED_INGREDIENTS are upserted with verified food formulation data
    for ing in SEED_INGREDIENTS:
        cursor.execute("""
        INSERT OR REPLACE INTO ingredients VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            ing["id"], ing["name"], ing["category"], ing["functional_role"],
            ing["min_inclusion"], ing["max_inclusion"], ing["cost_per_kg"],
            ing["protein"], ing["fat"], ing.get("saturated_fat", 0.0), ing["carbs"], ing.get("sugar", 0.0), ing.get("fibre", 0.0), ing.get("sodium", 0.0), ing["energy"],
            ing["allergens"], ing["vegan"], ing["gluten_free"], ing["dairy_free"], ing["halal"], ing["kosher"],
            ing.get("emulsification", 0.0), ing.get("water_binding", 0.0), ing.get("gelation", 0.0), ing.get("thickening", 0.0),
            ing.get("texture_impact", ""), ing.get("flavor_profile", ""), ing.get("evidence_claim", ""), ing.get("evidence_source", "")
        ))
    conn.commit()
    conn.close()

def get_all_ingredients(limit: Optional[int] = 500) -> List[Dict[str, Any]]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Prioritize grounded seed formulation ingredients first, then other verified ingredients
    seed_ids = [s["id"] for s in SEED_INGREDIENTS]
    placeholders = ",".join("?" for _ in seed_ids)
    
    if limit and limit > 0:
        query = "SELECT * FROM ingredients ORDER BY CASE WHEN id IN (" + placeholders + ") THEN 0 ELSE 1 END, id LIMIT ?"
        cursor.execute(query, seed_ids + [limit])
    else:
        query = "SELECT * FROM ingredients ORDER BY CASE WHEN id IN (" + placeholders + ") THEN 0 ELSE 1 END, id"
        cursor.execute(query, seed_ids)
        
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_ingredient_by_id(ing_id: str) -> Optional[Dict[str, Any]]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ingredients WHERE id = ?", (ing_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

