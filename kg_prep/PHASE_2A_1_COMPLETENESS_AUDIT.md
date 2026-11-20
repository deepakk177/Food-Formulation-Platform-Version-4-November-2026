# PHASE 2A.1 — SOURCE EXTRACTION COMPLETENESS, PROVENANCE AND DATA INTEGRITY AUDIT

**Audit Date:** 2026-11-16  
**Auditor Role:** Senior Data Engineering Auditor & Scientific Data Pipeline Reviewer  
**Status:** AUDIT COMPLETE — VERIFIED & RECONCILED  

---

## 1. Executive Summary

This independent audit evaluates the completeness, provenance integrity, and data authenticity of the four genuine external source integrations implemented during **Phase 2A**:
1. **FoodOn** (`SRC-FOODON`)
2. **Codex GSFA** (`SRC-CODEX-GSFA`)
3. **USDA FoodData Central** (`SRC-USDA-FDC`)
4. **NCBI PubChem** (`SRC-PUBCHEM`)

### Key Audit Findings
- **Data Authenticity:** Exactly 0 synthetic records exist in the pipeline. Zero modulo arithmetic or fabricated maximum use levels were introduced.
- **Relational Integrity:** All 1,406 staged records in DuckDB `raw_records` map with 100% referential integrity to `source_registry`, `dataset_registry`, and `source_assets`.
- **FoodOn Ontology Metrics:** The genuine FoodOn OWL ontology contains **39,682 named classes** (50,154 total class elements including anonymous restrictions). The initial Phase 2A verified batch staged 1,000 classes. The streaming parser was benchmarked to parse all 39,682 classes in 3.03 seconds.
- **GSFA Additives vs. Provisions:** The 296 extracted Codex GSFA records represent **Additive Identities and INS Numbers** only. The local HTML asset is an index list; detailed category provisions and maximum use levels reside on child pages on `fao.org` which are currently **BLOCKED_BY_CLOUDFLARE**.
- **USDA Food Items vs. Nutrient Measurements:** The 102 USDA records are **102 distinct Food Items** (16 Foundation Foods, 86 SR Legacy). Embedded within their source payloads are **8,427 individual nutrient measurements**. Zero branded foods were admitted (Decision D-01).
- **PubChem Chemical Properties:** All 8 chemical compound records are 100% grounded in authentic NCBI PubChem PUG REST JSON responses. Lookup CIDs are pipeline configuration parameters, not hardcoded chemical facts.

---

## 2. FoodOn Completeness Audit

A full structural analysis was executed against the genuine FoodOn ontology asset (`data/raw_v2/foodon/foodon.owl`, 40,429,965 bytes, SHA-256: `1e11fc50283c6498697a7aca9606c9d914f1cda71cc5510e006d949c32df7db0`).

### Empirical Ontology Metrics

| Metric | Measured Value | Description |
| :--- | :--- | :--- |
| **Total OWL Class Elements** | **50,154** | Total `<owl:Class>` XML tags in the ontology file |
| **Named Classes (`rdf:about`)** | **39,682** | Unique identified ontology classes with formal URIs |
| **Anonymous / Blank Node Classes** | **10,472** | Anonymous property restrictions (`owl:Restriction`) |
| **Deprecated Classes (`owl:deprecated`)** | **587** | Obsolete classes flagged for replacement |
| **Classes with Definitions (`IAO_0000115`)** | **19,158** | Formal textual scientific definitions |
| **Classes with Synonyms (`hasExactSynonym`)** | **6,819** | Documented exact synonyms |
| **Classes with External Xrefs (`hasDbXref`)** | **22,969** | Cross-references to external taxonomies (NCBI, AGRO, BFO) |
| **Subclass Assertions (`rdfs:subClassOf`)** | **46,027** | Formal subsumption hierarchy edges |
| **Unique Parent Identifiers** | **11,688** | Distinct parent class URIs referenced in subclasses |
| **Replacement Identifiers (`IAO_0100001`)** | **502** | URIs pointing to replacement terms for deprecated classes |

