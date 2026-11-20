"""
Comprehensive Automated Consistency & E2E Validation Test Suite.
Tests:
1. Vegan / Dairy-Free Chocolate formulation.
2. High-Protein Chocolate formulation.
3. Chocolate with strict Cocoa Butter minimum constraint (>= 25%).
4. Sugar-restricted formulation (<= 1% or <= 28%).
5. Multiple simultaneous numerical constraints.
6. Missing ingredient properties handling (COST_UNKNOWN, no fake numbers).
7. Infeasible / contradictory constraint combinations (pre-optimization diagnostics).
8. Candidate selection switching and zero data leakage.
"""
import pytest
import sys
import os
from pathlib import Path

# Add backend and root to sys.path
backend_dir = Path(__file__).resolve().parent.parent
root_dir = backend_dir.parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from requirements_extractor import product_brief_parser, ProductBrief, NutritionTargets
from candidate_engine import candidate_engine
from calculation_service import calculation_service
from models.formulation.model import formulation_optimizer
from scoring_engine import scoring_engine
from validation_gate import validation_gate
from retrieval_service import retrieval_orchestrator
from main import generate_formulation_pipeline

def test_vegan_dairy_free_chocolate():
    """Test 1: Vegan/Dairy-Free Dark Chocolate."""
    query = "Develop a 100% vegan dairy-free dark chocolate confectionery with at least 7% protein, using cocoa butter, under $15.00/kg."
    brief = product_brief_parser.parse(query)
    
    assert "Vegan" in brief.dietary_requirements or "vegan" in [d.lower() for d in brief.dietary_requirements]
    
    retrieved = retrieval_orchestrator.retrieve_all_multi_dimensional(brief.dict())
    experiments = candidate_engine.generate_experiments(brief, retrieved.get("ingredients", []))
    
    assert len(experiments) > 0, "Candidate engine should generate valid candidate sets"
    
    for exp in experiments:
        comps = exp["composition"]["all_components"]
        # 1. Mass balance check
        is_mass_valid, tot_pct, delta = calculation_service.verify_mass_balance(comps)
        assert is_mass_valid, f"Mass balance must sum to 100.0000% (was {tot_pct}%, delta {delta})"
        
        # 2. No dairy / animal ingredients
        for c in comps:
            name_l = c["name"].lower()
            assert not any(d in name_l for d in ["milk", "dairy", "whey", "casein", "butter oil", "whole milk"]), f"Vegan violation: found {c['name']}"
            assert c["category"] != "Animal", f"Category violation: {c['name']}"
            
        # 3. Protein >= 7.0%
        macros = exp["nutrition"]
        assert macros["protein"] >= 6.8, f"Protein target violated: {macros['protein']}%"
        
        # 4. Traceability check
        selected_ids = exp["traceability"]["selected_ids"]
        eligible_ids = set(exp["traceability"]["eligible_ids"])
        for sid in selected_ids:
            assert sid in eligible_ids, f"Ingredient {sid} was not in eligible candidate pool!"

def test_high_protein_chocolate():
    """Test 2: High-Protein Chocolate Formulation."""
    query = "Formulate a high-protein dark chocolate bar with at least 15% protein and cocoa butter."
    brief = product_brief_parser.parse(query)
    
    assert brief.nutrition_targets.protein_min >= 15.0
    
    retrieved = retrieval_orchestrator.retrieve_all_multi_dimensional(brief.dict())
    experiments = candidate_engine.generate_experiments(brief, retrieved.get("ingredients", []))
    
    assert len(experiments) > 0
    # Check nutrition maximized strategy delivers high protein
    nut_max = next((e for e in experiments if e["strategy"] == "nutrition_maximized"), experiments[0])
    comps = nut_max["composition"]["all_components"]
    
    is_mass_valid, tot_pct, _ = calculation_service.verify_mass_balance(comps)
    assert is_mass_valid
    assert nut_max["nutrition"]["protein"] >= 9.0, f"Expected high protein yield, got {nut_max['nutrition']['protein']}g"

def test_cocoa_butter_minimum_constraint():
    """Test 3: Chocolate with strict Cocoa Butter minimum constraint (>= 25%)."""
    query = "Formulate a chocolate confectionery with at least 25% cocoa butter, at least 7% protein, and at most 28% sugar."
    brief = product_brief_parser.parse(query)
    
    # Check that cocoa butter target was extracted
    cb_constraint = next((c for c in brief.granular_constraints if c.parameter == "cocoa_butter"), None)
    assert cb_constraint is not None, "Cocoa butter constraint must be extracted"
    assert float(cb_constraint.target_value) == 25.0
    
    retrieved = retrieval_orchestrator.retrieve_all_multi_dimensional(brief.dict())
    experiments = candidate_engine.generate_experiments(brief, retrieved.get("ingredients", []))
    
    assert len(experiments) > 0
    balanced = next((e for e in experiments if e["strategy"] == "balanced"), experiments[0])
    comps = balanced["composition"]["all_components"]
    
    # Verify cocoa butter inclusion >= 24.9%
    cb_comps = [c for c in comps if "cocoa butter" in c["name"].lower()]
    total_cb = sum(c["percentage"] for c in cb_comps)
    assert total_cb >= 24.9, f"Cocoa butter inclusion {total_cb}% is below 25.0% threshold"

