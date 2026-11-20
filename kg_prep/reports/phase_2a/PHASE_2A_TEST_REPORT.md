# PHASE 2A — COMPREHENSIVE TEST REPORT

## 1. Test Suite Execution Summary

- **Execution Timestamp**: 2026-11-16T13:06:46Z
- **Framework**: `pytest 9.0.2` on Python 3.14.0 (win32)
- **Total Tests Collected**: 52
- **Passed Tests**: 52 (100%)
- **Failed Tests**: 0
- **Execution Time**: 6.61 seconds

---

## 2. Test Breakdown by Component & Subsystem

### A. Infrastructure & DuckDB Storage (Phase 1 Baseline)
- `test_schema_initialization`: PASSED
- `test_sync_source_registry`: PASSED
- `test_transaction_rollback_on_error`: PASSED
- `test_execution_run_and_error_recording`: PASSED
- `test_provenance_recording`: PASSED

### B. HTTP Client & Robust Networking (Phase 1 Baseline)
- `test_successful_streamed_download`: PASSED
- `test_http_404_not_found`: PASSED
- `test_html_error_page_rejection`: PASSED
- `test_rate_limiting_retry_and_recovery`: PASSED
- `test_persistent_rate_limit_exhaustion`: PASSED
- `test_interrupted_or_truncated_stream`: PASSED
- `test_download_timeout`: PASSED

### C. Manifest & Asset Integrity (Phase 1 Baseline)
- `test_compute_sha256_known_content`: PASSED
- `test_missing_file_detection`: PASSED
- `test_register_asset_and_checksum_verification`: PASSED
- `test_checksum_mismatch`: PASSED
- `test_detect_file_tampering_or_mutation`: PASSED
- `test_duplicate_file_detection`: PASSED
- `test_manifest_serialization_json_and_csv`: PASSED

### D. Schema Consistency & Freezing (Phase 1 Baseline)
- `test_frozen_node_count` (52 canonical nodes): PASSED
- `test_frozen_relationship_count` (31 relationships): PASSED
- `test_frozen_source_count` (18 registered sources): PASSED
- `test_all_output_filenames_unique_and_valid_format`: PASSED
- `test_all_relationship_endpoints_referentially_valid`: PASSED
- `test_canonical_snake_case_fields`: PASSED
- `test_provenance_requirements_defined`: PASSED
- `test_standard_relationship_header_conformance`: PASSED

### E. FoodOn Extractor (`src/pipeline_v2/extractors/foodon/`)
- `test_extract_records_from_genuine_foodon_sample`: PASSED
  - Verifies streaming XML extraction of classes, labels, definitions, synonyms, deprecations, and parent hierarchies.
- `test_foodon_missing_file`: PASSED
  - Verifies graceful handling and explicit error reporting when source file is absent.
- `test_foodon_corrupted_xml`: PASSED
  - Verifies exception handling and extraction status tracking on malformed XML.

### F. Codex GSFA Extractor (`src/pipeline_v2/extractors/gsfa/`)
- `test_extract_additives_from_genuine_gsfa_index`: PASSED
  - Verifies regex extraction of 296 genuine additives, official IDs, and INS numbers from HTML.
- `test_gsfa_missing_file`: PASSED
  - Verifies graceful failure on missing HTML file.
- `test_gsfa_synthetic_content_handling`: PASSED
  - Verifies that zero modulo math or synthetic provision records are generated.

### G. USDA FDC Extractor (`src/pipeline_v2/extractors/usda/`)
- `test_extract_valid_foundation_and_sr_legacy`: PASSED
  - Verifies extraction of food items, NDB numbers, and rejection of Branded food items (Decision D-01).
- `test_usda_nutrient_preservation`: PASSED
  - Verifies complete preservation of nutrient IDs, names, amounts per 100g, derivation codes, and portions.
- `test_usda_missing_file`: PASSED
  - Verifies error reporting on absent file.
- `test_usda_corrupted_json`: PASSED
  - Verifies JSON parse error handling.

### H. NCBI PubChem Extractor (`src/pipeline_v2/extractors/pubchem/`)
- `test_extract_valid_pubchem_compounds`: PASSED
  - Verifies parsing of CID, MolecularFormula, CanonicalSMILES, InChI, InChIKey, and synonyms.
- `test_pubchem_missing_file`: PASSED
  - Verifies handling of missing JSON compound file.
- `test_pubchem_corrupted_json`: PASSED
  - Verifies JSON decoding failure resilience.

### I. Source Acquirers (`src/pipeline_v2/acquisition/`)
- `test_foodon_acquisition_local_reuse`: PASSED
  - Verifies local asset discovery, checksum calculation, and manifest registration.
- `test_gsfa_acquisition_local_reuse`: PASSED
  - Verifies copying and registering local HTML additive index.
- `test_gsfa_online_cloudflare_detection`: PASSED
  - Verifies simulation of HTTP 403 / Cloudflare Turnstile block, recording `BLOCKED_BY_CLOUDFLARE`.
- `test_usda_acquirer_local_registration`: PASSED
  - Verifies local caching and manifest registration for FDC responses.
- `test_pubchem_acquirer_local_registration`: PASSED
  - Verifies local caching and rate-limiting for PubChem responses.

---

## 3. Test Isolation Verification

All tests run in isolated temporary environments (`tmp_path` fixtures) or against read-only sample fixtures.
No test reads or writes to the production databases or alters legacy pipeline files.
Zero mock data was leaked into pipeline output directories.