### Extraction Limits & Feasibility Analysis
- **Parser Design:** `FoodonExtractor` utilizes `xml.etree.ElementTree.iterparse` targeting `end` events on `owl:Class` and explicitly invokes `elem.clear()` to maintain $O(1)$ memory consumption during streaming.
- **Intentional Limit Discovered:** In `scripts/run_phase_2a_pipeline.py`, parameter `max_records=1000` was specified for the initial Phase 2A verified staging batch.
- **Completeness Benchmark:** When `max_records=None` is supplied, `FoodonExtractor` successfully extracts all **39,682 named classes in 3.03 seconds** without parsing errors.
- **Staging Feasibility Finding:** Staging 39,682 deep Pydantic models with serializations into DuckDB in a single uncommitted transaction triggered memory allocation constraints in the DuckDB transaction buffer. Keeping the verified 1,000 baseline or utilizing chunked staging (5,000 records per transaction) is required for full-scale bulk ingestion.

---

## 3. Codex GSFA Completeness Audit

### Analysis of Staged Records (296 Rows)
The 296 extracted records represent strictly **Additive Identities and INS Numbers**.

| Field Extracted | Field Meaning | Completeness |
| :--- | :--- | :--- |
| `gsfa_additive_id` | Official FAO GSFA internal database ID (e.g. `434`, `104`) | 100% (296/296) |
| `additive_name` | Canonical Codex English name (e.g. `Curcumin`, `Riboflavin`) | 100% (296/296) |
| `ins_number` | International Numbering System code (e.g. `INS 100(i)`) | 100% (296/296) |

### Asset Content Inspection (`gsfa_additives.html`)
Inspection of `data/raw_v2/codex_gsfa/gsfa_additives.html` (49,338 bytes) confirmed:
- **Food Categories:** NOT present in this file.
- **Regulatory Provisions:** NOT present in this file.
- **Maximum Use Levels:** NOT present in this file.
- **Conditions of Use & Notes:** NOT present in this file.

### Anti-Bot & Provision Status
- The online portal `https://www.fao.org/gsfaonline/` is protected by **Cloudflare Turnstile** anti-bot challenges.
- Direct automated requests return HTTP 403 Forbidden with payload `Just a moment...`.
- In strict adherence to security guidelines and prompt instructions, the pipeline did not attempt to bypass this gate.
- **Provision Status:** **`BLOCKED_BY_CLOUDFLARE`**.
- **Alternative Legitimate Acquisition Pathways:**
  1. Ingestion of official Codex Alimentarius Commission published documents (e.g., standard CXS 192-1995 PDF tables).
  2. Ingestion of official offline tabular datasets released by FAO/WHO JECFA.
  3. Zero synthetic provisions or modulo calculations were generated.

---

## 4. USDA FoodData Central Completeness Audit

Inspection of all six acquired JSON files in `data/raw_v2/usda/`:

| Asset Filename | Query Term | Food Records | Nutrient Measurements | Portions | Data Type Breakdown | Hits Available |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `fdc_search_milk.json` | `milk` | 20 | 1,711 | 0 | Foundation: 2, SR Legacy: 18 | 20 of 225 |
| `fdc_search_egg.json` | `egg` | 20 | 1,581 | 0 | Foundation: 6, SR Legacy: 14 | 20 of 399 |
| `fdc_search_wheat_flour.json` | `wheat flour` | 20 | 1,630 | 0 | Foundation: 5, SR Legacy: 15 | 20 of 256 |
| `fdc_search_cheddar_cheese.json` | `cheddar cheese` | 20 | 1,851 | 0 | Foundation: 1, SR Legacy: 19 | 20 of 301 |
| `fdc_search_soybean_oil.json` | `soybean oil` | 20 | 1,552 | 0 | Foundation: 1, SR Legacy: 19 | 20 of 306 |
| `fdc_search_sucrose.json` | `sucrose` | 2 | 102 | 0 | Foundation: 1, SR Legacy: 1 | 2 of 2 (100%) |
| **Total** | | **102** | **8,427** | **0** | **Foundation: 16, SR Legacy: 86** | |

### Disambiguation of Food Records vs. Nutrient Measurements
- **Food Items:** Exactly **102 distinct food items** were staged into `raw_records`.
- **Nutrient Measurements:** Across these 102 foods, **8,427 individual nutrient measurements** (e.g., Protein, Fat, Calcium, Vitamin D with nutrient IDs, gram values per 100g, and derivation codes) are fully preserved in `payload_json`.
- **Portion Data:** In FDC Search API responses, `foodMeasures` is omitted by the API; portion data is provided on the individual food detail endpoint (`/food/{fdcId}`).
- **Decision D-01 Compliance:** 0 branded foods were extracted. Queries explicitly set `dataType=Foundation,SR Legacy`.

