# PHASE 0.1 / 0.2: STATUS OF ARCHITECTURAL DECISIONS

**Document Version:** 2.0.0 (Phase 0.2 Revision)  
**Status:** ALL STRATEGIC DECISIONS RATIFIED  
**Reference:** See [PHASE_0_2_DECISION_REGISTER.md](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/PHASE_0_2_DECISION_REGISTER.md)  

---

## 1. Resolution of Phase 0.1 Open Decisions

All five strategic decisions presented in Phase 0.1 have been reviewed and ratified:

| Decision ID | Domain | Ratified Choice | Status |
|---|---|---|---|
| **D-01** | USDA Ingestion Scope | **Option A**: Foundation Foods + SR Legacy Only (~10,000 foods, ~60 MB). Excludes commercial branded foods. | **RESOLVED & FROZEN** |
| **D-02** | Codex GSFA Provisions | **Option A**: Targeted official provision extraction for core categories (Dairy 01.0, Fats/Oils 02.0, Confectionery 05.0, Cereals 06.0, Bakery 07.0, Beverages 14.0). | **RESOLVED & FROZEN** |
| **D-03** | Gated Datasets Strategy | **Option A**: Register in `source_registry.yaml` with explicit status (`AUTHENTICATION_REQUIRED`, `MANUAL_REVIEW_REQUIRED`) and skip gracefully without generating mock records. | **RESOLVED & FROZEN** |
| **D-04** | Missing Values & Solver Safety | **Option A**: Strict Null Safety (no imputation in candidate pool; strict gating in candidate engine; missing costs report `COST_UNKNOWN`). | **RESOLVED & FROZEN** |
| **D-05** | Output CSV Header Schema | **Option A**: Canonical lowercase `snake_case` schema across all CSVs; legacy compatibility adapters deferred to Phase 8 backend integration. | **RESOLVED & FROZEN** |

---

## 2. Technical Implementation Notes for Phase 1

With all strategic decisions ratified, the following technical implementation considerations are frozen for Phase 1:

1. **Configuration Structure**:
   `config_v2/` will contain:
   - `source_registry.yaml`: Authority endpoints, licenses, access modes, and authentication states.
   - `node_schemas.yaml`: Strict column names, data types, mandatory keys for all frozen nodes.
   - `relationship_schemas.yaml`: Validated endpoints, allowed edge types, directional constraints.
   - `normalizer_rules.yaml`: Dimensional conversion factors and controlled synonym dictionaries.
2. **DuckDB Analytical Store**:
   `grounded_food_knowledge.duckdb` schema initialized with tables for `datasets`, `source_files`, `raw_records`, `normalized_records`, `provenance`, `entity_mappings`, `relationships`, `conflicts`, `rejected_records`, and `pipeline_runs`.
3. **Execution Safety**:
   Zero legacy files will be overwritten during Phase 1–7. The new implementation resides in `src/pipeline_v2/` and outputs to `data/output_v2/`.
