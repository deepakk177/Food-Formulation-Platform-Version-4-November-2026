# PHASE 0.2: FINAL CANONICAL SCHEMA FREEZE & GRAPH SPECIFICATION

**Document Version:** 1.0.0  
**Status:** FROZEN & RATIFIED FOR IMPLEMENTATION  
**Phase:** Phase 0.2 Architectural Correction  
**Scope:** Complete structural specification of all Canonical Nodes, Reified Nodes, and Relationship Contracts for the Food Formulation Knowledge Graph.

---

## 1. Resolved & Disambiguated Domain Entities

### A. Flavor Representation: `FlavorMolecule` vs. `SensoryFlavorDescriptor`
- **Defect in Legacy Pipeline**: Two redundant files existed (`Flavors.csv` and `FlavorMolecules.csv`), leading to ungrounded string matching.
- **Ratified Resolution**:
  - `Flavors.csv` is **DEPRECATED & ELIMINATED**.
  - **`FlavorMolecule`** (`Nodes/FlavorMolecules.csv`): Discrete chemical entity responsible for aroma (e.g., *Vanillin [CAS: 121-33-5]*, *Limonene [CAS: 5989-27-5]*). Linked to PubChem and FlavorDB.
  - **`SensoryFlavorDescriptor`** (`Nodes/SensoryFlavorDescriptors.csv`): Controlled perceptual sensory vocabulary (*sweet*, *citrus*, *vanilla*, *caramel*, *woody*, *green*, *pungent*).
  - **Edge**: `(FlavorMolecule)-[:EXHIBITS_FLAVOR_DESCRIPTOR]->(SensoryFlavorDescriptor)`.

### B. Physical Properties: `PropertyMeasurement` vs. `IngredientSpecification`
- **Defect in Legacy Pipeline**: Conflated manufacturer quality limits with empirical laboratory observations.
- **Ratified Resolution**:
  - **`IngredientSpecification`** (`Nodes/IngredientSpecifications.csv`): The manufacturer's commercial specification contract for an `IngredientGrade` (e.g., Cargill's specification sheet for Xanthan Gum 200 Mesh: Moisture $\le 12.0\%$, Mesh through 200 mesh $\ge 95\%$, Viscosity range $1200 - 1600\text{ mPa}\cdot\text{s}$). Bounded acceptance envelope.
  - **`PropertyMeasurement`** (`Nodes/PropertyMeasurements.csv`): An empirical laboratory measurement of a physical parameter on a sample under specific experimental conditions (e.g., rheology flow curve measured in a published paper at shear rate $50\text{ s}^{-1}$, $25^\circ\text{C}$, $\text{pH } 6.5$, resulting in $1420\text{ mPa}\cdot\text{s}$). Observation instance.

### C. Retail Products vs. Culinary Recipes vs. Industrial Formulations
- **Defect in Legacy Pipeline**: Product label declarations, home recipes, and factory batches were collapsed into `Products.csv`.
- **Ratified Resolution**:
  - **`CommercialProduct`** (`Nodes/CommercialProducts.csv`): Retail packaged goods (e.g., *Nutella*, *Coca-Cola*) with GTIN barcode, brand, and packaging statement.
  - **`ProductIngredientDeclaration`** (`Nodes/ProductIngredientDeclarations.csv`): Reified declaration node for each ingredient listed on a commercial product label. Has `declaration_order` ($1, 2, \dots$), `declared_percentage` (numeric or `NULL` if not disclosed), `is_characterizing`, `allergen_warning`. Never conflated with a formulation recipe!
  - **`Recipe`** (`Nodes/Recipes.csv`): Culinary food preparation recipe (home/restaurant) with `RecipeComponent` (kitchen quantities, e.g., 2 cups flour) and `RecipeStep` (kitchen instructions).
  - **`Formulation`** (`Nodes/Formulations.csv`): Industrial factory formulation with `FormulationVersion` and `FormulationComponent` (strict mass balance $\sum x_i = 100.000\%$).

### D. Nutrient Profile Representation
- **`NutrientProfile`** (`Nodes/NutrientProfiles.csv`): A reified envelope node grouping a coherent set of analytical nutrient measurements for an ingredient from a single validated release (e.g., `NP-FDC-167512-2024`). Prevents mixing conflicting assays from different years or methods.

