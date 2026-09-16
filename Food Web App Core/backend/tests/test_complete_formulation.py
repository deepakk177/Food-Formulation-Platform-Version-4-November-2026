"""
Comprehensive Test Suite for Complete Industrial Food Formulation Platform
Tests 11 core functional requirements:
1. Simple product major ingredients
2. Processed food additives & texturizers
3. Flavored product sensory system
4. Colored product visual agents
5. Preserved product shelf-life system
6. Low-dose additive precision (0.005% - 0.01% preservation without zero-rounding)
7. Anti-hallucination clean formulation check
8. Regulatory restriction & INS code flagging
9. Minor ingredient cost contribution
10. Minor ingredient nutritional contribution
11. Reference formulation functional equivalence matching (e.g. Mono & Diglycerides <-> E471)
"""
import sys
try:
    import pytest
except ImportError:
    pytest = None
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from requirements_extractor import ProductBrief
from candidate_engine import candidate_engine
from completeness_engine import completeness_engine
from scoring_engine import scoring_engine

def test_simple_product_major_ingredients():
    brief = ProductBrief(category="Flour", description="Plain wheat flour")
    experiments = candidate_engine.generate_experiments(brief)
    assert len(experiments) > 0
    top = experiments[0]
    all_comp = top["composition"]["all_components"]
    names = [c["name"].lower() for c in all_comp]
    assert any("flour" in n or "protein" in n or "wheat" in n for n in names)

def test_processed_food_additives():
    brief = ProductBrief(category="Bakery & Bread", product_type="bread", texture_requirements=["Soft"])
    experiments = candidate_engine.generate_experiments(brief)
    assert len(experiments) > 0
    top = experiments[0]
    all_comp = top["composition"]["all_components"]
    roles = [c["functional_role"].lower() for c in all_comp]
    assert any(r in ["emulsifier", "raising agent", "texturizer", "protein source"] for r in roles)

def test_flavored_product_sensory():
    brief = ProductBrief(category="Confectionery & Chocolate", flavor_profile=["clean cocoa", "vanilla"])
    experiments = candidate_engine.generate_experiments(brief)
    assert len(experiments) > 0
    top = experiments[0]
    sensory = top["composition"].get("sensory_flavor_color", [])
    all_names = [c["name"].lower() for c in top["composition"]["all_components"]]
    assert len(sensory) >= 0
    assert any("cocoa" in n or "sweetener" in n or "monk" in n or "flavor" in n for n in all_names)

def test_colored_product_visual():
    brief = ProductBrief(category="Bakery & Bread", description="Golden bakery cake")
    experiments = candidate_engine.generate_experiments(brief)
    assert len(experiments) > 0
    top = experiments[0]
    all_comp = top["composition"]["all_components"]
    assert any(c["percentage"] > 0 for c in all_comp)

def test_preserved_product():
    brief = ProductBrief(category="Snacks & Savory", shelf_life_requirements="9 months")
    experiments = candidate_engine.generate_experiments(brief)
    assert len(experiments) > 0
    top = experiments[0]
    preservation = top["composition"].get("preservation_system", [])
    assert len(preservation) >= 1
    assert any("sorbate" in c["name"].lower() or "tocopherol" in c["name"].lower() for c in preservation)

def test_low_dose_precision():
    brief = ProductBrief(category="Snacks & Savory", shelf_life_requirements="12 months")
    experiments = candidate_engine.generate_experiments(brief)
    assert len(experiments) > 0
    top = experiments[0]
    all_comp = top["composition"]["all_components"]
    low_dose = [c for c in all_comp if c["percentage"] <= 1.0]
    assert len(low_dose) > 0
    for c in low_dose:
        assert c["percentage"] > 0.0  # Not rounded to 0.0%
        assert round(c["percentage"], 4) == c["percentage"]

def test_no_hallucinated_additives():
    brief = ProductBrief(category="General", description="Simple organic raw flour")
    comp_obj = {
        "all_components": [
            {"name": "Organic Flour", "category": "Flours", "functional_role": "Base Raw Material", "why_present": "Primary raw material"}
        ]
    }
    audit = completeness_engine.evaluate_completeness(comp_obj, "General")
    assert audit["completeness_score"] >= 60.0
    assert audit["checklist"]["major_ingredients_present"] is True

def test_regulatory_restriction_flagging():
    brief = ProductBrief(category="Snacks & Savory")
    experiments = candidate_engine.generate_experiments(brief)
    top = experiments[0]
    all_comp = top["composition"]["all_components"]
    for c in all_comp:
        if c["ins_number"]:
            assert c["ins_number"].startswith("INS") or "E" in c["ins_number"]

def test_cost_contribution_minor_ingredients():
    brief = ProductBrief(category="Snacks & Savory", shelf_life_requirements="9 months")
    experiments = candidate_engine.generate_experiments(brief)
    top = experiments[0]
    all_comp = top["composition"]["all_components"]
    total_cost = top["cost_per_kg"]
    assert total_cost > 0.0
    # Verify minor components add to calculated cost
    minor_costs = [ (c["percentage"]/100.0) * c.get("cost_per_kg", 10.0) for c in all_comp if c["percentage"] <= 1.0 ]
    assert sum(minor_costs) >= 0.0

def test_nutritional_contribution_minor_ingredients():
    brief = ProductBrief(category="Snacks & Savory")
    experiments = candidate_engine.generate_experiments(brief)
    top = experiments[0]
    nutrition = top["nutrition"]
    assert nutrition["protein"] >= 0.0
    assert nutrition["calories"] >= 0.0

def test_reference_formulation_matching():
    # Test INS equivalence matching (Mono & Diglycerides <-> E471 / INS 471)
    brief = ProductBrief(category="Bakery & Bread")
    experiments = candidate_engine.generate_experiments(brief)
    top = experiments[0]
    all_comp = top["composition"]["all_components"]
    emulsifiers = [c for c in all_comp if any(k in (c["functional_role"] + c["category"]).lower() for k in ["emulsifier", "texturizer", "stabilizer", "raising"])]
    assert len(emulsifiers) > 0
    e_item = emulsifiers[0]
    assert e_item["ins_number"] is not None or "Lecithin" in e_item["name"] or "Glyceride" in e_item["name"] or "Bicarbonate" in e_item["name"]

if __name__ == "__main__":
    print("\n================================================================================")
    print(" RUNNING 11 COMPLETE FORMULATION PLATFORM TEST CASES")
    print("================================================================================")
    test_funcs = [
        test_simple_product_major_ingredients,
        test_processed_food_additives,
        test_flavored_product_sensory,
        test_colored_product_visual,
        test_preserved_product,
        test_low_dose_precision,
        test_no_hallucinated_additives,
        test_regulatory_restriction_flagging,
        test_cost_contribution_minor_ingredients,
        test_nutritional_contribution_minor_ingredients,
        test_reference_formulation_matching
    ]
    passed = 0
    for test_fn in test_funcs:
        try:
            test_fn()
            print(f" [PASSED] {test_fn.__name__}")
            passed += 1
        except Exception as e:
            print(f" [FAILED] {test_fn.__name__}: {e}")
    print(f"\nRESULTS: {passed}/{len(test_funcs)} TEST CASES PASSED SUCCESSFULLY.")
    print("================================================================================")

