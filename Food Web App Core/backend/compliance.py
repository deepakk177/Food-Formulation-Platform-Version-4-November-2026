from typing import Dict, Any, List

def evaluate_compliance(composition: Dict[str, Any], constraints: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates ingredient composition and constraints against FSSAI, FDA, and EFSA standards.
    """
    results = {
        "FSSAI": {"status": "Passed", "alerts": []},
        "FDA": {"status": "Passed", "alerts": []},
        "EFSA": {"status": "Passed", "alerts": []}
    }
    
    ingredients = composition.get("bulk_ingredients", []) + composition.get("functional_ingredients", [])
    
    # 1. Allergen & Strict Dietary Constraints Checks
    is_vegan = constraints.get("vegan", False)
    is_gluten_free = constraints.get("gluten_free", False)
    excluded_allergens = constraints.get("allergens_exclude", [])
    
    for ing in ingredients:
        name = ing.get("name", "").lower()
        allergen = ing.get("allergen", "None")
        
        # Vegan Check
        if is_vegan and allergen in ["Milk", "Egg"]:
            msg = f"Violation: Vegan product contains allergen {allergen} from ingredient '{ing.get('name')}'"
            results["EFSA"]["status"] = "Failed"
            results["EFSA"]["alerts"].append(msg)
            results["FDA"]["status"] = "Failed"
            results["FDA"]["alerts"].append(msg)
            results["FSSAI"]["status"] = "Failed"
            results["FSSAI"]["alerts"].append(msg)
            
        # Gluten Free Check
        if is_gluten_free and allergen == "Gluten":
            msg = f"Violation: Gluten-Free product contains gluten-based ingredient '{ing.get('name')}'"
            results["FDA"]["status"] = "Failed"
            results["FDA"]["alerts"].append(msg)
            results["FSSAI"]["status"] = "Failed"
            results["FSSAI"]["alerts"].append(msg)
            
        # User Allergen Exclusion
        if allergen in excluded_allergens:
            msg = f"Allergen warning: '{ing.get('name')}' contains excluded allergen '{allergen}'"
            for region in results:
                # If it's already Failed, don't overwrite the status, just add the warning log
                if results[region]["status"] != "Failed":
                    results[region]["status"] = "Warning"
                results[region]["alerts"].append(msg)

    # 2. Limits and Additive restrictions (Example rules)
    for ing in ingredients:
        name = ing.get("name", "").lower()
        pct = ing.get("percentage", 0.0)
        category = ing.get("category", "")
        role = ing.get("functional_role", "")
        
        # Preservatives limit checks
        if category == "Preservation" or role == "Preservation":
            if pct > 0.1: # Standard general limit for food additives
                msg = f"FSSAI/EFSA Alert: Preservative '{ing.get('name')}' concentration ({pct}%) exceeds standard limit of 0.10%"
                if results["FSSAI"]["status"] != "Failed":
                    results["FSSAI"]["status"] = "Warning"
                results["FSSAI"]["alerts"].append(msg)
                
                if results["EFSA"]["status"] != "Failed":
                    results["EFSA"]["status"] = "Warning"
                results["EFSA"]["alerts"].append(msg)

        # Sweeteners limit checks
        if role == "Sweetener" or category == "Sweetener":
            if name in ["stevia extract", "sucralose"] and pct > 0.05:
                msg = f"FDA/EFSA Warning: High-intensity sweetener '{ing.get('name')}' exceeds standard formula limits (0.05%) for consumer beverages."
                if results["FDA"]["status"] != "Failed":
                    results["FDA"]["status"] = "Warning"
                results["FDA"]["alerts"].append(msg)
                
                if results["EFSA"]["status"] != "Failed":
                    results["EFSA"]["status"] = "Warning"
                results["EFSA"]["alerts"].append(msg)

    return results
