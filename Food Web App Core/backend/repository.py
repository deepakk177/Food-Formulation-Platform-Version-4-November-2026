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

    cursor.execute("SELECT count(*) FROM ingredients")
    count = cursor.fetchone()[0]

    if count == 0:
        for ing in SEED_INGREDIENTS:
            cursor.execute("""
            INSERT OR REPLACE INTO ingredients VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                ing["id"], ing["name"], ing["category"], ing["functional_role"],
                ing["min_inclusion"], ing["max_inclusion"], ing["cost_per_kg"],
                ing["protein"], ing["fat"], ing["saturated_fat"], ing["carbs"], ing["sugar"], ing["fibre"], ing["sodium"], ing["energy"],
                ing["allergens"], ing["vegan"], ing["gluten_free"], ing["dairy_free"], ing["halal"], ing["kosher"],
                ing.get("emulsification", 0.0), ing.get("water_binding", 0.0), ing.get("gelation", 0.0), ing.get("thickening", 0.0),
                ing["texture_impact"], ing["flavor_profile"], ing["evidence_claim"], ing["evidence_source"]
            ))
        conn.commit()
    conn.close()

def get_all_ingredients(limit: Optional[int] = 500) -> List[Dict[str, Any]]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if limit and limit > 0:
        cursor.execute("SELECT * FROM ingredients LIMIT ?", (limit,))
    else:
        cursor.execute("SELECT * FROM ingredients")
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
