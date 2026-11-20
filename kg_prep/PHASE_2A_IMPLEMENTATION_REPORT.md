# PHASE 2A — IMPLEMENTATION REPORT: GENUINE SOURCE ACQUISITION & ISOLATED EXTRACTORS

## 1. Executive Summary

Phase 2A of the reconstructed Food Formulation Knowledge Graph preparation pipeline has been successfully implemented and verified under `kg_prep/src/pipeline_v2/`.

Following the frozen design contracts from Phase 0.2 (`PHASE_0_2_FINAL_SCHEMA_FREEZE.md`, `PHASE_0_2_DECISION_REGISTER.md`) and the core infrastructure established in Phase 1, Phase 2A integrates the first batch of four genuine external sources:
1. **FoodOn** (`SRC-FOODON`): The open-source Food Ontology (OWL RDF/XML).
2. **Codex GSFA** (`SRC-CODEX-GSFA`): Codex Alimentarius General Standard for Food Additives (CXS 192-1995).
3. **USDA FoodData Central** (`SRC-USDA-FDC`): Foundation Foods and SR Legacy nutrient profiles.
4. **NCBI PubChem** (`SRC-PUBCHEM`): Chemical compound structure and descriptor data via PUG REST.

### Key Metrics Achieved
- **Authentic Raw Assets Acquired and Manifested**: 16 assets registered with SHA-256 verification.
- **Genuine Source Records Extracted and Staged**: 1,406 records staged into DuckDB `raw_records`.
- **Synthetic Data Generated**: Exactly 0.
- **Modulo/Fabricated Category Mappings**: Exactly 0.
- **Legacy Pipeline Files Modified**: Exactly 0 (`kg_prep/src/` remains completely untouched).
- **Unit Test Suite**: 52 passed tests in 6.61 seconds (34 Phase 1 + 18 Phase 2A).

---

## 2. Source-by-Source Implementation Details

### A. FoodOn (`SRC-FOODON`)
- **Acquisition Component**: `src/pipeline_v2/acquisition/foodon_acquirer.py`
- **Extractor Component**: `src/pipeline_v2/extractors/foodon/extractor.py`
- **Raw Asset**: `data/raw_v2/foodon/foodon.owl` (40,429,965 bytes, SHA-256: `1e11fc50283c6498697a7aca9606c9d914f1cda71cc5510e006d949c32df7db0`).
- **Implementation Strategy**:
  - Reused verified genuine FoodOn OWL file located in local assets.
  - Implemented streaming XML parsing via `xml.etree.ElementTree.iterparse` targeting `owl:Class` elements to ensure constant $O(1)$ memory overhead over the 40.4 MB RDF/XML document.
  - Extracted complete native class URIs (e.g. `http://purl.obolibrary.org/obo/FOODON_00001002`), `rdfs:label`, `obo:IAO_0000115` (definitions), `oboInOwl:hasExactSynonym`, `rdfs:subClassOf` parent class URIs, `owl:deprecated` flags, replacement terms (`term_replaced_by`), and external database cross-references (`hasDbXref`).
  - Preserved full taxonomy without assuming every class is an ingredient and without heuristics.
- **Batch Extracted**: 1,000 authentic OWL classes staged to DuckDB `raw_records`.

### B. Codex GSFA (`SRC-CODEX-GSFA`)
- **Acquisition Component**: `src/pipeline_v2/acquisition/gsfa_acquirer.py`
- **Extractor Component**: `src/pipeline_v2/extractors/gsfa/extractor.py`
- **Raw Asset**: `data/raw_v2/gsfa/gsfa_additives.html` (49,430 bytes, SHA-256: `ff06587e0d5abdc84e6b6a2650964013a34fc80f4483880052ee8f124679fae8`).
- **Forensic Findings & Anti-Bot Protection**:
  - Legacy directory contained `CXS_192e.pdf` and `ins/CXG_036e.pdf` which were discovered to be corrupt 1-page Microsoft login redirect HTML pages (3,190 bytes). These were discarded.
  - Probing the live remote portal `https://www.fao.org/gsfaonline/` revealed an active **Cloudflare Turnstile anti-bot challenge** returning HTTP 403.
  - In strict compliance with system rules, prompt constraints, and safety guidelines, the automated pipeline did not attempt to bypass or spoof this gate. Status `BLOCKED_BY_CLOUDFLARE` was recorded.
  - The genuine local HTML additive index (`gsfa_additives.html`, containing 285+ genuine entries) was acquired and ingested.
