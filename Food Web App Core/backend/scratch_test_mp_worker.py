import os
import sys
import time
from pathlib import Path
from multiprocessing import Pool, cpu_count

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from models.formulation.model import formulation_optimizer
from scoring_engine import scoring_engine
from candidate_engine import candidate_engine

def worker_task(args):
    idx, combo, targets, brief_dict = args
    ing_dicts = []
    for ing in combo:
        ing_dicts.append({
            "name": ing["name"],
            "category": ing.get("category", "General"),
            "functional_role": ing.get("functional_role", "Base Raw Material"),
            "protein": float(ing.get("protein", 0.0) or 0.0),
            "fat": float(ing.get("fat", 0.0) or 0.0),
            "carbs": float(ing.get("carbs", 0.0) or 0.0),
            "calories": float(ing.get("calories", 0.0) or 0.0),
            "cost_per_kg": ing.get("cost_per_kg")
        })

    opt_res, _ = formulation_optimizer.predict_with_uncertainty({
        "ingredients": ing_dicts,
        "targets": targets,
        "strategy": "balanced"
    })
    return idx, opt_res.get("is_feasible", False)

if __name__ == "__main__":
    combo = [
        {'name': 'Pea Protein Isolate (85%)', 'protein': 85.0, 'fat': 4.0, 'carbs': 2.0, 'calories': 380.0, 'cost_per_kg': 12.4},
        {'name': 'Prime Press Cocoa Butter', 'protein': 0.0, 'fat': 100.0, 'carbs': 0.0, 'calories': 884.0, 'cost_per_kg': 18.5},
        {'name': 'Erythritol Polyol', 'protein': 0.0, 'fat': 0.0, 'carbs': 100.0, 'calories': 0.0, 'cost_per_kg': 6.2},
        {'name': 'Natural Bourbon Vanilla Extract', 'protein': 0.0, 'fat': 0.0, 'carbs': 12.0, 'calories': 288.0, 'cost_per_kg': 38.0},
        {'name': 'Almond Flour', 'protein': 21.0, 'fat': 50.0, 'carbs': 20.0, 'calories': 590.0, 'cost_per_kg': 13.5}
    ]
    targets = {'protein_min': 7.0, 'cocoa_butter_min': 25.0, 'almond_min': 8.0, 'sugar_max': 28.0, 'cost_target': 15.0}
    brief_dict = {"description": "test brief"}

    tasks = [(i, combo, targets, brief_dict) for i in range(200)]
    t0 = time.time()
    with Pool(processes=min(cpu_count(), 10)) as pool:
        results = pool.map(worker_task, tasks)
    dt = time.time() - t0
    print(f"Executed {len(results)} tasks in {dt:.2f}s ({len(results)/dt:.1f} tasks/sec)")
