import sys
import time
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from models.formulation.model import formulation_optimizer

combo = [
    {'name': 'Pea Protein Isolate (85%)', 'protein': 85.0, 'fat': 4.0, 'carbs': 2.0, 'calories': 380.0, 'cost_per_kg': 12.4},
    {'name': 'Prime Press Cocoa Butter', 'protein': 0.0, 'fat': 100.0, 'carbs': 0.0, 'calories': 884.0, 'cost_per_kg': 18.5},
    {'name': 'Erythritol Polyol', 'protein': 0.0, 'fat': 0.0, 'carbs': 100.0, 'calories': 0.0, 'cost_per_kg': 6.2},
    {'name': 'Natural Bourbon Vanilla Extract', 'protein': 0.0, 'fat': 0.0, 'carbs': 12.0, 'calories': 288.0, 'cost_per_kg': 38.0},
    {'name': 'Almond Flour', 'protein': 21.0, 'fat': 50.0, 'carbs': 20.0, 'calories': 590.0, 'cost_per_kg': 13.5}
]
targets = {'protein_min': 7.0, 'cocoa_butter_min': 25.0, 'almond_min': 8.0, 'sugar_max': 28.0, 'cost_target': 15.0}

t0 = time.time()
N = 500
for i in range(N):
    res, _ = formulation_optimizer.predict_with_uncertainty({
        'ingredients': combo,
        'targets': targets,
        'strategy': 'balanced'
    })
dt = time.time() - t0
print(f"Sequential: {N} in {dt:.3f}s -> {N/dt:.1f} evaluations/sec")
