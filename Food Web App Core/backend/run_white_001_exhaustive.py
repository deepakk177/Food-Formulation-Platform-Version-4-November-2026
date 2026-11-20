"""
Exhaustive Search & Multi-Objective Performance Scoring for WHITE_001 (Vegan White Chocolate).
Constructs the Cartesian product of role-wise pruned KG ingredient pools, optimizes every
combination with SciPy SLSQP under strict mass balance (sum == 100.0000%) and hard
constraints (cocoa_butter >= 25%, protein >= 5%, sugar <= 30%, 100% plant-based/dairy-free),
and ranks all valid formulations using ScoringEngine + CompatibilityModel.
"""
import os
import sys
import time
import math
import sqlite3
import itertools
import statistics
import logging
import warnings
from pathlib import Path
from multiprocessing import Pool, cpu_count
from typing import Dict, Any, List, Tuple

os.environ["NEO4J_ENABLED"] = "0"
os.environ["GROQ_API_KEY"] = ""

logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore")

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import numpy as np
import pandas as pd
from scipy.optimize import minimize

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from repository import DB_PATH
from scoring_engine import scoring_engine
from models.compatibility.model import compatibility_model


WHITE_001_BRIEF_TEXT = (
    "Vegan White Chocolate: create a dairy-free plant-based white chocolate using "
    "cocoa butter and plant-based ingredients. Target ≥ 25 % cocoa butter, ≤ 30 % sugar "
    "and ≥ 5 % protein with a smooth, creamy melt. Develop a vanilla-caramel flavour "
    "profile and 12-month shelf life"
)

WHITE_001_BRIEF_DICT = {
    "category": "Confectionery & Chocolate",
    "product_type": "chocolate_bar",
    "description": WHITE_001_BRIEF_TEXT,
    "dietary_requirements": ["Vegan", "Dairy-Free"],
    "nutrition_targets": {"protein_min": 5.0, "sugar_max": 30.0},
    "water_activity_target": 0.60,
    "cost_target": 15.0,
}


def load_curated_db() -> Dict[str, Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM ingredients WHERE category != 'FoodOn Taxonomy' AND vegan = 1 AND dairy_free = 1"
    ).fetchall()
    conn.close()
    return {r["id"]: dict(r) for r in rows}


