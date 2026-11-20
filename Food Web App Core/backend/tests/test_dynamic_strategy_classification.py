"""
Unit and Integration Tests for Dynamic Candidate Set Strategy Classification
and Cost Consistency (Parts 1-5).
"""
import pytest
from strategy_classifier import dynamic_strategy_classifier, STRATEGY_LABELS
from candidate_engine import candidate_engine
from requirements_extractor import product_brief_parser

def test_dynamic_classification_screenshot_example():
    """
    Validates Part 6 Example:
    Candidate | Protein | Calories | Minerals | Cost/kg
    Set A | 45 g | 432 | 696 mg | $13.06
    Set B | 38 g | 313 | 618 mg | $8.51
    Set C | 48.9 g | 315 | 783 mg | $10.86
    Set D | 7.2 g | 269 | 588 mg | $8.96
    """
    candidates = [
        {
            "candidate_id": "FC-001",
            "is_feasible": True,
            "cost_per_kg": 13.06,
            "cost_status": "KNOWN",
            "nutrition": {"protein": 45.0, "calories": 432, "key_minerals_mg": 696, "fibre": 2.0, "sugar": 15.0},
            "scoring": {"overall_score": 83.2, "radar": {"Nutrition": 85.0, "Compatibility": 88.0, "FRC": 85.0, "Constraint_Satisfaction": 80.0}},
            "composition": {"all_components": [{"name": "Soy Lecithin", "functional_role": "Emulsifier", "percentage": 1.5}]}
        },
        {
            "candidate_id": "FC-002",
            "is_feasible": True,
            "cost_per_kg": 8.51,
            "cost_status": "KNOWN",
            "nutrition": {"protein": 38.0, "calories": 313, "key_minerals_mg": 618, "fibre": 1.5, "sugar": 18.0},
            "scoring": {"overall_score": 90.4, "radar": {"Nutrition": 75.0, "Compatibility": 78.0, "FRC": 70.0, "Constraint_Satisfaction": 85.0}},
            "composition": {"all_components": [{"name": "Sugar", "functional_role": "Sweetener", "percentage": 25.0}]}
        },
        {
            "candidate_id": "FC-003",
            "is_feasible": True,
            "cost_per_kg": 10.86,
            "cost_status": "KNOWN",
            "nutrition": {"protein": 48.9, "calories": 315, "key_minerals_mg": 783, "fibre": 3.0, "sugar": 10.0},
            "scoring": {"overall_score": 83.8, "radar": {"Nutrition": 95.0, "Compatibility": 80.0, "FRC": 75.0, "Constraint_Satisfaction": 85.0}},
            "composition": {"all_components": [{"name": "Soy Protein Isolate", "functional_role": "Protein Source", "percentage": 50.0}]}
        },
        {
            "candidate_id": "FC-004",
            "is_feasible": True,
            "cost_per_kg": 8.96,
            "cost_status": "KNOWN",
            "nutrition": {"protein": 7.2, "calories": 269, "key_minerals_mg": 588, "fibre": 4.0, "sugar": 8.0},
            "scoring": {"overall_score": 83.8, "radar": {"Nutrition": 70.0, "Compatibility": 82.0, "FRC": 80.0, "Constraint_Satisfaction": 80.0}},
            "composition": {"all_components": [{"name": "Oat Flour", "functional_role": "Base Raw Material", "percentage": 30.0}]}
        }
    ]

    classified = dynamic_strategy_classifier.classify_candidates(candidates)

    by_id = {c["candidate_id"]: c["strategy_label"] for c in classified}
    
    # FC-002 has lowest cost -> MUST be Cost Optimized
    assert by_id["FC-002"] == "Cost Optimized"

    # FC-003 has highest protein & minerals -> MUST be Nutrition Maximized
    assert by_id["FC-003"] == "Nutrition Maximized"

    # FC-001 has high functional texturizers -> Functionality & Flavor
    assert by_id["FC-001"] == "Functionality & Flavor"

    # FC-004 has balanced macros -> Balanced Set
    assert by_id["FC-004"] == "Balanced Set"

def test_dynamic_shift_across_runs():
    """
    Verifies that Candidate IDs are NOT hardcoded to strategies.
    If FC-001 is cheapest in Run 2, it receives Cost Optimized.
    """
    candidates = [
        {
            "candidate_id": "FC-001",
            "is_feasible": True,
            "cost_per_kg": 3.50,
            "cost_status": "KNOWN",
            "nutrition": {"protein": 15.0, "calories": 250, "key_minerals_mg": 400, "fibre": 2.0, "sugar": 10.0},
            "scoring": {"overall_score": 80.0, "radar": {"Nutrition": 60.0, "Compatibility": 75.0, "FRC": 70.0, "Constraint_Satisfaction": 80.0}},
            "composition": {"all_components": []}
        },
        {
            "candidate_id": "FC-002",
            "is_feasible": True,
            "cost_per_kg": 15.00,
            "cost_status": "KNOWN",
            "nutrition": {"protein": 60.0, "calories": 380, "key_minerals_mg": 900, "fibre": 6.0, "sugar": 2.0},
            "scoring": {"overall_score": 88.0, "radar": {"Nutrition": 98.0, "Compatibility": 80.0, "FRC": 80.0, "Constraint_Satisfaction": 90.0}},
            "composition": {"all_components": []}
        }
    ]

    classified = dynamic_strategy_classifier.classify_candidates(candidates)
    by_id = {c["candidate_id"]: c["strategy_label"] for c in classified}

    # Here FC-001 is cheapest -> MUST be Cost Optimized
    assert by_id["FC-001"] == "Cost Optimized"
    # FC-002 is highest nutrition -> MUST be Nutrition Maximized
    assert by_id["FC-002"] == "Nutrition Maximized"

def test_pipeline_integration_dynamic_strategies():
    """
    Runs actual CandidateEngine for the Chocolate brief and verifies
    that all 4 distinct strategies are assigned dynamically without hardcoding.
    """
    brief = product_brief_parser.parse(
        "Create a high-protein vegan chocolate bar with at least 25% cocoa butter, at least 7% protein, at most 28% sugar."
    )
    experiments = candidate_engine.generate_experiments(brief)
    assert len(experiments) >= 4

    assigned_labels = [c["strategy_label"] for c in experiments]
    expected_categories = {"Cost Optimized", "Nutrition Maximized", "Balanced Set", "Functionality & Flavor"}

    # Ensure all 4 strategy labels exist
    for expected in expected_categories:
        assert expected in assigned_labels, f"Expected {expected} in assigned labels: {assigned_labels}"

    # Verify that the candidate labeled 'Cost Optimized' genuinely has the minimum or near-minimum cost
    cost_opt_cand = next(c for c in experiments if c["strategy_label"] == "Cost Optimized")
    min_cost = min(c["cost_per_kg"] for c in experiments if c["cost_per_kg"] is not None)
    assert abs(cost_opt_cand["cost_per_kg"] - min_cost) < 0.01
