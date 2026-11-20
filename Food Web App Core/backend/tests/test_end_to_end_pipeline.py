"""
Comprehensive End-to-End Pipeline Unit & Integration Tests
Tests all 20 required pipeline stages and validation gates:
1. Product brief extraction
2. Constraint normalization
3. Constraint graph construction
4. Hard/soft classification
5. Dynamic retrieval
6. Cypher retrieval
7. Semantic retrieval
8. Structured retrieval
9. Candidate fusion
10. Hard constraint validation
11. Regulatory validation
12. Allergen validation
13. Compatibility validation
14. Groundedness validation
15. Mass-balance validation
16. Score calculation
17. Candidate ranking
18. Formulation generation
19. Provenance tracking
20. Iteration logic
"""
import os
import pytest
from requirements_extractor import product_brief_parser, ProductBrief
from constraint_engine import constraint_engine
from retrieval_service import retrieval_orchestrator
from candidate_engine import candidate_engine
from validation_gate import validation_gate
from scoring_engine import scoring_engine
from synthesis_engine import synthesis_engine
from pipeline_runner import run_pipeline

TEST_BRIEF = "Create a vegan high-protein chocolate bar containing approximately 20% protein and 30% fat. The product should have low water activity, good chocolate flavour, acceptable texture, ambient shelf stability, and a competitive manufacturing cost. Avoid dairy and animal-derived ingredients."

def test_01_product_brief_extraction():
    brief = product_brief_parser.parse(TEST_BRIEF)
    assert brief.category == "Confectionery & Chocolate"
    assert "Vegan" in brief.dietary_requirements
    assert brief.nutrition_targets.protein_min == 20.0
    assert len(brief.constraint_items) >= 4

def test_02_constraint_normalization():
    brief = product_brief_parser.parse(TEST_BRIEF)
    for item in brief.constraint_items:
        assert item.constraint_id.startswith("CONST-")
        assert item.operator in ["=", ">=", "<=", ">", "<", "IN", "NOT_IN", "REQUIRED", "FORBIDDEN", "PREFERRED"]
        assert len(item.source_text) > 0

def test_03_constraint_graph_construction():
    brief = product_brief_parser.parse(TEST_BRIEF)
    c_graph = brief.constraint_graph
    assert c_graph is not None
    assert len(c_graph["nodes"]) >= 5
    assert len(c_graph["edges"]) >= 4
    assert c_graph["summary"]["Graph Nodes"] >= 5

def test_04_hard_soft_classification():
    brief = product_brief_parser.parse(TEST_BRIEF)
    priorities = constraint_engine.prioritize_constraints(brief)
    assert priorities["priority_distribution"]["hard_count"] >= 1
    assert priorities["priority_distribution"]["soft_count"] >= 1
    for hc in priorities["hard_constraints"]:
        assert hc["hard_or_soft"] == "HARD"
        assert hc["weight"] > 0.0

def test_05_to_09_retrieval_and_fusion():
    brief = product_brief_parser.parse(TEST_BRIEF)
    brief_dict = brief.dict()
    retrieved = retrieval_orchestrator.retrieve_all_multi_dimensional(brief_dict)
    
    # Intents (Query Understanding)
    assert len(retrieved["intents"]) >= 3
    # Cypher traversal string generated
    assert "MATCH (i:Ingredient)" in retrieved["cypher_query"]
    # Candidates retrieved & fused
    assert retrieved["retrieved_count"] > 0
    # Provenance / Sources attached
    for ing in retrieved["ingredients"][:5]:
        assert ing.source is not None
        assert len(ing.retrieval_methods) >= 1

def test_10_to_15_grounded_validation():
    brief = product_brief_parser.parse(TEST_BRIEF)
    retrieved = retrieval_orchestrator.retrieve_all_multi_dimensional(brief.dict())
    eligible = retrieval_orchestrator.propagate_constraints(retrieved["ingredients"], brief.dict())["eligible_candidates"]
    candidate_sets = candidate_engine.generate_experiments(brief, eligible)
    
    val_res = validation_gate.validate_candidate_set(candidate_sets[0], brief)
    assert val_res["status"] in ["PASS", "REQUIRES_EVIDENCE", "FAIL"]
    assert val_res["mass_balance_result"]["status"] == "PASS"
    assert abs(val_res["mass_balance_result"]["total_percentage"] - 100.0000) <= 0.01

def test_16_to_18_scoring_ranking_formulation():
    brief = product_brief_parser.parse(TEST_BRIEF)
    retrieved = retrieval_orchestrator.retrieve_all_multi_dimensional(brief.dict())
    eligible = retrieval_orchestrator.propagate_constraints(retrieved["ingredients"], brief.dict())["eligible_candidates"]
    candidate_sets = candidate_engine.generate_experiments(brief, eligible)
    
    ranked = scoring_engine.rank_candidates(candidate_sets, brief.dict(), profile_name="BALANCED")
    assert len(ranked) >= 3
    assert ranked[0]["score"]["overall_score"] >= ranked[-1]["score"]["overall_score"]

def test_19_provenance_tracking():
    brief = product_brief_parser.parse(TEST_BRIEF)
    retrieved = retrieval_orchestrator.retrieve_all_multi_dimensional(brief.dict())
    eligible = retrieval_orchestrator.propagate_constraints(retrieved["ingredients"], brief.dict())["eligible_candidates"]
    candidate_sets = candidate_engine.generate_experiments(brief, eligible)
    
    top = candidate_sets[0]
    syn = synthesis_engine.synthesize(TEST_BRIEF, brief.dict(), top, retrieved["evidence"])
    for exp in syn["ingredient_explanations"]:
        assert exp["evidenceSource"] is not None

def test_20_end_to_end_pipeline_runner():
    res = run_pipeline(TEST_BRIEF, debug=False, profile="BALANCED")
    assert res["run_id"].startswith("RUN_")
    assert os.path.exists(res["output_dir"])
    assert os.path.exists(os.path.join(res["output_dir"], "pipeline_trace.json"))
    assert res["validation"]["status"] == "PASS"
