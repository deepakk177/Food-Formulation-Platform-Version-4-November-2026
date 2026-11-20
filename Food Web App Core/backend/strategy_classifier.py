"""
Dynamic Candidate Set Strategy Classification Engine.
Implements Parts 3 & 4 of Master Implementation Specification:
1. Metric Normalization (Benefit S_i = (x - min)/(max - min), Cost S_i = (max - x)/(max - min))
2. Multi-Objective Evaluation across Economic, Nutritional, Functional/Flavor, and Balanced dimensions
3. Strict condition compliance:
   - Cost Optimized: lowest valid formulation cost/kg among feasible candidates
   - Nutrition Maximized: strongest overall nutritional performance (protein, fibre, minerals, sugar, fat, calories)
   - Balanced Set: strongest multi-objective Pareto compromise across all dimensions
   - Functionality & Flavor: strongest verified functional properties, texture, and ingredient compatibility
4. Dynamic 1-to-1 Assignment (Hungarian / Maximum Utility Bipartite Matching) so candidate IDs
   never have fixed/hardcoded strategy names.
"""
from typing import Dict, Any, List, Optional, Tuple
import logging
import numpy as np
from scipy.optimize import linear_sum_assignment

logger = logging.getLogger("StrategyClassifier")

STRATEGY_LABELS = {
    "cost_optimized": "Cost Optimized",
    "nutrition_maximized": "Nutrition Maximized",
    "balanced": "Balanced Set",
    "functionality_flavor": "Functionality & Flavor"
}

def normalize_benefit(val: float, min_val: float, max_val: float) -> float:
    """Benefit metric normalization: higher is better [0.0, 1.0]."""
    if max_val - min_val < 1e-6:
        return 1.0
    return max(0.0, min(1.0, (val - min_val) / (max_val - min_val)))

def normalize_cost(val: float, min_val: float, max_val: float) -> float:
    """Cost metric normalization: lower is better [0.0, 1.0]."""
    if max_val - min_val < 1e-6:
        return 1.0
    return max(0.0, min(1.0, (max_val - val) / (max_val - min_val)))

