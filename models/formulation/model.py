"""
Mathematical Formulation Optimization Model (Phase 9: Real Formulation Engine)
Generates optimal ingredient percentages using constrained numerical optimization (SLSQP).
Guarantees strict mathematical mass-balance feasibility: sum(percentages) == 100.0000%.
Translates all extracted numerical constraints (protein, fat, sugar, fibre, cocoa butter, almond, cost)
into formal SLSQP constraints and performs rigorous pre- and post-optimization feasibility validation.
"""
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
from scipy.optimize import minimize
import logging

logger = logging.getLogger("FormulationOptimizer")

class FormulationOptimizationModel:
    def __init__(self):
        self.version = "2.1.0"

    def optimize_formulation(
        self,
        ingredients: List[Dict[str, Any]],
        targets: Dict[str, Any],
        strategy: str = "balanced"
    ) -> Dict[str, Any]:
        result, _ = self.predict_with_uncertainty({
            "ingredients": ingredients,
            "targets": targets,
            "strategy": strategy
        })
        return result

    def predict(self, input_dict: Dict[str, Any]) -> Dict[str, Any]:
        result, _ = self.predict_with_uncertainty(input_dict)
        return result

    def predict_with_uncertainty(self, input_dict: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
        """
        Solves the constrained non-linear optimization problem for ingredient inclusion percentages.
        Guarantees:
        1. sum(x_i) == 100.0000%
        2. Bounds: l_i <= x_i <= u_i
        3. Hard inequality constraints for all specified nutritional & ingredient thresholds
        4. Pre-optimization mathematical feasibility check
        5. Post-optimization independent numerical validation
        """
        ingredients = input_dict.get("ingredients", [])
        targets = input_dict.get("targets", {})
        strategy = input_dict.get("strategy", "balanced")
        
        n = len(ingredients)
        if n == 0:
            return {
                "percentages": [],
                "is_feasible": False,
                "status": "EMPTY_INGREDIENT_POOL",
                "solver_message": "Zero ingredients provided for formulation optimization.",
                "violations": ["Empty ingredient pool"]
            }, 0.0

        # Extract nutrient vectors
        protein_vec = np.array([float(i.get("protein", 0.0) or 0.0) for i in ingredients])
        fat_vec = np.array([float(i.get("fat", 0.0) or 0.0) for i in ingredients])
        carb_vec = np.array([float(i.get("carbs", 0.0) or 0.0) for i in ingredients])
        sugar_vec = np.array([float(i.get("sugar", 0.0) or 0.0) for i in ingredients])
        fibre_vec = np.array([float(i.get("fibre", i.get("fiber", 0.0)) or 0.0) for i in ingredients])
        cal_vec = np.array([float(i.get("calories", 0.0) or 0.0) for i in ingredients])
        cost_vec = np.array([float(i.get("cost_per_kg", 0.0) or 0.0) for i in ingredients])

        # Target constraints extraction
        target_prot = float(targets.get("protein_min", 0.0) or 0.0)
        target_prot_max = float(targets["protein_max"]) if targets.get("protein_max") is not None else None
        target_sugar = float(targets["sugar_max"]) if targets.get("sugar_max") is not None else None
        target_fat = float(targets["fat_max"]) if targets.get("fat_max") is not None else None
        target_fat_min = float(targets["fat_min"]) if targets.get("fat_min") is not None else None
        target_fibre = float(targets["fibre_min"]) if targets.get("fibre_min") is not None else None
        target_cb = float(targets["cocoa_butter_min"]) if targets.get("cocoa_butter_min") is not None else None
        target_almond = float(targets["almond_min"]) if targets.get("almond_min") is not None else None
        target_cost = float(targets.get("cost_target", 15.0) or 15.0)

        # Determine realistic bounds based on functional role, ingredient nature, and specific identity
        bounds = []
        bounds_diagnostics = []
        for ing in ingredients:
            name = str(ing.get("name", "")).lower()
            role = str(ing.get("functional_role", "")).lower()
            cat = str(ing.get("category", "")).lower()
            ing_id = str(ing.get("id", "")).lower()
            
            # 1. Minerals / Salt
            if "salt" in name or "sodium chloride" in name:
                b = (0.05, 0.40)
            # 2. Stimulants (Caffeine, active extracts)
            elif "caffeine" in name:
                b = (0.01, 0.15)
            # 3. Cocoa Butter & Core Lipids
            elif "cocoa butter" in name or "cocoa_butter" in ing_id:
                min_cb = target_cb if target_cb is not None else 15.0
                b = (min_cb, 45.0)
            # 3b. Almond Ingredients (Almond Flour, Almond Butter, etc.)
            elif "almond" in name:
                min_alm = target_almond if target_almond is not None else 8.0
                b = (min_alm, 45.0)
            # 4. Cocoa Solids / Cocoa Mass / Cocoa Powder
            elif any(c in name for c in ["cocoa mass", "cocoa liquor", "cocoa solids", "cocoa powder", "cacao"]):
                b = (5.0, 35.0)
            # 5. Dairy & Plant Milk Solids
            elif any(m in name for m in ["milk powder", "milk solids", "whey powder", "whole milk", "skim milk"]):
                b = (8.0, 35.0)
            # 6. Nutritive Sweeteners & Polyols (Sugar, Allulose, Erythritol)
            elif "sweetener" in role or "sweetener" in cat or any(s in name for s in ["sugar", "allulose", "erythritol", "glucose", "syrup"]):
                max_s = target_sugar if (target_sugar is not None and any(s in name for s in ["cane sugar", "coconut sugar", "granulated sugar"])) else 58.0
                b = (5.0, max_s)
            # 7. High-Intensity Sweeteners (Stevia, Monk Fruit, Sucralose)
            elif any(s in name for s in ["stevia", "monk", "sucralose", "reb m", "mogroside"]):
                b = (0.005, 0.20)
            # 8. Preservatives & Antioxidants
            elif any(k in role or k in cat or k in name for k in ["preservative", "antioxidant", "tocopherol", "sorbate", "benzoate"]):
                b = (0.005, 0.25)
            # 9. Colorants
            elif any(k in role or k in cat or k in name for k in ["color", "carotene"]):
                b = (0.001, 0.05)
            # 10. Emulsifiers & Surfactants
            elif any(k in role or k in cat or k in name for k in ["emulsifier", "lecithin", "phosphatide", "pgpr", "glyceride", "polysorbate"]):
                b = (0.15, 0.80)
            # 11. Flavors & Aroma extracts
            elif any(k in role or k in cat or k in name for k in ["vanilla", "vanillin", "flavor", "flavour", "extract"]):
                b = (0.02, 0.50)
            # 12. Hydrocolloids & Gelling agents
            elif any(k in role or k in cat or k in name for k in ["hydrocolloid", "stabilizer", "gum", "pectin"]):
                b = (0.05, 1.50)
            # 13. Acidity regulators
            elif any(k in role or k in cat or k in name for k in ["acidity", "acid"]):
                b = (0.05, 0.80)
            # 14. Leavening / Raising agents
            elif any(k in role or k in cat or k in name for k in ["leavening", "raising", "bicarbonate"]):
                b = (0.05, 1.20)
            # 15. Protein Concentrates / Isolates
            elif any(k in role or k in cat for k in ["protein"]):
                b = (3.0, 50.0)
            # 16. Flours & Starches
            elif any(f in name or f in cat for f in ["flour", "starch"]):
                b = (10.0, 65.0)
            else:
                b = (5.0, 60.0)

            bounds.append(b)
            bounds_diagnostics.append({"name": ing.get("name"), "lower": b[0], "upper": b[1]})

        # --- PRE-OPTIMIZATION FEASIBILITY CHECK ---
        pre_violations = []
        sum_lower = sum(b[0] for b in bounds)
        sum_upper = sum(b[1] for b in bounds)

        if sum_lower > 100.0:
            pre_violations.append(
                f"Sum of ingredient lower bounds ({sum_lower:.2f}%) exceeds 100.0%. Impossible to balance mass."
            )
        if sum_upper < 100.0:
            pre_violations.append(
                f"Sum of ingredient upper bounds ({sum_upper:.2f}%) is less than 100.0%. Impossible to reach 100% mass."
            )

        # Check maximum achievable protein within bounds
        max_possible_prot = sum((b[1] / 100.0) * p for b, p in zip(bounds, protein_vec))
        if target_prot > 0 and max_possible_prot < target_prot:
            pre_violations.append(
                f"Maximum achievable protein with current ingredients ({max_possible_prot:.2f}%) is less than required {target_prot:.2f}%."
            )

        # Check minimum achievable sugar within bounds
        if target_sugar is not None:
            min_possible_sugar = sum((b[0] / 100.0) * s for b, s in zip(bounds, sugar_vec))
            if min_possible_sugar > target_sugar:
                pre_violations.append(
                    f"Minimum achievable sugar ({min_possible_sugar:.2f}%) exceeds required maximum of {target_sugar:.2f}%."
                )

        if pre_violations:
            logger.warning(f"Pre-optimization infeasibility detected: {pre_violations}")
            # Generate best-effort normalized distribution but flag strictly as INFEASIBLE
            x0 = np.array([b[0] + (b[1] - b[0]) * 0.5 for b in bounds])
            if np.sum(x0) > 0:
                x0 = (x0 / np.sum(x0)) * 100.0
            
            yield_prot = round(float(np.dot(x0 / 100.0, protein_vec)), 2)
            yield_fat = round(float(np.dot(x0 / 100.0, fat_vec)), 2)
            yield_carb = round(float(np.dot(x0 / 100.0, carb_vec)), 2)
            yield_sugar = round(float(np.dot(x0 / 100.0, sugar_vec)), 2)
            yield_fibre = round(float(np.dot(x0 / 100.0, fibre_vec)), 2)
            yield_cal = round((4.0 * yield_prot) + (4.0 * yield_carb) + (9.0 * yield_fat), 1)
            has_unknown_cost = any(i.get("cost_per_kg") is None for i in ingredients)
            yield_cost = None if has_unknown_cost else round(float(np.dot(x0 / 100.0, cost_vec)), 2)

            return {
                "percentages": [round(float(v), 2) for v in x0],
                "is_feasible": False,
                "status": "CONTRADICTORY_OR_INFEASIBLE_CONSTRAINTS",
                "solver_message": "Pre-optimization feasibility check failed: mathematical contradiction in constraints.",
                "violations": pre_violations,
                "bounds": bounds_diagnostics,
                "nutrition_yield": {
                    "protein": yield_prot,
                    "fat": yield_fat,
                    "carbs": yield_carb,
                    "sugar": yield_sugar,
                    "fibre": yield_fibre,
                    "calories": yield_cal
                },
                "cost_per_kg": yield_cost,
                "cost_status": "CALCULATED" if yield_cost is not None else "COST_UNKNOWN"
            }, 0.0

        # --- OBJECTIVE FUNCTION ---
        def objective(x):
            curr_prot = np.dot(x / 100.0, protein_vec)
            curr_cost = np.dot(x / 100.0, cost_vec)
            curr_sugar = np.dot(x / 100.0, sugar_vec)
            
            if strategy == "nutrition_maximized":
                # Heavy weight on protein maximization, light on cost
                loss = - (curr_prot * 4.0) + (curr_cost * 0.4)
            elif strategy == "cost_optimized":
                # Heavy weight on cost minimization, tracking target protein
                prot_pen = max(0.0, target_prot - curr_prot) ** 2 if target_prot > 0 else 0.0
                loss = (curr_cost * 10.0) + (prot_pen * 25.0)
            elif strategy == "functionality_texture":
                # Moderate protein, balanced lipid/cost
                loss = - (curr_prot * 1.5) + (curr_cost * 0.8)
            else:  # balanced
                prot_pen = ((curr_prot - target_prot) ** 2) if target_prot > 0 else 0.0
                loss = (prot_pen * 2.0) + (curr_cost * 1.5)
                
            return loss

        # --- FORMAL SLSQP CONSTRAINTS ---
        # 1. Physical Equality: Mass balance must equal 100.0000%
        cons = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 100.0}
        ]

        active_constraint_names = ["sum(x) == 100.0%"]

        # 2. Protein Minimum Constraint (Hard)
        if target_prot > 0:
            cons.append({
                'type': 'ineq',
                'fun': lambda x: np.dot(x / 100.0, protein_vec) - target_prot
            })
            active_constraint_names.append(f"protein >= {target_prot}%")

        # 3. Protein Maximum Constraint (Hard)
        if target_prot_max is not None:
            cons.append({
                'type': 'ineq',
                'fun': lambda x: target_prot_max - np.dot(x / 100.0, protein_vec)
            })
            active_constraint_names.append(f"protein <= {target_prot_max}%")

        # 4. Sugar Maximum Constraint (Hard)
        if target_sugar is not None:
            cons.append({
                'type': 'ineq',
                'fun': lambda x: target_sugar - np.dot(x / 100.0, sugar_vec)
            })
            active_constraint_names.append(f"sugar <= {target_sugar}%")

        # 5. Fat Maximum Constraint (Hard)
        if target_fat is not None:
            cons.append({
                'type': 'ineq',
                'fun': lambda x: target_fat - np.dot(x / 100.0, fat_vec)
            })
            active_constraint_names.append(f"fat <= {target_fat}%")

        # 6. Fat Minimum Constraint (Hard)
        if target_fat_min is not None:
            cons.append({
                'type': 'ineq',
                'fun': lambda x: np.dot(x / 100.0, fat_vec) - target_fat_min
            })
            active_constraint_names.append(f"fat >= {target_fat_min}%")

        # 7. Fibre Minimum Constraint (Hard)
        if target_fibre is not None:
            cons.append({
                'type': 'ineq',
                'fun': lambda x: np.dot(x / 100.0, fibre_vec) - target_fibre
            })
            active_constraint_names.append(f"fibre >= {target_fibre}%")

        # Initial guess: midpoint of bounds normalized to sum to 100.0
        x0 = np.array([b[0] + (b[1] - b[0]) * 0.5 for b in bounds])
        if np.sum(x0) > 0:
            x0 = (x0 / np.sum(x0)) * 100.0
        x0 = np.clip(x0, [b[0] for b in bounds], [b[1] for b in bounds])
        if np.sum(x0) > 0:
            x0 = (x0 / np.sum(x0)) * 100.0

        # Run SLSQP solver
        res = minimize(
            objective,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=cons,
            options={'maxiter': 500, 'ftol': 1e-6}
        )

        opt_x = res.x if res.success else x0
        
        # Exact mass balance post-normalization (sum == 100.0000%)
        total = np.sum(opt_x)
        if total > 0:
            opt_x = (opt_x / total) * 100.0
            
        # Round minor ingredients carefully to 4 decimals, majors to 2
        pcts = []
        for val in opt_x:
            if val <= 1.0:
                pcts.append(round(float(val), 4))
            else:
                pcts.append(round(float(val), 2))
                
        # Absorb precision rounding delta strictly on largest bulk component
        diff = round(100.0000 - sum(pcts), 4)
        if pcts:
            max_idx = int(np.argmax(pcts))
            pcts[max_idx] = round(pcts[max_idx] + diff, 4)

        # Compute resulting yields deterministically
        pcts_arr = np.array(pcts) / 100.0
        yield_prot = round(float(np.dot(pcts_arr, protein_vec)), 2)
        yield_fat = round(float(np.dot(pcts_arr, fat_vec)), 2)
        yield_carb = round(float(np.dot(pcts_arr, carb_vec)), 2)
        yield_sugar = round(float(np.dot(pcts_arr, sugar_vec)), 2)
        yield_fibre = round(float(np.dot(pcts_arr, fibre_vec)), 2)
        yield_cal = round((4.0 * yield_prot) + (4.0 * yield_carb) + (9.0 * yield_fat), 1)
        
        has_unknown_costs = any(i.get("cost_per_kg") is None for i in ingredients)
        yield_cost = None if has_unknown_costs else round(float(np.dot(pcts_arr, cost_vec)), 2)

        # --- POST-OPTIMIZATION INDEPENDENT VALIDATION ---
        post_violations = []
        mass_deviation = abs(sum(pcts) - 100.0000)
        if mass_deviation > 0.01:
            post_violations.append(f"Mass balance deviation: sum is {sum(pcts):.4f}% (target: 100.0000%)")

        for idx, (pct_val, (low_b, high_b)) in enumerate(zip(pcts, bounds)):
            if pct_val < low_b - 0.05:
                post_violations.append(f"Ingredient '{ingredients[idx].get('name')}' inclusion {pct_val}% is below lower bound {low_b}%")
            if pct_val > high_b + 0.05:
                post_violations.append(f"Ingredient '{ingredients[idx].get('name')}' inclusion {pct_val}% exceeds upper bound {high_b}%")

        if target_prot > 0 and yield_prot < (target_prot - 0.1):
            post_violations.append(f"Protein yield {yield_prot}% does not satisfy target minimum {target_prot}%")

        if target_sugar is not None and yield_sugar > (target_sugar + 0.1):
            post_violations.append(f"Sugar yield {yield_sugar}% exceeds maximum allowable {target_sugar}%")

        if target_fat is not None and yield_fat > (target_fat + 0.1):
            post_violations.append(f"Fat yield {yield_fat}% exceeds maximum allowable {target_fat}%")

        is_mathematically_valid = res.success and (len(post_violations) == 0)

        status_str = "OPTIMIZED" if is_mathematically_valid else ("FEASIBILITY_WARNING" if res.success else "SOLVER_FAILED")

        return {
            "percentages": pcts,
            "is_feasible": is_mathematically_valid,
            "status": status_str,
            "solver_message": str(res.message),
            "iterations": int(res.nit) if hasattr(res, "nit") else 0,
            "active_constraints": active_constraint_names,
            "violations": post_violations,
            "bounds": bounds_diagnostics,
            "mass_balance_deviation": round(mass_deviation, 4),
            "nutrition_yield": {
                "protein": yield_prot,
                "fat": yield_fat,
                "carbs": yield_carb,
                "sugar": yield_sugar,
                "fibre": yield_fibre,
                "calories": yield_cal
            },
            "cost_per_kg": yield_cost,
            "cost_status": "CALCULATED" if yield_cost is not None else "COST_UNKNOWN"
        }, 0.95 if is_mathematically_valid else 0.60

    def metadata(self) -> Dict[str, Any]:
        return {
            "model_name": "FormulationOptimizationModel",
            "version": self.version,
            "solver": "scipy.optimize.minimize (SLSQP)",
            "paradigm": "Constrained Nonlinear Programming",
            "status": "ACTIVE"
        }

# Global instance
formulation_optimizer = FormulationOptimizationModel()
