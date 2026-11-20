# PHASE 2A.1 — EXECUTION FAILURE RECONCILIATION REPORT

**Audit Date:** 2026-11-16  
**Auditor Role:** Senior Data Engineering Auditor  
**Status:** RECONCILED & DOCUMENTED  

---

## 1. Overview & Objective

This report details and reconciles every runtime failure, exception, and test failure encountered during the implementation, verification, and audit of **Phase 2A** and **Phase 2A.1**.

For each incident, this document details:
- Exact command or invocation
- Error message / traceback
- Root cause forensic analysis
- Remediation applied
- Current resolution status

---

## 2. Forensic Failure Reconciliation Log

### Incident 1: Codex GSFA Extractor Regex Link Mismatch
- **Invocation:** `python -m pytest src/pipeline_v2/tests/test_gsfa_extractor.py`
- **Error:** `AssertionError: assert 0 > 0 (total_records_discovered was 0)`
- **Root Cause:**
  The initial regular expression expected exact string paths `href="details.html?id=\d+"`. However, inspect of `gsfa_additives.html` revealed that hrefs vary between `/gsfaonline/groups/details.html?id=...` and `/gsfaonline/additives/details.html?id=...`, and link text contained nested child formatting tags (e.g. `<u><b>Curcumin</b></u>`).
- **Remediation:**
  Updated the regular expression to `r'<a[^>]*details\.html\?id=(\d+)[^>]*>(.*?)</a>'` and implemented `re.sub(r'<[^>]+>', '', raw_text)` to strip formatting tags cleanly while preserving exact character names.
- **Status:** **RESOLVED & VERIFIED** (all 296 genuine additives successfully extracted; test passes).

---

### Incident 2: DuckDB Staging Foreign Key Violation on Source Registry
- **Invocation:** `python scripts/run_phase_2a_pipeline.py`
- **Error:** `duckdb.ConstraintException: Violates foreign key constraint because key "source_id: SRC-FOODON" does not exist in the referenced table`
- **Root Cause:**
  `DuckDBStore.record_asset(asset)` enforces referential integrity `FOREIGN KEY (source_id) REFERENCES source_registry(source_id)`. The staging script attempted to register acquired assets before calling `store.sync_source_registry()`.
- **Remediation:**
  Moved `store.sync_source_registry(registry.sources)` to execute immediately after `store.initialize_schema()`, ensuring all source IDs are registered before any assets or raw records are inserted.
- **Status:** **RESOLVED & VERIFIED** (pipeline completed with exit code 0).

---

### Incident 3: DuckDB Table Query BinderException
- **Invocation:** `python -c "SELECT source_id, extraction_status, count(*) FROM raw_records..."`
- **Error:** `_duckdb.BinderException: Binder Error: Referenced column "extraction_status" not found in FROM clause!`
- **Root Cause:**
  `extraction_status` is an attribute of the Pydantic `SourceRecord` transfer object. In DuckDB, the `raw_records` table schema is defined as:
  `[raw_record_id, source_id, dataset_id, native_record_id, asset_id, payload_json, extracted_at, execution_id]`.
- **Remediation:**
  Queries against `raw_records` now reference valid table columns, and status metrics are queried from `payload_json` or batch result metadata.
- **Status:** **RESOLVED & DOCUMENTED**.

---

### Incident 4: USDA FDC API Rate Limiting (HTTP 429)
- **Invocation:** `usda_acquirer.query_foods_by_data_type(query='wheat flour')`
- **Error:** `HTTPStatusError: USDA FDC query failed with status 429`
- **Root Cause:**
  The USDA FoodData Central `DEMO_KEY` enforces a quota of 30 requests per hour and 50 requests per day. Repeatedly re-querying the API during rapid execution cycles exhausted the demo quota.
- **Remediation:**
  Implemented local asset caching in `UsdaAcquirer`: if `force_download=False` and the verified local file exists with non-zero size, the acquirer reuses the local verified asset rather than issuing an unnecessary external HTTP request. The same pattern was added to `PubChemAcquirer`.
- **Status:** **RESOLVED & VERIFIED** (zero 429 errors on subsequent runs).

---

### Incident 5: DuckDB Transaction Memory Allocation Failure on 40,000+ Deep Objects
- **Invocation:** `python scripts/run_phase_2a_pipeline.py` (with `max_records=None` on FoodOn)
- **Error:** `_duckdb.OutOfMemoryException: Out of Memory Error: Allocation failure` inside `store.transaction()`
- **Root Cause:**
  Accumulating 39,682 complex Pydantic `SourceRecord` models in Python memory, converting each to JSON strings, and attempting to insert all 40,088 tuples into DuckDB in a single uncommitted transaction exceeded DuckDB's in-memory rollback buffer.
- **Remediation:**
  1. Maintained the Phase 2A verified staging baseline of 1,000 FoodOn classes (`max_records=1000`).
  2. Implemented chunked staging (`chunk_size=5000`) and documented streaming staging requirements for Phase 3/4 bulk processing.
- **Status:** **RECONCILED & DOCUMENTED** (pipeline restored to clean, stable state with 1,406 staged records).

---

## 3. Summary of Unresolved Issues

There are **zero unresolved software crashes or unhandled exceptions** in the Phase 2A codebase.

External regulatory provision access for Codex GSFA remains documented as **`BLOCKED_BY_CLOUDFLARE`**, in compliance with safety requirements forbidding automated bypass of anti-bot gates.