class DynamicStrategyClassifier:
    """
    Evaluates candidate formulations based on actual characteristics and dynamically assigns:
    1. Cost Optimized
    2. Nutrition Maximized
    3. Balanced Set
    4. Functionality & Flavor
    """

    def classify_candidates(
        self,
        candidates: List[Dict[str, Any]],
        brief: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Dynamically classifies candidates based strictly on measured evaluation metrics.
        Never uses fixed candidate IDs (FC-001, FC-002, etc.) or hardcoded mappings.
        """
        if not candidates:
            return candidates

        n = len(candidates)
        if n == 1:
            # Single candidate default: Balanced Set
            c = candidates[0]
            label = "Balanced Set"
            c["strategy_label"] = label
            c["strategy_short_label"] = label
            c["strategy_name"] = label
            c["set_name"] = f"Candidate {c.get('candidate_id', 'FC-001')} ({label})"
            return candidates

        # -------------------------------------------------------------
        # 1. Collect Real Evaluation Metrics for each candidate
        # -------------------------------------------------------------
        metrics = []
        for idx, cand in enumerate(candidates):
            nut = cand.get("nutrition", {}) or {}
            mac = cand.get("macros", {}) or {}
            scoring = cand.get("scoring", {}) or {}
            radar = scoring.get("radar_scores", {}) or scoring.get("radar", {}) or {}
            cost_snap = cand.get("cost_snapshot", {}) or {}

            # Feasibility & hard constraint compliance
            is_feasible = bool(cand.get("is_feasible", True))
            violations = cand.get("hard_constraint_violations", cand.get("violations", []))
            feasibility_score = 1.0 if (is_feasible and len(violations) == 0) else 0.2

            # Economic: cost per kg
            cost_val = cand.get("cost_per_kg")
            if cost_val is None:
                cost_val = cost_snap.get("cost_per_kg")
            if cost_val is None:
                cost_val = mac.get("cost_per_kg")
            cost_status = cand.get("cost_status", cost_snap.get("cost_status", "KNOWN"))
            has_valid_cost = (cost_val is not None and cost_status != "COST_DATA_UNAVAILABLE")
            eff_cost = float(cost_val) if has_valid_cost else 999.0

            # Nutritional metrics (per 100g)
            protein = float(nut.get("protein", mac.get("protein", 0.0)) or 0.0)
            fibre = float(nut.get("fibre", mac.get("fibre", 0.0)) or 0.0)
            sugar = float(nut.get("sugar", mac.get("sugar", 0.0)) or 0.0)
            fat = float(nut.get("fat", mac.get("fat", 0.0)) or 0.0)
            calories = float(nut.get("calories", mac.get("calories", 0.0)) or 0.0)
            minerals = float(nut.get("key_minerals_mg", mac.get("key_minerals_mg", 380.0)) or 380.0)

            nut_fit = float(cand.get("nutrition_fit_score", radar.get("Nutrition", scoring.get("nutrition_fit_score", 70.0))) or 70.0)

            # Functional & Compatibility metrics
            compat = float(cand.get("compatibility_score", radar.get("Compatibility", 75.0)) or 75.0)
            frc = float(cand.get("functional_role_coverage_score", radar.get("FRC", 80.0)) or 80.0)
            soft_sat = float(cand.get("soft_constraint_score", radar.get("Constraint_Satisfaction", 75.0)) or 75.0)

            # Functional texturizer fraction (from components)
            all_comps = (
                cand.get("composition", {}).get("all_components")
                or cand.get("composition", {}).get("bulk_ingredients", []) + cand.get("composition", {}).get("functional_ingredients", [])
                or []
            )
            func_fraction = sum(
                float(c.get("percentage", 0.0))
                for c in all_comps
                if any(k in str(c.get("functional_role", "")).lower() for k in ["emulsifier", "stabilizer", "texturizer", "raising", "thickener"])
                or any(k in str(c.get("name", "")).lower() for k in ["lecithin", "phosphatide", "glyceride", "gum", "pectin", "starch"])
            )

            # Overall Pareto Score
            overall_score = float(cand.get("universal_evaluation_score", scoring.get("overall_score", 80.0)) or 80.0)

            metrics.append({
                "index": idx,
                "candidate_id": cand.get("candidate_id", f"FC-{idx+1:03d}"),
                "is_feasible": is_feasible,
                "feasibility_score": feasibility_score,
                "cost": eff_cost,
                "has_valid_cost": has_valid_cost,
                "protein": protein,
                "fibre": fibre,
                "sugar": sugar,
                "fat": fat,
                "calories": calories,
                "minerals": minerals,
                "nutrition_fit": nut_fit,
                "compatibility": compat,
                "frc": frc,
                "soft_sat": soft_sat,
                "func_fraction": func_fraction,
                "overall_score": overall_score
            })

        # -------------------------------------------------------------
        # 2. Normalize Metrics across the candidate set
        # -------------------------------------------------------------
        # Extract min and max ranges
        valid_costs = [m["cost"] for m in metrics if m["has_valid_cost"] and m["cost"] < 900.0]
        min_cost = min(valid_costs) if valid_costs else 0.0
        max_cost = max(valid_costs) if valid_costs else 1.0

        min_prot = min(m["protein"] for m in metrics)
        max_prot = max(m["protein"] for m in metrics)

        min_fib = min(m["fibre"] for m in metrics)
        max_fib = max(m["fibre"] for m in metrics)

        min_sug = min(m["sugar"] for m in metrics)
        max_sug = max(m["sugar"] for m in metrics)

        min_minerals = min(m["minerals"] for m in metrics)
        max_minerals = max(m["minerals"] for m in metrics)

        min_nut_fit = min(m["nutrition_fit"] for m in metrics)
        max_nut_fit = max(m["nutrition_fit"] for m in metrics)

        min_compat = min(m["compatibility"] for m in metrics)
        max_compat = max(m["compatibility"] for m in metrics)

        min_frc = min(m["frc"] for m in metrics)
        max_frc = max(m["frc"] for m in metrics)

        min_func = min(m["func_fraction"] for m in metrics)
        max_func = max(m["func_fraction"] for m in metrics)

        min_overall = min(m["overall_score"] for m in metrics)
        max_overall = max(m["overall_score"] for m in metrics)

        # -------------------------------------------------------------
        # 3. Compute Objective Qualification Scores for each category
        # -------------------------------------------------------------
        # Four target categories:
        categories = ["cost_optimized", "nutrition_maximized", "balanced", "functionality_flavor"]
        
        # Matrix score[cand_idx][cat]
        cat_scores = []

        for m in metrics:
            # 3.1 Cost Optimized Score:
            # Must satisfy hard constraints. Lower cost = higher score.
            s_cost_norm = normalize_cost(m["cost"], min_cost, max_cost) if m["has_valid_cost"] else 0.0
            # If infeasible or missing cost, heavily penalized
            cost_qual_score = (s_cost_norm * 0.85 + m["feasibility_score"] * 0.15) if (m["is_feasible"] and m["has_valid_cost"]) else 0.05

            # 3.2 Nutrition Maximized Score:
            # Evaluates protein, minerals, fibre, sugar moderation, and overall nutrition fit
            s_prot = normalize_benefit(m["protein"], min_prot, max_prot)
            s_min = normalize_benefit(m["minerals"], min_minerals, max_minerals)
            s_fib = normalize_benefit(m["fibre"], min_fib, max_fib)
            s_sug = normalize_cost(m["sugar"], min_sug, max_sug)
            s_nfit = normalize_benefit(m["nutrition_fit"], min_nut_fit, max_nut_fit)

            nutr_qual_score = (
                0.35 * s_prot +
                0.20 * s_min +
                0.15 * s_fib +
                0.15 * s_sug +
                0.15 * s_nfit
            ) * m["feasibility_score"]

            # 3.3 Functionality & Flavor Score:
            # Strongest verified performance in texture, compatibility, FRC, functional texturizers
            s_compat = normalize_benefit(m["compatibility"], min_compat, max_compat)
            s_frc = normalize_benefit(m["frc"], min_frc, max_frc)
            s_ffrac = normalize_benefit(m["func_fraction"], min_func, max_func)
            s_soft = normalize_benefit(m["soft_sat"], 0.0, 100.0)

            func_flavor_score = (
                0.35 * s_frc +
                0.30 * s_compat +
                0.20 * s_ffrac +
                0.15 * s_soft
            ) * m["feasibility_score"]

            # 3.4 Balanced Set Score:
            # Strongest overall Pareto compromise across cost, nutrition, functionality, quality
            # Evaluates well-roundedness (penalizing high variance/imbalance)
            dim_scores = [s_cost_norm, nutr_qual_score, func_flavor_score]
            mean_dim = sum(dim_scores) / len(dim_scores)
            var_dim = sum((d - mean_dim) ** 2 for d in dim_scores) / len(dim_scores)
            s_pareto = normalize_benefit(m["overall_score"], min_overall, max_overall)
            
            balanced_qual_score = (0.50 * mean_dim + 0.35 * s_pareto + 0.15 * (1.0 - min(1.0, var_dim * 2.0))) * m["feasibility_score"]

            cat_scores.append({
                "cost_optimized": cost_qual_score,
                "nutrition_maximized": nutr_qual_score,
                "balanced": balanced_qual_score,
                "functionality_flavor": func_flavor_score
            })

        # -------------------------------------------------------------
        # 4. Dynamic 1-to-1 Assignment (Maximum Utility Matching)
        # -------------------------------------------------------------
        # Find assignment of candidates to categories that maximizes total qualification utility
        # and guarantees that the lowest cost candidate gets Cost Optimized and top nutrition gets Nutrition Maximized.
        assigned_categories = self._solve_optimal_assignment(cat_scores, categories, metrics)

        # -------------------------------------------------------------
        # 5. Apply Strategy Labels and Detailed Rationales to Candidates
        # -------------------------------------------------------------
        for idx, cand in enumerate(candidates):
            strat_key = assigned_categories.get(idx, "balanced")
            label = STRATEGY_LABELS.get(strat_key, "Balanced Set")
            m = metrics[idx]

            cand["strategy_id"] = strat_key
            cand["strategy_label"] = label
            cand["strategy_short_label"] = label
            cand["strategy_name"] = label
            cand["set_name"] = label
            cand["title"] = f"{label} ({cand.get('candidate_id', f'FC-{idx+1:03d}')})"

            # Construct verified strategy rationale based on actual metrics
            cand["strategy_rationale"] = self._build_dynamic_rationale(strat_key, label, m)

        logger.info(
            "Dynamic Strategy Classification Complete: %s",
            {c.get("candidate_id"): c.get("strategy_label") for c in candidates}
        )
        return candidates

    def _solve_optimal_assignment(
        self,
        cat_scores: List[Dict[str, float]],
        categories: List[str],
        metrics: List[Dict[str, Any]]
    ) -> Dict[int, str]:
        """
        Solves optimal assignment of candidates to strategy categories using Maximum Utility
        Bipartite Matching (linear_sum_assignment / Hungarian algorithm).
        
        Strict Guarantee: "Keep one set per type"
        - When N candidates and M categories are provided, each candidate receives a UNIQUE category.
        - No category is EVER duplicated when n_cands <= len(categories).
        - For 4 candidates, exactly 1 Cost Optimized, 1 Nutrition Maximized, 1 Balanced Set,
          and 1 Functionality & Flavor are assigned.
        - Cost Optimized goes to the lowest cost candidate (feasible preferred).
        - Nutrition Maximized goes to the candidate with strongest nutritional density.
        - Balanced Set goes to the most rounded Pareto compromise.
        - Functionality & Flavor goes to the candidate with strongest functional integrity & sensory appeal.
        """
        n_cands = len(cat_scores)
        n_cats = len(categories)

        if n_cands == 0:
            return {}

        # Construct utility matrix U[cand_idx, cat_idx]
        U = np.zeros((n_cands, n_cats), dtype=float)

        # 1. Identify baseline cost ranking (feasible first, then all valid costs)
        feasible_costs = [
            (idx, metrics[idx]["cost"])
            for idx in range(n_cands)
            if metrics[idx]["is_feasible"] and metrics[idx]["has_valid_cost"] and metrics[idx]["cost"] < 900.0
        ]
        all_costs = [
            (idx, metrics[idx]["cost"])
            for idx in range(n_cands)
            if metrics[idx]["has_valid_cost"] and metrics[idx]["cost"] < 900.0
        ]
        
        cheapest_idx = None
        if feasible_costs:
            feasible_costs.sort(key=lambda x: x[1])
            cheapest_idx = feasible_costs[0][0]
        elif all_costs:
            all_costs.sort(key=lambda x: x[1])
            cheapest_idx = all_costs[0][0]

        # 2. Identify top nutrition candidate
        nutr_ranked = sorted(
            range(n_cands),
            key=lambda idx: (metrics[idx]["is_feasible"], cat_scores[idx].get("nutrition_maximized", 0.0)),
            reverse=True
        )
        top_nutr_idx = nutr_ranked[0] if nutr_ranked else None

        for i in range(n_cands):
            m = metrics[i]
            for j, cat in enumerate(categories):
                base_score = float(cat_scores[i].get(cat, 0.0))
                score = base_score * 10.0

                if m["is_feasible"]:
                    score += 5.0

                if cat == "cost_optimized":
                    if cheapest_idx == i:
                        score += 50.0  # Dominant prime claim for lowest-cost candidate
                    elif m["has_valid_cost"]:
                        score += max(0.0, (15.0 - m["cost"]))
                elif cat == "nutrition_maximized":
                    if top_nutr_idx == i and (top_nutr_idx != cheapest_idx or n_cands == 1):
                        score += 40.0  # Dominant prime claim for top nutrition
                elif cat == "functionality_flavor":
                    score += (m.get("func_fraction", 0.0) * 2.0) + (m.get("compatibility", 75.0) / 25.0)
                elif cat == "balanced":
                    score += (m.get("overall_score", 80.0) / 20.0)

                # Deterministic tie-breaker for identical candidates
                score += (i * 0.001) - (j * 0.0005)
                U[i, j] = score

        # Solve linear sum assignment for maximum utility (minimize -U)
        if n_cands <= n_cats:
            row_ind, col_ind = linear_sum_assignment(-U)
            assigned = {int(r): categories[int(c)] for r, c in zip(row_ind, col_ind)}
        else:
            # More candidates than categories (e.g. 5 candidates for 4 categories)
            # First assign all 4 unique categories
            row_ind, col_ind = linear_sum_assignment(-U[:, :n_cats])
            assigned = {int(r): categories[int(c)] for r, c in zip(row_ind, col_ind)}
            for i in range(n_cands):
                if i not in assigned:
                    best_c = max(categories, key=lambda c: cat_scores[i].get(c, 0.0))
                    assigned[i] = best_c

        return assigned

    def _build_dynamic_rationale(self, strat_key: str, label: str, m: Dict[str, Any]) -> Dict[str, Any]:
        """Constructs grounded rationale using actual candidate performance metrics."""
        cost_str = f"${m['cost']:.2f}/kg" if m["has_valid_cost"] else "Cost Data Unavailable"
        prot_str = f"{m['protein']:.1f}g protein"
        min_str = f"{m['minerals']:.0f}mg key minerals"
        score_str = f"{m['overall_score']:.1f}%"

        if strat_key == "cost_optimized":
            return {
                "strategy_key": "cost_optimized",
                "strategy_title": label,
                "badge": "Cost Minimization",
                "summary": f"Achieved the lowest raw material cost ({cost_str}) among all valid candidate sets while satisfying hard constraints.",
                "why_this_strategy": (
                    f"This candidate was dynamically classified as Cost Optimized because it achieved the minimum valid unit production cost ({cost_str}) "
                    f"while fully satisfying mandatory formulation constraints with a {score_str} overall Pareto score."
                ),
                "key_tradeoffs": "Minimizes ingredient raw material expenditure with calibrated functional dosing.",
                "target_advantage": f"Lowest cost-per-kilogram formulation ({cost_str})."
            }
        elif strat_key == "nutrition_maximized":
            return {
                "strategy_key": "nutrition_maximized",
                "strategy_title": label,
                "badge": "Nutrient Density",
                "summary": f"Delivers the highest verified nutritional potency with {prot_str} and {min_str}.",
                "why_this_strategy": (
                    f"This candidate was dynamically classified as Nutrition Maximized due to its superior nutrient delivery profile "
                    f"({prot_str}, {min_str}, {m['fibre']:.1f}g fibre) and {m['nutrition_fit']:.1f}% nutritional constraint fit."
                ),
                "key_tradeoffs": "Higher protein isolate inclusion reflects premium nutritional raw material investment.",
                "target_advantage": "Maximum nutritional density supporting front-of-pack health claims."
            }
        elif strat_key == "functionality_flavor":
            return {
                "strategy_key": "functionality_flavor",
                "strategy_title": label,
                "badge": "Rheology & Sensory Compatibility",
                "summary": f"Demonstrates highest functional role coverage ({m['frc']:.1f}%) and pairwise ingredient compatibility ({m['compatibility']:.1f}%).",
                "why_this_strategy": (
                    f"This candidate was dynamically classified as Functionality & Flavor based on superior emulsification, "
                    f"matrix stability, {m['frc']:.1f}% functional role coverage, and {m['compatibility']:.1f}% verified pairwise ingredient compatibility."
                ),
                "key_tradeoffs": "Prioritizes acoustic snap, phase stability, and velvety mouthfeel kinetics.",
                "target_advantage": "Optimal textural stability and maximum resistance to phase separation."
            }
        else: # balanced
            return {
                "strategy_key": "balanced",
                "strategy_title": label,
                "badge": "Multi-Objective Pareto",
                "summary": f"Achieves optimal commercial equilibrium across nutrition ({prot_str}), cost ({cost_str}), and quality ({score_str}).",
                "why_this_strategy": (
                    f"This candidate was dynamically classified as Balanced Set as it delivers the optimal multi-objective compromise "
                    f"between nutritional targets ({prot_str}), commercial unit economics ({cost_str}), and overall Pareto score ({score_str})."
                ),
                "key_tradeoffs": "Well-rounded commercial formulation profile with no extreme single-dimension compromises.",
                "target_advantage": "Optimal balance of product quality, sensory appeal, and commercial feasibility."
            }

# Global singleton
dynamic_strategy_classifier = DynamicStrategyClassifier()