### E. Packaging Specifications & Materials
- **`PackagingSpecification`** (`Nodes/PackagingSpecifications.csv`): The container format and barrier performance specification (e.g., *Aseptic Carton Tetra Brik 250ml*, *Multilayer Standup Pouch*). Stores Oxygen Transmission Rate (OTR) and Water Vapor Transmission Rate (WVTR).
- **`PackagingMaterial`** (`Nodes/PackagingMaterials.csv`): The physical substrate material (e.g., *PET*, *HDPE*, *Aluminum Foil*, *PLA*, *Glass*).
- **Edge**: `(PackagingSpecification)-[:USES_MATERIAL]->(PackagingMaterial)`.

### F. Process Sequence Representation
- Process sequences are represented as a directed acyclic graph (DAG) of **`ProcessStep`** nodes linked via **`PRECEDES`** edges, anchored to a parent `FormulationVersion` via `(FormulationVersion)-[:HAS_PROCESS_SEQUENCE]->(ProcessStep)`.

---

## 2. Frozen Canonical Node Inventory

| File Path | Entity Type | Primary Key | Mandatory Fields | Optional Fields | Data Source |
|---|---|---|---|---|---|
| `Nodes/Ingredients.csv` | `Ingredient` | `ingredient_id` | `ingredient_id, canonical_name, entity_type, validation_status, created_at` | `synonyms, foodon_id, botanical_name` | FoodOn, USDA FDC |
| `Nodes/IngredientGrades.csv` | `IngredientGrade` | `ingredient_grade_id` | `ingredient_grade_id, ingredient_id, grade_name, quality_standard` | `purity_percentage, material_state` | Manufacturer Specs |
| `Nodes/IngredientSpecifications.csv` | `IngredientSpecification`| `specification_id` | `specification_id, ingredient_grade_id, parameter_name, operator, unit` | `limit_min, limit_max, test_method` | Manufacturer TDS |
| `Nodes/FoodCategories.csv` | `FoodCategory` | `category_id` | `category_id, category_code, category_name, taxonomy_system` | `parent_category_id, description` | Codex GSFA, FoodOn |
| `Nodes/ExternalIdentifiers.csv` | `ExternalIdentifier` | `identifier_id` | `identifier_id, entity_id, id_namespace, external_key` | `source_url, verification_date` | Cross-refs (PubChem, CAS, FDC, UNII) |
| `Nodes/Nutrients.csv` | `Nutrient` | `nutrient_id` | `nutrient_id, canonical_name, infoods_tag, canonical_unit` | `nutrient_group, description` | INFOODS, USDA FDC |
| `Nodes/NutrientProfiles.csv` | `NutrientProfile` | `nutrient_profile_id` | `nutrient_profile_id, ingredient_id, source_dataset_id, dataset_version` | `publication_date, laboratory_name` | USDA FDC, IFCT |
| `Nodes/NutrientMeasurements.csv` | `NutrientMeasurement` | `measurement_id` | `measurement_id, nutrient_profile_id, nutrient_id, value_numeric, unit, basis`| `value_min, value_max, derivation_method` | USDA FDC |
| `Nodes/Compounds.csv` | `Compound` | `compound_id` | `compound_id, canonical_name, molecular_formula, molecular_weight` | `canonical_smiles, inchi_key, cas_number` | PubChem, ChEBI |
| `Nodes/FlavorMolecules.csv` | `FlavorMolecule` | `flavor_molecule_id` | `flavor_molecule_id, canonical_name, pubchem_cid` | `fema_number, cas_number, odor_threshold`| FlavorDB, FEMA |
| `Nodes/SensoryFlavorDescriptors.csv`| `SensoryFlavorDescriptor`| `descriptor_id` | `descriptor_id, descriptor_name` | `flavor_category, description` | FlavorDB |
| `Nodes/FunctionalRoles.csv` | `FunctionalRole` | `functional_role_id` | `functional_role_id, role_name, standard_code` | `definition, technological_purpose` | Codex INS, FoodOn |
| `Nodes/Allergens.csv` | `Allergen` | `allergen_id` | `allergen_id, allergen_name, statutory_jurisdiction` | `allergenic_proteins, advisory_code` | Statutory Allergen Regs |
| `Nodes/IngredientInteractions.csv`| `IngredientInteraction` | `interaction_id` | `interaction_id, ingredient_a_id, ingredient_b_id, interaction_type` | `observed_effect, ph_condition, matrix_type`| Research Literature |
| `Nodes/CompatibilityRules.csv` | `CompatibilityRule` | `rule_id` | `rule_id, rule_name, rule_expression, severity` | `mitigation_strategy, scientific_rationale` | Food Chemistry Consensus|
| `Nodes/Constraints.csv` | `Constraint` | `constraint_id` | `constraint_id, parameter_name, operator, unit, basis, scope` | `limit_value_numeric, limit_min, limit_max` | Regulatory Standards |
| `Nodes/Recipes.csv` | `Recipe` | `recipe_id` | `recipe_id, recipe_title, cuisine, source_dataset_id` | `prep_time_minutes, cook_time_minutes` | Culinary Repositories |
| `Nodes/RecipeComponents.csv` | `RecipeComponent` | `recipe_component_id`| `recipe_component_id, recipe_id, ingredient_id, raw_text` | `quantity_numeric, quantity_unit, mass_grams`| Culinary Repositories |
| `Nodes/RecipeSteps.csv` | `RecipeStep` | `recipe_step_id` | `recipe_step_id, recipe_id, step_number, instruction_text` | `inferred_technique` | Culinary Repositories |
| `Nodes/CommercialProducts.csv` | `CommercialProduct` | `product_id` | `product_id, gtin_barcode, product_name, brand_name` | `ingredients_text, category_id, net_weight` | Open Food Facts |
| `Nodes/ProductIngredientDeclarations.csv`| `ProductIngredientDeclaration`| `declaration_id`| `declaration_id, product_id, ingredient_id, declaration_order` | `declared_percentage, is_characterizing` | Open Food Facts |
| `Nodes/Formulations.csv` | `Formulation` | `formulation_id` | `formulation_id, project_name, target_category_id, formulation_type` | `batch_mass_kg, legal_jurisdiction` | Patents, Pilot Trials |
| `Nodes/FormulationVersions.csv` | `FormulationVersion` | `version_id` | `version_id, formulation_id, version_code, is_validated` | `water_activity, ph_measured, moisture_pct` | Patents, Pilot Trials |
| `Nodes/FormulationComponents.csv`| `FormulationComponent` | `component_id` | `component_id, version_id, ingredient_grade_id, inclusion_percentage` | `inclusion_min, inclusion_max, batch_phase`| Patents, Pilot Trials |
| `Nodes/Processes.csv` | `Process` | `process_id` | `process_id, process_name, unit_operation_type` | `description, standard_classification` | Food Engineering Standard|
| `Nodes/ProcessSteps.csv` | `ProcessStep` | `process_step_id` | `process_step_id, version_id, process_id, sequence_order` | `duration_seconds, temperature_c, pressure_bar`| Patents, Pilot Trials |
| `Nodes/Equipment.csv` | `Equipment` | `equipment_id` | `equipment_id, equipment_name, equipment_category` | `capacity_max, manufacturer` | Food Engineering Standard|
| `Nodes/PackagingSpecifications.csv`| `PackagingSpecification`| `packaging_id` | `packaging_id, package_format_name` | `otr_cc_m2_day, wvtr_g_m2_day, volume_ml` | Packaging Technical Specs|
| `Nodes/PackagingMaterials.csv` | `PackagingMaterial` | `material_id` | `material_id, material_name, polymer_code` | `recycle_code, barrier_properties` | Packaging Technical Specs|
| `Nodes/Regulations.csv` | `Regulation` | `regulation_id` | `regulation_id, regulation_name, jurisdiction, authority` | `effective_date, version_code` | Statutory Legal Texts |
| `Nodes/RegulatoryPermissions.csv`| `RegulatoryPermission` | `permission_id` | `permission_id, regulation_id, ingredient_id, category_id, status` | `max_level_numeric, unit, conditions_of_use`| Codex GSFA, FSSAI |
| `Nodes/Suppliers.csv` | `Supplier` | `supplier_id` | `supplier_id, supplier_name, country_headquarters` | `website_url, supplier_type` | Manufacturer Catalogs |
| `Nodes/CostRecords.csv` | `CostRecord` | `cost_record_id` | `cost_record_id, price_value, currency, pricing_unit, price_type, price_date`| `supplier_id, ingredient_grade_id, valid_until`| Market Data, Quotes |
| `Nodes/ShelfLifeStudies.csv` | `ShelfLifeStudy` | `study_id` | `study_id, target_entity_id, temperature_celsius, duration_days` | `relative_humidity_pct, observed_failure_mode`| Research Literature |
| `Nodes/SensoryAttributes.csv` | `SensoryAttribute` | `attribute_id` | `attribute_id, attribute_name, sensory_modality` | `evaluation_scale, reference_anchor` | Sensory Science Literature|
| `Nodes/SensoryEvaluations.csv` | `SensoryEvaluation` | `evaluation_id` | `evaluation_id, target_entity_id, attribute_id, mean_score` | `panel_size, standard_deviation` | Sensory Science Literature|
| `Nodes/Claims.csv` | `Claim` | `claim_id` | `claim_id, claim_text, claim_type, regulatory_jurisdiction` | `minimum_threshold, qualifying_criterion` | Regulatory Standards |
| `Nodes/Evidence.csv` | `Evidence` | `evidence_id` | `evidence_id, evidence_type, evidence_quality, document_title, source_dataset_id`| `document_doi, patent_number, page, excerpt`| Primary Source Citations |
| `Nodes/Sources.csv` | `Source` | `source_id` | `source_id, source_name, authority_organization, official_url` | `jurisdiction, licensing_terms` | Source Registry |
| `Nodes/Datasets.csv` | `Dataset` | `dataset_id` | `dataset_id, source_id, dataset_version, release_date, sha256_hash` | `download_url, record_count` | Asset Manifest |

