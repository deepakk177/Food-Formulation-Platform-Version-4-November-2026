# Food Formulation Knowledge Graph (KG) Architecture Inventory

## Overview
This document inventories the existing Knowledge Graph Preparation (`kg_prep`) and platform backend architecture within the Food Formulation Platform. It outlines existing modules, schemas, normalizers, validators, database layers, and extension points to ensure zero architectural replacement and strict reuse/extension.

---

## 1. Module Inventory

| Module Name | File Path | Purpose | Primary Inputs | Primary Outputs | Key Dependencies | Extension Points |
|---|---|---|---|---|---|---|
| **CLI Entry Point** | [`kg_prep/main.py`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/main.py) | CLI entry for data acquisition orchestrator | Command line flags (`--all`, `--source`, `--domain`) | Exit code (0/1), execution trigger | `asyncio`, `argparse`, `DataLakeOrchestrator` | Add CLI flags for dataset pipeline stages |
| **Profiler Entry Point** | [`kg_prep/main_profiler.py`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/main_profiler.py) | Scans data lake, restructures raw directories, runs sub-profilers | `data/`, `config/` | Reports in `reports/`, dataset summary CSVs | `pandas`, `pathlib`, profiler engines | Integration of new domain profiler rules |
| **Data Lake & Pipeline Orchestrator** | [`kg_prep/src/orchestrator.py`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/src/orchestrator.py) | Central coordinator for acquisition streams, processing modules 1-6 | `config/config.yaml`, dataset registry, raw data files | Directs execution across modules | `HTTPClient`, `MetadataManager`, `COLLECTOR_REGISTRY` | Dataset adapters registration & pipeline stage hooks |
| **Base Collector** | [`kg_prep/src/base_collector.py`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/src/base_collector.py) | Abstract base class for raw data source collectors | Source config dictionary | Raw files stored in `data/raw/<domain>/<source>/` | `HTTPClient`, `MetadataManager` | Inherit `BaseCollector` for new dataset adapters |
| **Source Collectors** | [`kg_prep/src/collectors/`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/src/collectors/) | Individual source downloaders (USDA FDC, FooDB, FlavorDB, etc.) | Source configuration, HTTP endpoints | Raw zips, JSONs, HTMLs, CSVs in raw data lake | `aiohttp`, `HTTPClient`, `checksum` | New dataset adapters (ComBase, NECTAR, Texture, LCA, Scoring) |
| **Metadata Manager** | [`kg_prep/src/metadata_manager.py`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/src/metadata_manager.py) | Manages centralized dataset metadata database & download ledger | Raw file attributes, acquisition status | `data/metadata.json`, `data/download_log.csv` | `json`, `csv`, `hashlib` | Adding SHA256 verification and grounded DB sync |
| **Knowledge Fusion Engine** | [`kg_prep/src/knowledge_fusion/engine.py`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/src/knowledge_fusion/engine.py) | Entity consolidation, synonym resolution, canonical ID mapping | Intermediate entity CSVs | Canonical node CSVs in `data/output/Nodes/`, `id_mappings.json` | `EntityResolver`, `UnitNormalizer`, `pandas` | Deterministic entity linking rules & source priority handling |
| **Entity Resolver** | [`kg_prep/src/knowledge_fusion/resolver.py`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/src/knowledge_fusion/resolver.py) | Deterministic string normalization and entity deduplication | Raw record list, exact_only flag | Resolved canonical entity dictionary, ID mapping | `re`, `unicodedata` | Deterministic matching strategies (CAS, InChIKey, PubChem) |
| **Unit Normalizer** | [`kg_prep/src/knowledge_fusion/unit_normalizer.py`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/src/knowledge_fusion/unit_normalizer.py) | Unit standardization for mass, concentration, temperature, etc. | Raw measurement strings | Standardized numerical value & canonical unit | `re` | Mathematical unit conversion rules |
| **Relationship Builder** | [`kg_prep/src/relationship_builder/builder.py`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/src/relationship_builder/builder.py) | Builds canonical relationship tables with endpoint validation | Raw relationship CSVs, canonical node tables, ID mappings | Relationship CSVs in `data/output/Relationships/` | `pandas`, `json` | New relationship specifications (CO_OCCURS_IN_RECIPE, GROWS_IN, etc.) |
| **Pipeline Validator** | [`kg_prep/src/validator/checker.py`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/src/validator/checker.py) | Audits schema compliance, duplicate IDs, referential integrity | `data/output/Nodes/`, `data/output/Relationships/` | `data/output/validation_report.json` | `pandas`, `json` | Grounded database traceability & quality metric checks |
| **Neo4j DataLoader** | [`kg_prep/src/neo4j_loader.py`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/src/neo4j_loader.py) | Loads canonical CSVs into Neo4j graph database | Node and relationship CSVs in `data/output/` | Graph database nodes and edges in Neo4j | `neo4j`, `pandas` | Neo4j label and relationship type mapping extensions |
| **Resilient HTTP Client** | [`kg_prep/src/utils/http_client.py`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/src/utils/http_client.py) | Asynchronous HTTP client with backoff and rate limits | Request URLs, parameters | File byte streams, text responses | `aiohttp`, `asyncio` | Domain-specific rate limits and header overrides |
| **Checksum Verification** | [`kg_prep/src/utils/checksum.py`](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/kg_prep/src/utils/checksum.py) | File integrity hashing | File path | SHA256 string | `hashlib` | Automated checksum validation on download |

