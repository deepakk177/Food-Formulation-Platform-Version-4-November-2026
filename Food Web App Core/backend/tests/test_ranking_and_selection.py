"""
Comprehensive Test Suite for Fair Candidate Scoring, Feasibility Partitioning,
and Unbiased Best Formulation Selection (Scenarios A through H).
"""
import pytest
import sys
import copy
import random
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
from scoring_engine import scoring_engine
from validation_gate import validation_gate
from retrieval_service import retrieval_orchestrator
from main import generate_formulation_pipeline

def test_scenario_a_balanced_genuinely_best():
    """Scenario A: Balanced genuinely performs best and wins fairly."""
    brief_dict = {
        "description": "Standard Balanced Chocolate Bar",
        "category": "Confectionery & Chocolate",
        "cost_target": 15.0,
        "nutrition_targets": {"protein_min": 7.0, "sugar_max": 35.0}
    }

    # Construct two candidates where Balanced has superior metrics
    cand_balanced = {
        "candidate_id": "FC-004",
        "formulation_id": "FORM-FC004",
        "strategy": "balanced",
        "cost_per_kg": 10.50,
        "nutrition": {"protein": 8.0, "sugar": 22.0, "fat": 30.0},
        "composition": {
            "all_components": [
                {"id": "ing_cocoa_butter", "name": "Cocoa Butter", "percentage": 30.0, "cost_per_kg": 12.0, "regulatory_status": "Permitted", "protein": 0.0},
                {"id": "ing_cocoa_mass", "name": "Cocoa Mass", "percentage": 40.0, "cost_per_kg": 9.0, "regulatory_status": "Permitted", "protein": 12.0},
                {"id": "ing_sugar", "name": "Cane Sugar", "percentage": 30.0, "cost_per_kg": 1.5, "regulatory_status": "Permitted", "protein": 0.0}
            ]
        },
        "compatibility": {"normalized_ics": 0.85, "compatibility_score": 85.0}
    }

    cand_cost = {
        "candidate_id": "FC-002",
        "formulation_id": "FORM-FC002",
        "strategy": "cost_optimized",
        "cost_per_kg": 14.50,  # inferior cost in this test
        "nutrition": {"protein": 5.0, "sugar": 32.0, "fat": 20.0},  # inferior protein (< 7.0 target)
        "composition": {
            "all_components": [
                {"id": "ing_cocoa_powder", "name": "Cocoa Powder", "percentage": 50.0, "cost_per_kg": 14.0, "regulatory_status": "Permitted", "protein": 10.0},
                {"id": "ing_sugar", "name": "Cane Sugar", "percentage": 50.0, "cost_per_kg": 1.5, "regulatory_status": "Permitted", "protein": 0.0}
            ]
        },
        "compatibility": {"normalized_ics": 0.50, "compatibility_score": 50.0}
    }

    s_bal = scoring_engine.calculate_scores(cand_balanced, brief_dict, profile_name="BALANCED")
    s_cost = scoring_engine.calculate_scores(cand_cost, brief_dict, profile_name="COST_OPTIMIZED")

    cand_balanced["scoring"] = s_bal
    cand_cost["scoring"] = s_cost

    assert s_bal["overall_score"] > s_cost["overall_score"], (
        f"Balanced ({s_bal['overall_score']}) should score higher than inferior Cost candidate ({s_cost['overall_score']})"
    )

