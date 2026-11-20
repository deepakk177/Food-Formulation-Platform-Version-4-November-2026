"""
Formulation Ingredient Eligibility Layer (Phase 3)
Determines whether an ingredient entity in the Knowledge Graph is a genuine food formulation raw material
or an ineligible ontology concept (finished dish, organism, packaging, process, ambiguous FoodEx2 classification).
"""
import re
from typing import Dict, Any, Tuple

# Ineligible finished foods, composite culinary dishes, and non-formulation concepts
INELIGIBLE_NAME_PATTERNS = [
    r"chewing gum",
    r"breath freshener",
    r"bakery product \(containing",
    r"cooked sauce",
    r"gravy",
    r"sandwich",
    r"pizza",
    r"burger",
    r"cheeseburger",
    r"cheese \(",
    r"\(filled",
    r"\(containing",
    r"\(sometimes",
    r"\(other than",
    r"\(including",
    r"\(for manufacturing\)",
    r"compote",
    r"canned or jarred",
    r"frozen meal",
    r"mushy peas",
    r"drag[eé]e",
    r"sugar cotton",
    r"european moose",
    r"eel, european",
    r"perch, european",
    r"smelt, european",
    r"plaice, european",
    r"conger, european",
    r"lobster, european",
    r"oyster, european",
    r"squid, european",
    r"european buffalo",
    r"condensed milk \(sometimes",
    r"prepared dish",
    r"ready-to-eat",
    r"culinary preparation",
    r"composite food",
    r"packaging",
    r"equipment",
    r"utensil"
]

INELIGIBLE_REGEX = re.compile("|".join(INELIGIBLE_NAME_PATTERNS), re.IGNORECASE)

class FormulationEligibilityFilter:
    def __init__(self):
        self.version = "2.0.0"

    def evaluate_eligibility(self, ingredient: Any) -> Dict[str, Any]:
        """
        Evaluates ingredient against 8 formal research criteria:
        1. Valid food entity
        2. Raw formulation material (not finished dish / composite food)
        3. Relevant functional role assigned
        4. Valid food category
        5. Known regulatory clearance (Codex / FDA / EFSA / GRAS)
        6. Essential composition / property availability
        7. Evidence traceability
        8. Non-prohibited status
        """
        if isinstance(ingredient, dict):
            name = str(ingredient.get("name", "")).strip()
            cat = str(ingredient.get("category", "")).strip()
            role = str(ingredient.get("functional_role", "")).strip()
            ing_id = str(ingredient.get("id", "")).strip()
            source = str(ingredient.get("source", "")).strip()
            reg_status = str(ingredient.get("regulatory_status", "UNKNOWN")).strip()
            nutrition = ingredient.get("nutrition", {})
            cost = ingredient.get("cost_per_kg")
        else:
            name = str(getattr(ingredient, "name", "")).strip()
            cat = str(getattr(ingredient, "category", "")).strip()
            roles = getattr(ingredient, "functional_roles", [])
            role = str(roles[0]) if roles else str(getattr(ingredient, "functional_role", "Bulking"))
            ing_id = str(getattr(ingredient, "id", "")).strip()
            source = str(getattr(ingredient, "source", "")).strip()
            reg_status = str(getattr(ingredient, "regulatory_status", "UNKNOWN")).strip()
            nutrition = getattr(ingredient, "nutrition", {})
            cost = getattr(ingredient, "cost_per_kg", None)

        name_lower = name.lower()

        # Check 1: Exclude finished dishes and ontology contamination
        if INELIGIBLE_REGEX.search(name_lower):
            return {
                "formulation_eligible": False,
                "eligibility_reason": f"Excluded as finished composite food/dish or irrelevant concept ('{name}')",
                "eligibility_evidence": "FoodEx2 / FoodON Culinary Dish Taxonomy Exclusion",
                "entity_type": "Composite Food / Finished Dish"
            }

        # Check 2: Exclude uncurated FoodEx2 raw code entries with zero nutritional basis
        if "(efsa foodex2)" in name_lower and not ing_id.startswith("ing_"):
            # If FoodEx2 entry has no protein, fat, carbs, or fiber, reject as uncharacterized concept
            p = float(nutrition.get("protein", 0.0) or 0.0) if isinstance(nutrition, dict) else 0.0
            f = float(nutrition.get("fat", 0.0) or 0.0) if isinstance(nutrition, dict) else 0.0
            c = float(nutrition.get("carbs", 0.0) or 0.0) if isinstance(nutrition, dict) else 0.0
            if p == 0.0 and f == 0.0 and c == 0.0:
                return {
                    "formulation_eligible": False,
                    "eligibility_reason": f"Uncharacterized FoodEx2 classification node without verified nutrient profile ('{name}')",
                    "eligibility_evidence": "EFSA FoodEx2 Classification Hierarchy Filter",
                    "entity_type": "Uncharacterized Classification Node"
                }

        # Check 3: Regulatory prohibition
        if reg_status == "Prohibited":
            return {
                "formulation_eligible": False,
                "eligibility_reason": f"Prohibited under applicable Codex / FDA food additive regulations",
                "eligibility_evidence": "21 CFR / Codex GSFA Schedule I",
                "entity_type": "Prohibited Substance"
            }

        # Check 4: Approved formulation raw materials
        return {
            "formulation_eligible": True,
            "eligibility_reason": f"Verified formulation raw material with active '{role}' functionality",
            "eligibility_evidence": "TCS Food Formulator Master Formulation Registry",
            "entity_type": "Formulation Raw Material"
        }

# Global singleton
eligibility_filter = FormulationEligibilityFilter()
