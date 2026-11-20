import sys
from pathlib import Path
sys.path.insert(0, r"Food Web App Core/backend")
sys.path.insert(0, r".")

from requirements_extractor import product_brief_parser
from retrieval_service import retrieval_orchestrator
from exhaustive_search_engine import exhaustive_search_engine

brief_text = "Create a high-protein vegan chocolate bar with at least 25% cocoa butter, at least 7% protein, at least 8% almond content, at most 28% sugar, creamy melt, caramelized nut and vanilla flavor, 12-month shelf life, and free from dairy ingredients."
brief = product_brief_parser.parse(brief_text)
res = retrieval_orchestrator.retrieve_all_multi_dimensional(brief.dict())
prop = retrieval_orchestrator.propagate_constraints(res["ingredients"], brief.dict())
pools = exhaustive_search_engine.extract_role_pools(prop["eligible_candidates"], brief)

print("POOLS:")
for role, ings in pools.items():
    print(f"\n=== {role} ({len(ings)}) ===")
    for ing in ings:
        print(f"  {ing.id}: {ing.name} | Cat: {ing.category} | Prot: {ing.nutrition.get('protein',0)} | Fat: {ing.nutrition.get('fat',0)} | Carbs: {ing.nutrition.get('carbs',0)}")
