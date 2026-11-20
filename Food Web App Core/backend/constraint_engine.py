"""
Programmatic Constraint Engine for TCS Food Formulator
Enforces strict separation between Hard Constraints (veto / feasibility) and Soft Objectives (quality ranking),
loads external priority configuration, builds Constraint Graphs, and performs ingredient interaction & compatibility analysis.
"""
import os
import yaml
import logging
from typing import Dict, Any, List, Tuple, Optional
from retrieval_service import RetrievedIngredient
from requirements_extractor import ProductBrief, ConstraintItem

logger = logging.getLogger("ConstraintEngine")

PROHIBITED_INGREDIENTS_MAP = {
    "vegan": ["milk", "egg", "whey", "butter", "gelatin", "heavy cream", "skim milk", "whole eggs", "unsalted butter", "yogurt culture", "carmine", "lard", "tallow"],
    "dairy_free": ["milk", "whey", "butter", "heavy cream", "skim milk", "unsalted butter", "yogurt culture", "casein", "caseinate", "lactose"],
    "gluten_free": ["wheat flour", "wheat", "rye", "barley", "gluten", "malt", "spelt"],
    "peanut_free": ["peanuts", "peanut oil", "peanut butter"],
    "soy_free": ["soy lecithin", "soybean oil", "soymilk", "soy protein", "tofu"]
}

# Known incompatible pairs (e.g. high acid + unbuffered protein)
INCOMPATIBLE_PAIRS = [
    ("citric acid", "unbuffered pea protein"),
    ("high acid fruit", "milk protein isolate"),
    ("calcium carbonate", "unbuffered phosphoric acid")
]

class PrioritizedConstraint:
    def __init__(
        self,
        name: str,
        type: str,
        weight: float,
        hard_or_soft: str,
        reason: str,
        source: str,
        parameter: str = "",
        operator: str = "",
        target_value: Any = None
    ):
        self.name = name
        self.type = type
        self.weight = weight
        self.hard_or_soft = hard_or_soft  # "HARD" or "SOFT"
        self.reason = reason
        self.source = source
        self.parameter = parameter
        self.operator = operator
        self.target_value = target_value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "weight": self.weight,
            "hard_or_soft": self.hard_or_soft,
            "reason": self.reason,
            "source": self.source,
            "parameter": self.parameter,
            "operator": self.operator,
            "target_value": self.target_value
        }

class ConstraintResult:
    def __init__(self, name: str, target: Any, actual: Any, status: str, is_hard: bool = True, reason: str = ""):
        self.name = name
        self.target = target
        self.actual = actual
        self.status = status  # "satisfied", "violated", "unavailable"
        self.is_hard = is_hard
        self.reason = reason

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "target": self.target,
            "actual": self.actual,
            "status": self.status,
            "is_hard": self.is_hard,
            "reason": self.reason
        }

