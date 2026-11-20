import sys, time
from multiprocessing import Pool, cpu_count
from pathlib import Path
sys.path.insert(0, r"Food Web App Core/backend")
sys.path.insert(0, r".")

from models.formulation.model import formulation_optimizer

sample_ingredients = [
    {"name": "Pea Protein", "category": "Plant Protein", "functional_role": "Protein Source", "protein": 85.0, "fat": 7.0, "carbs": 2.0, "cost_per_kg": 4.5},
    {"name": "Cocoa Butter", "category": "Fats & Oils", "functional_role": "Fat Source", "protein": 0.0, "fat": 100.0, "carbs": 0.0, "cost_per_kg": 9.0},
    {"name": "Erythritol", "category": "Sweeteners", "functional_role": "Sweetener", "protein": 0.0, "fat": 0.0, "carbs": 0.0, "cost_per_kg": 3.5},
    {"name": "Vanilla Extract", "category": "Flavors", "functional_role": "Flavor", "protein": 0.0, "fat": 0.0, "carbs": 12.0, "cost_per_kg": 25.0},
    {"name": "Inulin", "category": "Fibres", "functional_role": "Binder/Texture", "protein": 0.0, "fat": 0.0, "carbs": 95.0, "cost_per_kg": 3.8}
]
targets = {"protein_min": 7.0, "cost_target": 10.0}

def eval_one(i):
    res, _ = formulation_optimizer.predict_with_uncertainty({
        "ingredients": sample_ingredients,
        "targets": targets,
        "strategy": "balanced"
    })
    return res["is_feasible"]

if __name__ == "__main__":
    cores = min(10, cpu_count())
    n = 2000
    t0 = time.time()
    with Pool(cores) as p:
        res = p.map(eval_one, range(n), chunksize=50)
    t1 = time.time()
    elapsed = t1 - t0
    rate = n / elapsed
    print(f"Cores: {cores}, {n} items in {elapsed:.2f}s ({rate:.1f} per sec)")
    est_total_s = 231660 / rate
    print(f"Estimated time for 231,660: {est_total_s:.1f}s ({est_total_s/60:.1f} minutes)")
