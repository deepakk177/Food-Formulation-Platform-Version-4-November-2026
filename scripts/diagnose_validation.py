import sys
sys.path.insert(0, 'Food Web App Core/backend')
from tests.test_end_to_end_pipeline import TEST_BRIEF
from requirements_extractor import product_brief_parser
from retrieval_service import retrieval_orchestrator
from constraint_engine import constraint_engine
from candidate_engine import candidate_engine
from validation_gate import validation_gate

brief = product_brief_parser.parse(TEST_BRIEF)
retrieved = retrieval_orchestrator.retrieve_all_multi_dimensional(brief.dict())
eligible = constraint_engine.filter_eligible_ingredients(retrieved["ingredients"], brief)
candidates = candidate_engine.generate_experiments(brief, eligible)

val = validation_gate.validate_candidate_set(candidates[0], brief)
print("STATUS:", val["status"])
print("FAILURE REASONS:", val["failure_reasons"])
print("REQUIRES EVIDENCE REASONS:", val["requires_evidence_reasons"])
print("HARD RESULTS:")
for hr in val["hard_constraint_results"]:
    print(" ", hr)

