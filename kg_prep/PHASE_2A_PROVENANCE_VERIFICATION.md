# PHASE 2A — PROVENANCE VERIFICATION REPORT

## 1. Overview & Provenance Verification Objective

This document verifies the integrity, authenticity, and complete lineage tracking for all raw assets and source records acquired during **Phase 2A** of the Food Formulation Knowledge Graph preparation pipeline.

In compliance with the Phase 0.2 frozen design contracts (`PHASE_0_2_FINAL_SCHEMA_FREEZE.md`) and the strict data authenticity requirements:
1. Every staged record in DuckDB `raw_records` originates from an authenticated external source asset.
2. Every raw asset is registered in the immutable manifest (`data/manifests_v2/phase_2a_manifest.json` and `.csv`) and DuckDB `source_assets` table with an SHA-256 cryptographic checksum.
3. Zero synthetic records, zero random values, and zero modulo mappings were introduced.

---

## 2. Manifest Inventory & Checksum Verification

All 16 acquired raw assets have been verified against their SHA-256 cryptographic digests:

| Asset ID | Source ID | Filename | Size (Bytes) | SHA-256 Digest | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `AST-FOODON-OWL-001` | `SRC-FOODON` | `foodon.owl` | 40,429,965 | `1e11fc50283c6498697a7aca9606c9d914f1cda71cc5510e006d949c32df7db0` | VERIFIED |
| `AST-CODEX-GSFA-ADDITIVES-001` | `SRC-CODEX-GSFA` | `gsfa_additives.html` | 49,430 | `ff06587e0d5abdc84e6b6a2650964013a34fc80f4483880052ee8f124679fae8` | VERIFIED |
| `AST-USDA-SEARCH-MILK` | `SRC-USDA-FDC` | `fdc_search_milk.json` | 936,392 | `09d9362e46bc995a7887d9372eaa13c0b421df0b3deb1bfaadc92448ba4a5572` | VERIFIED |
| `AST-USDA-SEARCH-EGG` | `SRC-USDA-FDC` | `fdc_search_egg.json` | 896,718 | `e7468ce065ec2bb0e57de4d5503821a4607291790e103de80b9453debf5ad83b` | VERIFIED |
| `AST-USDA-SEARCH-WHEAT_FLOUR` | `SRC-USDA-FDC` | `fdc_search_wheat_flour.json` | 907,756 | `70f49418139ac88a94f1cd369b4a1f4a8825d360d0e8d7a39484a46e6f601987` | VERIFIED |
| `AST-USDA-SEARCH-CHEDDAR_CHEESE` | `SRC-USDA-FDC` | `fdc_search_cheddar_cheese.json` | 1,057,863 | `c38f1cd8a547e60f4b15d3994bd54ac72de9cc8db2c0569634f08f40fd002944` | VERIFIED |
| `AST-USDA-SEARCH-SOYBEAN_OIL` | `SRC-USDA-FDC` | `fdc_search_soybean_oil.json` | 718,019 | `bda1db5e3cc8801d1fdb60d06a106f1e236e17c20b364a5a7cab8ce319bbe150` | VERIFIED |
| `AST-USDA-SEARCH-SUCROSE` | `SRC-USDA-FDC` | `fdc_search_sucrose.json` | 55,179 | `b518af85c5b6f9e3ff195b5392125fb3c4e007695a4b60bb9203fc00432c7a66` | VERIFIED |
| `AST-PUBCHEM-CID-1183` | `SRC-PUBCHEM` | `pubchem_cid_1183.json` | 7,490 | `313947dab7c99aecaae367ae395fc33f48d013066572da5d365f6d412e3b7f91` | VERIFIED |
| `AST-PUBCHEM-CID-2519` | `SRC-PUBCHEM` | `pubchem_cid_2519.json` | 13,963 | `0ef9c3f692331a3c8ddd4c8bbdf2128df38fd106b06d3e71724cf31bb7775435` | VERIFIED |
| `AST-PUBCHEM-CID-311` | `SRC-PUBCHEM` | `pubchem_cid_311.json` | 9,506 | `31b203d27aca6fa70ff4e2e491d369cead0b3309fc133ab29e9fc1afc999293d` | VERIFIED |
| `AST-PUBCHEM-CID-5988` | `SRC-PUBCHEM` | `pubchem_cid_5988.json` | 9,362 | `0f73f61f1ea11a5e3ff6dd19be5eb7e613152327796191b6770ec26581a11d3b` | VERIFIED |
| `AST-PUBCHEM-CID-54670067` | `SRC-PUBCHEM` | `pubchem_cid_54670067.json` | 11,348 | `46387131153e02991ca655d8fc3c44513678e5b25e09e9c558c56e58c84b97a0` | VERIFIED |
| `AST-PUBCHEM-CID-712` | `SRC-PUBCHEM` | `pubchem_cid_712.json` | 5,056 | `e44bc7ab44e0c22afe33a0bc1b948948b9f2cc2d8bb8ec9f83f8a1f2b2634b99` | VERIFIED |
| `AST-PUBCHEM-CID-23665764` | `SRC-PUBCHEM` | `pubchem_cid_23665764.json` | 728 | `91020a7e84db39bc9e1e60cc327c474093a81855ed22475db8eea48419160c4c` | VERIFIED |
| `AST-PUBCHEM-CID-104` | `SRC-PUBCHEM` | `pubchem_cid_104.json` | 958 | `d0bd55919853edf9d7817b9688d3d8dedec14d4166fc49923471193485c0d505` | VERIFIED |

