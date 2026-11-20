import sys
sys.path.insert(0, "Food Web App Core/backend")
from requirements_extractor import product_brief_parser
from retrieval_service import retrieval_orchestrator

user_brief = "Vegan White Chocolate: Create a dairy-free white chocolate using cocoa butter and plant-based ingredients. Target >=25% cocoa butter, <=30% sugar and >=5% protein with a smooth, creamy melt. Develop a vanilla-caramel flavor profile and 12-month shelf life."
brief = product_brief_parser.parse(user_brief)
brief_dict = brief.dict()

retrieved = retrieval_orchestrator.retrieve_all_multi_dimensional(brief_dict)
all_raw = retrieved["ingredients"]

prop_results = retrieval_orchestrator.propagate_constraints(all_raw, brief_dict)
removed = prop_results["removed_candidates"]

for r in removed:
    if "cocoa butter" in r["ingredient"].lower():
        print("Removed ingredient:", r["ingredient"])
        print("Reason:", r["removed_because"])
        print("Constraint:", r["constraint"])
        print("Evidence:", r["evidence"])
        print("-" * 40)
