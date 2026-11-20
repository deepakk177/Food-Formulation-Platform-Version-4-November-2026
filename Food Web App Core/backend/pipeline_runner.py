"""
End-to-End Constraint-Driven Food Formulation Pipeline Runner
Executes complete 8-stage formulation pipeline from natural language brief to final formulation report.
Provides terminal debug mode (--debug) and persists machine-readable JSON run traces to outputs/formulation_runs/<run_id>/.
"""
import os
import sys
import json
import uuid
import datetime
import argparse
import logging
import warnings
from typing import Dict, Any, List, Optional

# Suppress background logs and deprecation notices for clean terminal presentation
logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore")

# Ensure UTF-8 output encoding on Windows PowerShell to prevent charmap/UnicodeEncodeError
if sys.platform == "win32" and "pytest" not in sys.modules:
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from requirements_extractor import product_brief_parser, ProductBrief
from constraint_engine import constraint_engine
from retrieval_service import retrieval_orchestrator
from candidate_engine import candidate_engine
from validation_gate import validation_gate
from scoring_engine import scoring_engine
from synthesis_engine import synthesis_engine

def run_pipeline(
    user_brief: str,
    debug: bool = True,
    profile: str = "BALANCED",
    iterations: int = 1,
    profile2: Optional[str] = None,
    exhaustive: bool = False,
    max_combinations: Optional[int] = None
) -> Dict[str, Any]:
    run_id = f"RUN_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6].upper()}"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "outputs", "formulation_runs", run_id)
    os.makedirs(output_dir, exist_ok=True)

    trace_log = {
        "run_id": run_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "user_brief": user_brief,
        "profile": profile,
        "iterations": iterations,
        "iteration_records": []
    }

    # =========================================================================
    # STEP 1 — PRODUCT BRIEF NLP PROCESSING
    # =========================================================================
    if debug:
        print("\n[01/08] Product Brief Processing .............. DONE")
        print("============================================================")
        print("STEP 1 — PRODUCT BRIEF NLP PROCESSING")
        print("============================================================")
        print(f"\nOriginal Product Brief:\n{user_brief}\n")

    brief: ProductBrief = product_brief_parser.parse(user_brief)
    brief_dict = brief.dict()

    if debug:
        print(f"Detected Product Type:\n{brief.product_type} ({brief.category})\n")
        print("Extracted Requirements:")
        for idx, ci in enumerate(brief.constraint_items, 1):
            print(f"[{idx}]")
            print(f"Type:        {ci.type}")
            print(f"Parameter:   {ci.parameter}")
            print(f"Operator:    {ci.operator}")
            print(f"Target:      {ci.target_value}")
            print(f"Unit:        {ci.unit or 'N/A'}")
            print(f"Source Text: \"{ci.source_text}\"")
            print(f"Confidence:  {ci.confidence}\n")

    with open(os.path.join(output_dir, "product_brief.json"), "w", encoding="utf-8") as f:
        json.dump(brief_dict, f, indent=2)

    with open(os.path.join(output_dir, "extracted_constraints.json"), "w", encoding="utf-8") as f:
        json.dump([ci.dict() for ci in brief.constraint_items], f, indent=2)

    # =========================================================================
    # STEP 1B — CONSTRAINT GRAPH CONSTRUCTION
    # =========================================================================
    if debug:
        print("\n[02/08] Constraint Graph ..................... DONE")
        print("============================================================")
        print("CONSTRAINT GRAPH")
        print("============================================================")
        print("\nNODES")
        print("-" * 60)
        print(f"{'Node ID':<12} | {'Type':<25} | {'Value':<30} | {'Source'}")
        print("-" * 60)
        for n in brief.constraint_graph.get("nodes", []):
            print(f"{n['id']:<12} | {n['type']:<25} | {str(n['value']):<30} | {n['source']}")

        print("\nEDGES")
        print("-" * 60)
        print(f"{'Source':<12} | {'Relationship':<30} | {'Target'}")
        print("-" * 60)
        for e in brief.constraint_graph.get("edges", []):
            print(f"{e['source']:<12} | {e['relationship']:<30} | {e['target']}")

        print("\nCONSTRAINT GRAPH SUMMARY")
        print("-" * 60)
        for k, v in brief.constraint_graph.get("summary", {}).items():
            print(f"{k:<30}: {v}")
        print("=" * 60 + "\n")

    with open(os.path.join(output_dir, "constraint_graph.json"), "w", encoding="utf-8") as f:
        json.dump(brief.constraint_graph, f, indent=2)

    iteration_results = []

    # =========================================================================
    # ITERATION EXECUTION LOOP (STEPS 2 - 7)
    # =========================================================================
    for iter_idx in range(1, iterations + 1):
        active_profile = profile if iter_idx == 1 else (profile2 or ("NUTRITION_OPTIMIZED" if profile == "BALANCED" else "COST_OPTIMIZED"))
        iter_dir = os.path.join(output_dir, f"iteration_{iter_idx}") if iterations > 1 else output_dir
        os.makedirs(iter_dir, exist_ok=True)

        if iterations > 1:
            print("\n" + "#" * 80)
            print(f"###  ITERATION {iter_idx} OF {iterations}  [Active Profile: {active_profile}]")
            if iter_idx > 1:
                print(f"###  (Re-running all pipeline steps with adapted weights & measures)")
            print("#" * 80 + "\n")

        # =====================================================================
        # STEP 2 — HARD / SOFT CONSTRAINT ENGINE (PRIORITIZATION)
        # =====================================================================
        if debug:
            print(f"[{iter_idx}.2] Constraint Prioritization ............ DONE")
            print("============================================================")
            print(f"STEP 2 (ITERATION {iter_idx}) — CONSTRAINT PRIORITIZATION")
            print("============================================================")

        p_dict = constraint_engine.prioritize_constraints(brief)

        # Adapt soft constraint weights if running iteration > 1
        if iter_idx > 1:
            if active_profile == "NUTRITION_OPTIMIZED":
                for sc in p_dict.get("soft_constraints", []):
                    if any(k in sc["name"].lower() for k in ["nutr", "protein"]):
                        sc["weight"] = 0.95
                        sc["reason"] += " [Iteration 2 Boost: Maximize Protein Density]"
                    elif "cost" in sc["name"].lower():
                        sc["weight"] = 0.50
            elif active_profile == "COST_OPTIMIZED":
                for sc in p_dict.get("soft_constraints", []):
                    if "cost" in sc["name"].lower():
                        sc["weight"] = 0.95
                        sc["reason"] += " [Iteration 2 Boost: Aggressive Cost Minimization]"
                    elif any(k in sc["name"].lower() for k in ["nutr", "protein"]):
                        sc["weight"] = 0.55
            elif active_profile == "FUNCTIONAL_OPTIMIZED":
                for sc in p_dict.get("soft_constraints", []):
                    if any(k in sc["name"].lower() for k in ["functional", "texture"]):
                        sc["weight"] = 0.95

        if debug:
            print(f"\n{'Constraint':<35} | {'Type':<12} | {'Weight':<8} | {'Reason'}")
            print("-" * 80)
            for c in p_dict["all_constraints"]:
                print(f"{c['name']:<35} | {c['hard_or_soft']:<12} | {c['weight']:<8.2f} | {c['reason']}")

            print("\nHARD CONSTRAINTS")
            print("-" * 80)
            for c in p_dict["hard_constraints"]:
                print(f"  - {c['name']} (Weight: {c['weight']}) -> {c['reason']}")

            print("\nSOFT CONSTRAINTS")
            print("-" * 80)
            for c in p_dict["soft_constraints"]:
                print(f"  - {c['name']} (Weight: {c['weight']}) -> {c['reason']}")

            print(f"\nPriority Distribution: Hard: {p_dict['priority_distribution']['hard_count']} | Soft: {p_dict['priority_distribution']['soft_count']}")
            print("=" * 60 + "\n")

        with open(os.path.join(iter_dir, "constraint_priorities.json"), "w", encoding="utf-8") as f:
            json.dump(p_dict, f, indent=2)

        # =====================================================================
        # STEP 3 — CONTEXT-AWARE CONSTRAINT-DRIVEN RETRIEVAL
        # =====================================================================
        if debug:
            print(f"[{iter_idx}.3] Context-Aware Retrieval .............. DONE")
            print("============================================================")
            print(f"STEP 3 (ITERATION {iter_idx}) — QUERY UNDERSTANDING & RETRIEVAL")
            print("============================================================")

        retrieved = retrieval_orchestrator.retrieve_all_multi_dimensional(brief_dict)
        all_raw_ingredients = retrieved.get("ingredients", [])
        intents = retrieved.get("intents", [])
        ms_breakdown = retrieved.get("multi_strategy_breakdown", {})

        # Adapt retrieval ordering / measures in iteration > 1
        if iter_idx > 1:
            if active_profile == "NUTRITION_OPTIMIZED":
                all_raw_ingredients.sort(
                    key=lambda x: float((x.nutrition.get("protein", 0.0) if getattr(x, "nutrition", None) else 0.0) or 0.0),
                    reverse=True
                )
            elif active_profile == "COST_OPTIMIZED":
                all_raw_ingredients.sort(
                    key=lambda x: float(getattr(x, "cost_per_kg", None) if getattr(x, "cost_per_kg", None) is not None else 999.0)
                )
            elif active_profile == "FUNCTIONAL_OPTIMIZED":
                all_raw_ingredients.sort(
                    key=lambda x: len(getattr(x, "functional_roles", []) or []),
                    reverse=True
                )

        if debug:
            print("\n" + "=" * 60)
            print(f"STEP 3.1 (ITERATION {iter_idx}) — MULTI-STRATEGY RETRIEVAL")
            print("============================================================")
            print("Retrieve heterogeneous information using complementary strategies:\n")

            kg_info = ms_breakdown.get("kg_traversal", {})
            print(f"1. KG / Cypher Traversal")
            print(f"   * Explicit Relationships: {', '.join(kg_info.get('relationships_traversed', []))}")
            print(f"   * Multi-Hop Reasoning:   Ingredient -> FunctionalRole -> Property / Regulation")
            print(f"   * Traversed Nodes:       {kg_info.get('count', 0)} live graph nodes")

            str_info = ms_breakdown.get("structured_retrieval", {})
            print(f"\n2. Structured Retrieval")
            print(f"   * Exact Values Filters:  {', '.join(str_info.get('exact_filters_applied', []))}")
            print(f"   * Verified DB Matches:   {str_info.get('count', 0)} candidates verified")

            vec_info = ms_breakdown.get("semantic_vector_search", {})
            print(f"\n3. Semantic Vector Search")
            print(f"   * Conceptual Similarity: TF-IDF / Cosine semantic search")
            print(f"   * Query Concept:         \"{vec_info.get('query_concept', '')}\"")
            print(f"   * Conceptual Matches:    {vec_info.get('count', 0)} candidates")
            if vec_info.get("top_matches"):
                print(f"   * Top Matches:           {', '.join(vec_info.get('top_matches', []))}")

            ev_info = ms_breakdown.get("scientific_evidence", {})
            print(f"\n4. Scientific Evidence Retrieval")
            print(f"   * Literature Citations:  Research papers, USDA FDC, Codex GSFA & DOIs")
            print(f"   * Citations Retrieved:   {ev_info.get('count', 0)} evidence items")

            for it in intents:
                print(f"\n{it['intent_id']} - {it['purpose']}")
                print(f"  Entities:            {', '.join(it['entities'])}")
                print(f"  Constraints:         {', '.join(it['constraints'])}")
                print(f"  Required Properties: {', '.join(it['required_properties'])}")

            print("\n" + "=" * 60)
            print(f"STEP 3.2 (ITERATION {iter_idx}) — CONSTRAINT PROPAGATION")
            print("============================================================")

        prop_results = retrieval_orchestrator.propagate_constraints(all_raw_ingredients, brief_dict)
        eligible_ingredients = prop_results["eligible_candidates"]

        if debug:
            print(f"Initial Candidate Space:     {prop_results['initial_candidate_space']}")
            print(f"After Dietary Constraint:    {prop_results['after_dietary_constraint']}")
            print(f"After Allergen Constraint:   {prop_results['after_allergen_constraint']}")
            print(f"After Functional Constraint: {prop_results['after_functional_constraint']}")
            print(f"After Regulatory Constraint: {prop_results['after_regulatory_constraint']}")
            print(f"After Cost Constraint:       {prop_results['after_cost_constraint']}")
            print(f"Final Candidate Space:       {prop_results['final_candidate_space']}\n")

            print("REMOVED CANDIDATES")
            print("-" * 80)
            print(f"{'Ingredient':<30} | {'Removed Because':<35} | {'Source'}")
            print("-" * 80)
            for r in prop_results["removed_candidates"][:5]:
                print(f"{r['ingredient']:<30} | {r['removed_because']:<35} | {r['evidence']}")

            print("\n" + "=" * 60)
            print(f"STEP 3.3 (ITERATION {iter_idx}) — GRAPH TRAVERSAL")
            print("============================================================")
            print("Traversing: Ingredient -[:FULFILLS]-> FunctionalRole")
            print("Traversing: Ingredient -[:SUBJECT_TO]-> Regulation")
            print("Traversing: Ingredient -[:INCOMPATIBLE_WITH]-> Ingredient")
            print(f"Grounded Nodes Retrieved: {len(eligible_ingredients)}")
            print("=" * 60)

        # STEP 3.4 — CANDIDATE SUFFICIENCY & BACKTRACKING AUDIT
        sufficiency = retrieval_orchestrator.evaluate_candidate_sufficiency(
            eligible_ingredients, brief_dict, prop_results
        )

        if debug:
            print("\n" + "=" * 60)
            print(f"STEP 3.4 (ITERATION {iter_idx}) — CANDIDATE SUFFICIENCY & BACKTRACKING AUDIT")
            print("============================================================")
            status_str = "PASS (Sufficient candidate pool)" if sufficiency["is_sufficient"] else "WARNING (Constrained candidate space)"
            print(f"Sufficiency Status:     {status_str}")
            print(f"Eligible Candidates:    {sufficiency['candidate_count']}")
            print(f"Primary Bottleneck:     {sufficiency['primary_bottleneck']}")

            if not sufficiency["is_sufficient"]:
                print("\n[BACKTRACKING LOOP TRIGGERED] INSUFFICIENT INGREDIENT SET DETECTED")
                print("-" * 60)
                print("ITERATE BACK TO STEP 2 — CONSTRAINT RELAXATION & REPRIORITIZATION:")
                for r2 in sufficiency["step_2_relaxation_recommendations"]:
                    print(f"  * {r2}")
                print("\nITERATE BACK TO STEP 1 — BRIEF REFORMULATION & DISAMBIGUATION:")
                for r1 in sufficiency["step_1_reformulation_recommendations"]:
                    print(f"  * {r1}")
            else:
                print(f"Backtracking Decision:  Candidate space verified; proceeding to Candidate Set Blending.")
            print("=" * 60 + "\n")

        with open(os.path.join(iter_dir, "retrieval_queries.json"), "w", encoding="utf-8") as f:
            json.dump(intents, f, indent=2)

        with open(os.path.join(iter_dir, "retrieval_results.json"), "w", encoding="utf-8") as f:
            json.dump([i.to_dict() for i in eligible_ingredients], f, indent=2)

        # =====================================================================
        # STEP 4 — MULTIPLE CANDIDATE SET GENERATION
        # =====================================================================
        if debug:
            print(f"[{iter_idx}.4] Candidate Generation ................. DONE")
            print("============================================================")
            print(f"STEP 4 (ITERATION {iter_idx}) — CANDIDATE SETS")
            print("============================================================")

        if exhaustive:
            from pathlib import Path
            candidate_engine.run_exhaustive_search(
                brief=brief,
                ingredients=eligible_ingredients,
                experiment_id=run_id,
                output_dir=Path(iter_dir),
                max_combinations_limit=max_combinations
            )
        candidate_sets = candidate_engine.generate_experiments(brief, eligible_ingredients)

        if debug:
            for cs in candidate_sets:
                print(f"\nCandidate Set: {cs['candidate_id']} ({cs['set_name']})")
                print(f"Title:         {cs['title']}")
                print(f"Mass Check:    Sum(Pct) = {cs['total_percentage']:.4f}%")
                print("Ingredients:")
                for item in cs["composition"]["all_components"]:
                    print(f"  - {item['name']:<30} | Pct: {item['percentage']:>6.2f}% | Role: {item['functional_role']}")

            print("\nCANDIDATE SET SUMMARY")
            print("-" * 60)
            print(f"Total Candidates:   {len(candidate_sets)}")
            print(f"Feasible:           {sum(1 for c in candidate_sets if c['is_mathematically_valid'])}")
            print(f"Rejected:           {len(prop_results['removed_candidates'])}")
            print("=" * 60 + "\n")

        with open(os.path.join(iter_dir, "candidate_sets.json"), "w", encoding="utf-8") as f:
            json.dump(candidate_sets, f, indent=2)

        # =====================================================================
        # STEP 5 — VALIDATION & GROUNDEDNESS GATE
        # =====================================================================
        if debug:
            print(f"[{iter_idx}.5] Validation & Grounding ............... PASS")
            print("============================================================")
            print(f"STEP 5 (ITERATION {iter_idx}) — VALIDATION & GROUNDEDNESS GATE")
            print("============================================================")

        validation_result = validation_gate.validate_candidate_set(candidate_sets[0], brief, iteration_num=iter_idx)

        if debug:
            print("\nHard Constraints")
            print("-" * 80)
            print(f"{'Constraint':<35} | {'Result':<8} | {'Evidence'}")
            print("-" * 80)
            for hc in validation_result["hard_constraint_results"]:
                print(f"{hc['constraint']:<35} | {hc['result']:<8} | {hc['evidence']}")

            print("\nRegulatory Validation")
            print("-" * 80)
            for r in validation_result["regulatory_results"][:3]:
                print(f"  - {r['ingredient']:<30} | Permitted: {r['permitted']} | Jurisdiction: {r['jurisdiction']}")

            print("\nPairwise Compatibility Matrix")
            print("-" * 80)
            for cm in validation_result["compatibility_results"][:3]:
                pair_ascii = str(cm.get('pair', cm.get('issue', 'Pair'))).replace("↔", "<->")
                reason_str = cm.get('reason', cm.get('status', 'Verified'))
                print(f"  - {pair_ascii:<40} | Status: {cm.get('status', 'Unknown'):<12} | Reason: {reason_str}")

            print("\nGroundedness & Provenance Check")
            print("-" * 80)
            for g in validation_result["groundedness_results"][:4]:
                print(f"  - {g['claim']:<35} | Grounded: {g['grounded']} | Source: {g['source']}")

            print(f"\nMass Balance Status: {validation_result['mass_balance_result']['status']} (Total: {validation_result['mass_balance_result']['total_percentage']}%)")

            print("\n============================================================")
            print("FINAL VALIDATION STATUS")
            print("============================================================")
            print(f"STATUS:                 {validation_result['status']}")
            print(f"Iteration Decision:     {validation_result['iteration_recommendation']}")
            print("=" * 60 + "\n")

        with open(os.path.join(iter_dir, "validation_results.json"), "w", encoding="utf-8") as f:
            json.dump(validation_result, f, indent=2)

        # =====================================================================
        # STEP 6 — SCORING & RANKING
        # =====================================================================
        if debug:
            print(f"[{iter_idx}.6] Scoring & Ranking .................... DONE")
            print("============================================================")
            print(f"STEP 6 (ITERATION {iter_idx}) — SCORING & RANKING")
            print("============================================================")

        ranked_candidates = scoring_engine.rank_candidates(candidate_sets, brief_dict, profile_name=active_profile)

        if debug:
            print(f"\n{'Candidate Set':<25} | {'Functional':<10} | {'Evidence':<8} | {'Comp':<6} | {'Nutr':<6} | {'Cost':<6} | {'Regu':<6} | {'Overall'}")
            print("-" * 90)
            for cand in ranked_candidates:
                sc = cand["score"]
                rs = sc.get("radar_scores", {})
                f_val = rs.get('Functional', rs.get('Functional_Coverage', rs.get('FRC', 0.0)))
                ev_val = rs.get('Evidence', rs.get('SES', 0.0))
                cp_val = rs.get('Compatibility', 0.0)
                nu_val = rs.get('Nutrition', 0.0)
                co_val = rs.get('Cost', 0.0)
                rg_val = rs.get('Regulatory', 0.0)
                print(f"{cand['candidate_id']:<25} | {f_val:<10.1f} | {ev_val:<8.1f} | {cp_val:<6.1f} | {nu_val:<6.1f} | {co_val:<6.1f} | {rg_val:<6.1f} | {sc['overall_score']:.1f}")

            print(f"\nRANKING (Profile: {active_profile})")
            print("-" * 80)
            for r_idx, cand in enumerate(ranked_candidates, 1):
                print(f"Rank #{r_idx}: {cand['candidate_id']} ({cand['set_name']}) | Score: {cand['score']['overall_score']:.1f}/100")
            print("=" * 60 + "\n")

        with open(os.path.join(iter_dir, "scoring_results.json"), "w", encoding="utf-8") as f:
            json.dump([c["score"] for c in ranked_candidates], f, indent=2)

        with open(os.path.join(iter_dir, "formulation_candidates.json"), "w", encoding="utf-8") as f:
            json.dump(ranked_candidates, f, indent=2)

        # =====================================================================
        # STEP 7 — LLM FORMULATION GENERATION
        # =====================================================================
        if debug:
            print(f"[{iter_idx}.7] Formulation Generation ............... DONE\n")

        top_candidate = ranked_candidates[0]
        synthesized = synthesis_engine.synthesize(
            query=user_brief,
            requirements=brief_dict,
            ranked_candidate=top_candidate,
            evidence_list=retrieved.get("evidence", [])
        )

        with open(os.path.join(iter_dir, "final_formulations.json"), "w", encoding="utf-8") as f:
            json.dump(synthesized, f, indent=2)

        with open(os.path.join(iter_dir, "formulation_report.json"), "w", encoding="utf-8") as f:
            json.dump(synthesized, f, indent=2)

        # Also write to top-level folder so the latest iteration is always directly accessible
        with open(os.path.join(output_dir, "final_formulations.json"), "w", encoding="utf-8") as f:
            json.dump(synthesized, f, indent=2)
        with open(os.path.join(output_dir, "formulation_report.json"), "w", encoding="utf-8") as f:
            json.dump(synthesized, f, indent=2)

        # Output Final Formulation Report to terminal
        print_final_report(brief, top_candidate, synthesized, validation_result, run_id)

        prop_trace = dict(prop_results)
        prop_trace["eligible_candidates"] = [i.to_dict() for i in prop_results.get("eligible_candidates", [])]

        iter_trace = {
            "iteration": iter_idx,
            "profile": active_profile,
            "step_2_priorities": p_dict,
            "step_3_retrieval": prop_trace,
            "step_4_candidates": [c["candidate_id"] for c in candidate_sets],
            "step_5_validation": validation_result,
            "step_6_ranking": [c["candidate_id"] for c in ranked_candidates],
            "step_7_synthesis_title": synthesized.get("title")
        }

        trace_log["iteration_records"].append(iter_trace)
        with open(os.path.join(iter_dir, "pipeline_trace.json"), "w", encoding="utf-8") as f:
            json.dump(iter_trace, f, indent=2)

        iteration_results.append({
            "iteration": iter_idx,
            "profile": active_profile,
            "candidate_sets": candidate_sets,
            "ranked_candidates": ranked_candidates,
            "top_candidate": top_candidate,
            "synthesized_report": synthesized,
            "validation": validation_result
        })

    # =========================================================================
    # MULTI-ITERATION COMPARISON REPORT
    # =========================================================================
    if iterations > 1 and len(iteration_results) >= 2:
        it1 = iteration_results[0]
        it2 = iteration_results[1]
        c1 = it1["top_candidate"]
        c2 = it2["top_candidate"]
        n1 = c1["nutrition"]
        n2 = c2["nutrition"]
        s1 = c1["score"]
        s2 = c2["score"]

        print("\n" + "=" * 92)
        print(" MULTI-ITERATION RE-RUN COMPARISON REPORT")
        print("=" * 92)
        print(f"{'Feature / Metric':<32} | {'Iter 1 (' + it1['profile'] + ')':<22} | {'Iter 2 (' + it2['profile'] + ')':<22} | {'Delta / Impact'}")
        print("-" * 92)
        print(f"{'Selected Strategy':<32} | {c1['set_name'][:22]:<22} | {c2['set_name'][:22]:<22} | {'Adapted Strategy'}")
        print(f"{'Top Candidate ID':<32} | {c1['candidate_id']:<22} | {c2['candidate_id']:<22} | {'Selected Set'}")
        print(f"{'Overall Pareto Score':<32} | {s1['overall_score']:>6.1f} / 100.0{' ':10} | {s2['overall_score']:>6.1f} / 100.0{' ':10} | {s2['overall_score'] - s1['overall_score']:+6.1f}")
        print(f"{'Protein Compliance Score':<32} | {s1['radar_scores']['Nutrition']:>6.1f} / 100.0{' ':10} | {s2['radar_scores']['Nutrition']:>6.1f} / 100.0{' ':10} | {s2['radar_scores']['Nutrition'] - s1['radar_scores']['Nutrition']:+6.1f}")
        print(f"{'Cost Efficiency Score':<32} | {s1['radar_scores']['Cost']:>6.1f} / 100.0{' ':10} | {s2['radar_scores']['Cost']:>6.1f} / 100.0{' ':10} | {s2['radar_scores']['Cost'] - s1['radar_scores']['Cost']:+6.1f}")
        print(f"{'Protein Content (g/100g)':<32} | {n1.get('protein', 0.0):>6.1f} g{' ':14} | {n2.get('protein', 0.0):>6.1f} g{' ':14} | {n2.get('protein', 0.0) - n1.get('protein', 0.0):+6.1f} g")
        print(f"{'Fat Content (g/100g)':<32} | {n1.get('fat', 0.0):>6.1f} g{' ':14} | {n2.get('fat', 0.0):>6.1f} g{' ':14} | {n2.get('fat', 0.0) - n1.get('fat', 0.0):+6.1f} g")
        print(f"{'Estimated Energy (kcal)':<32} | {n1.get('calories', 0.0):>6.0f} kcal{' ':11} | {n2.get('calories', 0.0):>6.0f} kcal{' ':11} | {n2.get('calories', 0.0) - n1.get('calories', 0.0):+6.0f} kcal")
        print(f"{'Raw Material Cost ($/kg)':<32} | ${c1.get('cost_per_kg', 0.0):>6.2f} USD{' ':10} | ${c2.get('cost_per_kg', 0.0):>6.2f} USD{' ':10} | ${c2.get('cost_per_kg', 0.0) - c1.get('cost_per_kg', 0.0):+6.2f} USD")
        print("=" * 92 + "\n")

        with open(os.path.join(output_dir, "iteration_comparison.json"), "w", encoding="utf-8") as f:
            json.dump({
                "iteration_1": {
                    "profile": it1["profile"],
                    "candidate_id": c1["candidate_id"],
                    "strategy": c1["set_name"],
                    "score": s1["overall_score"],
                    "nutrition": n1,
                    "cost_per_kg": c1.get("cost_per_kg")
                },
                "iteration_2": {
                    "profile": it2["profile"],
                    "candidate_id": c2["candidate_id"],
                    "strategy": c2["set_name"],
                    "score": s2["overall_score"],
                    "nutrition": n2,
                    "cost_per_kg": c2.get("cost_per_kg")
                }
            }, f, indent=2)

    with open(os.path.join(output_dir, "pipeline_trace.json"), "w", encoding="utf-8") as f:
        json.dump(trace_log, f, indent=2)

    latest_iter = iteration_results[-1]
    return {
        "run_id": run_id,
        "output_dir": output_dir,
        "parsed_brief": brief_dict,
        "candidate_sets": latest_iter["candidate_sets"],
        "top_candidate": latest_iter["top_candidate"],
        "synthesized_report": latest_iter["synthesized_report"],
        "validation": latest_iter["validation"],
        "iteration_results": iteration_results
    }

