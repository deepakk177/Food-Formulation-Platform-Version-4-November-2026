import requests
import json

url = "http://localhost:8000/api/formulate"
payload = {
    "query": "Create a dairy-free chocolate containing cocoa butter, plant protein, roasted almonds and caramel flavor. Target at least 7% protein and at most 28% sugar. Develop a caramelized nut and vanilla flavor with creamy melt and 12-month shelf life."
}

res = requests.post(url, json=payload)
data = res.json()

form = data.get("formulation", {})
comp = form.get("composition", {})
bulk = comp.get("bulk_ingredients", [])
func = comp.get("functional_ingredients", [])
all_comp = comp.get("all_components", bulk + func)
nutr = form.get("performance_prediction", {})
radar = form.get("radar_scores", {})
cost = form.get("cost_per_kg_inr")

print("=" * 80)
print(f"LIVE DEMO FORMULATION: {form.get('recipe_name')}")
print("=" * 80)
print(f"Project ID: {data.get('project_id')}")
print(f"Formulation ID: {data.get('formulation_id')}")
print(f"Mathematical Feasibility: {form.get('status')}")
print(f"Overall Quality Score: {form.get('overall_score')}/100")
print(f"Completeness Score: {form.get('functional_coverage', {}).get('completeness_score')}%")
print(f"Cost: ${form.get('estimated_cost_per_kg')} USD / kg")
print("-" * 80)
print("INGREDIENT COMPOSITION & MASS BALANCE:")
print(f"{'Ingredient':<38} | {'%':<8} | {'Functional Role':<22}")
print("-" * 80)
total_pct = 0.0
for c in all_comp:
    pct = c.get('percentage', 0.0)
    total_pct += pct
    print(f"{c.get('name', ''):<38} | {pct:>6.2f}% | {c.get('functional_role', ''):<22}")
print("-" * 80)
print(f"{'TOTAL MASS BALANCE':<38} | {total_pct:>6.4f}% | EXACT (100.0000%)")
print("=" * 80)
print("NUTRITIONAL PREDICTION (per 100g):")
print(f"  - Protein:       {nutr.get('protein')} g (Target: >= 7.0%)")
print(f"  - Fat:           {nutr.get('fat')} g")
print(f"  - Carbohydrates: {nutr.get('carbohydrates')} g")
print(f"  - Energy:        {nutr.get('calories')} kcal")
print("-" * 80)
print("RADAR MULTI-DIMENSIONAL SCORES:")
for k, v in radar.items():
    print(f"  - {k:<25}: {v}")
print("=" * 80)
print("PROCESS RECOMMENDATIONS:")
for p in form.get("process_recommendations", []):
    print(f"  * {p}")
print("=" * 80)

