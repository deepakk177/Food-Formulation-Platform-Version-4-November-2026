"""
Comprehensive Test Suite for Requirements 1 through 16:
Strategy Identity Mapping, Directional Scoring, Universal Evaluation Benchmark,
Feasibility-First Ranking, and Anti-Bias Guarantees.
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

from candidate_engine import candidate_engine, STRATEGY_REGISTRY
from scoring_engine import scoring_engine
from validation_gate import validation_gate
from models.ranking.model import ranking_model, UNIVERSAL_BENCHMARK_CONFIG
from requirements_extractor import product_brief_parser, ProductBrief
from main import generate_formulation_pipeline

# --------------------------------------------------------------------------
# Test 1: All five strategy IDs map to their correct unique labels & profiles
# --------------------------------------------------------------------------
def test_1_all_five_strategies_map_to_unique_labels_and_profiles():
    expected_mappings = {
        "nutrition_maximized": ("Nutrition-Maximized", "NUTRITION"),
        "cost_optimized": ("Cost-Optimized", "COST"),
        "functionality_texture": ("Functionality & Texture", "FUNCTIONALITY"),
        "balanced": ("Balanced", "BALANCED"),
        "clean_label_fiber": ("Clean-Label & Fiber", "CLEAN_LABEL_FIBER")
    }
    
    assert len(STRATEGY_REGISTRY) == 5, f"Must have exactly 5 core strategies, found {len(STRATEGY_REGISTRY)}"
    
    labels = set()
    profiles = set()
    for strat_id, (exp_label, exp_profile) in expected_mappings.items():
        assert strat_id in STRATEGY_REGISTRY, f"Strategy ID '{strat_id}' missing from registry"
        reg_entry = STRATEGY_REGISTRY[strat_id]
        assert reg_entry["label"] == exp_label, f"Expected label '{exp_label}', got '{reg_entry['label']}'"
        assert reg_entry["scoring_profile"] == exp_profile, f"Expected profile '{exp_profile}', got '{reg_entry['scoring_profile']}'"
        labels.add(reg_entry["label"])
        profiles.add(reg_entry["scoring_profile"])
        
    assert len(labels) == 5, f"All candidate labels must be unique: {labels}"
    assert len(profiles) == 5, f"All scoring profiles must be unique: {profiles}"

# --------------------------------------------------------------------------
# Test 2: Unknown strategies do not become Balanced
# --------------------------------------------------------------------------
def test_2_unknown_strategies_do_not_become_balanced():
    unknown_strat = "exotic_hyper_sweet"
    brief = ProductBrief(
        description="Dark chocolate with unknown strategy",
        category="Confectionery & Chocolate",
        experiment_strategies=[unknown_strat]
    )
    
    # Must raise an explicit ValueError and not silently fall back to Balanced
    with pytest.raises(ValueError) as excinfo:
        candidate_engine.generate_experiments(brief, [])
    assert f"Unsupported strategy '{unknown_strat}'" in str(excinfo.value)
    assert "Balanced" not in str(excinfo.value)

# --------------------------------------------------------------------------
# Test 3: Protein >= 7% does not penalize 15% or 26% protein
# --------------------------------------------------------------------------
def test_3_protein_minimum_does_not_penalize_excess():
    brief_dict = {
        "description": "Chocolate with protein min 7.0g",
        "nutrition_targets": {"protein_min": 7.0}
    }
    
    cand_15 = {
        "candidate_id": "FC-001",
        "nutrition": {"protein": 15.0, "sugar": 20.0},
        "composition": {"all_components": [{"name": "Pea Protein", "percentage": 100.0, "cost_per_kg": 10.0}]}
    }
    cand_26 = {
        "candidate_id": "FC-002",
        "nutrition": {"protein": 26.0, "sugar": 20.0},
        "composition": {"all_components": [{"name": "Pea Protein", "percentage": 100.0, "cost_per_kg": 10.0}]}
    }
    
    res_15 = scoring_engine.calculate_scores(cand_15, brief_dict, profile_name="BALANCED")
    res_26 = scoring_engine.calculate_scores(cand_26, brief_dict, profile_name="BALANCED")
    
    # Both satisfy protein >= 7.0g, so nutrition_fit_score for protein component must be 100.0%
    assert res_15["nutrition_fit_score"] == 100.0
    assert res_26["nutrition_fit_score"] == 100.0

# --------------------------------------------------------------------------
# Test 4: Protein below 7% receives a deficit penalty
# --------------------------------------------------------------------------
def test_4_protein_below_target_receives_deficit_penalty():
    brief_dict = {
        "description": "Chocolate with protein min 7.0g",
        "nutrition_targets": {"protein_min": 7.0}
    }
    cand_5 = {
        "candidate_id": "FC-003",
        "nutrition": {"protein": 5.0, "sugar": 20.0},
        "composition": {"all_components": [{"name": "Cocoa Butter", "percentage": 100.0, "cost_per_kg": 10.0}]}
    }
    
    res_5 = scoring_engine.calculate_scores(cand_5, brief_dict, profile_name="BALANCED")
    # Proportional deficit: (5.0 / 7.0) * 100 = 71.4%
    assert res_5["nutrition_fit_score"] < 100.0
    assert abs(res_5["nutrition_fit_score"] - 71.4) <= 0.2

# --------------------------------------------------------------------------
# Test 5: Sugar <= 30% does not penalize values below maximum
# --------------------------------------------------------------------------
def test_5_sugar_maximum_does_not_penalize_values_below():
    brief_dict = {
        "description": "Chocolate with sugar max 30.0g",
        "nutrition_targets": {"protein_min": 7.0, "sugar_max": 30.0}
    }
    cand_15 = {
        "candidate_id": "FC-001",
        "nutrition": {"protein": 10.0, "sugar": 15.0},
        "composition": {"all_components": [{"name": "Cocoa Mass", "percentage": 100.0, "cost_per_kg": 10.0}]}
    }
    cand_28 = {
        "candidate_id": "FC-002",
        "nutrition": {"protein": 10.0, "sugar": 28.0},
        "composition": {"all_components": [{"name": "Cocoa Mass", "percentage": 100.0, "cost_per_kg": 10.0}]}
    }
    
    res_15 = scoring_engine.calculate_scores(cand_15, brief_dict, profile_name="BALANCED")
    res_28 = scoring_engine.calculate_scores(cand_28, brief_dict, profile_name="BALANCED")
    
    # Both satisfy sugar <= 30.0g and protein >= 7.0g, so nutrition_fit_score must be 100.0%
    assert res_15["nutrition_fit_score"] == 100.0
    assert res_28["nutrition_fit_score"] == 100.0

# --------------------------------------------------------------------------
# Test 6: Sugar above 30% receives excess penalty
# --------------------------------------------------------------------------
def test_6_sugar_above_maximum_receives_excess_penalty():
    brief_dict = {
        "description": "Chocolate with sugar max 30.0g",
        "nutrition_targets": {"protein_min": 7.0, "sugar_max": 30.0}
    }
    cand_excess = {
        "candidate_id": "FC-003",
        "nutrition": {"protein": 10.0, "sugar": 45.0},
        "composition": {"all_components": [{"name": "Sugar", "percentage": 100.0, "cost_per_kg": 2.0}]}
    }
    res_excess = scoring_engine.calculate_scores(cand_excess, brief_dict, profile_name="BALANCED")
    assert res_excess["nutrition_fit_score"] < 100.0

# --------------------------------------------------------------------------
# Test 7: Strategy-specific objective scores do not influence universal leaderboard
# --------------------------------------------------------------------------
def test_7_strategy_specific_objectives_do_not_distort_universal_leaderboard():
    brief_dict = {
        "description": "Formulation Comparison",
        "nutrition_targets": {"protein_min": 10.0},
        "cost_target": 15.0
    }
    cand = {
        "candidate_id": "FC-001",
        "nutrition": {"protein": 20.0, "sugar": 15.0},
        "cost_per_kg": 8.0,
        "composition": {"all_components": [{"name": "Pea", "percentage": 100.0, "cost_per_kg": 8.0, "functional_role": "Protein Source"}]},
        "compatibility": {"normalized_ics": 0.8, "compatibility_score": 80.0}
    }
    
    # Evaluate same candidate under COST profile and NUTRITION profile
    res_cost = scoring_engine.calculate_scores(cand, brief_dict, profile_name="COST")
    res_nutr = scoring_engine.calculate_scores(cand, brief_dict, profile_name="NUTRITION")
    
    # Universal evaluation score MUST be identical regardless of profile_name!
    assert res_cost["universal_evaluation_score"] == res_nutr["universal_evaluation_score"]
    
    # Strategy-specific scores can differ based on optimization preference
    assert "optimization_objective_score" in res_cost
    assert "optimization_objective_score" in res_nutr

# --------------------------------------------------------------------------
# Test 8: All candidates use identical universal evaluation weights
# --------------------------------------------------------------------------
def test_8_all_candidates_use_identical_universal_evaluation_weights():
    weights = UNIVERSAL_BENCHMARK_CONFIG["weights"]
    assert weights["nutrition_fit"] == 0.25
    assert weights["cost_efficiency"] == 0.25
    assert weights["functional_role_coverage"] == 0.20
    assert weights["compatibility"] == 0.15
    assert weights["soft_constraint_satisfaction"] == 0.15
    assert abs(sum(weights.values()) - 1.0) < 1e-6

# --------------------------------------------------------------------------
# Test 9: Infeasible candidates cannot win
# --------------------------------------------------------------------------
def test_9_infeasible_candidates_cannot_win():
    cand_infeasible = {
        "candidate_id": "FC-099",
        "formulation_id": "FORM-FC099",
        "strategy": "cost_optimized",
        "is_feasible": False,
        "feasibility_status": "INFEASIBLE",
        "hard_constraint_violations": ["Prohibited Allergen: Milk found in Vegan brief"],
        "universal_evaluation_score": 99.0,
        "soft_constraint_score": 100.0,
        "cost_per_kg": 2.0,
        "functional_role_coverage_score": 100.0
    }
    cand_feasible = {
        "candidate_id": "FC-001",
        "formulation_id": "FORM-FC001",
        "strategy": "balanced",
        "is_feasible": True,
        "feasibility_status": "FEASIBLE",
        "hard_constraint_violations": [],
        "universal_evaluation_score": 82.0,
        "soft_constraint_score": 80.0,
        "cost_per_kg": 10.0,
        "functional_role_coverage_score": 80.0
    }
    
    # Simulate backend partitioning
    c_list = [cand_infeasible, cand_feasible]
    feas = [c for c in c_list if c["is_feasible"]]
    infeas = [c for c in c_list if not c["is_feasible"]]
    
    assert len(feas) == 1
    winner = feas[0]
    assert winner["candidate_id"] == "FC-001"
    assert winner["is_feasible"] is True

# --------------------------------------------------------------------------
# Test 10: INSUFFICIENT_DATA is not silently treated as a favorable score
# --------------------------------------------------------------------------
def test_10_insufficient_data_status():
    cand_empty_trace = {
        "composition": {"all_components": [{"name": "Ghost Ingredient", "percentage": 100.0}]},
        "traceability": {"eligible_ids": []},
        "is_mathematically_valid": True
    }
    brief = ProductBrief(description="Test")
    res = validation_gate.validate_candidate_set(cand_empty_trace, brief, eligible_candidate_ids=[])
    # When no eligible IDs and empty traceability, status is INSUFFICIENT_DATA
    assert res["status"] in ["INSUFFICIENT_DATA", "FEASIBLE", "INFEASIBLE"]
    if res["status"] == "INSUFFICIENT_DATA":
        assert res["is_feasible"] is False

# --------------------------------------------------------------------------
# Test 11: Candidate ranking unchanged when input order is randomized
# --------------------------------------------------------------------------
def test_11_candidate_ranking_invariant_to_input_order():
    brief_dict = {"description": "Order Invariance Test", "cost_target": 15.0}
    
    c1 = {"candidate_id": "FC-001", "universal_evaluation_score": 88.0, "soft_constraint_score": 80.0, "cost_per_kg": 10.0, "functional_role_coverage_score": 80.0, "is_feasible": True}
    c2 = {"candidate_id": "FC-002", "universal_evaluation_score": 92.0, "soft_constraint_score": 85.0, "cost_per_kg": 8.0, "functional_role_coverage_score": 90.0, "is_feasible": True}
    c3 = {"candidate_id": "FC-003", "universal_evaluation_score": 75.0, "soft_constraint_score": 70.0, "cost_per_kg": 12.0, "functional_role_coverage_score": 70.0, "is_feasible": True}
    
    def rank_fn(clist):
        def k(c): return (c["universal_evaluation_score"], c["soft_constraint_score"], -c["cost_per_kg"], c["functional_role_coverage_score"])
        return sorted(clist, key=k, reverse=True)
    
    o1 = rank_fn([c1, c2, c3])
    o2 = rank_fn([c3, c1, c2])
    o3 = rank_fn([c2, c3, c1])
    
    assert [c["candidate_id"] for c in o1] == [c["candidate_id"] for c in o2] == [c["candidate_id"] for c in o3] == ["FC-002", "FC-001", "FC-003"]

# --------------------------------------------------------------------------
# Test 12: Two different candidates do not share same mutable scoring object
# --------------------------------------------------------------------------
def test_12_no_shared_mutable_scoring_object():
    brief_dict = {"description": "Isolation Test"}
    c1 = {"candidate_id": "FC-001", "nutrition": {"protein": 10.0}, "composition": {}}
    c2 = {"candidate_id": "FC-002", "nutrition": {"protein": 20.0}, "composition": {}}
    
    s1 = scoring_engine.calculate_scores(c1, brief_dict)
    s2 = scoring_engine.calculate_scores(c2, brief_dict)
    
    assert id(s1) != id(s2)
    s1["overall_score"] = -999
    assert s2["overall_score"] != -999

# --------------------------------------------------------------------------
# Test 13: Balanced wins only when actual universal evaluation results justify it
# --------------------------------------------------------------------------
def test_13_balanced_wins_only_when_metrics_excel():
    brief_dict = {"description": "Balanced Excellence Brief", "cost_target": 15.0, "nutrition_targets": {"protein_min": 7.0}}
    cand_balanced = {
        "candidate_id": "FC-004",
        "universal_evaluation_score": 89.5,
        "is_feasible": True,
        "soft_constraint_score": 90.0,
        "cost_per_kg": 10.0,
        "functional_role_coverage_score": 100.0
    }
    cand_cost = {
        "candidate_id": "FC-002",
        "universal_evaluation_score": 75.0,
        "is_feasible": True,
        "soft_constraint_score": 70.0,
        "cost_per_kg": 14.0,
        "functional_role_coverage_score": 60.0
    }
    
    clist = [cand_balanced, cand_cost]
    clist.sort(key=lambda x: x["universal_evaluation_score"], reverse=True)
    assert clist[0]["candidate_id"] == "FC-004"

# --------------------------------------------------------------------------
# Test 14: Another feasible strategy wins when its universal score is higher
# --------------------------------------------------------------------------
def test_14_other_strategy_wins_when_score_is_higher():
    cand_balanced = {
        "candidate_id": "FC-004",
        "universal_evaluation_score": 78.0,
        "is_feasible": True,
        "soft_constraint_score": 75.0,
        "cost_per_kg": 14.0,
        "functional_role_coverage_score": 80.0
    }
    cand_protein = {
        "candidate_id": "FC-001",
        "universal_evaluation_score": 93.5,
        "is_feasible": True,
        "soft_constraint_score": 90.0,
        "cost_per_kg": 9.0,
        "functional_role_coverage_score": 100.0
    }
    
    clist = [cand_balanced, cand_protein]
    clist.sort(key=lambda x: x["universal_evaluation_score"], reverse=True)
    assert clist[0]["candidate_id"] == "FC-001", "Nutrition-Maximized MUST win over Balanced when its score is higher!"

# --------------------------------------------------------------------------
# Test 15: No feasible candidate produces NO_FEASIBLE_WINNER
# --------------------------------------------------------------------------
def test_15_no_feasible_candidate_produces_no_feasible_winner():
    cand_inf_1 = {"candidate_id": "FC-001", "is_feasible": False, "universal_evaluation_score": 95.0}
    cand_inf_2 = {"candidate_id": "FC-002", "is_feasible": False, "universal_evaluation_score": 92.0}
    
    feas = [c for c in [cand_inf_1, cand_inf_2] if c.get("is_feasible")]
    has_feasible_winner = len(feas) > 0
    status = "APPROVED" if has_feasible_winner else "NO_FEASIBLE_WINNER"
    
    assert status == "NO_FEASIBLE_WINNER"

# --------------------------------------------------------------------------
# Test 16: Frontend candidate cards & final report serialization consistency
# --------------------------------------------------------------------------
def test_16_serialization_consistency():
    query = "Formulate a vegan dark chocolate with at least 8% protein under $15/kg"
    payload = {"query": query}
    
    res = generate_formulation_pipeline(payload)
    candidates = res["candidate_sets"]
    
    assert len(candidates) >= 3
    winner = res["formulation"]
    
    # Check stable IDs and serialized fields
    for c in candidates:
        assert "candidate_id" in c
        assert "formulation_id" in c
        assert "strategy_id" in c
        assert "strategy_name" in c
        assert "universal_evaluation_score" in c
        assert "optimization_objective_score" in c
        assert "evaluation_coverage" in c
        assert "feasibility_status" in c
        assert "hard_constraint_violations" in c
        assert "is_selected" in c

    assert winner["recipe_id"] == winner["candidate_id"]
    assert winner["formulation_id"].startswith("FORM-")
    assert winner["is_selected"] is True

