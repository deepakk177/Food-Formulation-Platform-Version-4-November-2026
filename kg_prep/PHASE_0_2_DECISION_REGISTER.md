# PHASE 0.2: USER DECISION REGISTER & DESIGN FREEZE

**Document Version:** 1.0.0  
**Status:** FROZEN & RATIFIED  
**Phase:** Phase 0.2 Architectural Correction  
**Authority:** Approved by System Architect & Platform Requirements  

---

## 1. Ratified User Decisions

| # | Domain Decision | Approved Strategy | Technical Specification | Operational Impact |
|---|---|---|---|---|
| **D-01** | **USDA FDC Ingestion Scope** | **Foundation Foods + SR Legacy Only** | Restrict acquisition to USDA Foundation Foods and Standard Reference (SR Legacy) releases. Ingestion filters out ~380,000 volatile, low-quality commercial branded foods. | Reduces raw dataset size from >2 GB to ~60 MB; ensures all nutritional values represent certified laboratory assay data; eliminates commercial junk foods. |
| **D-02** | **Codex GSFA Provisions Extraction** | **Targeted Official Provision Extraction** | Target the core food categories relevant to the formulation platform: Category 01.0 (Dairy), 02.0 (Fats/Oils), 05.0 (Confectionery), 06.0 (Cereals), 07.0 (Bakery), and 14.0 (Beverages). Extract directly from official Codex tables/provisions. | Eliminates modulo arithmetic fabrication; guarantees 100% verified legal maximum levels with exact table/section citations for core target categories. |
| **D-03** | **Gated Datasets Handling** | **Register & Graceful Skip (Zero Mocks)** | Sources requiring proprietary licenses or institutional credentials (Recipe1M+, ICMR-NIN IFCT 2017, ComBase) are formally registered in `config_v2/source_registry.yaml` with status `AUTHENTICATION_REQUIRED` or `MANUAL_REVIEW_REQUIRED`. | Pipeline executes cleanly without hanging or crashing; zero synthetic fallback rows are generated; missing sources are highlighted honestly in validation manifests. |
| **D-04** | **Missing Nutritional & Cost Data** | **Strict Null Safety (No Imputation)** | Missing nutritional macros, physical parameters, and ingredient costs are stored strictly as `NULL`. No synthetic constants ($12.50/kg, 150 kcal, etc.) and no blind statistical imputation in the candidate pool. | Formulation candidate engine enforces strict gating: ingredients with missing macros are ineligible for nutritional optimization; missing costs report `COST_UNKNOWN`. |
| **D-05** | **Output CSV Header Standards** | **Canonical Snake_Case with Phase 8 Adapters** | All canonical Node and Relationship CSVs use lowercase `snake_case` column naming (`source_id`, `target_id`, `relationship_type`, `confidence`, `validation_status`). Legacy dual PascalCase headers (`SourceID`, `TargetID`) are deprecated. | Clean schema standardization; downstream compatibility adapters will be isolated to Phase 8 backend migration. |

---

## 2. Invariant Policies Established in Phase 0.2

1. **Anti-Fabrication Invariant**: Under no circumstances shall any collector, extractor, normalizer, or resolver generate mock records, synthetic limits, modulo assignments, or placeholder files to bypass missing data.
2. **Evidence Separation Invariant**: Fixed confidence scores (e.g. 1.0 for officially published) are abolished. Every assertion must track `evidence_type`, `extraction_confidence`, `evidence_quality`, and `verification_status` independently.
3. **Product vs Recipe Separation Invariant**: Retail commercial products with label ingredient declarations (`CommercialProduct` / `ProductIngredientDeclaration`) must never be conflated with culinary recipes (`Recipe` / `RecipeComponent`) or industrial batch formulations (`Formulation` / `FormulationComponent`).
4. **Percentage Non-Inference Invariant**: Percentages on commercial product declarations must remain `NULL` unless explicitly printed on the package. The pipeline shall never infer exact ingredient percentages from ingredient declaration order.
5. **Cost Hierarchy Invariant**: Wholesale raw commodity mandi prices (e.g., AGMARKNET) must never be represented as manufacturer or supplier ingredient quotations.
