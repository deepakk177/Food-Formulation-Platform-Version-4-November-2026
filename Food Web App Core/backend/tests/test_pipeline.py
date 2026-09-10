"""
Automated Test Suite for Grounded Food Formulation Pipeline
"""
import pytest
from neo4j_client import neo4j_client
from retrieval_service import retrieval_orchestrator
from requirements_extractor import requirements_extractor
from constraint_engine import constraint_engine
from candidate_engine import candidate_engine
from scoring_engine import scoring_engine
from synthesis_engine import synthesis_engine

def test_neo4j_health():
    health = neo4j_client.get_health()
    assert "connected" in health
    assert "nodeCount" in health

def test_requirement_extraction():
    prompt = "Create a vegan high-protein chocolate bar with smooth texture, 20% protein and low water activity"
    reqs = requirements_extractor.extract(prompt)
    assert reqs.product_type == "chocolate_bar"
    assert "vegan" in reqs.dietary_constraints
    assert "protein" in reqs.nutrition_targets
    assert reqs.nutrition_targets["protein"].value == 20.0
    assert "dairy" in reqs.exclusions

def test_hard_constraint_filtering():
    reqs = requirements_extractor.extract("Make a vegan chocolate bar")
    retrieved = retrieval_orchestrator.retrieve_ingredients()
    eligible = constraint_engine.filter_eligible_ingredients(retrieved, reqs)
    
    # Verify no dairy ingredients remain in eligible pool
    for ing in eligible:
        assert "milk" not in ing.name.lower()
        assert "egg" not in ing.name.lower()
        assert "butter" not in ing.name.lower()

def test_candidate_generation_math_consistency():
    reqs = requirements_extractor.extract("Make a vegan 20% protein bar")
    retrieved = retrieval_orchestrator.retrieve_ingredients()
    candidates = candidate_engine.generate_candidates(retrieved, reqs)
    
    assert len(candidates) > 0
    top_cand = candidates[0]
    assert top_cand.is_mathematically_valid
    assert abs(top_cand.total_percentage - 100.0) <= 0.1

def test_scoring_engine():
    reqs = requirements_extractor.extract("Make a high-protein bar")
    retrieved = retrieval_orchestrator.retrieve_ingredients()
    candidates = candidate_engine.generate_candidates(retrieved, reqs)
    ranked = scoring_engine.rank_candidates(candidates, reqs)
    
    assert len(ranked) > 0
    score = ranked[0]["score"]
    assert score["is_feasible"]
    assert 0.0 <= score["performance"]["overall"] <= 100.0

def test_synthesis_engine():
    reqs = requirements_extractor.extract("Make a vegan protein bar")
    retrieved_data = retrieval_orchestrator.retrieve_all_multi_dimensional(reqs.dict())
    candidates = candidate_engine.generate_candidates(retrieved_data["ingredients"], reqs)
    ranked = scoring_engine.rank_candidates(candidates, reqs)[0]
    
    report = synthesis_engine.synthesize(
        query="Make a vegan protein bar",
        requirements=reqs.dict(),
        ranked_candidate=ranked,
        evidence_list=retrieved_data["evidence"]
    )
    
    assert "title" in report
    assert "process_recommendations" in report
    assert len(report["process_recommendations"]) >= 3