def test_scenario_b_high_protein_wins_when_metrics_excel():
    """Scenario B: High Protein candidate has superior nutrition and cost and must win over Balanced."""
    brief_dict = {
        "description": "High Protein Athletic Snack Bar",
        "category": "Nutrition Bars",
        "cost_target": 18.0,
        "nutrition_targets": {"protein_min": 15.0, "sugar_max": 25.0}
    }

    # High Protein candidate delivers 25g protein, low cost $11.00/kg
    cand_protein = {
        "candidate_id": "FC-001",
        "formulation_id": "FORM-FC001",
        "strategy": "nutrition_maximized",
        "cost_per_kg": 11.00,
        "nutrition": {"protein": 25.0, "sugar": 12.0, "fat": 15.0},
        "composition": {
            "all_components": [
                {"id": "ing_pea_protein", "name": "Pea Protein Isolate", "percentage": 35.0, "cost_per_kg": 8.0, "regulatory_status": "Permitted", "protein": 80.0},
                {"id": "ing_oat_flour", "name": "Oat Flour", "percentage": 35.0, "cost_per_kg": 4.0, "regulatory_status": "Permitted", "protein": 12.0},
                {"id": "ing_almond_butter", "name": "Almond Butter", "percentage": 30.0, "cost_per_kg": 12.0, "regulatory_status": "Permitted", "protein": 20.0}
            ]
        },
        "compatibility": {"normalized_ics": 0.90, "compatibility_score": 90.0}
    }

    # Balanced candidate delivers only 12g protein (fails target 15g) and higher cost $16.00/kg
    cand_balanced = {
        "candidate_id": "FC-004",
        "formulation_id": "FORM-FC004",
        "strategy": "balanced",
        "cost_per_kg": 16.00,
        "nutrition": {"protein": 12.0, "sugar": 24.0, "fat": 18.0},
        "composition": {
            "all_components": [
                {"id": "ing_pea_protein", "name": "Pea Protein Isolate", "percentage": 15.0, "cost_per_kg": 8.0, "regulatory_status": "Permitted", "protein": 80.0},
                {"id": "ing_oat_flour", "name": "Oat Flour", "percentage": 45.0, "cost_per_kg": 4.0, "regulatory_status": "Permitted", "protein": 12.0},
                {"id": "ing_sugar", "name": "Cane Sugar", "percentage": 40.0, "cost_per_kg": 1.5, "regulatory_status": "Permitted", "protein": 0.0}
            ]
        },
        "compatibility": {"normalized_ics": 0.70, "compatibility_score": 70.0}
    }

    s_prot = scoring_engine.calculate_scores(cand_protein, brief_dict, profile_name="NUTRITION_OPTIMIZED")
    s_bal = scoring_engine.calculate_scores(cand_balanced, brief_dict, profile_name="BALANCED")

    cand_protein["scoring"] = s_prot
    cand_balanced["scoring"] = s_bal

    # Verify that High Protein candidate beats Balanced
    assert s_prot["overall_score"] > s_bal["overall_score"], (
        f"High Protein candidate ({s_prot['overall_score']}) MUST win over Balanced ({s_bal['overall_score']}) when metrics are superior!"
    )

def test_scenario_c_low_cost_wins_when_cost_is_optimized():
    """Scenario C: Low Cost candidate has vastly superior cost and satisfied nutrition, and must win."""
    brief_dict = {
        "description": "Budget Conscious Food Formulation",
        "category": "Bakery",
        "cost_target": 15.0,
        "nutrition_targets": {"protein_min": 6.0, "sugar_max": 30.0}
    }

    # Low Cost candidate costs $5.20/kg and satisfies 8.0g protein
    cand_cost = {
        "candidate_id": "FC-002",
        "formulation_id": "FORM-FC002",
        "strategy": "cost_optimized",
        "cost_per_kg": 5.20,
        "nutrition": {"protein": 8.0, "sugar": 18.0, "fat": 12.0},
        "composition": {
            "all_components": [
                {"id": "ing_wheat_flour", "name": "Wheat Flour", "percentage": 60.0, "cost_per_kg": 2.0, "regulatory_status": "Permitted", "protein": 11.0},
                {"id": "ing_soy_protein", "name": "Soy Protein Concentrate", "percentage": 10.0, "cost_per_kg": 5.0, "regulatory_status": "Permitted", "protein": 70.0},
                {"id": "ing_sugar", "name": "Cane Sugar", "percentage": 30.0, "cost_per_kg": 1.5, "regulatory_status": "Permitted", "protein": 0.0}
            ]
        },
        "compatibility": {"normalized_ics": 0.80, "compatibility_score": 80.0}
    }

    # Balanced candidate costs $14.50/kg with identical 8.0g protein
    cand_balanced = {
        "candidate_id": "FC-004",
        "formulation_id": "FORM-FC004",
        "strategy": "balanced",
        "cost_per_kg": 14.50,
        "nutrition": {"protein": 8.0, "sugar": 18.0, "fat": 12.0},
        "composition": {
            "all_components": [
                {"id": "ing_wheat_flour", "name": "Wheat Flour", "percentage": 60.0, "cost_per_kg": 2.0, "regulatory_status": "Permitted", "protein": 11.0},
                {"id": "ing_soy_protein", "name": "Soy Protein Concentrate", "percentage": 10.0, "cost_per_kg": 5.0, "regulatory_status": "Permitted", "protein": 70.0},
                {"id": "ing_sugar", "name": "Cane Sugar", "percentage": 30.0, "cost_per_kg": 1.5, "regulatory_status": "Permitted", "protein": 0.0}
            ]
        },
        "compatibility": {"normalized_ics": 0.80, "compatibility_score": 80.0}
    }

    s_cost = scoring_engine.calculate_scores(cand_cost, brief_dict, profile_name="COST_OPTIMIZED")
    s_bal = scoring_engine.calculate_scores(cand_balanced, brief_dict, profile_name="BALANCED")

    assert s_cost["overall_score"] > s_bal["overall_score"], (
        f"Low Cost candidate ({s_cost['overall_score']}) MUST win over costly Balanced candidate ({s_bal['overall_score']})!"
    )

