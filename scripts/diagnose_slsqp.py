import sys
sys.path.insert(0, 'Food Web App Core/backend')
from requirements_extractor import product_brief_parser
from candidate_engine import candidate_engine
import numpy as np

brief = product_brief_parser.parse('Design a vegan, gluten-free high protein bar')

from models.formulation.model import formulation_optimizer
from scipy.optimize import minimize

# Let's inspect the cost_optimized run directly
def check_cost_opt(data):
    ingredients = data.get("ingredients", [])
    targets = data.get("targets", {})
    strategy = data.get("strategy", "balanced")
    if strategy == "cost_optimized":
        protein_vec = np.array([float(i.get("protein", 0.0) or 0.0) for i in ingredients])
        target_prot = float(targets.get("protein_min", 20.0) or 20.0)
        print("cost_optimized ingredients and protein:")
        for ing, p in zip(ingredients, protein_vec):
            print(f"  {ing['name']}: {p}% protein")
        print(f"target_prot: {target_prot}")
        print(f"max in protein_vec: {np.max(protein_vec)}")

check_cost_opt_wrap = formulation_optimizer.predict_with_uncertainty
formulation_optimizer.predict_with_uncertainty = lambda d: (check_cost_opt(d), check_cost_opt_wrap(d)[1])[1:]
exps = candidate_engine.generate_experiments(brief)