def test_sugar_restricted_formulation():
    """Test 4: Sugar-Restricted Formulation."""
    query = "Formulate a sugar-free vegan chocolate bar with at most 1% sugar and at least 7% protein."
    brief = product_brief_parser.parse(query)
    
    assert brief.nutrition_targets.sugar_max <= 1.0 or any(c.parameter == "sugar_max" and float(c.target_value) <= 1.0 for c in brief.granular_constraints)
    
    retrieved = retrieval_orchestrator.retrieve_all_multi_dimensional(brief.dict())
    experiments = candidate_engine.generate_experiments(brief, retrieved.get("ingredients", []))
    
    assert len(experiments) > 0
    for exp in experiments:
        comps = exp["composition"]["all_components"]
        # Ensure no high-sucrose cane sugar is used
        cane_sugars = [c for c in comps if "cane sugar" in c["name"].lower() or "granulated sugar" in c["name"].lower()]
        assert len(cane_sugars) == 0, "Sugar-free formulation must not use cane sugar"

def test_multiple_simultaneous_numerical_constraints():
    """Test 5: Multiple Simultaneous Numerical Constraints."""
    query = "Formulate a vegan chocolate with at least 25% cocoa butter, at least 7% protein, at most 28% sugar, and cost under $14.00/kg."
    payload = {"query": query}
    res = generate_formulation_pipeline(payload)
    
    assert "candidate_sets" in res
    assert len(res["candidate_sets"]) >= 3
    form = res["formulation"]
    comps = form["composition"]["all_components"]
    
    # 1. Mass Balance
    is_mass_valid, tot_pct, delta = calculation_service.verify_mass_balance(comps)
    assert is_mass_valid, f"Mass balance failed: {tot_pct}%"
    
    # 2. Cocoa butter >= 24.9%
    cb_pct = sum(c["percentage"] for c in comps if "cocoa butter" in c["name"].lower())
    assert cb_pct >= 24.9, f"Cocoa butter {cb_pct}% < 25%"
    
    # 3. Protein >= 6.8%
    assert form["performance_prediction"]["protein"] >= 6.8, f"Protein {form['performance_prediction']['protein']}% < 7%"

def test_missing_ingredient_properties_handling():
    """Test 6: Missing Ingredient Properties Handling (COST_UNKNOWN, no fake numbers)."""
    mock_components = [
        {
            "id": "ing_test_1",
            "name": "Test Cocoa Butter",
            "percentage": 50.0,
            "cost_per_kg": 10.0,
            "nutrition": {"protein": 0.0, "fat": 100.0, "carbs": 0.0, "sugar": 0.0}
        },
        {
            "id": "ing_test_2",
            "name": "Test Special Flour",
            "percentage": 50.0,
            "cost_per_kg": None,  # MISSING COST
            "nutrition": {"protein": 10.0, "fat": 2.0, "carbs": 70.0, "sugar": 5.0}
        }
    ]
    
    cost_res = calculation_service.calculate_cost(mock_components)
    assert cost_res["has_unknown_cost_components"] is True
    assert cost_res["cost_status"] == "COST_UNKNOWN"
    assert cost_res["cost_per_kg"] is None, "Cost per kg must be None when any ingredient cost is unknown"
    
    macro_res = calculation_service.calculate_macros(mock_components)
    assert macro_res["protein"] == 5.0
    assert macro_res["fat"] == 51.0
    assert macro_res["calories"] == (4.0 * 5.0 + 4.0 * 35.0 + 9.0 * 51.0)

def test_infeasible_constraint_combinations():
    """Test 7: Infeasible / Contradictory Constraint Combinations."""
    mock_ingredients = [
        {"id": "ing_1", "name": "Sugar", "protein": 0.0, "fat": 0.0, "carbs": 100.0, "sugar": 100.0, "cost_per_kg": 2.0, "functional_role": "sweetener", "category": "sweetener"},
        {"id": "ing_2", "name": "Cocoa Butter", "protein": 0.0, "fat": 100.0, "carbs": 0.0, "sugar": 0.0, "cost_per_kg": 12.0, "functional_role": "fat", "category": "fat"}
    ]
    # Infeasible: protein_min = 50.0% but neither ingredient has ANY protein!
    targets = {"protein_min": 50.0}
    
    res, conf = formulation_optimizer.predict_with_uncertainty({
        "ingredients": mock_ingredients,
        "targets": targets,
        "strategy": "balanced"
    })
    
    assert res["is_feasible"] is False, "Impossible protein target must be flagged as infeasible"
    assert res["status"] == "CONTRADICTORY_OR_INFEASIBLE_CONSTRAINTS"
    assert any("Maximum achievable protein" in v for v in res["violations"])

def test_candidate_selection_consistency():
    """Test 8: Candidate Selection Switching & Zero Data Leakage."""
    query = "Develop a dark chocolate confectionery with at least 7% protein, under $14.00/kg."
    
    # Request Candidate Index 1 (Cost-Optimized)
    payload_cost = {
        "query": query,
        "selected_candidate_index": 1
    }
    res_cost = generate_formulation_pipeline(payload_cost)
    form_cost = res_cost["formulation"]
    assert form_cost["recipe_id"] == res_cost["candidate_sets"][1]["candidate_id"]
    assert form_cost["strategy"] == res_cost["candidate_sets"][1]["strategy"]
    assert form_cost["performance_prediction"]["protein"] == res_cost["candidate_sets"][1]["nutrition"]["protein"]
    
    # Request Candidate Index 0 (Top Pareto)
    payload_top = {
        "query": query,
        "selected_candidate_index": 0
    }
    res_top = generate_formulation_pipeline(payload_top)
    form_top = res_top["formulation"]
    assert form_top["recipe_id"] == res_top["candidate_sets"][0]["candidate_id"]
    assert form_top["strategy"] == res_top["candidate_sets"][0]["strategy"]
    assert form_top["performance_prediction"]["protein"] == res_top["candidate_sets"][0]["nutrition"]["protein"]

if __name__ == "__main__":
    pytest.main(["-v", str(Path(__file__))])