---

## 3. DuckDB Relational Provenance Audit

The DuckDB staging store (`data/intermediate_v2/kg_staging.duckdb`) enforces relational integrity through foreign keys:

```sql
raw_records.source_id -> source_registry.source_id
raw_records.asset_id  -> source_assets.asset_id
raw_records.execution_id -> execution_runs.execution_id
```

### Staged Record Counts by Source & Verification Status

| Source ID | Source Registry Name | Staged Records | Integrity Check | Rejection Reason |
| :--- | :--- | :--- | :--- | :--- |
| `SRC-FOODON` | Food Ontology | 1,000 | 100% Valid OWL Classes | None (streaming parsed) |
| `SRC-CODEX-GSFA` | Codex Additives Index | 296 | 100% Genuine Additives | None (legacy fake PDFs rejected) |
| `SRC-USDA-FDC` | USDA FoodData Central | 102 | 100% Foundation / SR Legacy | None (Branded filter active) |
| `SRC-PUBCHEM` | NCBI PubChem REST | 8 | 100% Live PUG REST Hits | None (throttled & verified) |
| **Total** | | **1,406** | **100% Genuine** | |

---

## 4. Legacy Defect Elimination Proof

1. **Synthetic Generation Elimination**:
   `mock_generator.py` and any synthetic generation routines are completely bypassed. Zero synthetic records were created or staged.
2. **Modulo Arithmetic Elimination**:
   The legacy formula `category_id = (ins_num % 16) + 1` was eliminated. GSFA additives contain only authentic names, official GSFA IDs, and INS numbers.
3. **Branded Foods Exclusion (Decision D-01)**:
   USDA FDC queries were explicitly restricted to `Foundation` and `SR Legacy`. All branded products are rejected to eliminate manufacturer-specific bias and formulation noise.
4. **Cloudflare Turnstile Handling**:
   The remote FAO portal was probed and detected as `BLOCKED_BY_CLOUDFLARE`. No unauthorized bypass, CAPTCHA solving, or synthetic filler was applied; the system reported this state cleanly and reused genuine local assets.

---

## 5. Audit Trail & Verification Conclusion

All staged records are 100% traceable to their original raw assets. Cryptographic digests, execution run timestamps, and source endpoints are permanently recorded in DuckDB and manifest artifacts.
