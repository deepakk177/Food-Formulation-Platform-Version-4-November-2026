"""
Programmatic Constraint Engine for TCS Food Formulator
Enforces strict separation between Hard Constraints (veto / feasibility) and Soft Objectives (quality ranking),
and performs ingredient interaction & compatibility analysis.
"""
import logging
from typing import Dict, Any, List, Tuple
from retrieval_service import RetrievedIngredient
from requirements_extractor import ProductBrief

logger = logging.getLogger("ConstraintEngine")

PROHIBITED_INGREDIENTS_MAP = {
    "vegan": ["milk", "egg", "whey", "butter", "gelatin", "heavy cream", "skim milk", "whole eggs", "unsalted butter", "yogurt culture"],
    "dairy_free": ["milk", "whey", "butter", "heavy cream", "skim milk", "unsalted butter", "yogurt culture"],
    "gluten_free": ["wheat flour", "wheat", "rye", "barley", "gluten"],
    "peanut_free": ["peanuts", "peanut oil", "peanut butter"],
    "soy_free": ["soy lecithin", "soybean oil", "soymilk", "soy protein"]
}

# Known incompatible pairs (e.g. high acid + unbuffered protein)
INCOMPATIBLE_PAIRS = [
    ("citric acid", "unbuffered pea protein"),
    ("high acid fruit", "milk protein isolate")
]

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

        # 1. Dietary Hard Exclusions
        for diet in brief.dietary_requirements:
            diet_key = diet.lower().replace("-", "_")
            prohibited_list = PROHIBITED_INGREDIENTS_MAP.get(diet_key, [])
            for prohibited in prohibited_list:
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
        """Filters candidate ingredient list, removing any ingredient violating HARD constraints."""
        eligible = []
        for ing in ingredients:
            allowed, _ = self.evaluate_ingredient_hard_constraints(ing, brief)
            if allowed:
                eligible.append(ing)
            else:
                logger.info(f"[ConstraintEngine] Filtered out ingredient '{ing.name}' due to Hard Constraint violation.")
        return eligible

    def analyze_compatibility(self, ingredient_names: List[str]) -> Tuple[bool, List[str]]:
        """Analyzes pairwise compatibility of ingredient list."""
        incompatibilities = []
        names_lower = [n.lower() for n in ingredient_names]
        
        for itemA, itemB in INCOMPATIBLE_PAIRS:
            matchA = any(itemA in n for n in names_lower)
            matchB = any(itemB in n for n in names_lower)
            if matchA and matchB:
                incompatibilities.append(f"Incompatible pair detected: '{itemA}' and '{itemB}'")

        is_compatible = len(incompatibilities) == 0
        return is_compatible, incompatibilities

# Global singleton instance
constraint_engine = ConstraintEngine()
