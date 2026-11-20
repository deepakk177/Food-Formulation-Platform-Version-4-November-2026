# PHASE 1: KNOWN IMPLEMENTATION LIMITATIONS & SCOPE BOUNDARIES

**Document Version:** 1.0.0  
**Phase:** Phase 1 Infrastructure & Source Registry  
**Status:** FROZEN & DOCUMENTED  

---

## 1. Architectural Scope Boundaries Respected

In strict accordance with Phase 1 constraints:
1. **Zero Source-Specific Extraction**: No parsing logic has been implemented for FoodOn OWL, USDA FDC CSVs, FlavorDB JSONs, Codex GSFA HTML, Open Food Facts, or research literature PDFs. Source extraction modules are deferred to Phase 2.
2. **Zero Entity Resolution**: No fuzzy, syntactic, or ontology-driven entity resolution has been executed. Entity resolution is deferred to Phase 3.
3. **Zero Production CSV Exports**: No node CSV files (`Nodes/*.csv`) or relationship CSV files (`Relationships/*.csv`) have been generated. The directories `data/output_v2/` remain strictly unpopulated.
4. **Zero Production Code Refactoring**: Legacy code under `kg_prep/src/` has remained completely untouched. All Phase 1 modules are isolated in `kg_prep/src/pipeline_v2/` and `kg_prep/config_v2/`.

---

## 2. Source Integration Status & Limitations

| Source ID | Source Name | Access Status | Known Limitations & Mitigation |
| :--- | :--- | :--- | :--- |
| `SRC-FOODON` | FoodOn Ontology | `LOCAL_AVAILABLE` | 40.4 MB RDF/XML file verified locally. Contains taxonomic parent-child classes only; lacks industrial functional grades and quantitative nutrient contents. |
| `SRC-FLAVORDB` | FlavorDB | `LOCAL_AVAILABLE` | 20 local JSON files verified. Contains qualitative aroma descriptors; lacks quantitative olfactory thresholds and sensory intensity ratings. |
| `SRC-CODEX-GSFA` | Codex GSFA (CXS 192-1995) | `LOCAL_PARTIAL` | Local index verified; provision tables must be scraped in Phase 2 for core categories only (01.0, 02.0, 05.0, 06.0, 07.0, 14.0). Lacks industrial batch dosages. |
| `SRC-USDA-FDC` | USDA FoodData Central | `REMOTE_AVAILABLE` | Bulk CSV (~60 MB uncompressed) scoped strictly to Foundation Foods + SR Legacy per Decision D-01. Branded foods excluded from foundational nutritional baseline. |
| `SRC-OPENFOODFACTS` | Open Food Facts | `LOCAL_PARTIAL` | Label ingredient lists are in descending weight order. Exact quantitative percentages are populated ONLY when explicitly disclosed on the label; non-disclosure is preserved as NULL. |
| `SRC-PUBCHEM` | PubChem (NCBI) | `REMOTE_AVAILABLE` | Direct PUG REST API. Rate-limited to 5 requests/sec. Chemical structure and molecular weight provider; does not specify food formulation usage levels. |
| `SRC-PEER-REVIEWED-LIT` | Research Papers (PDFs) | `LOCAL_AVAILABLE` | 3 peer-reviewed food engineering PDFs (~1.8 MB) verified locally. Tabular extraction requires specialized PDF parsing in Phase 2. |
| `SRC-MANUFACTURER-SPECS`| Supplier TDS Sheets | `LOCAL_AVAILABLE` | Local TDS spec sheets verified. Contains trade-name commercial grades requiring entity resolution to FoodOn canonical ingredients in Phase 3. |
| `SRC-FSSAI` | FSSAI Gazettes | `REMOTE_AVAILABLE` | Download endpoints marked `NOT_VERIFIED` pending official gazette URL verification during Phase 2 acquisition. |
| `SRC-COMMODITY-COST` | Agricultural Mandi Cost Data | `REMOTE_AVAILABLE` | Wholesale spot mandi prices (`COMMODITY_MANDI`). Must never be represented as manufacturer or supplier quotations. |
| `SRC-RECIPE1M` | Recipe1M+ Dataset | `BLOCKED_REQUIRES_REGISTRATION` | Requires formal institutional MIT CSAIL registration. Registered and skipped gracefully without mock fallback data per Decision D-03. |
| `SRC-ICMR-IFCT` | ICMR-NIN IFCT 2017 | `BLOCKED_REQUIRES_LICENSE` | Gated proprietary Indian food composition database requiring commercial license. Registered and skipped gracefully without mock fallback data per Decision D-03. |

---

## 3. Technical & Operational Limitations

### A. HTTP Acquisition Client
- **Network Isolation in Phase 1**: The client was tested strictly against a local ephemeral HTTP server (`127.0.0.1`). Live remote downloads are deferred to Phase 2.
- **Strict Content-Type Validation**: If an external server returns an HTML landing page (e.g. Cloudflare challenge or login portal) when expecting a CSV or ZIP dataset, the client throws `ContentTypeError` and terminates immediately. It will never save an HTML page as a data archive.

### B. Asset Manifest Tracking
- **Checksum Calculation**: Checksums are computed via streaming chunks (64 KB buffer) to ensure stability on large multi-gigabyte files. Checksums are computed strictly from disk bytes; no placeholder hashes are permitted.

### C. DuckDB Storage Layer
- **Local Relational Scope**: DuckDB operates in single-process mode (`kg_staging.duckdb` or in-memory). It is not designed for concurrent multi-writer web server access, which is appropriate for offline ETL pipeline execution.
- **Zero Fabrication Guarantee**: The database schema initializes with zero factual records. Provenance tables will only be populated as authentic source assets are acquired and extracted in subsequent phases.