---

## 2. Existing Schemas & Data Models

### Node Schemas (`data/output/Nodes/`)
1. **Ingredients**: `ID`, `Name`, `Source`
2. **Products**: `ID`, `Name`, `IngredientsText`, `Source`
3. **Nutrients**: `ID`, `Name`, `Value`, `Unit`, `Source`
4. **Compounds**: `ID`, `Name`, `ChemicalFormula`, `CASNumber`, `Source`
5. **Flavors**: `ID`, `Name`, `Source`
6. **FlavorMolecules**: `ID`, `Name`, `PubChemID`, `FEMANumber`, `CASNumber`, `Source`
7. **FunctionalRoles**: `ID`, `Name`, `Source`
8. **FoodAdditives**: `ID`, `Name`, `Source`
9. **INS**: `ID`, `Name`, `Source`
10. **FoodCategories**: `ID`, `Name`, `Source`
11. **Regulations**: `ID`, `Name`, `Source`
12. **Constraints**: `ID`, `Name`, `LimitValue`, `NormalizedValue`, `NormalizedUnit`, `Source`
13. **Processes**: `ID`, `Name`, `Source`
14. **ProcessConditions**: `ID`, `Name`, `Source`
15. **Allergens**: `ID`, `Name`, `Source`
16. **Properties**: `ID`, `Name`, `Value`, `Source`
17. **Packaging**: `ID`, `Name`, `Source`
18. **Equipment**: `ID`, `Name`, `Source`
19. **Evidence**: `ID`, `Name`, `Text`, `Source`
20. **Sources**: `ID`, `Name`, `Type`, `Source`

### Relationship Schemas (`data/output/Relationships/`)
Headers for all relationship files: `SourceID`, `TargetID`, `RelationshipType`, `SourceDataset`

1. `ingredient_contains_compound` (`Ingredients` → `Compounds`)
2. `ingredient_has_nutrient` (`Ingredients` → `Nutrients`)
3. `ingredient_has_flavor` (`Ingredients` → `Flavors`)
4. `ingredient_performs_role` (`Ingredients` → `FunctionalRoles`)
5. `ingredient_has_property` (`Ingredients` → `Properties`)
6. `ingredient_used_in_product` (`Ingredients` → `Products`)
7. `product_requires_process` (`Products` → `Processes`)
8. `process_has_condition` (`Processes` → `ProcessConditions`)
9. `product_complies_with` (`Products` → `Regulations`)
10. `foodadditive_has_ins` (`FoodAdditives` → `INS`)
11. `foodadditive_allowed_in_foodcategory` (`FoodAdditives` → `FoodCategories`)
12. `regulation_has_constraint` (`Regulations` → `Constraints`)
13. `evidence_supports_entity` (`Evidence` → `FoodAdditives`)
14. `product_in_category` (`Products` → `FoodCategories`)

---

## 3. Directory Layout Standards
- **Raw Input Directory**: `data/raw/` (`structured/`, `semi_structured/`, `unstructured/`)
- **Intermediate Processing Directory**: `data/intermediate/`
- **Grounded Audit Database Directory**: `data/grounded/` (`grounded_food_knowledge.duckdb`)
- **KG CSV Output Directory**: `data/output/Nodes/` and `data/output/Relationships/`
- **Manifest Directory**: `data/manifest/` (`dataset_manifest.csv`, `pipeline_runs.csv`)
- **Quality & Audit Reports Directory**: `data/reports/` and `data/validation/`

---

## 4. Platform Database & Runtime Integration
- **Relational Backend**: `Food Web App Core/backend/database.py` (SQLAlchemy / SQLite `tcs_food_formulator.db`)
- **Graph Backend**: `Food Web App Core/backend/neo4j_client.py` and `kg_prep/src/neo4j_loader.py` (Neo4j driver with Bolt interface)
- **Analytical Audit Database**: Grounded Validation database using `DuckDB` at `data/grounded/grounded_food_knowledge.duckdb`.

---

## 5. Summary of Architectural Extension Plan
1. **Collector Adapters**: Extend `COLLECTOR_REGISTRY` in `kg_prep/src/collectors/` for missing target datasets (ComBase, NECTAR, Texture, Poore & Nemecek, Blue Foods, Mushroom LCA, FPED, HEI, Nutri-Score, Health Star Rating).
2. **Grounded Database Engine**: Integrate DuckDB grounded database in `kg_prep/src/grounded/` for immutable raw payload, normalized record, field-level provenance, conflict tracking, and audit log storage.
3. **Deterministic Entity & Relationship Normalization**: Extend `KnowledgeFusionEngine` and `RelationshipBuilder` to map newly ingested scientific datasets strictly into canonical KG nodes and edges.
4. **Data Quality & Audit Pipeline**: Extend `PipelineValidator` and logging metrics to enforce zero hallucination, rejected record tracking, conflict reporting, and reproducibility tests.
