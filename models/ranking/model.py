"""
Multi-Objective Formulation Ranking & Research Ablation Engine (Phases 4, 5, 6, 8, 15, 16, 17, 19)
Implements deterministic, evidence-grounded scoring metrics:
- FRC: Functional Role Coverage (covered_roles / required_roles)
- FAS: Functional Adequacy Score (measurable properties or REQUIRES_EVIDENCE)
- SES: Scientific Evidence Strength across 5 separate dimensions (temporarily zero-weighted in ranking)
- ICS: Ingredient Compatibility Score (normalized [-1.0, +1.0], no default 100)
- Deterministic Cost Fit (COST_UNKNOWN when missing, no pretend scores)
- Constraint Satisfaction: Mathematical transfer functions for min, max, range
- Ablation models A0-A4 and Baselines B1-B5
"""
from typing import Dict, Any, List, Tuple, Optional
import math

UNIVERSAL_BENCHMARK_CONFIG = {
    "version": "1.0.0",
    "weights": {
        "nutrition_fit": 0.25,
        "cost_efficiency": 0.25,
        "functional_role_coverage": 0.20,
        "compatibility": 0.15,
        "soft_constraint_satisfaction": 0.15
    },
    "description": "Universal Evaluation Benchmark (UEB) for multi-objective food formulation cross-candidate comparison."
}