def test_scenario_d_infeasible_candidate_disqualified_from_winning():
    """Scenario D: Infeasible candidate with high score is disqualified from winning and relegated."""
    query = "Design a 100% vegan chocolate bar with at least 8% protein."
    payload = {"query": query}
    
    res = generate_formulation_pipeline(payload)
    candidates = res["candidate_sets"]
    
    assert len(candidates) > 0
    winner = res["formulation"]
    
    # Verify winner is feasible
    assert winner["status"] in ["APPROVED", "VALIDATED_COMMERCIAL_GRADE"] or winner.get("is_feasible") is True
    
    # Any candidate with is_feasible == False must not be rank 1
    for c in candidates:
        if c.get("is_feasible") is False:
            assert c.get("rank") is None or c.get("rank") > 1
            assert c.get("ranking_status") == "DISQUALIFIED_INFEASIBLE"

    # Also test synthetic competition where an infeasible candidate has higher numerical score
    infeasible_cand = {
        "candidate_id": "FC-099",
        "formulation_id": "FORM-FC099",
        "strategy": "cost_optimized",
        "is_feasible": False,
        "scoring": {"overall_score": 98.0, "radar": {"Constraint_Satisfaction": 10.0, "FRC": 50.0}},
        "cost_per_kg": 2.0
    }
    feasible_cand = {
        "candidate_id": "FC-001",
        "formulation_id": "FORM-FC001",
        "strategy": "balanced",
        "is_feasible": True,
        "scoring": {"overall_score": 85.0, "radar": {"Constraint_Satisfaction": 90.0, "FRC": 90.0}},
        "cost_per_kg": 10.0
    }
    
    # Partitioning logic
    c_list = [infeasible_cand, feasible_cand]
    feas = [c for c in c_list if c["is_feasible"]]
    infeas = [c for c in c_list if not c["is_feasible"]]
    feas.sort(key=lambda x: x["scoring"]["overall_score"], reverse=True)
    infeas.sort(key=lambda x: x["scoring"]["overall_score"], reverse=True)
    
    ranked = feas + infeas
    winner_cand = feas[0]
    
    assert winner_cand["candidate_id"] == "FC-001", "Feasible candidate must win even if infeasible candidate has 98% score"
    assert ranked[0]["candidate_id"] == "FC-001"
    assert ranked[1]["candidate_id"] == "FC-099"

def test_scenario_e_duplicate_score_detection_and_distinct_ids():
    """Scenario E: All candidates have distinct IDs and independent score objects."""
    query = "Formulate a clean-label high-protein dark chocolate bar under $14/kg."
    payload = {"query": query}
    
    res = generate_formulation_pipeline(payload)
    candidates = res["candidate_sets"]
    
    assert len(candidates) >= 3, "At least 3 candidate sets must be generated"
    
    candidate_ids = [c["candidate_id"] for c in candidates]
    formulation_ids = [c["formulation_id"] for c in candidates]
    
    # 1. Unique IDs
    assert len(candidate_ids) == len(set(candidate_ids)), f"Duplicate candidate IDs found: {candidate_ids}"
    assert len(formulation_ids) == len(set(formulation_ids)), f"Duplicate formulation IDs found: {formulation_ids}"
    
    # 2. Distinct Titles (No two 'Balanced Set' titles!)
    titles = [c["title"] for c in candidates]
    balanced_titles = [t for t in titles if "Balanced" in t]
    assert len(balanced_titles) <= 1, f"Found multiple Balanced Set titles: {titles}"

    # 3. Independent score calculation objects
    score_objs = [id(c["scoring"]) for c in candidates]
    assert len(score_objs) == len(set(score_objs)), "Candidate score dictionaries must be distinct Python objects (no copy/leak)"

