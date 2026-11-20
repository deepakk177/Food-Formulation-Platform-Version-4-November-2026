import sys
sys.path.insert(0, "Food Web App Core/backend")
from pipeline_runner import run_pipeline

user_brief = "Vegan White Chocolate: Create a dairy-free plant-based white chocolate using cocoa butter and plant-based ingredients. Target >=25% cocoa butter, <=30% sugar and >=5% protein with a smooth, creamy melt. Develop a vanilla-caramel flavor profile and 12-month shelf life."

res = run_pipeline(user_brief=user_brief, debug=True, profile="BALANCED")
print("Optimization Status:", res["top_candidate"]["is_mathematically_valid"])
print("Top Candidate:", res["top_candidate"]["candidate_id"])
for c in res["top_candidate"]["composition"]["all_components"]:
    print(f"  {c['name']}: {c['percentage']}% ({c['quantity_g']}g) - Role: {c['functional_role']}")
print("Nutrition:", res["top_candidate"]["nutrition"])
print("Overall Score:", res["top_candidate"]["score"]["overall_score"])
print("Validation Status:", res["validation"]["status"])