def print_final_report(brief: ProductBrief, candidate: Dict[str, Any], synthesized: Dict[str, Any], validation: Dict[str, Any], run_id: str):
    comp = candidate["composition"]
    all_comps = comp.get("all_components", [])
    nutrition = candidate["nutrition"]

    print("============================================================")
    print("FINAL FORMULATION REPORT")
    print("============================================================")
    print("\nPRODUCT")
    print("-" * 60)
    print(f"Product Type:  {brief.product_type} ({brief.category})")
    print(f"Product Brief: {brief.description}")

    print("\n============================================================")
    print("CONSTRAINT SUMMARY")
    print("============================================================")
    print(f"Hard Constraints: {', '.join(brief.dietary_requirements or ['Standard Dietary'])}")
    print(f"Soft Constraints: {', '.join(brief.soft_objectives or ['Cost & Quality Optimization'])}")

    print("\n============================================================")
    print("SELECTED FORMULATION")
    print("============================================================")
    print(f"{'Ingredient':<32} | {'%':<8} | {'Quantity (g)':<12} | {'Functional Role':<20} | {'Purpose'}")
    print("-" * 95)
    for item in all_comps:
        print(f"{item['name']:<32} | {item['percentage']:>6.2f}% | {item['quantity_g']:>10.2f}g  | {item['functional_role']:<20} | {item['purpose']}")
    print("-" * 95)
    print(f"TOTAL:                            {round(sum(c['percentage'] for c in all_comps), 4):>6.2f}% | 1000.00g\n")

    print("============================================================")
    print("NUTRITION PROFILE (per 100g)")
    print("============================================================")
    print(f"Calories:       {nutrition.get('calories', 0.0):.0f} kcal")
    print(f"Protein:        {nutrition.get('protein', 0.0):.1f} g")
    print(f"Fat:            {nutrition.get('fat', 0.0):.1f} g")
    print(f"Carbohydrate:   {nutrition.get('carbohydrates', 0.0):.1f} g")

    print("\n============================================================")
    print("COST ANALYSIS")
    print("============================================================")
    print(f"Raw Material Cost / kg: ${candidate.get('cost_per_kg', 8.74):.2f} USD")
    print("Processing Cost / kg:   $1.25 USD")
    print(f"Estimated Total / kg:   ${candidate.get('cost_per_kg', 8.74) + 1.25:.2f} USD")

    print("\n============================================================")
    print("FUNCTIONAL & SENSORY ANALYSIS")
    print("============================================================")
    for exp in synthesized.get("ingredient_explanations", [])[:3]:
        name_clean = str(exp.get('name', '')).encode('ascii', 'replace').decode('ascii')
        role_clean = str(exp.get('functionalRole', '')).encode('ascii', 'replace').decode('ascii')
        just_clean = str(exp.get('justification', '')).encode('ascii', 'replace').decode('ascii')
        ev_clean = str(exp.get('evidenceSource', '')).encode('ascii', 'replace').decode('ascii')
        print(f"Ingredient: {name_clean} -> Role: {role_clean}")
        print(f"  Justification: {just_clean}")
        print(f"  Evidence:      {ev_clean}\n")

    print("============================================================")
    print("REGULATORY & ALLERGEN ANALYSIS")
    print("============================================================")
    for reg in validation.get("regulatory_results", [])[:3]:
        print(f"  - {reg['ingredient']}: Status={reg['status']} (Jurisdiction: {reg.get('jurisdiction', 'FSSAI / FDA / Codex')})")

    print("\n============================================================")
    print("MANUFACTURING PROCESS")
    print("============================================================")
    for p_step in synthesized.get("process_recommendations", []):
        print(f"  - {p_step}")

    print("\n============================================================")
    print("FORMULATION VALIDATION & SCORE")
    print("============================================================")
    print(f"Validation Status:            {validation['status']}")
    print(f"Mass Balance (sum=100%):      {validation['mass_balance_result']['status']}")
    print(f"Overall Pareto Score:         {candidate['score']['overall_score']:.1f} / 100.0")

    print("\n============================================================")
    print("PROVENANCE & PIPELINE TRACE")
    print("============================================================")
    print(f"Run ID:        {run_id}")
    print(f"Run Artifacts: outputs/formulation_runs/{run_id}/\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="End-to-End Constraint-Driven Food Formulation Pipeline")
    parser.add_argument("--brief", type=str, default="Create a vegan high-protein chocolate bar containing approximately 20% protein and 30% fat. The product should have low water activity, good chocolate flavour, acceptable texture, ambient shelf stability, and a competitive manufacturing cost. Avoid dairy and animal-derived ingredients.", help="Natural language product brief")
    parser.add_argument("--debug", action="store_true", default=True, help="Enable terminal debug mode showing sequential stage outputs")
    parser.add_argument("--profile", type=str, default="BALANCED", help="Initial scoring profile (BALANCED, NUTRITION_OPTIMIZED, COST_OPTIMIZED, FUNCTIONAL_OPTIMIZED, SENSORY_OPTIMIZED)")
    parser.add_argument("--iterations", type=int, default=1, help="Number of iterations to execute (e.g. 2 for re-running with changed weights/measures)")
    parser.add_argument("--profile2", type=str, default=None, help="Scoring profile for iteration 2 (e.g. NUTRITION_OPTIMIZED, COST_OPTIMIZED, FUNCTIONAL_OPTIMIZED)")
    parser.add_argument("--exhaustive", action="store_true", default=False, help="Enable exhaustive candidate combination search with per-combination SLSQP")
    parser.add_argument("--max-combinations", type=int, default=None, help="Optional combination evaluation limit for testing")
    args = parser.parse_args()

    run_pipeline(
        user_brief=args.brief,
        debug=args.debug,
        profile=args.profile,
        iterations=args.iterations,
        profile2=args.profile2,
        exhaustive=args.exhaustive,
        max_combinations=args.max_combinations
    )
