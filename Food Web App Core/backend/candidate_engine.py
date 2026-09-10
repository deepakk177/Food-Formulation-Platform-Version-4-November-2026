"""
Dynamic Constraint-Aware Candidate Generation & Multi-Objective Experiment Engine.
Generates dynamic formulation experiment candidates based on ProductBrief constraints and grounded ingredient facts.
Ensures strict sum(percentage) == 100.00% deterministically.
"""
import logging
from typing import Dict, Any, List, Optional
from retrieval_service import RetrievedIngredient, retrieval_orchestrator
from requirements_extractor import ProductBrief
from constraint_engine import constraint_engine

logger = logging.getLogger("CandidateEngine")

class CandidateSetDict(dict):
    """Dict subclass that enables attribute-style property access for test backward compatibility."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'CandidateSetDict' object has no attribute '{name}'")

class CandidateEngine:
    def __init__(self, tolerance: float = 0.01):
        self.tolerance = tolerance

    def normalize_percentages(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalizes ingredient percentages so that sum equals exactly 100.00%."""
        if not items:
            return items

        total = sum(item["percentage"] for item in items)
        if total <= 0:
            return items

        factor = 100.0 / total
        for item in items:
            item["percentage"] = round(item["percentage"] * factor, 2)

        # Adjust tiny rounding difference on largest bulk ingredient
        current_sum = round(sum(item["percentage"] for item in items), 2)
        diff = round(100.00 - current_sum, 2)
        if abs(diff) > 0 and len(items) > 0:
            items[0]["percentage"] = round(items[0]["percentage"] + diff, 2)

        return items

    def _calculate_grounded_macros(self, items: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculates exact macro yield from grounded ingredient facts."""
        prot = sum((item["percentage"] / 100.0) * item["detail"].nutrition.get("protein", 0.0) for item in items)
        fat = sum((item["percentage"] / 100.0) * item["detail"].nutrition.get("fat", 0.0) for item in items)
        carb = sum((item["percentage"] / 100.0) * item["detail"].nutrition.get("carbs", 0.0) for item in items)
        cal = sum((item["percentage"] / 100.0) * item["detail"].nutrition.get("calories", 0.0) for item in items)
        cost = sum((item["percentage"] / 100.0) * item["detail"].cost_per_kg for item in items)

        return {
            "protein": round(prot, 1),
            "fat": round(fat, 1),
            "carbohydrates": round(carb, 1),
            "calories": round(cal, 0),
            "cost_per_kg": round(cost, 2)
        }

    def generate_experiments(
        self, brief: ProductBrief, ingredients: Optional[List[RetrievedIngredient]] = None
    ) -> List[Dict[str, Any]]:
        """
        Dynamically generates multiple formulation experiment candidates from grounded ingredient pool.
        Each experiment represents a distinct scientific formulation strategy.
        """
        if not ingredients:
            retrieved = retrieval_orchestrator.retrieve_all_multi_dimensional(brief.dict())
            ingredients = retrieved["ingredients"]

        # 1. Hard Constraint Filter
        eligible = constraint_engine.filter_eligible_ingredients(ingredients, brief)

        if not eligible:
            logger.warning("Zero eligible ingredients satisfy hard constraints.")
            return []

        # Categorize eligible ingredients
        proteins = [i for i in eligible if "protein" in i.category.lower() or "protein" in i.name.lower() or any("protein" in r.lower() for r in i.functional_roles)]
        flours = [i for i in eligible if i.category in ["Flours", "Starches", "Bulk", "General"] and i not in proteins]
        sweeteners = [i for i in eligible if "sweetener" in i.category.lower() or "sugar" in i.name.lower() or "syrup" in i.name.lower()]
        emulsifiers = [i for i in eligible if i.category in ["Emulsifiers", "Hydrocolloids", "Fibres"] or any(r in ["Emulsifier", "Stabilizer", "Bulking Agent"] for r in i.functional_roles)]
        fats = [i for i in eligible if "fat" in i.category.lower() or "oil" in i.name.lower() or "butter" in i.name.lower()]

        # Fallback pools
        if not proteins: proteins = eligible
        if not flours: flours = eligible
        if not sweeteners: sweeteners = eligible
        if not emulsifiers: emulsifiers = eligible
        if not fats: fats = eligible

        experiments = []
        candidate_counter = 1

        strategies = brief.experiment_strategies or ["nutrition_maximized", "cost_optimized", "balanced", "functionality_texture"]

        # --- STRATEGY 1: Nutrition-Maximized Experiment ---
        if "nutrition_maximized" in strategies:
            # Sort proteins by highest protein content per 100g
            sorted_proteins = sorted(proteins, key=lambda x: x.nutrition.get("protein", 0), reverse=True)
            top_prot = sorted_proteins[0]
            top_flour = flours[0]
            top_fat = fats[0]
            top_sweetener = sweeteners[0]
            top_emulsifier = emulsifiers[0]

            set_raw = [
                {"detail": top_flour, "category": top_flour.category, "percentage": 25.0, "is_func": False},
                {"detail": top_fat, "category": top_fat.category, "percentage": 20.0, "is_func": False},
                {"detail": top_sweetener, "category": top_sweetener.category, "percentage": 20.0, "is_func": False},
                {"detail": top_prot, "category": "Functional Protein", "percentage": 25.0, "is_func": True, "role": "Protein Source"},
                {"detail": top_emulsifier, "category": "Functional Stabilizer", "percentage": 2.0, "is_func": True, "role": top_emulsifier.functional_roles[0] if top_emulsifier.functional_roles else "Emulsifier"}
            ]
            normalized = self.normalize_percentages(set_raw)
            macros = self._calculate_grounded_macros(normalized)

            bulk_list = [{"name": item["detail"].name, "category": item["category"], "percentage": item["percentage"], "id": item["detail"].id} for item in normalized if not item["is_func"]]
            func_list = [{"name": item["detail"].name, "functional_role": item.get("role", "Functional Agent"), "percentage": item["percentage"], "id": item["detail"].id} for item in normalized if item["is_func"]]

            experiments.append(CandidateSetDict({
                "candidate_id": f"FC-00{candidate_counter}",
                "title": f"Experiment A: Nutrition-Maximized Set ({brief.category or 'Food'})",
                "set_name": "Nutrition-Maximized Strategy",
                "composition": {
                    "bulk_ingredients": bulk_list,
                    "functional_ingredients": func_list
                },
                "total_percentage": 100.0,
                "is_mathematically_valid": True,
                "nutrition": {
                    "protein": macros["protein"],
                    "fat": macros["fat"],
                    "carbohydrates": macros["carbohydrates"],
                    "calories": macros["calories"],
                    "texture": brief.texture_requirements[0] if brief.texture_requirements else "Firm & Dense",
                    "mouthfeel": "Rich protein structure",
                    "viscosity": "Controlled flow viscosity",
                    "shelf_life": 9
                },
                "cost_per_kg": macros["cost_per_kg"],
                "process_steps": [
                    f"Phase 1 (Pre-Blending): High-speed pre-blend of {top_prot.name} and {top_flour.name} (5 mins at 120 RPM).",
                    f"Phase 2 (Lipid Emulsification): Melt {top_fat.name} and incorporate {top_emulsifier.name} under high shear (2000 RPM).",
                    "Phase 3 (Compounding & Extrusion): Combine liquid and dry pre-blend in twin-screw extruder; barrel temp 35C-40C.",
                    "Phase 4 (Forming & Cooling): Extrude slab onto cooling tunnel (12C for 15 mins) and cut into standard units.",
                    "Phase 5 (Packaging): Nitrogen flush flow-wrap packaging to maintain low water activity."
                ]
            }))
            candidate_counter += 1

        # --- STRATEGY 2: Cost-Optimized Experiment ---
        if "cost_optimized" in strategies:
            sorted_cost = sorted(eligible, key=lambda x: x.cost_per_kg)
            low_cost_bulk = sorted_cost[0]
            low_cost_protein = sorted(proteins, key=lambda x: x.cost_per_kg)[0]
            low_cost_sweetener = sorted(sweeteners, key=lambda x: x.cost_per_kg)[0]
            low_cost_fat = sorted(fats, key=lambda x: x.cost_per_kg)[0]
            low_cost_emulsifier = sorted(emulsifiers, key=lambda x: x.cost_per_kg)[0]

            set_raw = [
                {"detail": low_cost_bulk, "category": low_cost_bulk.category, "percentage": 35.0, "is_func": False},
                {"detail": low_cost_sweetener, "category": low_cost_sweetener.category, "percentage": 25.0, "is_func": False},
                {"detail": low_cost_fat, "category": low_cost_fat.category, "percentage": 18.0, "is_func": False},
                {"detail": low_cost_protein, "category": "Functional Protein", "percentage": 20.0, "is_func": True, "role": "Protein Source"},
                {"detail": low_cost_emulsifier, "category": "Functional Emulsifier", "percentage": 2.0, "is_func": True, "role": "Emulsifier"}
            ]
            normalized = self.normalize_percentages(set_raw)
            macros = self._calculate_grounded_macros(normalized)

            bulk_list = [{"name": item["detail"].name, "category": item["category"], "percentage": item["percentage"], "id": item["detail"].id} for item in normalized if not item["is_func"]]
            func_list = [{"name": item["detail"].name, "functional_role": item.get("role", "Functional Agent"), "percentage": item["percentage"], "id": item["detail"].id} for item in normalized if item["is_func"]]

            experiments.append(CandidateSetDict({
                "candidate_id": f"FC-00{candidate_counter}",
                "title": f"Experiment B: Cost-Optimized Set ({brief.category or 'Food'})",
                "set_name": "Cost-Optimized Strategy",
                "composition": {
                    "bulk_ingredients": bulk_list,
                    "functional_ingredients": func_list
                },
                "total_percentage": 100.0,
                "is_mathematically_valid": True,
                "nutrition": {
                    "protein": macros["protein"],
                    "fat": macros["fat"],
                    "carbohydrates": macros["carbohydrates"],
                    "calories": macros["calories"],
                    "texture": "Smooth",
                    "mouthfeel": "Standard crumb texture",
                    "viscosity": "Standard process viscosity",
                    "shelf_life": 12
                },
                "cost_per_kg": macros["cost_per_kg"],
                "process_steps": [
                    f"Phase 1 (Soluble Pre-Mix): Mix {low_cost_sweetener.name} with warm water (50C) for 10 mins.",
                    f"Phase 2 (Dry Dispersion): Sieve {low_cost_bulk.name} and blend at 800 RPM in planetary mixer.",
                    "Phase 3 (Homogenization): Vacuum blend liquid phase with dry powder to eliminate air entrainment.",
                    "Phase 4 (Setting & Cooling): Thermal set at 140C for 18 mins to set matrix structure.",
                    "Phase 5 (Packaging): Flow wrap under protective atmosphere."
                ]
            }))
            candidate_counter += 1

        # --- STRATEGY 3: Balanced Nutrition & Cost Experiment ---
        if "balanced" in strategies:
            mid_protein = proteins[len(proteins)//2]
            mid_flour = flours[len(flours)//2]
            mid_sweetener = sweeteners[len(sweeteners)//2]
            mid_fat = fats[len(fats)//2]
            mid_emulsifier = emulsifiers[len(emulsifiers)//2]

            set_raw = [
                {"detail": mid_flour, "category": mid_flour.category, "percentage": 30.0, "is_func": False},
                {"detail": mid_sweetener, "category": mid_sweetener.category, "percentage": 25.0, "is_func": False},
                {"detail": mid_fat, "category": mid_fat.category, "percentage": 20.0, "is_func": False},
                {"detail": mid_protein, "category": "Functional Protein", "percentage": 23.0, "is_func": True, "role": "Protein Source"},
                {"detail": mid_emulsifier, "category": "Functional Emulsifier", "percentage": 2.0, "is_func": True, "role": "Emulsifier"}
            ]
            normalized = self.normalize_percentages(set_raw)
            macros = self._calculate_grounded_macros(normalized)

            bulk_list = [{"name": item["detail"].name, "category": item["category"], "percentage": item["percentage"], "id": item["detail"].id} for item in normalized if not item["is_func"]]
            func_list = [{"name": item["detail"].name, "functional_role": item.get("role", "Functional Agent"), "percentage": item["percentage"], "id": item["detail"].id} for item in normalized if item["is_func"]]

            experiments.append(CandidateSetDict({
                "candidate_id": f"FC-00{candidate_counter}",
                "title": f"Experiment C: Balanced Nutrition + Cost Set ({brief.category or 'Food'})",
                "set_name": "Balanced Strategy",
                "composition": {
                    "bulk_ingredients": bulk_list,
                    "functional_ingredients": func_list
                },
                "total_percentage": 100.0,
                "is_mathematically_valid": True,
                "nutrition": {
                    "protein": macros["protein"],
                    "fat": macros["fat"],
                    "carbohydrates": macros["carbohydrates"],
                    "calories": macros["calories"],
                    "texture": "Balanced & Chewy",
                    "mouthfeel": "Smooth and clean melt",
                    "viscosity": "Moderate shear viscosity",
                    "shelf_life": 9
                },
                "cost_per_kg": macros["cost_per_kg"],
                "process_steps": [
                    "Phase 1: Pre-blend dry bulk ingredients thoroughly.",
                    "Phase 2: Hydrate functional emulsifiers and protein isolates.",
                    "Phase 3: High-shear compounding and homogenization.",
                    "Phase 4: Cold forming and extrusion.",
                    "Phase 5: High barrier protective packaging."
                ]
            }))
            candidate_counter += 1

        # --- STRATEGY 4: Functionality & Texture Focus Experiment ---
        if "functionality_texture" in strategies or "clean_label_fiber" in strategies:
            texturizer = emulsifiers[0]
            func_protein = proteins[0]
            func_flour = flours[0]
            func_fat = fats[0]

            set_raw = [
                {"detail": func_flour, "category": func_flour.category, "percentage": 28.0, "is_func": False},
                {"detail": func_fat, "category": func_fat.category, "percentage": 22.0, "is_func": False},
                {"detail": func_protein, "category": "Functional Protein", "percentage": 25.0, "is_func": True, "role": "Protein Source"},
                {"detail": texturizer, "category": "Functional Hydrocolloid", "percentage": 25.0, "is_func": True, "role": "Texturizer & Prebiotic Fiber"}
            ]
            normalized = self.normalize_percentages(set_raw)
            macros = self._calculate_grounded_macros(normalized)

            bulk_list = [{"name": item["detail"].name, "category": item["category"], "percentage": item["percentage"], "id": item["detail"].id} for item in normalized if not item["is_func"]]
            func_list = [{"name": item["detail"].name, "functional_role": item.get("role", "Texturizer"), "percentage": item["percentage"], "id": item["detail"].id} for item in normalized if item["is_func"]]

            experiments.append(CandidateSetDict({
                "candidate_id": f"FC-00{candidate_counter}",
                "title": f"Experiment D: Functionality & Texture Focus Set ({brief.category or 'Food'})",
                "set_name": "Functionality & Texture Strategy",
                "composition": {
                    "bulk_ingredients": bulk_list,
                    "functional_ingredients": func_list
                },
                "total_percentage": 100.0,
                "is_mathematically_valid": True,
                "nutrition": {
                    "protein": macros["protein"],
                    "fat": macros["fat"],
                    "carbohydrates": macros["carbohydrates"],
                    "calories": macros["calories"],
                    "texture": "Smooth & Aerated",
                    "mouthfeel": "Soft, moist crumb feel",
                    "viscosity": "High shear viscosity",
                    "shelf_life": 12
                },
                "cost_per_kg": macros["cost_per_kg"],
                "process_steps": [
                    f"Phase 1: Hydrate hydrocolloid {texturizer.name} in warm water (50C).",
                    "Phase 2: Add functional protein isolate under high shear.",
                    "Phase 3: Vacuum blend to eliminate air entrainment.",
                    "Phase 4: Thermal setting and pasteurization.",
                    "Phase 5: Nitrogen flush flow-wrap packaging."
                ]
            }))

        return experiments

    # Backward compatibility aliases
    def generate_candidates(self, ingredients: List[RetrievedIngredient], brief: Any) -> List[Dict[str, Any]]:
        brief_obj = brief if isinstance(brief, ProductBrief) else ProductBrief(**brief)
        return self.generate_experiments(brief_obj, ingredients)

    def generate_candidates_for_brief(self, brief_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
        brief = ProductBrief(**brief_dict)
        return self.generate_experiments(brief)

# Global singleton instance
candidate_engine = CandidateEngine()
