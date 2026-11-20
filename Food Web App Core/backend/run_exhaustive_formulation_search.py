"""
Exhaustive Formulation Search Pipeline Runner
Executes the full formulation pipeline with exhaustive ingredient combination search
and per-combination SLSQP percentage optimization for a product brief.
"""
import os
import sys
import argparse
import shutil
from pathlib import Path

# Setup paths
script_dir = Path(__file__).resolve().parent
workspace_root = script_dir.parent.parent
if str(workspace_root) not in sys.path:
    sys.path.insert(0, str(workspace_root))
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

# Ensure UTF-8 output encoding on Windows PowerShell to prevent charmap/UnicodeEncodeError
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import pandas as pd
from requirements_extractor import product_brief_parser, ProductBrief
from constraint_engine import constraint_engine
from retrieval_service import retrieval_orchestrator, RetrievedIngredient
from repository import get_all_ingredients, get_ingredient_by_id
from benchmark_briefs import BENCHMARK_BRIEFS
from exhaustive_search_engine import ExhaustiveFormulationSearchEngine

def load_subgraph_from_csv(
    csv_path: Path,
    brief_id: str
) -> List[RetrievedIngredient]:
    """Loads Dynamic Subgraph ingredients for brief_id from 06_dynamic_subgraph_ingredients.csv with full DB properties."""
    df = pd.read_csv(csv_path)
    sub_df = df[df["product_brief_id"] == brief_id]
    if sub_df.empty:
        return []

    db_items_by_id = {i["id"]: i for i in get_all_ingredients()}
    db_items_by_name = {i["name"].lower(): i for i in get_all_ingredients()}

    ingredients: List[RetrievedIngredient] = []
    for _, row in sub_df.iterrows():
        name = row["ingredient_name"]
        iid = row["ingredient_id"]
        f_roles = [r.strip() for r in str(row["functional_roles"]).split(";") if r.strip()]
        cat = row.get("category", "General")

        item = db_items_by_id.get(iid) or db_items_by_name.get(name.lower())
        if item:
            ri = RetrievedIngredient(
                id=item["id"],
                name=item["name"],
                category=item.get("category", cat),
                functional_roles=f_roles or [item.get("functional_role", "Base Raw Material")],
                nutrition={
                    "protein": float(item.get("protein", 0.0) or 0.0),
                    "fat": float(item.get("fat", 0.0) or 0.0),
                    "carbs": float(item.get("carbs", 0.0) or 0.0),
                    "calories": float(item.get("calories", item.get("energy", 0.0)) or 0.0)
                },
                cost_per_kg=float(item["cost_per_kg"]) if item.get("cost_per_kg") is not None else None,
                source=item.get("evidence_source", "tcs_food_formulator_kg.db"),
                regulatory_status=item.get("regulatory_status", "Permitted"),
                ins_number=item.get("ins_number"),
                vegan=bool(item.get("vegan", 1)),
                dairy_free=bool(item.get("dairy_free", 1)),
                gluten_free=bool(item.get("gluten_free", 1)),
                allergen=str(item.get("allergens", "None")),
                evidence_source=item.get("evidence_source", "USDA FDC / Codex GSFA")
            )
        else:
            ri = RetrievedIngredient(
                id=iid,
                name=name,
                category=cat,
                functional_roles=f_roles or ["Base Raw Material"],
                nutrition={"protein": 0.0, "fat": 0.0, "carbs": 0.0, "calories": 0.0},
                cost_per_kg=None,
                source="Knowledge Graph Subgraph",
                regulatory_status="Permitted"
            )
        ingredients.append(ri)
    return ingredients

def main():
    parser = argparse.ArgumentParser(description="Exhaustive Formulation Search with Per-Combination SLSQP Optimization")
    parser.add_argument("--brief-id", type=str, default="PB001", help="Benchmark brief ID (e.g. PB001)")
    parser.add_argument("--experiment-id", type=str, default="EXP-001", help="Experiment ID (e.g. EXP-001)")
    parser.add_argument("--brief-text", type=str, default=None, help="Custom product brief text")
    parser.add_argument("--max-combinations", type=int, default=None, help="Execution limit for testing (leaves run as non-exhaustive if set)")
    parser.add_argument("--subgraph-source", type=str, choices=["benchmark_csv", "fresh_retrieval", "auto"], default="auto", help="Source for dynamic subgraph")
    parser.add_argument("--output-dir", type=str, default=None, help="Results output directory")
    args = parser.parse_args()

    # 1. Determine Product Brief
    brief_data = None
    for b in BENCHMARK_BRIEFS:
        if b["id"] == args.brief_id:
            brief_data = b
            break

    if args.brief_text:
        brief_text = args.brief_text
        brief_cat = "Custom Product"
    elif brief_data:
        brief_text = brief_data["brief"]
        brief_cat = brief_data["category"]
    else:
        brief_text = "Create a vegan high-protein chocolate bar containing at least 20% protein and at most 25% fat. The product should feature a chewy texture, rich cocoa flavour, low water activity (aw <= 0.60), 12-month ambient shelf stability, and a competitive raw material cost below 10.0 USD/kg. Avoid dairy, whey, and animal-derived ingredients."
        brief_cat = "Protein Bars / Functional Snacks"

    # Parse Brief & Extract Constraints
    parsed_brief: ProductBrief = product_brief_parser.parse(brief_text)

    # 2. Dynamic Scientific Subgraph Construction
    subgraph_ingredients: List[RetrievedIngredient] = []
    benchmark_csv = workspace_root / "outputs" / "formulation_benchmark" / "06_dynamic_subgraph_ingredients.csv"

    if args.subgraph_source in ["benchmark_csv", "auto"] and benchmark_csv.exists() and brief_data:
        subgraph_ingredients = load_subgraph_from_csv(benchmark_csv, brief_data["id"])

    if not subgraph_ingredients:
        # Fresh retrieval via KG & constraint propagation
        retrieved_dict = retrieval_orchestrator.retrieve_all_multi_dimensional(parsed_brief.dict())
        prop_res = retrieval_orchestrator.propagate_constraints(retrieved_dict["ingredients"], parsed_brief.dict())
        subgraph_ingredients = prop_res.get("eligible_candidates", [])

    # 3. Setup Output Directory
    if args.output_dir:
        out_path = Path(args.output_dir)
    else:
        out_path = workspace_root / "results"
    out_path.mkdir(parents=True, exist_ok=True)

    # 4. Instantiate and Execute Exhaustive Engine
    engine = ExhaustiveFormulationSearchEngine(experiment_id=args.experiment_id)
    results = engine.run_exhaustive_optimization(
        brief=parsed_brief,
        subgraph_ingredients=subgraph_ingredients,
        output_dir=out_path,
        max_combinations_limit=args.max_combinations
    )

    # Also mirror results to backend results directory if different
    backend_res_dir = script_dir / "results"
    if backend_res_dir != out_path:
        backend_res_dir.mkdir(parents=True, exist_ok=True)
        for fname in ["exhaustive_candidate_results.csv", "valid_formulation_results.csv", "ranked_formulation_results.csv", "candidate_set_scores.csv", "experiment_summary.json"]:
            src_f = out_path / fname
            if src_f.exists():
                shutil.copy(src_f, backend_res_dir / fname)

    return results

if __name__ == "__main__":
    main()
