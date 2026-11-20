# PHASE 2A — KNOWN LIMITATIONS AND BLOCKERS REPORT

## 1. Scope & Objective

This document catalogs all known technical limitations, external blockers, rate limits, and boundary conditions encountered during **Phase 2A (Genuine Source Acquisition and Isolated Extractors)** of the Food Formulation Knowledge Graph reconstruction.

---

## 2. Source-Specific Limitations & External Blockers

### A. Codex GSFA Online Anti-Bot Protection (`SRC-CODEX-GSFA`)
- **Limitation**: The official FAO Codex GSFA Online search portal (`https://www.fao.org/gsfaonline/`) is protected by **Cloudflare Turnstile** anti-bot challenges.
- **Observed Behavior**: HTTP requests from automated clients receive HTTP 403 Forbidden with payload `Just a moment...` and a JavaScript challenge.
- **Architectural Policy**:
  - In strict compliance with safety directives, prompt constraints, and anti-circumvention rules, the pipeline **NEVER** bypasses, solves, or hacks anti-bot gates.
  - The status was logged as `BLOCKED_BY_CLOUDFLARE`.
- **Impact on Phase 2A**:
  - The genuine local additive index (`gsfa_additives.html`, 49,430 bytes, 296 genuine additives) was successfully acquired and extracted.
  - Fine-grained additive-foodcategory permission provisions (e.g. GMP maximum levels, specific category permissions) cannot be crawled dynamically from this remote web endpoint.
- **Mitigation for Future Phases**:
  - Acquire official published GSFA offline PDF tables or machine-readable exports, or ingest parsed tables through sanctioned offline ETL pathways rather than web scraping.
  - Zero synthetic provisions were generated to mask this limitation.

### B. USDA FoodData Central Rate Limits & Query Coverage (`SRC-USDA-FDC`)
- **Limitation**: USDA FDC API enforces rate limits on `DEMO_KEY` (30 requests/hour and 50 requests/day).
- **Observed Behavior**: Burst queries exceeding the quota result in HTTP 429 Too Many Requests.
- **Mitigation Implemented**:
  - Targeted staple food queries (`milk`, `egg`, `wheat flour`, `cheddar cheese`, `soybean oil`, `sucrose`) were retrieved, cached locally, and manifested.
  - In future bulk ingestion phases, a production API key from `api.data.gov` or the official bulk CSV/JSON dumps (e.g. `FoodData_Central_foundation_food_csv.zip`) should be utilized for offline bulk extraction.

### C. FoodOn Initial Batch Scaling (`SRC-FOODON`)
- **Limitation**: The full FoodOn ontology (`foodon.owl`) contains over 30,000 classes and is 40.4 MB in size.
- **Implementation Behavior**:
  - The streaming `iterparse` extractor was configured to stream an initial batch of 1,000 authentic classes to populate DuckDB `raw_records` without saturating intermediate memory during isolated extractor verification.
  - The streaming parser is completely scalable and capable of streaming the full 30,000+ classes without memory bloat in batch processing phases.

### D. NCBI PubChem Compound Ingestion Scope (`SRC-PUBCHEM`)
- **Limitation**: PUG REST API enforces a strict limit of 5 requests per second and dynamic throttling.
- **Implementation Behavior**:
  - 8 foundational food chemistry compounds (Vanillin, Caffeine, Citric acid, Sucrose, Vitamin C, Sodium benzoate, Potassium sorbate, Glycine) were acquired and extracted as proof-of-concept for the isolated extractor.
  - Future expansion will use batch PUG REST endpoints or PubChem SDF dumps for comprehensive compound ingestion.

---

## 3. Strict Boundary Guarantees Maintained

1. **No Cross-Source Entity Resolution (Deferred to Phase 3)**:
   Extractors operate in complete isolation. No cross-source merging (e.g., merging PubChem Caffeine CID 2519 with USDA Caffeine nutrient or FoodOn coffee concept) was performed.
2. **No Canonical CSV Exports Generated (Deferred to Phase 4)**:
   The `data/output_v2/` directory remains unpopulated. All records reside in `data/intermediate_v2/kg_staging.duckdb` table `raw_records`.
3. **No Synthetic / Modulo Data**:
   All 1,406 staged records are 100% genuine and verified against raw source assets.
