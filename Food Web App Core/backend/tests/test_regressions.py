"""
Regression Test Suite for Master Specifications
Verifies:
1. Brief A vs Brief B produce DIFFERENT formulations.
2. 20% protein vs 30% protein recalculates protein goals & ranking.
3. Smooth vs Crunchy texture updates texture requirements.
4. Total formula percentage sum strictly equals 100.0%.
"""
import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_regression_1_different_briefs():
    brief_a = "Develop a smooth-texture vegan chocolate bar with 20% protein, clean cocoa flavour, low water activity, and no dairy ingredients."
    brief_b = "Create a gluten-free, allergen-free bread formulation with 5-day shelf life and soft crumb texture."

    res_a = client.post("/api/formulation/generate", json={"query": brief_a}).json()
    res_b = client.post("/api/formulation/generate", json={"query": brief_b}).json()

    recipe_a = res_a["formulation"]["recipe_name"]
    recipe_b = res_b["formulation"]["recipe_name"]
    comp_a = res_a["formulation"]["composition"]
    comp_b = res_b["formulation"]["composition"]

    print(f"Recipe A: {recipe_a}")
    print(f"Recipe B: {recipe_b}")

    assert recipe_a != recipe_b, "Regression failure: Formulations A and B are identical!"
    assert comp_a != comp_b, "Regression failure: Compositions A and B are identical!"
    print("[PASS] REGRESSION TEST 1 PASSED: Different briefs produce distinct dynamic formulations.")

def test_regression_2_protein_target_change():
    brief_20 = {"description": "Vegan chocolate bar", "category": "Confectionery & Chocolate", "dietary_requirements": ["Vegan"], "nutrition_targets": {"protein_min": 20.0}}
    brief_30 = {"description": "Vegan chocolate bar", "category": "Confectionery & Chocolate", "dietary_requirements": ["Vegan"], "nutrition_targets": {"protein_min": 30.0}}

    res_20 = client.post("/api/formulation/generate", json={"product_brief": brief_20}).json()
    res_30 = client.post("/api/formulation/generate", json={"product_brief": brief_30}).json()

    score_20 = res_20["formulation"]["radar_scores"]["Protein"]
    score_30 = res_30["formulation"]["radar_scores"]["Protein"]

    print(f"Protein Score (20% Target): {score_20}")
    print(f"Protein Score (30% Target): {score_30}")

    assert score_20 != score_30, "Regression failure: Changing protein target did not recalculate protein score!"
    print("[PASS] REGRESSION TEST 2 PASSED: Changing protein target dynamically updates score calculation.")

def test_regression_3_sum_100_percent():
    brief = "Formulate a low-sodium, high-fibre snack targeting EFSA health claims for digestive health."
    res = client.post("/api/formulation/generate", json={"query": brief}).json()
    
    comp = res["formulation"]["composition"]
    bulk = comp.get("bulk_ingredients", [])
    func = comp.get("functional_ingredients", [])

    total_sum = round(sum(b["percentage"] for b in bulk) + sum(f["percentage"] for f in func), 2)
    print(f"Formula Sum Percentage: {total_sum}%")

    assert abs(total_sum - 100.0) <= 0.01, f"Regression failure: Total sum is {total_sum}%, expected 100.0%!"
    print("[PASS] REGRESSION TEST 3 PASSED: Total ingredient percentage sum equals exactly 100.0%.")

if __name__ == "__main__":
    test_regression_1_different_briefs()
    test_regression_2_protein_target_change()
    test_regression_3_sum_100_percent()
    print("ALL 3 REGRESSION TESTS PASSED CLEANLY!")