- **Extractor Logic**:
  - Extracted additive name, official GSFA additive ID, and INS number (e.g., `INS 100(i)` Curcumin, `INS 101(i)` Riboflavin).
  - Striped nested formatting tags cleanly without string corruption.
  - **Zero synthetic provisions**: Discarded legacy modulo-based category assignments (`INS_NUM % 16`) and random max use levels. Only genuine additive identity records were staged.
- **Batch Extracted**: 296 authentic food additives staged to DuckDB `raw_records`.

### C. USDA FoodData Central (`SRC-USDA-FDC`)
- **Acquisition Component**: `src/pipeline_v2/acquisition/usda_acquirer.py`
- **Extractor Component**: `src/pipeline_v2/extractors/usda/extractor.py`
- **Acquired Assets**:
  - `fdc_search_milk.json` (936,392 bytes, SHA-256: `09d9362e...`)
  - `fdc_search_egg.json` (896,718 bytes, SHA-256: `e7468ce0...`)
  - `fdc_search_wheat_flour.json` (907,756 bytes, SHA-256: `70f49418...`)
  - `fdc_search_cheddar_cheese.json` (1,057,863 bytes, SHA-256: `c38f1cd8...`)
  - `fdc_search_soybean_oil.json` (718,019 bytes, SHA-256: `bda1db5e...`)
  - `fdc_search_sucrose.json` (55,179 bytes, SHA-256: `b518af85...`)
- **Decision D-01 Compliance**:
  - Search queries strictly requested `dataType=Foundation,SR Legacy`.
  - The extractor strictly enforces Decision D-01: any food item with `dataType == "Branded"` is immediately rejected with reason `OUT_OF_SCOPE_DATA_TYPE:Branded`.
- **Extracted Fields**:
  - Food description, FDC ID, NDB number, publication date, food category.
  - Complete nutrient array: nutrient ID, nutrient name, nutrient number, unit name (e.g. `G`, `MG`, `UG`), per-100g amount, derivation code, and value.
  - Portions array: gram weight, portion description, modifier, measure unit.
- **Batch Extracted**: 102 authentic food nutrient profiles staged to DuckDB `raw_records` (0 rejected, 0 fabricated).

### D. NCBI PubChem (`SRC-PUBCHEM`)
- **Acquisition Component**: `src/pipeline_v2/acquisition/pubchem_acquirer.py`
- **Extractor Component**: `src/pipeline_v2/extractors/pubchem/extractor.py`
- **Acquired Assets**: 8 JSON assets covering foundational food compounds:
  - CID 1183 (Vanillin, 7,490 bytes, SHA-256: `313947da...`)
  - CID 2519 (Caffeine, 13,963 bytes, SHA-256: `0ef9c3f6...`)
  - CID 311 (Citric acid, 9,506 bytes, SHA-256: `31b203d2...`)
  - CID 5988 (Sucrose, 9,362 bytes, SHA-256: `0f73f61f...`)
  - CID 54670067 (L-Ascorbic acid / Vitamin C, 11,348 bytes, SHA-256: `46387131...`)
  - CID 712 (Sodium benzoate, 5,056 bytes, SHA-256: `e44bc7ab...`)
  - CID 23665764 (Potassium sorbate, 728 bytes, SHA-256: `91020a7e...`)
  - CID 104 (Glycine, 958 bytes, SHA-256: `d0bd5591...`)