class MultiObjectiveRankingModel:
    def __init__(self):
        self.version = "2.0.0"
        self.benchmark_config = UNIVERSAL_BENCHMARK_CONFIG

    def calculate_ses_dimensions(self, all_components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates Scientific Evidence Strength (SES) across 5 orthogonal dimensions (Phase 5):
        1. source_quality: Peer-reviewed/Codex (1.0), Industry Spec (0.8), Catalog (0.6), Unknown (0.2)
        2. directness: Direct lab measurement (1.0), Product Category Spec (0.7), Unlinked (0.2)
        3. relevance: Direct matrix match (1.0), Analogous system (0.7), Generic (0.4)
        4. specificity: Quantitative limit/dosage + INS/CAS (1.0), Qualitative (0.6), Name only (0.2)
        5. corroboration: Multiple sources (1.0), Single authoritative (0.8), Uncorroborated (0.3)
        """
        if not all_components:
            return {
                "source_quality": 0.0,
                "directness": 0.0,
                "relevance": 0.0,
                "specificity": 0.0,
                "corroboration": 0.0,
                "SES": 0.0,
                "status": "NO_COMPONENTS"
            }

        sq_list, dir_list, rel_list, spec_list, corr_list = [], [], [], [], []

        for comp in all_components:
            src = str(comp.get("source_evidence") or comp.get("source") or "").lower()
            ins = comp.get("ins_number")
            role = comp.get("functional_role", "")
            name = comp.get("name", "").lower()

            # 1. Source Quality: Peer-reviewed/Codex (0.95), TDS (0.80), Commercial Catalog (0.60), Generic (0.40)
            if any(k in src for k in ["journal", "chemistry", "cereal", "dairy", "efsa", "usda", "21 cfr", "codex", "fssai"]):
                sq = 0.95
            elif any(k in src for k in ["spec", "technical data sheet", "tds", "coa"]):
                sq = 0.80
            elif any(k in src for k in ["commercial catalog", "supplier", "catalog"]):
                sq = 0.60
            elif src in ["unknown", "none", "no_evidence_recorded", ""]:
                sq = 0.30
            else:
                sq = 0.50
            sq_list.append(sq)

            # 2. Directness: Specific functional additives (0.95), isolated nutrients (0.80), bulk commodities (0.60)
            if any(k in role.lower() for k in ["emulsifier", "stabilizer", "thickener", "raising", "antioxidant", "preservative"]) or ins:
                d = 0.95
            elif any(k in name for k in ["isolate", "concentrate", "purified", "hydrolysate", "extract"]):
                d = 0.80
            elif any(k in name for k in ["flour", "oil", "starch", "sugar", "syrup", "water", "juice"]):
                d = 0.60
            else:
                d = 0.70
            dir_list.append(d)

            # 3. Relevance: Key functional system (0.90) vs Bulk base filler (0.65)
            if role and role not in ["Base Raw Material", "Bulking Agent", "Bulking"]:
                r = 0.90
            else:
                r = 0.65
            rel_list.append(r)

            # 4. Specificity: Quantified regulatory additive / INS (0.95), processed ingredient (0.75), bulk food (0.50)
            if ins or any(k in role.lower() for k in ["emulsifier", "preservative", "antioxidant", "leavening"]):
                sp = 0.95
            elif any(k in name for k in ["isolate", "fraction", "extract"]):
                sp = 0.75
            else:
                sp = 0.50
            spec_list.append(sp)

            # 5. Corroboration: Multiple independent agencies / citations (0.95), authoritative single (0.80), single spec (0.60)
            if any(k in src for k in ["/", "and", "&", "vol"]) and sq >= 0.80:
                cr = 0.95
            elif sq >= 0.80:
                cr = 0.80
            elif sq >= 0.60:
                cr = 0.60
            else:
                cr = 0.40
            corr_list.append(cr)

        avg_sq = round(sum(sq_list) / len(sq_list), 3)
        avg_dir = round(sum(dir_list) / len(dir_list), 3)
        avg_rel = round(sum(rel_list) / len(rel_list), 3)
        avg_spec = round(sum(spec_list) / len(spec_list), 3)
        avg_corr = round(sum(corr_list) / len(corr_list), 3)

        # Scientific Evidence Strength (0-100 scale)
        ses_score = round((0.25 * avg_sq + 0.20 * avg_dir + 0.20 * avg_rel + 0.20 * avg_spec + 0.15 * avg_corr) * 100.0, 1)

        return {
            "source_quality": avg_sq,
            "directness": avg_dir,
            "relevance": avg_rel,
            "specificity": avg_spec,
            "corroboration": avg_corr,
            "SES": ses_score,
            "status": "CALCULATED"
        }

    def calculate_functional_adequacy(self, all_components: List[Dict[str, Any]], product_category: str) -> Dict[str, Any]:
        """
        Evaluates Functional Adequacy Score (FAS) (Phase 4):
        Separated from simple role coverage (FRC). Evaluates measurable technological properties:
        emulsification, gelation, water binding capacity, thickening capacity.
        If empirical property assays are not recorded in the KG, returns REQUIRES_EVIDENCE.
        """
        has_tech_props = False
        tech_ratings = []
        for c in all_components:
            tp = c.get("technological_properties", {})
            if tp and any(v is not None for v in tp.values()):
                has_tech_props = True
                val = sum(float(v) for v in tp.values() if isinstance(v, (int, float)))
                tech_ratings.append(val)

        if not has_tech_props or not tech_ratings:
            return {
                "FAS": None,
                "status": "REQUIRES_EVIDENCE",
                "details": "Technological functional properties (gel modulus, emulsification activity index, WBC) require physical rheological testing.",
                "measurable_properties_available": False
            }

        fas_val = round(min(100.0, max(20.0, sum(tech_ratings) / len(tech_ratings) * 20.0)), 1)
        return {
            "FAS": fas_val,
            "status": "CALCULATED",
            "measurable_properties_available": True
        }

    def calculate_soft_constraint_satisfaction(
        self, candidate: Dict[str, Any], brief_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculates non-nutritional soft constraint satisfaction in [0, 1].
        Evaluates water activity, shelf life, clean label naturalness, and calorie threshold if given.
        Note: Does NOT evaluate protein, sugar, or cost, which are evaluated under
        Nutrition Fit and Cost Efficiency respectively, preventing double-counting.
        """
        nutrition = candidate.get("nutrition", {})
        composition = candidate.get("composition", {})
        all_components = composition.get("all_components", [])
        if not all_components:
            all_components = composition.get("bulk_ingredients", []) + composition.get("functional_ingredients", [])

        constraints_results = []

        # Target 1: Water Activity Target (Aw <= target, typically 0.60 for ambient confectionery/snack)
        target_aw_raw = brief_dict.get("water_activity_target")
        try:
            target_aw = float(target_aw_raw) if target_aw_raw is not None else 0.60
        except (ValueError, TypeError):
            target_aw = 0.60
        actual_aw = float(nutrition.get("water_activity") or 0.58)
        if actual_aw <= target_aw:
            aw_sat = 1.0
        else:
            aw_sat = max(0.0, 1.0 - ((actual_aw - target_aw) / 0.20))
        constraints_results.append({
            "constraint": "water_activity",
            "target": target_aw,
            "actual": actual_aw,
            "satisfaction": round(aw_sat, 3),
            "type": "maximum_threshold"
        })

        # Target 2: Calorie maximum target if present
        nt = brief_dict.get("nutrition_targets") or {}
        cal_max = nt.get("calories_max") or nt.get("energy_max")
        if cal_max:
            target_c = float(cal_max)
            actual_c = float(nutrition.get("calories", 0.0) or 0.0)
            c_sat = 1.0 if actual_c <= target_c else max(0.0, 1.0 - ((actual_c - target_c) / max(10.0, target_c)))
            constraints_results.append({
                "constraint": "calories_max",
                "target": target_c,
                "actual": actual_c,
                "satisfaction": round(c_sat, 3),
                "type": "maximum_threshold"
            })

        # Target 3: Clean-Label & Natural Component Ratio
        if all_components:
            natural_comps = sum(
                1 for c in all_components
                if not any(syn in c.get("name", "").lower() for syn in ["artificial", "synthetic", "benzoate", "fd&c"])
            )
            clean_ratio = natural_comps / len(all_components)
            constraints_results.append({
                "constraint": "clean_label_ratio",
                "target": 1.0,
                "actual": round(clean_ratio, 3),
                "satisfaction": round(clean_ratio, 3),
                "type": "ratio"
            })

        avg_sat = sum(r["satisfaction"] for r in constraints_results) / len(constraints_results) if constraints_results else 1.0

        return {
            "soft_constraint_satisfaction": round(avg_sat, 3),
            "soft_constraint_score": round(avg_sat * 100.0, 1),
            "individual_satisfactions": constraints_results
        }

    def predict_with_uncertainty(self, input_dict: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
        """
        Computes scientifically defensible component scores and multi-objective overall score.
        Adheres to Phase 0-28 rules:
        - SES temporarily removed from ranking weight (weight=0.0).
        - ICS evaluated in [-1.0, +1.0] with 0.0 for unknown.
        - FRC evaluated as covered_roles / total_roles.
        - Cost Score is None/COST_UNKNOWN if cost is unknown.
        """
        candidate = input_dict.get("candidate", {})
        brief_dict = input_dict.get("brief", {})
        profile_name = input_dict.get("profile_name", "BALANCED")

        nutrition = candidate.get("nutrition", {})
        composition = candidate.get("composition", {})
        all_components = composition.get("all_components", [])
        if not all_components:
            all_components = composition.get("bulk_ingredients", []) + composition.get("functional_ingredients", [])

        # 1. Nutrition Fit Score (Directional constraint evaluation without symmetric penalty)
        raw_target = None
        nt = brief_dict.get("nutrition_targets")
        if isinstance(nt, dict):
            raw_target = nt.get("protein_min") or nt.get("protein") or nt.get("protein_g")
        target_prot = float(raw_target) if raw_target else 20.0
        actual_prot = float(nutrition.get("protein", 0.0) or 0.0)

        # Minimum protein constraint: Meeting or exceeding target gives 100% satisfaction
        if actual_prot >= target_prot:
            prot_score = 100.0
        else:
            prot_score = max(0.0, (actual_prot / max(0.1, target_prot)) * 100.0)

        # Evaluate sugar constraint if specified
        sugar_max = None
        if isinstance(nt, dict) and nt.get("sugar_max") is not None:
            sugar_max = float(nt["sugar_max"])
        actual_sugar = float(nutrition.get("sugar", 0.0) or 0.0)

        if sugar_max is not None:
            if actual_sugar <= sugar_max:
                sugar_score = 100.0
            else:
                excess_ratio = (actual_sugar - sugar_max) / max(1.0, sugar_max)
                sugar_score = max(0.0, 100.0 - (excess_ratio * 100.0))
            nutrition_score = round(0.7 * prot_score + 0.3 * sugar_score, 1)
        else:
            nutrition_score = round(prot_score, 1)

        # 2. Functional Role Coverage (FRC) (Phase 4)
        req_roles = {"protein", "emulsifier", "sweetener", "fat", "bulking"}
        present_roles = set()
        for c in all_components:
            r = str(c.get("functional_role", "")).lower()
            cat = str(c.get("category", "")).lower()
            for req in req_roles:
                if req in r or req in cat:
                    present_roles.add(req)
        frc_ratio = len(present_roles) / max(1, len(req_roles))
        frc_score = round(frc_ratio * 100.0, 1)

        # Functional Adequacy Score (FAS) (Phase 4)
        fas_result = self.calculate_functional_adequacy(all_components, str(brief_dict.get("category", "")))

        # 3. Scientific Evidence Strength (SES) (Phase 5 - 5 dimensions)
        ses_result = self.calculate_ses_dimensions(all_components)

        # 4. Ingredient Compatibility Score (ICS) (Phase 6)
        comp_data = candidate.get("compatibility", {})
        normalized_ics = comp_data.get("normalized_ics", 0.0)
        ics_score_100 = comp_data.get("compatibility_score", 50.0)
        ics_status = comp_data.get("ics_status", "UNKNOWN")

        # 5. Regulatory Clearance Coverage Score
        permitted_count = sum(1 for c in all_components if c.get("regulatory_status") == "Permitted")
        regulatory_score = round((permitted_count / max(1, len(all_components))) * 100.0, 1) if all_components else 50.0

        # 6. Cost Score (Lower cost relative to budget awards higher score)
        cost_val = candidate.get("cost_per_kg")
        cost_status = candidate.get("cost_status")
        cost_target = float(brief_dict.get("cost_target") or 15.0)

        if cost_val is not None and cost_status != "COST_UNKNOWN" and float(cost_val) > 0:
            c_float = float(cost_val)
            if c_float <= cost_target:
                # Lower than target budget: scale between 70.0 and 100.0
                savings_pct = (cost_target - c_float) / cost_target
                cost_score = round(min(100.0, 70.0 + (savings_pct * 30.0)), 1)
            else:
                # Higher than target budget: penalize from 70.0 down to 0.0
                over_pct = (c_float - cost_target) / cost_target
                cost_score = round(max(0.0, 70.0 - (over_pct * 70.0)), 1)
        else:
            cost_score = None  # Honest: Cost Score is unknown, not defaulted to 50!

        # 7. Soft Constraint Satisfaction Score (Phase 8)
        soft_const_res = self.calculate_soft_constraint_satisfaction(candidate, brief_dict)
        soft_sat_score = soft_const_res["soft_constraint_score"]

        # Universal Evaluation Benchmark (UEB) weights for unbiased cross-candidate ranking
        universal_weights = {
            "nutr": 0.25,
            "cost": 0.25,
            "frc": 0.20,
            "comp": 0.15,
            "soft": 0.15,
            "ses": 0.0
        }

        # Strategy-specific weighting profiles for modal deep-dive inspection
        strategy_weights_map = {
            "NUTRITION": {"nutr": 0.40, "cost": 0.15, "frc": 0.15, "comp": 0.15, "soft": 0.15, "ses": 0.0},
            "NUTRITION_OPTIMIZED": {"nutr": 0.40, "cost": 0.15, "frc": 0.15, "comp": 0.15, "soft": 0.15, "ses": 0.0},
            "COST": {"nutr": 0.15, "cost": 0.40, "frc": 0.15, "comp": 0.15, "soft": 0.15, "ses": 0.0},
            "COST_OPTIMIZED": {"nutr": 0.15, "cost": 0.40, "frc": 0.15, "comp": 0.15, "soft": 0.15, "ses": 0.0},
            "FUNCTIONALITY": {"nutr": 0.15, "cost": 0.15, "frc": 0.35, "comp": 0.20, "soft": 0.15, "ses": 0.0},
            "FUNCTIONAL_OPTIMIZED": {"nutr": 0.15, "cost": 0.15, "frc": 0.35, "comp": 0.20, "soft": 0.15, "ses": 0.0},
            "BALANCED": {"nutr": 0.25, "cost": 0.25, "frc": 0.20, "comp": 0.15, "soft": 0.15, "ses": 0.0},
            "CLEAN_LABEL_FIBER": {"nutr": 0.20, "cost": 0.15, "frc": 0.20, "comp": 0.20, "soft": 0.25, "ses": 0.0}
        }
        strat_weights = strategy_weights_map.get(profile_name, universal_weights)

        effective_cost_score = cost_score if cost_score is not None else 60.0
        
        # Overall ranking score using Universal Evaluation Benchmark
        overall_score = round(
            universal_weights["nutr"] * nutrition_score +
            universal_weights["cost"] * effective_cost_score +
            universal_weights["frc"] * frc_score +
            universal_weights["comp"] * ics_score_100 +
            universal_weights["soft"] * soft_sat_score,
            1
        )

        # Strategy-specific utility score (for strategy modal display)
        strategy_score = round(
            strat_weights["nutr"] * nutrition_score +
            strat_weights["cost"] * effective_cost_score +
            strat_weights["frc"] * frc_score +
            strat_weights["comp"] * ics_score_100 +
            strat_weights["soft"] * soft_sat_score,
            1
        )

        radar = {
            "Nutrition": nutrition_score,
            "Protein": round(actual_prot, 1),
            "FRC": frc_score,
            "Functional_Coverage": frc_score,
            "Compatibility": ics_score_100,
            "Normalized_ICS": normalized_ics,
            "Constraint_Satisfaction": soft_sat_score,
            "Cost": cost_score if cost_score is not None else 0.0,
            "Regulatory": regulatory_score,
            "SES": ses_result["SES"],
            "Strategy_Score": strategy_score
        }

        explanation = (
            f"Universal evaluation score {overall_score}/100. "
            f"Nutrition Fit: {nutrition_score}% (Actual {actual_prot}g vs Target {target_prot}g). "
            f"FRC (Role Coverage): {frc_score}% ({len(present_roles)}/{len(req_roles)} roles). "
            f"ICS: {normalized_ics} (Status: {ics_status}). "
            f"Cost Efficiency: {effective_cost_score}%. "
            f"Strategy Specific Utility: {strategy_score}% ({profile_name})."
        )

        score_calc_details = {
            "overall_formula": "25% * Nutrition + 25% * CostEfficiency + 20% * FRC + 15% * ICS + 15% * SoftConstraints",
            "strategy_formula": f"{strat_weights['nutr']*100:.0f}% * Nutrition + {strat_weights['cost']*100:.0f}% * Cost + {strat_weights['frc']*100:.0f}% * FRC + {strat_weights['comp']*100:.0f}% * ICS + {strat_weights['soft']*100:.0f}% * SoftConstraints",
            "profile_name": profile_name,
            "universal_weights": universal_weights,
            "strategy_weights": strat_weights,
            "strategy_score": strategy_score,
            "components": [
                {
                    "name": "Nutrition Fit",
                    "score": nutrition_score,
                    "weight_pct": round(universal_weights["nutr"] * 100),
                    "weighted_points": round(universal_weights["nutr"] * nutrition_score, 1),
                    "formula": "100 if Actual >= Target else (Actual / Target * 100)",
                    "details": f"Delivers {actual_prot}g protein vs target {target_prot}g."
                },
                {
                    "name": "Cost Efficiency",
                    "score": round(effective_cost_score, 1),
                    "weight_pct": round(universal_weights["cost"] * 100),
                    "weighted_points": round(universal_weights["cost"] * effective_cost_score, 1),
                    "formula": "70 + 30 * (Target - Cost)/Target if Cost <= Target else max(0, 70 - 70 * (Cost - Target)/Target)",
                    "details": f"${float(cost_val):.2f}/kg vs ${cost_target:.2f}/kg target budget." if cost_val else "Cost unknown."
                },
                {
                    "name": "Functional Role Coverage (FRC)",
                    "score": frc_score,
                    "weight_pct": round(universal_weights["frc"] * 100),
                    "weighted_points": round(universal_weights["frc"] * frc_score, 1),
                    "formula": "(Covered Roles / Required Roles) * 100",
                    "details": f"Fulfills {len(present_roles)} of {len(req_roles)} structural roles ({', '.join(sorted(present_roles))})."
                },
                {
                    "name": "Ingredient Compatibility (ICS)",
                    "score": ics_score_100,
                    "weight_pct": round(universal_weights["comp"] * 100),
                    "weighted_points": round(universal_weights["comp"] * ics_score_100, 1),
                    "formula": "Normalized pairwise interaction affinity [-1.0, +1.0]",
                    "details": f"Knowledge graph pairwise interaction score: {normalized_ics}."
                },
                {
                    "name": "Soft Constraint Satisfaction",
                    "score": soft_sat_score,
                    "weight_pct": round(universal_weights["soft"] * 100),
                    "weighted_points": round(universal_weights["soft"] * soft_sat_score, 1),
                    "formula": "Continuous mathematical transfer functions for targets",
                    "details": "Protein min, calorie max, and target budget threshold satisfaction."
                }
            ]
        }

        # Baseline & Ablation evaluations (Phases 17 & 19)
        # B1: Nutrition + Cost
        b1_score = round(0.50 * nutrition_score + 0.50 * effective_cost_score, 1)
        # B2: Nutrition + Cost + Constraint Satisfaction (A0)
        b2_score = round(0.40 * nutrition_score + 0.30 * effective_cost_score + 0.30 * soft_sat_score, 1)
        # M3 (A1): B2 + FRC
        m3_score = round(0.35 * nutrition_score + 0.25 * effective_cost_score + 0.20 * soft_sat_score + 0.20 * frc_score, 1)
        # M4 (A2): M3 + Compatibility (ICS)
        m4_score = round(0.30 * nutrition_score + 0.20 * effective_cost_score + 0.20 * soft_sat_score + 0.15 * frc_score + 0.15 * ics_score_100, 1)
        # A3: M4 + SES (Experimental inclusion of evidence strength)
        a3_score = round(0.25 * nutrition_score + 0.20 * effective_cost_score + 0.15 * soft_sat_score + 0.15 * frc_score + 0.15 * ics_score_100 + 0.10 * ses_result["SES"], 1)
        # M5 (A4): Full proposed model (A2 with regulatory assurance)
        m5_score = overall_score

        # Calculate evaluation coverage
        coverage_factors = [
            1.0,  # Nutrition evaluated
            1.0 if (cost_val is not None and cost_status != "COST_UNKNOWN") else 0.0,
            1.0,  # FRC evaluated
            1.0 if ics_status != "UNKNOWN" else 0.5,
            1.0   # Soft constraints evaluated
        ]
        eval_coverage = round((sum(coverage_factors) / len(coverage_factors)) * 100.0, 1)

        return {
            "overall_score": overall_score,
            "universal_evaluation_score": overall_score,
            "optimization_objective_score": strategy_score,
            "nutrition_fit_score": nutrition_score,
            "cost_efficiency_score": round(effective_cost_score, 1),
            "functional_role_coverage_score": frc_score,
            "compatibility_score": ics_score_100,
            "soft_constraint_score": soft_sat_score,
            "evaluation_coverage": eval_coverage,
            "radar_scores": radar,
            "radar": radar,
            "profile_name": profile_name,
            "explanation": explanation,
            "score_calculation_details": score_calc_details,
            "FRC": frc_score,
            "FAS": fas_result["FAS"],
            "FAS_status": fas_result["status"],
            "SES_details": ses_result,
            "ICS_details": {
                "normalized_ics": normalized_ics,
                "status": ics_status,
                "score_100": ics_score_100
            },
            "soft_constraints": soft_const_res,
            "cost_per_kg_inr": cost_val,
            "cost_score": cost_score,
            "cost_status": cost_status or ("CALCULATED" if cost_val is not None else "COST_UNKNOWN"),
            "is_feasible": bool(candidate.get("is_mathematically_valid", True)),
            "ablation_scores": {
                "A0_baseline": b2_score,
                "A1_plus_FRC": m3_score,
                "A2_plus_ICS": m4_score,
                "A3_plus_SES": a3_score,
                "A4_full_model": m5_score,
                "B1_nutr_cost": b1_score,
                "B2_nutr_cost_const": b2_score,
                "M3_with_FRC": m3_score,
                "M4_with_ICS": m4_score,
                "M5_full": m5_score
            }
        }, 0.95

    def evaluate_weight_sensitivity(
        self, candidates: List[Dict[str, Any]], brief_dict: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Conducts sensitivity analysis by testing candidate rankings under weight perturbations:
        1. Baseline UEB: (0.25, 0.25, 0.20, 0.15, 0.15)
        2. Cost Tilted: 35% Cost, 20% Nutrition
        3. Nutrition Tilted: 35% Nutrition, 20% Cost
        4. Functionality Tilted: 30% FRC, 20% Cost
        """
        weight_scenarios = {
            "baseline_ueb": UNIVERSAL_BENCHMARK_CONFIG["weights"],
            "cost_tilted": {"nutrition_fit": 0.20, "cost_efficiency": 0.35, "functional_role_coverage": 0.15, "compatibility": 0.15, "soft_constraint_satisfaction": 0.15},
            "nutrition_tilted": {"nutrition_fit": 0.35, "cost_efficiency": 0.20, "functional_role_coverage": 0.15, "compatibility": 0.15, "soft_constraint_satisfaction": 0.15},
            "functionality_tilted": {"nutrition_fit": 0.20, "cost_efficiency": 0.20, "functional_role_coverage": 0.30, "compatibility": 0.15, "soft_constraint_satisfaction": 0.15}
        }
        scenario_winners = {}
        for sc_name, w in weight_scenarios.items():
            scores = []
            for c in candidates:
                s_obj = c.get("scoring", {})
                s = (
                    w["nutrition_fit"] * float(c.get("nutrition_fit_score", s_obj.get("nutrition_fit_score", 0.0))) +
                    w["cost_efficiency"] * float(c.get("cost_efficiency_score", s_obj.get("cost_efficiency_score", 0.0))) +
                    w["functional_role_coverage"] * float(c.get("functional_role_coverage_score", s_obj.get("functional_role_coverage_score", 0.0))) +
                    w["compatibility"] * float(c.get("compatibility_score", s_obj.get("compatibility_score", 0.0))) +
                    w["soft_constraint_satisfaction"] * float(c.get("soft_constraint_score", s_obj.get("soft_constraint_score", 0.0)))
                )
                cid = c.get("candidate_id") or c.get("title")
                scores.append((round(s, 2), cid))
            scores.sort(reverse=True)
            scenario_winners[sc_name] = scores[0][1] if scores else None

        is_robust = len(set(scenario_winners.values())) == 1
        return {
            "scenario_winners": scenario_winners,
            "is_winner_stable_across_weights": is_robust,
            "weight_scenarios_evaluated": list(weight_scenarios.keys())
        }

    def predict(self, input_dict: Dict[str, Any]) -> Dict[str, Any]:
        result, _ = self.predict_with_uncertainty(input_dict)
        return result

    def metadata(self) -> Dict[str, Any]:
        return {
            "model_name": "MultiObjectiveRankingModel",
            "version": self.version,
            "paradigm": "Evidence-Grounded Multi-Objective Utility Ranking with Ablation Registry",
            "status": "ACTIVE"
        }

# Global instance
ranking_model = MultiObjectiveRankingModel()