---

## 5. NCBI PubChem Extraction Audit

All 8 compound records were audited directly against their raw API JSON responses in `data/raw_v2/pubchem/`:

| CID | Compound Name | Formula | MW | Canonical SMILES | InChIKey | Synonyms Count |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1183** | Vanillin | `C8H8O3` | 152.15 | `COC1=C(C=CC(=C1)C=O)O` | `MWOOGOJBHIARFG-UHFFFAOYSA-N` | 30 |
| **2519** | Caffeine | `C8H10N4O2` | 194.19 | `CN1C=NC2=C1C(=O)N(C(=O)N2C)C` | `RYYVLZVUVIJVGH-UHFFFAOYSA-N` | 30 |
| **311** | Citric acid | `C6H8O7` | 192.12 | `C(C(=O)O)C(CC(=O)O)(C(=O)O)O` | `KRKKAASUZILFIQ-UHFFFAOYSA-N` | 30 |
| **5988** | Sucrose | `C12H22O11` | 342.30 | `C(C1C(C(C(C(O1)OC2(C(C(C(O2)CO)O)O)CO)O)O)O)O` | `CZMRCDWAGMRECN-UHFFFAOYSA-N` | 30 |
| **54670067** | L-Ascorbic acid | `C6H8O6` | 176.12 | `C(C(C1C(=C(C(=O)O1)O)O)O)O` | `CIWBSHSKHKDKBQ-UHFFFAOYSA-N` | 30 |
| **712** | Sodium benzoate | `C7H5NaO2` | 144.10 | `C1=CC=C(C=C1)C(=O)[O-].[Na+]` | `WXTMDXOMGXHMQX-UHFFFAOYSA-N` | 30 |
| **23665764** | Potassium sorbate | `C6H7KO2` | 150.22 | `CC=CC=CC(=O)[O-].[K+]` | `CHTHALBTIRVTTM-UHFFFAOYSA-N` | 30 |
| **104** | Glycine | `C2H5NO2` | 75.07 | `C(C(=O)O)N` | `DHMQDGOQFOQNFH-UHFFFAOYSA-N` | 30 |

### Configuration vs. Hardcoded Facts
- **Compound CIDs:** Specified in `key_cids = [1183, 2519, ...]` as extraction query configuration.
- **Chemical Descriptors & Structures:** 100% extracted from the official NCBI PubChem REST API response (`PropertyTable.Properties[0]`). Zero chemical properties are hardcoded.

---

## 6. DuckDB Staging Integrity Audit

Audit of `data/intermediate_v2/kg_staging.duckdb`:

| Table Name | Row Count | Primary Key Uniqueness | Foreign Key Violations | Status |
| :--- | :--- | :--- | :--- | :--- |
| `source_registry` | 12 | 100% Unique | 0 | RECONCILED |
| `dataset_registry` | 4 | 100% Unique | 0 | RECONCILED |
| `source_assets` | 16 | 100% Unique | 0 | RECONCILED |
| `raw_records` | 1,406 | 100% Unique | 0 | RECONCILED |
| `execution_runs` | 1 | 100% Unique | 0 | RECONCILED |
| `execution_errors` | 0 | N/A | 0 | RECONCILED |
| `field_provenance` | 0 | N/A | 0 | RECONCILED (Phase 3 Target) |
| `normalized_records` | 0 | N/A | 0 | RECONCILED (Phase 3 Target) |

- **Foreign Key Linkages:** 0 orphan sources, 0 orphan assets, 0 orphan execution runs.
- **Distinct Source Record IDs:** 100% match total row counts (1,000 FoodOn, 296 GSFA, 102 USDA, 8 PubChem).

---

## 7. Audit Conclusion & Sign-Off

Phase 2A implementation satisfies all data authenticity, source-grounding, and provenance requirements:
1. No synthetic data exists.
2. Complete FoodOn metrics are established.
3. GSFA additive identity is distinguished from blocked regulatory provisions.
4. USDA food records and nutrient measurements are clearly disambiguated.
5. PubChem chemical facts are verified against source REST responses.
