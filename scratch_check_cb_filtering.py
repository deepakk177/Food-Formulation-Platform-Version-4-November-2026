import sys
sys.path.insert(0, "Food Web App Core/backend")
from requirements_extractor import product_brief_parser
from retrieval_service import retrieval_orchestrator
from constraint_engine import constraint_engine

user_brief = "Vegan White Chocolate: Create a dairy-free white chocolate using cocoa butter and plant-based ingredients. Target >=25% cocoa butter, <=30% sugar and >=5% protein with a smooth, creamy melt. Develop a vanilla-caramel flavor profile and 12-month shelf life."
brief = product_brief_parser.parse(user_brief)
brief_dict = brief.dict()

retrieved = retrieval_orchestrator.retrieve_all_multi_dimensional(brief_dict)
all_raw = retrieved["ingredients"]
print("All raw ingredients count:", len(all_raw))

cb_in_raw = [i for i in all_raw if "cocoa butter" in i.name.lower()]
print("Cocoa butter in raw:", [(i.id, i.name, i.vegan, i.dairy_free, i.category) for i in cb_in_raw])

prop_results = retrieval_orchestrator.propagate_constraints(all_raw, brief_dict)
eligible = prop_results["eligible_candidates"]
print("Eligible count:", len(eligible))

cb_in_eligible = [i for i in eligible if "cocoa butter" in i.name.lower()]
print("Cocoa butter in eligible:", [(i.id, i.name, i.vegan, i.dairy_free, i.category) for i in cb_in_eligible])

fats = [i for i in eligible if ("fat" in i.category.lower() or "oil" in i.name.lower() or "butter" in i.name.lower() or "lipid" in i.category.lower())]
print("Fats count:", len(fats))
print("Top 5 fats:", [f.name for f in fats[:5]])

cocoa_butters = [i for i in fats if "cocoa butter" in i.name.lower()]
print("cocoa_butters list:", [c.name for c in cocoa_butters])