class ConstraintEngine:
    def __init__(self):
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "config", "constraint_priority.yaml")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                logger.warning(f"Could not load constraint_priority.yaml: {e}")
        return {}

    def prioritize_constraints(self, brief: ProductBrief) -> Dict[str, Any]:
        """
        Prioritizes all extracted constraints into Hard and Soft categories
        using external priority configuration rules.
        """
        priority_cfg = self.config.get("constraint_priority", {})
        prioritized_list: List[PrioritizedConstraint] = []
        hard_list: List[PrioritizedConstraint] = []
        soft_list: List[PrioritizedConstraint] = []

        # If constraint_items exist on brief, process them
        items = getattr(brief, "constraint_items", [])
        if items:
            for item in items:
                type_key = item.type.lower()
                cfg_entry = priority_cfg.get(type_key, priority_cfg.get(item.type, {}))
                hard_soft = item.hard_or_soft or cfg_entry.get("hard_or_soft") or ("HARD" if getattr(item, "priority", item.importance) in ["CRITICAL", "HIGH"] and type_key in ["allergen", "ingredient_restriction", "regulatory", "dietary"] else "SOFT")
                weight = cfg_entry.get("weight", 0.90 if hard_soft == "HARD" else 0.70)
                reason = cfg_entry.get("reason", f"Extracted {item.type} requirement")
                source = cfg_entry.get("source", "Product Brief Parser")

                p_obj = PrioritizedConstraint(
                    name=f"{item.parameter} {item.operator} {item.target_value}".strip(),
                    type=item.type,
                    weight=weight,
                    hard_or_soft=hard_soft,
                    reason=reason,
                    source=source,
                    parameter=item.parameter,
                    operator=item.operator,
                    target_value=item.target_value
                )
                prioritized_list.append(p_obj)
                if hard_soft == "HARD":
                    hard_list.append(p_obj)
                else:
                    soft_list.append(p_obj)
        else:
            # Fallback for simple briefs
            for diet in brief.dietary_requirements:
                cfg = priority_cfg.get("dietary", {})
                p_obj = PrioritizedConstraint(
                    name=f"Dietary Exclusion: {diet}",
                    type="dietary",
                    weight=cfg.get("weight", 0.95),
                    hard_or_soft="HARD",
                    reason=cfg.get("reason", "Mandatory dietary label claim"),
                    source=cfg.get("source", "Dietary Standard Rules"),
                    parameter="dietary_pattern",
                    operator="FORBIDDEN",
                    target_value=diet
                )
                hard_list.append(p_obj)
                prioritized_list.append(p_obj)

            if brief.nutrition_targets.protein_min:
                cfg = priority_cfg.get("nutritional_minimum", {})
                p_obj = PrioritizedConstraint(
                    name=f"Protein Min >= {brief.nutrition_targets.protein_min}%",
                    type="nutrition",
                    weight=cfg.get("weight", 0.90),
                    hard_or_soft="HARD",
                    reason=cfg.get("reason", "Nutritional minimum constraint"),
                    source=cfg.get("source", "Nutritional Target Specification"),
                    parameter="protein_min",
                    operator=">=",
                    target_value=brief.nutrition_targets.protein_min
                )
                hard_list.append(p_obj)
                prioritized_list.append(p_obj)

        return {
            "all_constraints": [p.to_dict() for p in prioritized_list],
            "hard_constraints": [p.to_dict() for p in hard_list],
            "soft_constraints": [p.to_dict() for p in soft_list],
            "priority_distribution": {
                "hard_count": len(hard_list),
                "soft_count": len(soft_list),
                "total_count": len(prioritized_list)
            }
        }

    def evaluate_ingredient_hard_constraints(
        self, ingredient: RetrievedIngredient, brief: ProductBrief
    ) -> Tuple[bool, List[ConstraintResult]]:
        """
        Evaluates whether an individual ingredient violates any HARD constraints.
        Returns (is_allowed, list_of_results).
        """
        results = []
        is_allowed = True

        ing_name_lower = ingredient.name.lower()
        allergen_lower = ingredient.allergen.lower()

        is_plant_butter = any(pb in ing_name_lower for pb in ["cocoa butter", "almond butter", "peanut butter", "cashew butter", "shea butter", "seed butter"])

        # 1. Dietary Hard Exclusions
        for diet in brief.dietary_requirements:
            diet_key = diet.lower().replace("-", "_")
            prohibited_list = PROHIBITED_INGREDIENTS_MAP.get(diet_key, [])
            for prohibited in prohibited_list:
                if prohibited == "butter" and is_plant_butter:
                    continue
                if prohibited in ing_name_lower or prohibited in allergen_lower:
                    is_allowed = False
                    results.append(ConstraintResult(
                        name=f"Dietary Hard Constraint: {diet}",
                        target=f"No {prohibited}",
                        actual=ingredient.name,
                        status="violated",
                        is_hard=True,
                        reason=f"Ingredient '{ingredient.name}' violates mandatory '{diet}' constraint."
                    ))

        # Check explicit flags on ingredient object
        if "Vegan" in brief.dietary_requirements and not ingredient.vegan:
            if not is_plant_butter or "dairy" in allergen_lower:
                is_allowed = False
                results.append(ConstraintResult(
                    name="Vegan Flag Constraint",
                    target="Vegan == True",
                    actual=f"{ingredient.name} (Non-Vegan)",
                    status="violated",
                    is_hard=True,
                    reason=f"Ingredient '{ingredient.name}' is flagged as non-vegan."
                ))

        if "Gluten-Free" in brief.dietary_requirements and not ingredient.gluten_free:
            is_allowed = False
            results.append(ConstraintResult(
                name="Gluten-Free Flag Constraint",
                target="Gluten-Free == True",
                actual=f"{ingredient.name} (Contains Gluten)",
                status="violated",
                is_hard=True,
                reason=f"Ingredient '{ingredient.name}' is flagged as containing gluten."
            ))

        # 2. Explicit Exclusion List Check
        for exclusion in brief.excluded_ingredients:
            ex_lower = exclusion.lower()
            if ex_lower == "butter" and is_plant_butter:
                continue
            if ex_lower and (ex_lower in ing_name_lower or ex_lower in allergen_lower):
                is_allowed = False
                results.append(ConstraintResult(
                    name=f"Exclusion Hard Constraint: {exclusion}",
                    target=f"Prohibit {exclusion}",
                    actual=ingredient.name,
                    status="violated",
                    is_hard=True,
                    reason=f"Ingredient '{ingredient.name}' matches explicit exclusion '{exclusion}'."
                ))

        if is_allowed:
            results.append(ConstraintResult(
                name="Hard Dietary Check",
                target="Compliant",
                actual="Pass",
                status="satisfied",
                is_hard=True
            ))

        return is_allowed, results

    def filter_eligible_ingredients(
        self, ingredients: List[RetrievedIngredient], brief: ProductBrief
    ) -> List[RetrievedIngredient]:
        """Filters candidate ingredient list, removing any ingredient violating HARD constraints or Formulation Eligibility Filter."""
        from eligibility_engine import eligibility_filter
        eligible = []
        for ing in ingredients:
            # Check Phase 3: Formulation Eligibility Filter
            el_res = eligibility_filter.evaluate_eligibility(ing)
            if not el_res.get("formulation_eligible", True):
                logger.info(f"[ConstraintEngine] Excluded '{ing.name}' by Formulation Eligibility Filter: {el_res.get('eligibility_reason')}")
                continue

            allowed, _ = self.evaluate_ingredient_hard_constraints(ing, brief)
            if allowed:
                eligible.append(ing)
            else:
                logger.info(f"[ConstraintEngine] Filtered out ingredient '{ing.name}' due to Hard Constraint violation.")
        return eligible

    def analyze_compatibility(self, ingredient_names: List[str]) -> Tuple[bool, List[str]]:
        """Analyzes pairwise compatibility of ingredient list using compatibility model and KG."""
        from models.compatibility.model import compatibility_model
        ing_dicts = [{"name": n} for n in ingredient_names]
        eval_res, _ = compatibility_model.predict_with_uncertainty(ing_dicts)
        return eval_res["is_compatible"], eval_res["incompatibilities"]

# Global singleton instance
constraint_engine = ConstraintEngine()
