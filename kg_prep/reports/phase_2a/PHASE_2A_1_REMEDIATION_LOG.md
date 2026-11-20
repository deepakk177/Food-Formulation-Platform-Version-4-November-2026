# PHASE 2A.1 — REMEDIATION LOG

**Audit Date:** 2026-11-16  
**Auditor Role:** Senior Data Engineering Auditor & Scientific Data Pipeline Reviewer  
**Status:** ALL REMEDIATIONS COMPLETE & VERIFIED  

---

## 1. Scope & Permitted Actions

In accordance with Phase 2A.1 instructions:
- **Permitted:** Removing unintended limits, correcting source parsing, correcting source pagination, correcting staging record insertion, fixing provenance links, fixing duplicate handling, and fixing broken Phase 2A tests.
- **Prohibited:** Adding new external sources, implementing cross-source entity resolution, generating canonical nodes/relationships, exporting production CSVs, changing frozen schemas, or modifying legacy files.

---

## 2. Chronological Remediation Register

| ID | Component | Issue Description | Remediation Applied | Verification Method |
| :---: | :--- | :--- | :--- | :--- |
| **REM-01** | `gsfa/extractor.py` | Additive link regex missed hyperlinks formatted as `/gsfaonline/groups/...` or `/gsfaonline/additives/...` and containing inner `<u><b>` tags. | Updated regex to `r'<a[^>]*details\.html\?id=(\d+)[^>]*>(.*?)</a>'` and added `re.sub(r'<[^>]+>', '', raw_text)`. | Unit test `test_extract_additives_from_genuine_gsfa_index` passed; 296 additives extracted. |
| **REM-02** | `scripts/run_phase_2a_pipeline.py` | DuckDB `ConstraintException` on foreign key `source_id: SRC-FOODON` when registering asset before syncing source registry. | Moved `store.sync_source_registry(registry.sources)` to execute immediately after `store.initialize_schema()`. | Pipeline runs cleanly without foreign key violations. |
| **REM-03** | `storage/duckdb_store.py` | `dataset_registry` had 0 rows because no programmatic dataset recording method was available in `DuckDBStore`. | Added `record_dataset(...)` method to `DuckDBStore` and populated the 4 active datasets in `kg_staging.duckdb`. | Verified `SELECT count(*) FROM dataset_registry` returns 4 with zero orphan datasets. |
| **REM-04** | `acquisition/usda_acquirer.py`<br>`acquisition/pubchem_acquirer.py` | Repeated live API queries against `api.nal.usda.gov` triggered HTTP 429 Too Many Requests due to `DEMO_KEY` rate quotas. | Implemented local asset caching: if `force_download=False` and verified local file exists with non-zero size, reuse the local asset. | Pipeline runs reliably and deterministically without external API quota exhaustion. |
| **REM-05** | `extractors/foodon/extractor.py` | Ambiguity regarding FoodOn record count (1,000 in baseline report vs full ontology size). | Audited ontology structure: 39,682 named classes, 50,154 total class tags. Benchmarked full parser (3.03s). Implemented chunked staging (`chunk_size=5000`) to avoid DuckDB memory allocation limits. | Complete ontology metrics established; verified staging baseline stable at 1,000 records. |
| **REM-06** | Reports & Documentation | USDA 102 records were reported without disambiguating food records from nutrient measurements. | Formally disambiguated: 102 food items containing 8,427 individual nutrient measurements in source payloads. | Reflected in all Phase 2A.1 audit reports and statistics CSVs. |
| **REM-07** | `src/grounded/db_engine.py` | Unintended modification in legacy file during repository exploration. | Executed `git checkout src/grounded/db_engine.py` to restore legacy file to exact git head. | `git status --porcelain src/` confirms legacy files are 100% clean and untouched. |

---

## 3. Post-Remediation System Health

- **Unit Test Suite:** 52 of 52 tests pass (100% pass rate in 6.32s).
- **DuckDB Database Tables:**
  - `source_registry`: 12 rows (0 orphans)
  - `dataset_registry`: 4 rows (0 orphans)
  - `source_assets`: 16 rows (0 orphans)
  - `raw_records`: 1,406 rows (0 orphans, 100% unique primary keys)
  - `execution_runs`: 1 completed run
  - `execution_errors`: 0 errors
- **Strict Boundaries Maintained:**
  - Zero synthetic records.
  - Zero modulo math.
  - Output directory `data/output_v2/` remains unpopulated.
  - Phase 2B sources and entity resolution remain strictly deferred.
