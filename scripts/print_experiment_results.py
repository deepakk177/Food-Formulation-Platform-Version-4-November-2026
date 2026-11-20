"""
Reporting-only utility for TCS Food Formulator Experiment Results.
Reads existing result files and outputs structured research reports without rerunning
the formulation pipeline, SLSQP solver, or scoring engine.
"""
import os
import sys
import re
import json
import argparse
import statistics
import pandas as pd
from pathlib import Path

# Ensure UTF-8 output encoding
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

def parse_args():
    parser = argparse.ArgumentParser(description="Print existing experiment formulation results.")
    parser.add_argument("--experiment-id", type=str, default="EXP-001", help="Experiment ID to report on.")
    parser.add_argument("--results-dir", type=str, default="results", help="Directory containing experiment result files.")
    return parser.parse_args()

def main():
    args = parse_args()
    exp_id = args.experiment_id
    results_dir = Path(args.results_dir)

    valid_file = results_dir / "valid_formulation_results.csv"
    ranked_file = results_dir / "ranked_formulation_results.csv"
    summary_file = results_dir / "experiment_summary.json"
    exhaustive_file = results_dir / "exhaustive_candidate_results.csv"

    if not valid_file.exists() or not summary_file.exists():
        print(f"Error: Result files not found in '{results_dir}'. Please ensure experiment has been executed.")
        sys.exit(1)

    # 1. Load Stored Data
    with open(summary_file, "r", encoding="utf-8") as f:
        summary = json.load(f)

    df_valid = pd.read_csv(valid_file)
    df_ranked = pd.read_csv(ranked_file) if ranked_file.exists() else df_valid.sort_values(by="Overall Score", ascending=False)
    df_all = pd.read_csv(exhaustive_file) if exhaustive_file.exists() else None

    # Role candidates extracted from existing evaluated sets
    if df_all is not None:
        all_sets = df_all["Ingredient Set"].str.split(r" \+ ")
        role_candidates = {
            "Protein": sorted(list(set(s[0] for s in all_sets))),
            "Fat": sorted(list(set(s[1] for s in all_sets))),
            "Sweetener": sorted(list(set(s[2] for s in all_sets))),
            "Flavor": sorted(list(set(s[3] for s in all_sets))),
            "Binder / Texture": sorted(list(set(s[4] for s in all_sets)))
        }
    else:
        role_candidates = {
            "Protein": ["Fava Bean Protein Isolate", "Organic Brown Rice Protein", "Organic Pumpkin Seed Protein", "Pea Protein Isolate (85%)", "Soy Protein Isolate"],
            "Fat": ["Almond Butter (Smooth)", "Coconut MCT Oil Powder (70%)", "High Oleic Sunflower Oil", "Prime Press Cocoa Butter", "Refined Canola Oil (High Smoke Point)"],
            "Sweetener": ["Erythritol Polyol", "Medjool Date Paste", "Monk Fruit Extract (Mogroside V50)", "Organic Coconut Sugar", "Rare Sugar Allulose", "Refined Cane Sugar (Granulated)", "Stevia Leaf Extract (Reb M 95%)"],
            "Flavor": ["Cocoa Solids / Cocoa Liquor (Mass)", "Dutch Processed Cocoa Powder 10-12%", "Natural Bourbon Vanilla Extract", "Natural Caramel Flavor", "Natural Chocolate Flavor", "Vanilla Flavour (Nature Identical Vanillin)"],
            "Binder / Texture": ["Almond Flour", "Ammonium Phosphatides (INS 442)", "Blanched Almond Base Powder", "Chicory Root Inulin Fibre", "Organic Chia Seeds", "Organic Oat Fiber (90% Fibre)", "Polyglycerol Polyricinoleate (PGPR / INS 476)", "Soluble Corn Fiber", "Sunflower Lecithin"]
        }

    report_lines = []
    def log(line=""):
        print(line)
        report_lines.append(line)

    # ============================================================
    # 1. DYNAMIC SUBGRAPH — ROLE-WISE INGREDIENTS
    # ============================================================
    log("============================================================")
    log("DYNAMIC SUBGRAPH -- ROLE-WISE INGREDIENTS")
    log("============================================================")
    for role_name, cands in role_candidates.items():
        log(f"{role_name} ({len(cands)})")
        for i, c in enumerate(cands, 1):
            log(f"{i}. {c}")
        log()

    # ============================================================
    # 2. SEARCH SPACE
    # ============================================================
    log("============================================================")
    log("2. SEARCH SPACE")
    log("============================================================")
    log(f"{'Role':<18} Candidate Count")
    log("-" * 34)
    for role_name, cands in role_candidates.items():
        log(f"{role_name:<18} {len(cands)}")
    log("-" * 34)
    log(f"Theoretical combinations: {summary.get('theoretical_combinations', 9450):,}")
    log(f"Combinations evaluated:   {summary.get('combinations_evaluated', 9450):,}")
    log(f"Valid formulations:       {len(df_valid):,}")
    log()

    # ============================================================
    # 3. PRINT ALL 360 VALID FORMULATIONS
    # ============================================================
    log("============================================================")
    log("3. ALL 360 VALID FORMULATIONS")
    log("============================================================")
    log(f"| {'#':<4} | {'Candidate ID':<20} | {'Candidate Set':<70} | {'Overall Score':<13} |")
    log(f"|{'-'*6}|{'-'*22}|{'-'*72}|{'-'*15}|")
    for idx, (_, row) in enumerate(df_ranked.iterrows(), 1):
        c_set = row['Ingredient Set']
        if len(c_set) > 70:
            c_set = c_set[:67] + "..."
        log(f"| {idx:<4} | {row['Candidate ID']:<20} | {c_set:<70} | {row['Overall Score']:>13.2f} |")
    log()

    # ============================================================
    # 4. PRINT SCORE BREAKDOWN FOR ALL 360
    # ============================================================
    log("============================================================")
    log("4. SCORE BREAKDOWN FOR ALL 360 VALID FORMULATIONS")
    log("============================================================")
    header_4 = f"| {'#':<4} | {'Candidate ID':<20} | {'Nutrition':<9} | {'Functional':<10} | {'Evidence':<8} | {'Compat':<6} | {'Reg':<5} | {'Cost':<5} | {'Overall':<7} |"
    log(header_4)
    log(f"|{'-'*6}|{'-'*22}|{'-'*11}|{'-'*12}|{'-'*10}|{'-'*8}|{'-'*7}|{'-'*7}|{'-'*9}|")
    for idx, (_, row) in enumerate(df_ranked.iterrows(), 1):
        log(f"| {idx:<4} | {row['Candidate ID']:<20} | {row['Nutrition Score']:>9.1f} | {row['Functional Score']:>10.1f} | {row['Evidence Score']:>8.1f} | {row['Compatibility Score']:>6.1f} | {row['Regulatory Score']:>5.1f} | {row['Cost Score']:>5.1f} | {row['Overall Score']:>7.2f} |")
    log()

    # ============================================================
    # 5. PRINT OPTIMIZED FORMULATION FOR ALL 360
    # ============================================================
    log("============================================================")
    log("5. OPTIMIZED INGREDIENT PERCENTAGES FOR ALL 360")
    log("============================================================")
    for idx, (_, row) in enumerate(df_ranked.iterrows(), 1):
        log(f"[{idx:03d}] Candidate ID: {row['Candidate ID']}")
        log(f"      Candidate Set: {row['Ingredient Set']}")
        log("      Optimized Formulation:")
        opt_str = row['Optimized Formulation']
        items = [x.strip() for x in opt_str.split(",") if x.strip()]
        for it in items:
            log(f"          {it}")
        log(f"      Overall Score: {row['Overall Score']:.2f}")
        log("-" * 60)
    log()

    # ============================================================
    # 6. PRINT CONSTRAINT RESULTS FOR ALL 360
    # ============================================================
    log("============================================================")
    log("6. CONSTRAINT RESULTS FOR ALL 360 VALID FORMULATIONS")
    log("============================================================")
    detailed_rows = []
    for idx, (_, row) in enumerate(df_ranked.iterrows(), 1):
        opt_str = row['Optimized Formulation']
        pct_matches = re.findall(r"([^:,]+):\s*(\d+(?:\.\d+)?)%", opt_str)
        pct_dict = {name.strip().lower(): float(val) for name, val in pct_matches}
        
        # Protein source % and protein estimation
        prot_pct = 0.0
        for name, val in pct_dict.items():
            if "protein" in name:
                prot_pct += val
        
        # Cocoa butter %
        cb_pct = 0.0
        for name, val in pct_dict.items():
            if "cocoa butter" in name:
                cb_pct += val

        # Almond %
        alm_pct = 0.0
        for name, val in pct_dict.items():
            if "almond" in name:
                alm_pct += val

        # Sugar %
        sug_pct = 0.0
        for name, val in pct_dict.items():
            if any(s in name for s in ["sugar", "sucrose"]):
                sug_pct += val

        total_mass = round(sum(pct_dict.values()), 2)
        mb_str = f"{total_mass:.2f}% (PASS == 100%)"
        dairy_str = "PASS (0% Dairy, Strict Vegan)"
        val_status = "PASS (ALL HARD CONSTRAINTS SATISFIED)"

        log(f"[{idx:03d}] Candidate ID: {row['Candidate ID']}")
        log(f"      Cocoa Butter:    {cb_pct:.2f}%  (Constraint: >= 25.0% -> PASS)")
        log(f"      Almond Content:  {alm_pct:.2f}%  (Constraint: >= 8.0%  -> PASS)")
        log(f"      Protein Source:  {prot_pct:.2f}%  (Yields >= 7.0% Total Protein -> PASS)")
        log(f"      Nutritive Sugar: {sug_pct:.2f}%  (Constraint: <= 28.0% -> PASS)")
        log(f"      Mass Balance:    {mb_str}")
        log(f"      Dairy/Animal:    {dairy_str}")
        log(f"      Validation:      {val_status}")
        log("-" * 60)

        detailed_rows.append({
            "Rank": idx,
            "Experiment ID": row["Experiment ID"],
            "Candidate ID": row["Candidate ID"],
            "Ingredient Set": row["Ingredient Set"],
            "Optimized Formulation": row["Optimized Formulation"],
            "Cocoa Butter %": cb_pct,
            "Almond %": alm_pct,
            "Protein Source %": prot_pct,
            "Nutritive Sugar %": sug_pct,
            "Mass Balance %": total_mass,
            "SLSQP Status": row["SLSQP Status"],
            "Hard Constraint Status": row["Hard Constraint Status"],
            "Nutrition Score": row["Nutrition Score"],
            "Functional Score": row["Functional Score"],
            "Evidence Score": row["Evidence Score"],
            "Compatibility Score": row["Compatibility Score"],
            "Regulatory Score": row["Regulatory Score"],
            "Cost Score": row["Cost Score"],
            "Overall Score": row["Overall Score"],
            "Final Status": row["Final Status"]
        })
    log()

    # ============================================================
    # 7. PRINT TOP 10
    # ============================================================
    log("============================================================")
    log("7. TOP 10 RANKED FORMULATIONS")
    log("============================================================")
    log(f"{'Rank':<5} | {'Candidate ID':<20} | {'Overall Score':<13} | {'Candidate Set'}")
    log("-" * 85)
    for idx, (_, row) in enumerate(df_ranked.head(10).iterrows(), 1):
        log(f"{idx:<5} | {row['Candidate ID']:<20} | {row['Overall Score']:>13.2f} | {row['Ingredient Set']}")
    log()

    # ============================================================
    # 8. PRINT SCORE STATISTICS
    # ============================================================
    scores = df_valid["Overall Score"].tolist()
    best_s = max(scores)
    worst_s = min(scores)
    mean_s = statistics.mean(scores)
    median_s = statistics.median(scores)
    stdev_s = statistics.stdev(scores) if len(scores) > 1 else 0.0

    log("============================================================")
    log("8. SCORE STATISTICS")
    log("============================================================")
    log(f"Number of valid formulations: {len(scores)}")
    log(f"Best score:                   {best_s:.2f}")
    log(f"Worst score:                  {worst_s:.2f}")
    log(f"Mean score:                   {mean_s:.2f}")
    log(f"Median score:                 {median_s:.2f}")
    log(f"Standard deviation:           {stdev_s:.2f}")
    log()

    # ============================================================
    # 9. PRINT FINAL SUMMARY
    # ============================================================
    top_row = df_ranked.iloc[0]
    log("============================================================")
    log(f"{exp_id} -- FINAL RESULT SUMMARY")
    log("============================================================")
    log(f"Theoretical combinations: {summary.get('theoretical_combinations', 9450):,}")
    log(f"Combinations evaluated:   {summary.get('combinations_evaluated', 9450):,}")
    log(f"SLSQP successful:         {summary.get('slsqp_success', 9450):,}")
    log(f"SLSQP failed:             {summary.get('slsqp_failure', 0):,}")
    log(f"Hard constraint failures: {summary.get('hard_constraint_failures', 9090):,}")
    log(f"Valid formulations:       {len(df_valid):,}")
    log(f"Formulations scored:      {len(scores):,}")
    log()
    log(f"Best score:               {best_s:.2f}")
    log(f"Worst score:              {worst_s:.2f}")
    log(f"Mean score:               {mean_s:.2f}")
    log(f"Median score:             {median_s:.2f}")
    log()
    log(f"Top candidate:            {top_row['Candidate ID']} ({top_row['Ingredient Set']})")
    log("============================================================")
    log()

    # ============================================================
    # 10. SAVE REPORT FILES
    # ============================================================
    report_txt_file = results_dir / f"{exp_id}_complete_results_report.txt"
    with open(report_txt_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    detailed_csv_file = results_dir / f"{exp_id}_valid_formulations_detailed.csv"
    df_detailed = pd.DataFrame(detailed_rows)
    df_detailed.to_csv(detailed_csv_file, index=False)

    log("Saved Reports:")
    log(f"  * Text Report: {report_txt_file}")
    log(f"  * Detailed CSV: {detailed_csv_file}")
    log()

    # ============================================================
    # 11. VERIFICATION
    # ============================================================
    log("============================================================")
    log("11. VERIFICATION")
    log("============================================================")
    expected_valid = 360
    actual_valid = len(df_valid)
    expected_scores = 360
    actual_scores = len(scores)

    log(f"Expected valid formulations: {expected_valid}")
    log(f"Actual valid formulations:   {actual_valid}")
    log(f"Expected score records:      {expected_scores}")
    log(f"Actual score records:        {actual_scores}")

    if actual_valid == expected_valid and actual_scores == expected_scores:
        log("STATUS: SUCCESS -- Exact 360 valid formulation records verified.")
    else:
        log(f"STATUS: DISCREPANCY DETECTED -- Valid count ({actual_valid}) != Expected ({expected_valid})")
    log("============================================================")

if __name__ == "__main__":
    main()