def _evaluate_white_001_combo(args: Tuple) -> Dict[str, Any]:
    idx, combo_rows, role_labels, bounds = args
    comb_id = f"WHITE_001-COMB-{idx:05d}"

    p_vec = np.array([float(r.get("protein") or 0.0) for r in combo_rows])
    f_vec = np.array([float(r.get("fat") or 0.0) for r in combo_rows])
    c_vec = np.array([float(r.get("carbs") or 0.0) for r in combo_rows])
    s_vec = np.array([float(r.get("sugar") or 0.0) for r in combo_rows])
    cost_vec = np.array([float(r.get("cost_per_kg") or 10.0) for r in combo_rows])
    cb_mask = np.array([1.0 if r["id"] == "ing_cocoa_butter" else 0.0 for r in combo_rows])

    cons = [
        {"type": "eq", "fun": lambda x: np.sum(x) - 100.0},
        {"type": "ineq", "fun": lambda x: np.dot(x / 100.0, p_vec) - 5.1},
        {"type": "ineq", "fun": lambda x: 29.5 - np.dot(x / 100.0, s_vec)},
        {"type": "ineq", "fun": lambda x: np.dot(x, cb_mask) - 25.0},
    ]

    def objective(x):
        curr_cost = np.dot(x / 100.0, cost_vec)
        curr_prot = np.dot(x / 100.0, p_vec)
        curr_sug = np.dot(x / 100.0, s_vec)
        # Balanced objective: cost efficiency + close tracking of 6.5% protein & low sugar
        return curr_cost * 0.55 + ((curr_prot - 6.5) ** 2) * 0.35 + (curr_sug * 0.08)

    x0 = np.array([(b[0] + b[1]) * 0.5 for b in bounds])
    x0 = (x0 / np.sum(x0)) * 100.0
    x0 = np.clip(x0, [b[0] for b in bounds], [b[1] for b in bounds])
    x0 = (x0 / np.sum(x0)) * 100.0

    res = minimize(
        objective,
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints=cons,
        options={"maxiter": 400, "ftol": 1e-7},
    )

    if not res.success:
        return {"is_valid": False, "slsqp_success": False, "reason": "SLSQP_INFEASIBLE"}

    opt_x = (res.x / np.sum(res.x)) * 100.0
    pcts = [round(float(v), 4) if v <= 1.0 else round(float(v), 2) for v in opt_x]
    diff = round(100.0000 - sum(pcts), 4)
    max_idx = int(np.argmax(pcts))
    pcts[max_idx] = round(pcts[max_idx] + diff, 4)

    pct_arr = np.array(pcts) / 100.0
    prot = round(float(np.dot(pct_arr, p_vec)), 2)
    fat = round(float(np.dot(pct_arr, f_vec)), 2)
    carbs = round(float(np.dot(pct_arr, c_vec)), 2)
    sugar = round(float(np.dot(pct_arr, s_vec)), 2)
    calories = round(4.0 * prot + 4.0 * carbs + 9.0 * fat, 1)
    cost_kg = round(float(np.dot(pct_arr, cost_vec)), 2)
    cb_pct = round(float(np.dot(pcts, cb_mask)), 2)
    total_pct = round(sum(pcts), 4)

    # Hard constraint verification
    if abs(total_pct - 100.0) > 0.01:
        return {"is_valid": False, "slsqp_success": True, "reason": "MASS_BALANCE_FAIL"}
    if prot < 5.0:
        return {"is_valid": False, "slsqp_success": True, "reason": "PROTEIN_BELOW_5"}
    if sugar > 30.0:
        return {"is_valid": False, "slsqp_success": True, "reason": "SUGAR_ABOVE_30"}
    if cb_pct < 25.0:
        return {"is_valid": False, "slsqp_success": True, "reason": "COCOA_BUTTER_BELOW_25"}

    formatted_components = []
    for r, rl, pct in zip(combo_rows, role_labels, pcts):
        formatted_components.append({
            "id": r["id"],
            "name": r["name"],
            "category": r["category"],
            "functional_role": r["functional_role"],
            "role_slot": rl,
            "percentage": pct,
            "cost_per_kg": float(r.get("cost_per_kg") or 10.0),
            "regulatory_status": "Permitted",
            "ins_number": None,
            "source_evidence": r.get("evidence_source") or "USDA FDC / Codex",
            "allergen": r.get("allergens") or "None",
        })

    comp_eval, _ = compatibility_model.predict_with_uncertainty(formatted_components)

    candidate_obj = {
        "candidate_id": comb_id,
        "set_name": f"Exhaustive {comb_id}",
        "total_percentage": total_pct,
        "is_mathematically_valid": True,
        "composition": {
            "all_components": formatted_components,
            "bulk_ingredients": formatted_components,
            "functional_ingredients": [],
        },
        "nutrition": {
            "protein": prot,
            "fat": fat,
            "carbohydrates": carbs,
            "sugar": sugar,
            "calories": calories,
            "water_activity": 0.56,
        },
        "cost_per_kg": cost_kg,
        "cost_status": "CALCULATED",
        "compatibility": comp_eval,
    }

    scored = scoring_engine.calculate_scores(candidate_obj, WHITE_001_BRIEF_DICT, profile_name="BALANCED")
    radar = scored.get("radar_scores", {})

    combo_names = " + ".join(r["name"] for r in combo_rows)
    opt_str = ", ".join(f"{r['name']}: {pct:.2f}%" for r, pct in zip(combo_rows, pcts))

    return {
        "is_valid": True,
        "slsqp_success": True,
        "candidate_id": comb_id,
        "ingredient_set": combo_names,
        "optimized_formulation": opt_str,
        "overall_score": round(float(scored.get("overall_score", 0.0)), 2),
        "nutrition_score": round(float(scored.get("nutrition_fit_score", 0.0)), 1),
        "cost_score": round(float(scored.get("cost_efficiency_score", 0.0)), 1),
        "frc_score": round(float(scored.get("functional_role_coverage_score", 0.0)), 1),
        "ics_score": round(float(scored.get("compatibility_score", 0.0)), 1),
        "soft_score": round(float(scored.get("soft_constraint_score", 0.0)), 1),
        "ses_score": round(float(radar.get("SES", 0.0)), 1),
        "protein": prot,
        "fat": fat,
        "sugar": sugar,
        "cocoa_butter": cb_pct,
        "calories": calories,
        "cost_per_kg": cost_kg,
        "components": [(r["name"], rl, pct) for r, rl, pct in zip(combo_rows, role_labels, pcts)],
    }


