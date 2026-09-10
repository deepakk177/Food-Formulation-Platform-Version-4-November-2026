"""
Unit tests for Retrieval, Constraint Filtering, Dynamic Experiment Generation,
Math Normalization (sum=100.00%), Scoring, and Synthesis in Food Web App Core backend.
"""
import pytest
from requirements_extractor import product_brief_parser, ProductBrief
from retrieval_service import retrieval_orchestrator, RetrievedIngredient
from constraint_engine import constraint_engine
from candidate_engine import candidate_engine
from scoring_engine import scoring_engine
from synthesis_engine import synthesis_engine

def test_product_brief_parsing():
    query = "Design a vegan, gluten-free high protein chocolate bar with 20% protein and low cost"
    brief = product_brief_parser.parse(query)
    
    assert "Vegan" in brief.dietary_requirements
    assert "Gluten-Free" in brief.dietary_requirements
    assert brief.category == "Confectionery & Chocolate"
    assert brief.nutrition_targets.protein_min == 20.0
    assert "nutrition_maximized" in brief.experiment_strategies
    assert "cost_optimized" in brief.experiment_strategies

def test_multi_source_retrieval():
    brief_dict = {"category": "Confectionery & Chocolate", "description": "vegan protein bar"}
    retrieved = retrieval_orchestrator.retrieve_all_multi_dimensional(brief_dict)
    
    assert "ingredients" in retrieved
    assert retrieved["retrieved_count"] > 0
    
    ing = retrieved["ingredients"][0]
    assert isinstance(ing, RetrievedIngredient)
    assert ing.name != ""

def test_hard_constraint_filtering():
    brief = product_brief_parser.parse("Design a vegan chocolate bar")
    
    vegan_ing = RetrievedIngredient(
        id="ing_1", name="Pea Protein Isolate", category="Proteins", vegan=True, allergen="None"
    )
    non_vegan_ing = RetrievedIngredient(
        id="ing_2", name="Whey Protein Isolate", category="Proteins", vegan=False, allergen="Milk"
    )
    
    allowed_v, _ = constraint_engine.evaluate_ingredient_hard_constraints(vegan_ing, brief)
    allowed_nv, _ = constraint_engine.evaluate_ingredient_hard_constraints(non_vegan_ing, brief)
    
    assert allowed_v is True
    assert allowed_nv is False

def test_dynamic_experiment_generation_and_math_sum():
    brief = product_brief_parser.parse("Design a vegan, gluten-free high protein bar")
    experiments = candidate_engine.generate_experiments(brief)
    
    assert len(experiments) >= 3
    
    for exp in experiments:
        comp = exp["composition"]
        total_pct = sum(item["percentage"] for item in comp["bulk_ingredients"]) + \
                    sum(item["percentage"] for item in comp["functional_ingredients"])
        
        # Verify strict sum(percentage) == 100.00%
        assert round(total_pct, 2) == 100.00
        assert exp["is_mathematically_valid"] is True

def test_scoring_and_synthesis():
    brief = product_brief_parser.parse("Design a vegan high protein chocolate bar")
    experiments = candidate_engine.generate_experiments(brief)
    top_exp = experiments[0]
    
    scores = scoring_engine.calculate_scores(top_exp, brief.dict())
    assert "radar_scores" in scores
    assert scores["overall_score"] > 50.0
    
    report = synthesis_engine.synthesize(
        query=brief.description,
        requirements=brief.dict(),
        ranked_candidate=top_exp,
        evidence_list=[]
    )
    assert "process_recommendations" in report
    assert "composition" in report