- **API Throttling & Politeness**:
  - Implemented polite client-side rate limiting enforcing a minimum delay of 0.25 seconds between requests (<= 4 requests/sec, well within NCBI's 5 req/sec limit).
  - Fetched official compound properties and up to 30 curated synonyms per compound.
- **Extracted Fields**:
  - CID, Molecular Formula, Molecular Weight, Canonical SMILES, Isomeric SMILES, InChI, InChIKey, IUPAC Name, XLogP, Exact Mass, Charge, Heavy Atom Count, Synonyms.
- **Batch Extracted**: 8 authentic chemical compound records staged to DuckDB `raw_records`.

---

## 3. Data Integrity & Staging Architecture

### DuckDB Staging Integration
- **Database File**: `data/intermediate_v2/kg_staging.duckdb`
- **Table Populated**: `raw_records`
  - Total records: **1,406**
  - Schema:
    - `raw_record_id` (PRIMARY KEY, e.g. `RAW-SRC-FOODON-...`)
    - `source_id` (FOREIGN KEY -> `source_registry.source_id`)
    - `dataset_id` (STRING)
    - `native_record_id` (STRING)
    - `asset_id` (FOREIGN KEY -> `source_assets.asset_id`)
    - `payload_json` (JSON string containing full source-native payload)
    - `extracted_at` (TIMESTAMP)
    - `execution_id` (FOREIGN KEY -> `execution_runs.execution_id`)
- **Asset Provenance**:
  - Populated `source_assets` with 16 rows.
  - Linked to execution run `RUN-PHASE-2A-ACQUISITION-01`.
  - Enforced strict foreign key constraints; `sync_source_registry()` executed prior to staging.

### Manifest Manager Serialization
- Manifest updated and written to:
  - `data/manifests_v2/phase_2a_manifest.json`
  - `data/manifests_v2/phase_2a_manifest.csv`
- Tracks all 16 acquired assets with exact byte lengths and SHA-256 checksums.

---

## 4. Deliverables Index

| Deliverable | Path | Mirrored Path |
| :--- | :--- | :--- |
| Implementation Report | [PHASE_2A_IMPLEMENTATION_REPORT.md](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/PHASE_2A_IMPLEMENTATION_REPORT.md) | [reports/phase_2a/PHASE_2A_IMPLEMENTATION_REPORT.md](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/reports/phase_2a/PHASE_2A_IMPLEMENTATION_REPORT.md) |
| Source Acquisition Report | [PHASE_2A_SOURCE_ACQUISITION_REPORT.csv](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/PHASE_2A_SOURCE_ACQUISITION_REPORT.csv) | [reports/phase_2a/PHASE_2A_SOURCE_ACQUISITION_REPORT.csv](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/reports/phase_2a/PHASE_2A_SOURCE_ACQUISITION_REPORT.csv) |
| Extraction Statistics | [PHASE_2A_EXTRACTION_STATISTICS.csv](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/PHASE_2A_EXTRACTION_STATISTICS.csv) | [reports/phase_2a/PHASE_2A_EXTRACTION_STATISTICS.csv](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/reports/phase_2a/PHASE_2A_EXTRACTION_STATISTICS.csv) |
| Rejected Records Report | [PHASE_2A_REJECTED_RECORDS.csv](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/PHASE_2A_REJECTED_RECORDS.csv) | [reports/phase_2a/PHASE_2A_REJECTED_RECORDS.csv](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/reports/phase_2a/PHASE_2A_REJECTED_RECORDS.csv) |
| Source Coverage Report | [PHASE_2A_SOURCE_COVERAGE_REPORT.csv](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/PHASE_2A_SOURCE_COVERAGE_REPORT.csv) | [reports/phase_2a/PHASE_2A_SOURCE_COVERAGE_REPORT.csv](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/reports/phase_2a/PHASE_2A_SOURCE_COVERAGE_REPORT.csv) |
| Provenance Verification | [PHASE_2A_PROVENANCE_VERIFICATION.md](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/PHASE_2A_PROVENANCE_VERIFICATION.md) | [reports/phase_2a/PHASE_2A_PROVENANCE_VERIFICATION.md](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/reports/phase_2a/PHASE_2A_PROVENANCE_VERIFICATION.md) |
| Test Report | [PHASE_2A_TEST_REPORT.md](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/PHASE_2A_TEST_REPORT.md) | [reports/phase_2a/PHASE_2A_TEST_REPORT.md](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/reports/phase_2a/PHASE_2A_TEST_REPORT.md) |
| Known Limitations | [PHASE_2A_KNOWN_LIMITATIONS.md](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/PHASE_2A_KNOWN_LIMITATIONS.md) | [reports/phase_2a/PHASE_2A_KNOWN_LIMITATIONS.md](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/reports/phase_2a/PHASE_2A_KNOWN_LIMITATIONS.md) |