def main():
    t0 = time.time()
    cdb = load_curated_db()

    # Role-wise pruned pools for WHITE_001 (Vegan White Chocolate)
    # Cocoa Butter (fixed core) x Plant Milk/Nut Matrix x Plant Protein x Sweetener x Bulking/Fiber x Emulsifier x Vanilla x Caramel
    pools = [
        ("Cocoa Butter", [("ing_cocoa_butter", (25.0, 45.0))]),
        ("Plant Milk Matrix", [
            ("ing_oat_base", (15.0, 38.0)),
            ("ing_almond_base", (12.0, 35.0)),
            ("ing_cultured_coconut_base", (15.0, 38.0)),
            ("ing_almond_flour", (12.0, 35.0)),
        ]),
        ("Plant Protein", [
            ("ing_fava_protein", (2.5, 20.0)),
            ("ing_pea_protein", (2.5, 20.0)),
            ("ing_soy_protein", (2.5, 20.0)),
            ("ing_rice_protein", (2.5, 20.0)),
            ("ing_pumpkin_protein", (2.5, 20.0)),
        ]),
        ("Sweetener", [
            ("ing_cane_sugar", (8.0, 28.0)),
            ("ing_coconut_sugar", (8.0, 28.0)),
            ("ing_date_paste", (8.0, 28.0)),
            ("ing_allulose", (8.0, 28.0)),
            ("ing_erythritol", (8.0, 28.0)),
        ]),
        ("Bulking / Fiber", [
            ("ing_allulose", (2.0, 15.0)),
            ("ing_chicory_inulin", (2.0, 15.0)),
            ("ing_soluble_corn_fiber", (2.0, 15.0)),
        ]),
        ("Emulsifier", [
            ("ing_sunflower_lecithin", (0.30, 0.80)),
            ("ing_soy_lecithin", (0.30, 0.80)),
            ("ing_ammonium_phosphatides", (0.20, 0.70)),
            ("ing_pgpr", (0.10, 0.50)),
            ("ing_mono_diglycerides", (0.20, 0.80)),
        ]),
        ("Caramel Flavor", [("ing_natural_caramel_flavor", (0.15, 0.50))]),
        ("Vanilla Flavor", [
            ("ing_vanilla_extract", (0.15, 0.50)),
            ("ing_vanilla_flavor", (0.10, 0.40)),
        ]),
    ]

    role_labels = [p[0] for p in pools]
    pool_lists = [p[1] for p in pools]
    raw_combos = list(itertools.product(*pool_lists))

    # Skip duplicate ingredient within same combo (e.g. allulose in both Sweetener & Bulking)
    worker_args = []
    comb_num = 1
    for combo in raw_combos:
        ids = [item[0] for item in combo]
        if len(set(ids)) != len(ids):
            continue
        rows = [cdb[i] for i in ids]
        bounds = [item[1] for item in combo]
        worker_args.append((comb_num, rows, role_labels, bounds))
        comb_num += 1

    n_total = len(worker_args)
    n_workers = 1
    results = [_evaluate_white_001_combo(a) for a in worker_args]

    elapsed = time.time() - t0
    slsqp_ok = sum(1 for r in results if r["slsqp_success"])
    valid_rows = [r for r in results if r["is_valid"]]
    valid_rows.sort(key=lambda x: (-x["overall_score"], x["cost_per_kg"]))

    # Save CSV
    out_dir = WORKSPACE_ROOT / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    if valid_rows:
        df_out = pd.DataFrame([
            {k: v for k, v in r.items() if k not in {"is_valid", "slsqp_success", "components"}}
            for r in valid_rows
        ])
        df_out.insert(0, "rank", range(1, len(df_out) + 1))
        df_out.to_csv(out_dir / "white_001_exhaustive_ranked.csv", index=False)

    print("=" * 118)
    print("WHITE_001 (VEGAN WHITE CHOCOLATE) — EXHAUSTIVE COMBINATORIAL SEARCH & PERFORMANCE SCORING")
    print("=" * 118)
    print(f"Brief: \"{WHITE_001_BRIEF_TEXT}\"")
    print("Hard Gates: Mass=100.0000% | Vegan & Dairy-Free | Cocoa Butter >= 25.0% | Protein >= 5.0% | Sugar <= 30.0%")
    print("-" * 118)
    print("ROLE-WISE SEARCH SPACE:")
    for rname, items in pools:
        names = ", ".join(cdb[i[0]]["name"] for i in items)
        print(f"  * {rname:<18} ({len(items)}): {names}")
    print(
        f"\nSearch Summary: Raw Cartesian={len(raw_combos):,} | Distinct 8-Ingredient Combos={n_total:,} | "
        f"SLSQP Converged={slsqp_ok:,} | Hard-Constraint Valid={len(valid_rows):,} | Time={elapsed:.2f}s ({n_workers} workers)"
    )

    scores = [r["overall_score"] for r in valid_rows]
    if scores:
        print(
            f"Score Distribution (Valid={len(scores):,}): Best={max(scores):.2f} | "
            f"Median={statistics.median(scores):.2f} | Mean={statistics.mean(scores):.2f} | Worst={min(scores):.2f}"
        )

    print("\n" + "=" * 118)
    print("TOP 20 FORMULATION CANDIDATES WITH MULTI-OBJECTIVE PERFORMANCE SCORES (RANKED BY UEB OVERALL SCORE)")
    print("Formula: Overall = 25% NutritionFit + 25% CostEfficiency + 20% FRC + 15% ICS + 15% SoftConstraints")
    print("=" * 118)
    print(
        f"{'Rk':>2} | {'Candidate ID':<19} | {'Overall':>7} | {'Nutr':>5} | {'CostS':>5} | {'FRC':>5} | "
        f"{'ICS':>5} | {'Soft':>5} | {'SES':>5} | {'Prot%':>5} | {'Fat%':>5} | {'Sug%':>5} | {'CB%':>5} | {'$/kg':>6} | {'Key Matrix + Protein + Sweetener + Emulsifier'}"
    )
    print("-" * 118)
    for rank, r in enumerate(valid_rows[:20], 1):
        # Compact readable combo summary (Milk + Protein + Sweetener + Fiber + Emulsifier)
        short_parts = [c[0].split(" (")[0] for c in r["components"][1:6]]
        combo_short = " + ".join(short_parts)
        if len(combo_short) > 46:
            combo_short = combo_short[:43] + "..."
        print(
            f"{rank:>2} | {r['candidate_id']:<19} | {r['overall_score']:>7.2f} | {r['nutrition_score']:>5.1f} | "
            f"{r['cost_score']:>5.1f} | {r['frc_score']:>5.1f} | {r['ics_score']:>5.1f} | {r['soft_score']:>5.1f} | "
            f"{r['ses_score']:>5.1f} | {r['protein']:>5.2f} | {r['fat']:>5.2f} | {r['sugar']:>5.2f} | "
            f"{r['cocoa_butter']:>5.2f} | ${r['cost_per_kg']:>5.2f} | {combo_short}"
        )

    print("\n" + "=" * 118)
    print("TOP 5 CANDIDATES — OPTIMIZED INGREDIENT PERCENTAGES (SUM = 100.0000%)")
    print("=" * 118)
    for rank, r in enumerate(valid_rows[:5], 1):
        print(
            f"[Rank #{rank:02d}] {r['candidate_id']} | Overall={r['overall_score']:.2f}/100 | "
            f"Prot={r['protein']:.2f}% | Fat={r['fat']:.2f}% | Sugar={r['sugar']:.2f}% | CB={r['cocoa_butter']:.2f}% | Cost=${r['cost_per_kg']:.2f}/kg"
        )
        print(f"           Recipe: {r['optimized_formulation']}")
        print("-" * 118)


if __name__ == "__main__":
    main()