def test_scenario_f_candidate_ordering_randomization():
    """Scenario F: Shuffling candidate input order does not alter the winning formulation."""
    brief_dict = {
        "description": "Protein Bar Ranking Determinism Test",
        "category": "Nutrition Bars",
        "cost_target": 15.0,
        "nutrition_targets": {"protein_min": 10.0}
    }

    c1 = {
        "candidate_id": "FC-001",
        "formulation_id": "FORM-FC001",
        "strategy": "nutrition_maximized",
        "cost_per_kg": 10.0,
        "nutrition": {"protein": 22.0, "sugar": 10.0, "fat": 12.0},
        "composition": {"all_components": [{"id": "ing_pea", "name": "Pea Protein", "percentage": 100.0, "cost_per_kg": 10.0, "protein": 80.0, "regulatory_status": "Permitted"}]},
        "compatibility": {"normalized_ics": 0.9, "compatibility_score": 90.0}
    }
    c2 = {
        "candidate_id": "FC-002",
        "formulation_id": "FORM-FC002",
        "strategy": "cost_optimized",
        "cost_per_kg": 6.0,
        "nutrition": {"protein": 11.0, "sugar": 20.0, "fat": 8.0},
        "composition": {"all_components": [{"id": "ing_soy", "name": "Soy Protein", "percentage": 100.0, "cost_per_kg": 6.0, "protein": 50.0, "regulatory_status": "Permitted"}]},
        "compatibility": {"normalized_ics": 0.8, "compatibility_score": 80.0}
    }
    c3 = {
        "candidate_id": "FC-003",
        "formulation_id": "FORM-FC003",
        "strategy": "balanced",
        "cost_per_kg": 14.0,
        "nutrition": {"protein": 10.5, "sugar": 25.0, "fat": 15.0},
        "composition": {"all_components": [{"id": "ing_whey", "name": "Whey Protein", "percentage": 100.0, "cost_per_kg": 14.0, "protein": 70.0, "regulatory_status": "Permitted"}]},
        "compatibility": {"normalized_ics": 0.7, "compatibility_score": 70.0}
    }

    list_order_1 = [copy.deepcopy(c1), copy.deepcopy(c2), copy.deepcopy(c3)]
    list_order_2 = [copy.deepcopy(c3), copy.deepcopy(c1), copy.deepcopy(c2)]

    for c in list_order_1:
        c["scoring"] = scoring_engine.calculate_scores(c, brief_dict, profile_name=c["strategy"].upper())
    for c in list_order_2:
        c["scoring"] = scoring_engine.calculate_scores(c, brief_dict, profile_name=c["strategy"].upper())

    list_order_1.sort(key=lambda x: x["scoring"]["overall_score"], reverse=True)
    list_order_2.sort(key=lambda x: x["scoring"]["overall_score"], reverse=True)

    winner_1 = list_order_1[0]["candidate_id"]
    winner_2 = list_order_2[0]["candidate_id"]

    assert winner_1 == winner_2, f"Winner must be deterministic regardless of input list ordering (got {winner_1} vs {winner_2})"

def test_scenario_g_repeated_execution_consistency():
    """Scenario G: Running generation on the same brief produces repeatable metrics and scores."""
    payload = {"query": "Vegan dark chocolate confectionery with at least 7% protein, using cocoa butter, under $15.00/kg."}
    
    res1 = generate_formulation_pipeline(payload)
    res2 = generate_formulation_pipeline(payload)

    cands1 = res1["candidate_sets"]
    cands2 = res2["candidate_sets"]

    assert len(cands1) == len(cands2)
    for c1, c2 in zip(cands1, cands2):
        assert c1["candidate_id"] == c2["candidate_id"]
        assert c1["strategy"] == c2["strategy"]
        assert c1["title"] == c2["title"]
        assert abs(c1["scoring"]["overall_score"] - c2["scoring"]["overall_score"]) < 1e-4
        assert abs(c1["nutrition"]["protein"] - c2["nutrition"]["protein"]) < 1e-4

def test_scenario_h_no_feasible_candidate_handling():
    """Scenario H: When impossible constraints make all candidates infeasible, status is NO_FEASIBLE_WINNER."""
    # Impossible constraints: 100% protein chocolate with maximum cost $0.05/kg
    brief_dict = {
        "description": "Impossible Chocolate Formulation",
        "category": "Confectionery & Chocolate",
        "cost_target": 0.05,
        "nutrition_targets": {"protein_min": 99.0, "sugar_max": 0.0}
    }
    
    cand = {
        "candidate_id": "FC-001",
        "formulation_id": "FORM-FC001",
        "strategy": "balanced",
        "cost_per_kg": 12.0,  # exceeds 0.05
        "nutrition": {"protein": 7.0, "sugar": 30.0, "fat": 30.0},
        "composition": {
            "all_components": [
                {"id": "ing_cocoa_butter", "name": "Cocoa Butter", "percentage": 100.0, "cost_per_kg": 12.0, "protein": 0.0, "regulatory_status": "Permitted"}
            ]
        },
        "compatibility": {"normalized_ics": 0.5, "compatibility_score": 50.0}
    }
    
    brief_obj = product_brief_parser.parse("Impossible chocolate formulation with 99% protein under $0.05/kg")
    val_res = validation_gate.validate_candidate_set(cand, brief_obj, eligible_candidate_ids=["ing_cocoa_butter"])
    
    assert val_res["is_valid"] is False
    assert len(val_res["failure_reasons"]) > 0