---

## 3. Frozen Canonical Relationship Contracts

All relationship CSVs follow the standard lower_snake_case header contract:  
`['relationship_id', 'source_id', 'source_type', 'relationship_type', 'target_id', 'target_type', 'source_dataset_id', 'source_record_id', 'extraction_confidence', 'evidence_id', 'validation_status']`.

| Relationship Name | Source Node | Relationship Type | Target Node | Sourced vs Derived | Evidence Requirement |
|---|---|---|---|---|---|
| `ingredient_belongs_to_category` | `Ingredient` | `BELONGS_TO_CATEGORY` | `FoodCategory` | Sourced | FoodOn / USDA category hierarchy |
| `ingredient_is_a` | `Ingredient` | `IS_A` | `Ingredient` | Sourced | FoodOn OWL class hierarchy |
| `ingredient_has_grade` | `Ingredient` | `HAS_GRADE` | `IngredientGrade` | Sourced | Manufacturer TDS / Catalog |
| `grade_has_specification` | `IngredientGrade` | `HAS_SPECIFICATION` | `IngredientSpecification`| Sourced | Manufacturer TDS Table |
| `grade_supplied_by` | `IngredientGrade` | `SUPPLIED_BY` | `Supplier` | Sourced | Commercial supplier directory |
| `entity_has_external_identifier`| `Ingredient` / `Compound` | `HAS_EXTERNAL_IDENTIFIER` | `ExternalIdentifier` | Sourced | Database cross-reference |
| `ingredient_substitutes_for` | `Ingredient` | `SUBSTITUTES_FOR` | `Ingredient` | Derived | Mandatory peer-reviewed formulation trial |
| `ingredient_has_nutrient_profile`| `Ingredient` | `HAS_NUTRIENT_PROFILE` | `NutrientProfile` | Sourced | USDA FDC / IFCT food code |
| `profile_has_nutrient_measurement`| `NutrientProfile` | `HAS_NUTRIENT_MEASUREMENT`| `NutrientMeasurement`| Sourced | USDA FDC `food_nutrient.csv` |
| `measurement_measures_nutrient` | `NutrientMeasurement` | `MEASURES_NUTRIENT` | `Nutrient` | Sourced | INFOODS / FDC nutrient code |
| `ingredient_contains_compound` | `Ingredient` | `CONTAINS_COMPOUND` | `Compound` | Sourced | FooDB / Literature chemical analysis |
| `ingredient_has_flavor_molecule`| `Ingredient` | `HAS_FLAVOR_MOLECULE` | `FlavorMolecule` | Sourced | FlavorDB natural source association |
| `molecule_exhibits_descriptor` | `FlavorMolecule` | `EXHIBITS_FLAVOR_DESCRIPTOR`| `SensoryFlavorDescriptor`| Sourced | FlavorDB / FEMA aroma descriptor |
| `ingredient_has_functional_role`| `Ingredient` | `HAS_FUNCTIONAL_ROLE` | `FunctionalRole` | Sourced | Codex INS technological purpose |
| `ingredient_has_allergen` | `Ingredient` | `HAS_ALLERGEN` | `Allergen` | Sourced | Statutory allergen classification |
| `grade_has_property_measurement`| `IngredientGrade` | `HAS_PROPERTY_MEASUREMENT`| `PropertyMeasurement`| Sourced | Laboratory test report / COA |
| `ingredient_participates_in_interaction`| `Ingredient` | `PARTICIPATES_IN_INTERACTION`| `IngredientInteraction`| Sourced | Peer-reviewed food chemistry paper |
| `interaction_governed_by_rule` | `IngredientInteraction` | `GOVERNED_BY_RULE` | `CompatibilityRule` | Derived | Food science domain rule |
| `subject_supported_by_evidence` | Any Subject Entity | `SUPPORTED_BY_EVIDENCE` | `Evidence` | Sourced | Primary literature/patent citation |
| `recipe_has_component` | `Recipe` | `HAS_RECIPE_COMPONENT` | `RecipeComponent` | Sourced | Culinary recipe ingredient line |
| `component_uses_ingredient` | `RecipeComponent` | `USES_INGREDIENT` | `Ingredient` | Derived | Deterministic entity resolution |
| `recipe_has_step` | `Recipe` | `HAS_RECIPE_STEP` | `RecipeStep` | Sourced | Culinary instruction sequence |
| `product_has_declaration` | `CommercialProduct` | `HAS_INGREDIENT_DECLARATION`| `ProductIngredientDeclaration`| Sourced | Open Food Facts label crawl |
| `declaration_uses_ingredient` | `ProductIngredientDeclaration`| `USES_INGREDIENT` | `Ingredient` | Derived | Deterministic entity resolution |
| `formulation_has_version` | `Formulation` | `HAS_VERSION` | `FormulationVersion` | Sourced | Pilot plant batch trial / Patent example |
| `version_has_component` | `FormulationVersion` | `HAS_FORMULATION_COMPONENT`| `FormulationComponent`| Sourced | Industrial formulation batch table |
| `component_uses_grade` | `FormulationComponent` | `USES_INGREDIENT_GRADE` | `IngredientGrade` | Sourced | Formulation grade specification |
| `version_has_process_sequence` | `FormulationVersion` | `HAS_PROCESS_SEQUENCE` | `ProcessStep` | Sourced | Manufacturing flow diagram |
| `step_precedes_step` | `ProcessStep` / `RecipeStep`| `PRECEDES` | `ProcessStep` / `RecipeStep`| Sourced | Linear sequence specification |
| `process_step_uses_equipment` | `ProcessStep` | `USES_EQUIPMENT` | `Equipment` | Sourced | Disclosed processing machinery |
| `regulation_defines_permission` | `Regulation` | `DEFINES` | `RegulatoryPermission`| Sourced | Codex GSFA / FSSAI statutory table |
| `permission_permitted_in_category`| `RegulatoryPermission` | `PERMITTED_IN` | `FoodCategory` | Sourced | Codex GSFA Table 2 provision |
| `permission_governs_additive` | `RegulatoryPermission` | `GOVERNS_ADDITIVE` | `Ingredient` | Sourced | Codex INS additive match |
| `grade_has_cost_record` | `IngredientGrade` | `HAS_COST_RECORD` | `CostRecord` | Sourced | Verified quote / Mandi bulletin |
| `version_has_shelf_life_study` | `FormulationVersion` | `HAS_SHELF_LIFE_STUDY` | `ShelfLifeStudy` | Sourced | Stability trial report / Literature |
| `version_has_sensory_evaluation`| `FormulationVersion` | `HAS_SENSORY_EVALUATION`| `SensoryEvaluation` | Sourced | Sensory panel test report |
| `packaging_uses_material` | `PackagingSpecification`| `USES_MATERIAL` | `PackagingMaterial` | Sourced | Packaging engineering specification |
| `claim_governed_by_regulation` | `Claim` | `GOVERNED_BY_REGULATION` | `Regulation` | Sourced | Statutory claim criteria |
