# Phase 2A.3 Targeted Correction Log

## Overview
Phase 2A.3 is an audit and targeted correction phase. In accordance with Section 7 of the Master Engineering Contract, all corrections made directly address verified root causes discovered during physical database queries, file inspections, and manifest audits. No legacy code was altered, no synthetic data was fabricated, and no approved schemas were modified.

---

## Targeted Corrections Implemented

### Correction 1: Resolution of USDA Foundation Count Discrepancy
- **Issue**: Phase 2A.2 reported 316 foods in `foundationDownload.json`, but DuckDB staged 318 Foundation foods and 7,793 SR Legacy foods (total 8,111).
- **Investigation & Root Cause**:
  1. The bulk archive `foundationDownload.json` contains exactly 316 unique food items.
  2. Phase 2A staged a targeted search sample of 102 foods under dataset `DSK-USDA-FDC-2024-04` from 6 search queries.
  3. 14 of those search sample foods overlapped with the 316 bulk Foundation foods and were preserved idempotently under their original Phase 2A asset reference.
  4. **Exactly two foods** in the search sample (`AST-USDA-SEARCH-MILK` FDC ID `2758990` "Sweetened condensed milk", and `AST-USDA-SEARCH-WHEAT_FLOUR` FDC ID `2758996` "Tortilla, wheat flour, shelf stable") were authentic Foundation foods added to the live USDA FDC database that were not included in the static 2024-10-31 bulk archive snapshot.
  5. 86 foods in the search sample were SR Legacy foods, matching the bulk SR Legacy dataset.
- **Action Taken**: Documented the mathematical reconciliation:
  $$\text{Total Foundation Foods} = 316\text{ (Bulk)} + 2\text{ (Live Search Queries)} = 318\text{ Foods}$$
  $$\text{Total SR Legacy Foods} = 7,707\text{ (Bulk)} + 86\text{ (Search Queries)} = 7,793\text{ Foods}$$
  $$\text{Total Unique USDA Foods} = 318 + 7,793 = 8,111\text{ Unique Foods}$$
- **Verification**: Zero duplicate FDC IDs exist in DuckDB (`count(DISTINCT native_record_id) == count(*)`).

---

### Correction 2: PubChem Historical Records & Food Formulation Chemicals
- **Issue**: Phase 2A and Phase 2A.2 reports had conflicting chemical labels for the 8 PubChem records.
- **Investigation & Root Cause**:
  1. Physical inspection of `data/raw_v2/pubchem/pubchem_cid_*.json` proved that the exact same 8 JSON files were used from Phase 2A through Phase 2A.2: CIDs `[1183, 2519, 311, 5988, 54670067, 712, 23665764, 104]`.
  2. The underlying chemicals in these 8 files are:
     - CID 1183: Vanillin (mislabeled as "Water" in 2A.2 report)
     - CID 2519: Caffeine
     - CID 311: Citric Acid
     - CID 5988: Sucrose
     - CID 54670067: L-Ascorbic Acid (mislabeled as "L-Lactic Acid" in 2A.2 report)
     - CID 712: Formaldehyde (mistakenly described as Sodium Benzoate in 2A and Sodium Chloride in 2A.2)
     - CID 23665764: Sodium p-methylbenzylsulfonate (mistakenly described as Potassium Sorbate in 2A and Stevioside in 2A.2)
     - CID 104: 3-Oxoadipate enol-lactone (mistakenly described as Glycine in 2A and Nitrogen in 2A.2)
  3. The underlying data was never replaced; the discrepancies were reporting errors.
- **Action Taken**:
  1. Preserved all 8 original pilot compounds intact without deletion or alteration under dataset `DSK-PUBCHEM-2026`.
  2. Acquired the authentic PubChem REST API JSON records for the 8 genuine food chemicals via `PubChemAcquirer`:
     - CID 962: Water (Oxidane, $18.015\text{ g/mol}$)
     - CID 750: Glycine ($75.067\text{ g/mol}$)
     - CID 517055: Sodium Benzoate ($144.10\text{ g/mol}$)
     - CID 23676745: Potassium Sorbate ($150.22\text{ g/mol}$)
     - CID 107689: L-Lactic Acid ($90.078\text{ g/mol}$)
     - CID 5234: Sodium Chloride ($58.44\text{ g/mol}$)
     - CID 442089: Stevioside ($804.9\text{ g/mol}$)
     - CID 947: Molecular Nitrogen ($28.014\text{ g/mol}$)
  3. Extracted and staged these 8 genuine food formulation compounds into DuckDB `raw_records` under dataset `DSK-PUBCHEM-COMPOUNDS`.
- **Outcome**: PubChem compound count expanded to **16 unique genuine compounds**, fully registered in `source_assets` and `raw_records`.

---

### Correction 3: DuckDB Dataset Registry Foreign Key Repair
- **Issue**: Database integrity audit revealed 406 rows in `raw_records` pointing to `dataset_id` values not present in `dataset_registry`.
- **Investigation & Root Cause**:
  1. The 102 search sample USDA foods had `dataset_id = 'DSK-USDA-FDC-2024-04'`.
  2. The 296 Phase 2A Codex GSFA records had `dataset_id = 'DSK-CODEX-GSFA-2023'`.
  3. The 8 pilot PubChem records had `dataset_id = 'DSK-PUBCHEM-2026'`.
  4. Phase 2A.2 runner registered only the bulk dataset IDs in `dataset_registry`.
- **Action Taken**:
  1. Registered `DSK-USDA-FDC-2024-04`, `DSK-CODEX-GSFA-2023`, and `DSK-PUBCHEM-2026` in `dataset_registry` with authoritative source associations and descriptions.
- **Verification**: Querying for orphaned dataset references in `raw_records` now returns **0 rows**. Referential integrity is 100%.

---

### Correction 4: Schema Inventory & Version Clarification
- **Issue**: Apparent contradictions between earlier documentation numbers (52 nodes, 31 relationships, 18 sources) and Phase 0.2 freeze numbers (41 nodes, 38 relationships, 12 sources).
- **Investigation & Root Cause**:
  1. **52 Nodes**: Phase 0.1 created an unpruned initial list of 52 food domain concepts. Phase 0.2 Decision D-03 consolidated these into **41 Node Entities** (25 Canonical + 16 Reified/Measurement). In Phase 2A reports, the author erroneously wrote "52 canonical nodes" by confusing it with the **52 passing unit tests** (`collected 52 items`).
  2. **31 Relationships**: Phase 0.1 proposed 31 direct relationships. Phase 0.2 Decision D-02 reified property measurements, constraint applications, and regulatory permissions, expanding the relationship count to **38 Canonical Relationships**.
  3. **18 Sources**: `config_v2/sources.yaml` defines **12 Approved External Sources**. Phase 2A.2 staged **18 source assets** in `source_assets`. The author conflated asset count with source count.
- **Action Taken**: Documented the definitive inventory in `PHASE_2A_3_SCHEMA_RECONCILIATION.csv`. Confirmed that `test_schema_consistency.py` rigorously validates:
  - `registry.nodes`: Exactly 41
  - `registry.relationships`: Exactly 38
  - `registry.sources`: Exactly 12

---

### Correction 5: Execution Tracking Lifecycle Cleanup
- **Issue**: `RUN-PHASE-2A-ACQUISITION-01` remained in `RUNNING` status in DuckDB `execution_runs`.
- **Action Taken**: Updated status to `COMPLETED` with timestamp. Registered execution `RUN-PHASE-2A-3-RECONCILIATION-01` tracking Phase 2A.3 corrections. Zero dangling runs remain.
