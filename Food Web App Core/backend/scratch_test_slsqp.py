import sys
from pathlib import Path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from models.formulation.model import formulation_optimizer

combo = [
    {'name': 'Pea Protein Isolate (85%)', 'category': 'Proteins', 'functional_role': 'Protein Source', 'protein': 85.0, 'fat': 4.0, 'carbs': 2.0, 'calories': 380.0, 'cost_per_kg': 12.4},
    {'name': 'Prime Press Cocoa Butter', 'category': 'Fats & Oils', 'functional_role': 'Fats & Oils', 'protein': 0.0, 'fat': 100.0, 'carbs': 0.0, 'calories': 884.0, 'cost_per_kg': 18.5},
    {'name': 'Erythritol Polyol', 'category': 'Sweeteners', 'functional_role': 'Sweetener', 'protein': 0.0, 'fat': 0.0, 'carbs': 100.0, 'calories': 0.0, 'cost_per_kg': 6.2},
    {'name': 'Natural Bourbon Vanilla Extract', 'category': 'Flavoring & Cocoa', 'functional_role': 'Flavor System', 'protein': 0.0, 'fat': 0.0, 'carbs': 12.0, 'calories': 288.0, 'cost_per_kg': 38.0},
    {'name': 'Almond Flour', 'category': 'Nut Flours', 'functional_role': 'Bulk Ingredient', 'protein': 21.0, 'fat': 50.0, 'carbs': 20.0, 'calories': 590.0, 'cost_per_kg': 13.5}
]

res, _ = formulation_optimizer.predict_with_uncertainty({
    'ingredients': combo,
    'targets': {'protein_min': 7.0, 'cocoa_butter_min': 25.0, 'almond_min': 8.0, 'sugar_max': 28.0, 'cost_target': 15.0},
    'strategy': 'balanced'
})

print('Feasible:', res['is_feasible'])
print('Percentages:', res['percentages'])
print('Sum:', sum(res['percentages']))
for ing, pct in zip(combo, res['percentages']):
    print(f"  {ing['name']}: {pct}%")
