import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from requirements_extractor import product_brief_parser
from scoring_engine import scoring_engine
from candidate_engine import candidate_engine
from repository import get_ingredient_by_id

brief_text = "Create a high-protein vegan chocolate bar with at least 25% cocoa butter, at least 7% protein, at least 8% almond content, at most 28% sugar, creamy melt, caramelized nut and vanilla flavor, 12-month shelf life, and free from dairy ingredients."
brief = product_brief_parser.parse(brief_text)

combo_ids = [
    ("ing_pea_protein", 6.0),
    ("ing_cocoa_butter", 28.0),
    ("ing_erythritol", 51.5),
    ("ing_vanilla_extract", 0.5),
    ("ing_almond_flour", 14.0)
]

set_raw = []
for idx, (ing_id, pct) in enumerate(combo_ids):
    ing_detail = get_ingredient_by_id(ing_id)
    set_raw.append({
        "detail": ing_detail,
        "category": ing_detail.category,
        "percentage": pct,
        "role": ing_detail.functional_roles[0] if ing_detail.functional_roles else "Base Raw Material",
        "formulation_role": "Base Raw Material",
        "addition_order": idx + 1
    })

macros = candidate_engine._calculate_grounded_macros(set_raw)
formatted_components = [candidate_engine._format_component(item) for item in set_raw]

cand = {
    "candidate_id": "EXP-001-COMB-000001",
    "set_name": "Test Formulation",
    "title": "Pea Protein + Cocoa Butter + Erythritol + Vanilla + Almond Flour",
    "total_percentage": 100.0,
    "is_mathematically_valid": True,
    "composition": {
        "all_components": formatted_components,
        "bulk_ingredients": formatted_components,
        "functional_ingredients": []
    },
    "nutrition": macros,
    "cost_per_kg": macros.get("cost_per_kg"),
    "cost_status": macros.get("cost_status"),
    "compatibility": {}
}

res = scoring_engine.calculate_scores(cand, brief.model_dump())
print("Overall Score:", res.get("overall_score"))
print("Radar:", res.get("radar_scores"))
print("Weights:", res.get("weights"))
