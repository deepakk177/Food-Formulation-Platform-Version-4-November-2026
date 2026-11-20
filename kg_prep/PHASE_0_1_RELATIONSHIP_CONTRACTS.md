# PHASE 0.1 / 0.2: CANONICAL RELATIONSHIP CONTRACTS & EDGE SPECIFICATIONS

**Document Version:** 2.0.0 (Phase 0.2 Revision)  
**Status:** FROZEN & RATIFIED  
**Scope:** Formal contract specifications for every allowable relationship edge in the reconstructed Food Formulation Knowledge Graph.

---

## 1. Architectural Rules for Relationship Generation

1. **Directional Semantics**: Every relationship is strictly directional: `(SourceNode:SourceType)-[:RELATIONSHIP_TYPE]->(TargetNode:TargetType)`.
2. **Mandatory Endpoint Existence**: An edge cannot be created unless both Source and Target IDs are present in their respective canonical node tables. Referential integrity failures result in relationship rejection.
3. **No Duplicate Aliases**: In the legacy pipeline, duplicate edge files existed (`product_has_category` vs `product_in_category`; `product_uses_process` vs `product_requires_process`; `compound_identified_by_pubchem` self-loop). All aliases are eliminated in favor of single canonical relationship specifications.
4. **Canonical Lowercase Snake_Case Headers**: All relationship CSVs adhere strictly to:
   ```
   relationship_id,source_id,source_type,relationship_type,target_id,target_type,source_dataset_id,source_record_id,extraction_confidence,evidence_id,verification_status
   ```
5. **Mandatory Provenance & Evidence**: Every relationship record must contain `source_dataset_id`, `source_record_id`, `extraction_confidence`, `verification_status`, and an `evidence_id` wherever an empirical, experimental, or legal claim is asserted.
6. **No Modulo or Blind Substring Matching**: Relationships must be explicitly present in the source or derived via validated formal rules. Heuristic substring matching is prohibited.

---

## 2. Canonical Relationship Inventory (38 Formal Contracts)

### Group A: Ingredient Identity, Classification & Sourcing

#### 1. `ingredient_belongs_to_category`
- **Direction**: `(Ingredient:Ingredient)-[:BELONGS_TO_CATEGORY]->(FoodCategory:FoodCategory)`
- **Meaning**: Classifies a raw or functional ingredient into a standard food categorization taxonomy (Codex GSFA or FoodOn).
- **Source**: FoodOn OWL subclass hierarchy or USDA FoodData Central food group.
- **Evidence Requirement**: Explicit hierarchy assertion in FoodOn OWL or USDA food group.
- **Nature**: Explicitly sourced.

#### 2. `ingredient_is_a`
- **Direction**: `(ChildIngredient:Ingredient)-[:IS_A]->(ParentIngredient:Ingredient)`
- **Meaning**: Taxonomic parent-child subsumption (e.g., *Pea Protein Isolate IS_A Pea Protein*; *Durum Wheat Flour IS_A Wheat Flour*).
- **Source**: FoodOn Ontology.
- **Nature**: Explicitly sourced.

#### 3. `ingredient_has_grade`
- **Direction**: `(Ingredient:Ingredient)-[:HAS_GRADE]->(IngredientGrade:IngredientGrade)`
- **Meaning**: Connects a generic ingredient to a specific commercial purity, processing, or regulatory grade.
- **Source**: Manufacturer Technical Specifications (Tate & Lyle, Cargill, Ingredion, ADM).
- **Nature**: Explicitly sourced.

#### 4. `grade_has_specification`
- **Direction**: `(IngredientGrade:IngredientGrade)-[:HAS_SPECIFICATION]->(IngredientSpecification:IngredientSpecification)`
- **Meaning**: Associates an ingredient grade with its formal technical parameter limits (mesh size, moisture max, microbial counts).
- **Source**: Manufacturer Specification Sheets / Technical Data Sheets (TDS).
- **Nature**: Explicitly sourced.

#### 5. `grade_supplied_by`
- **Direction**: `(IngredientGrade:IngredientGrade)-[:SUPPLIED_BY]->(Supplier:Supplier)`
- **Meaning**: Identifies the commercial manufacturer or distributor providing a specific ingredient grade.
- **Source**: Manufacturer Product Directories / Supplier Catalogs.
- **Nature**: Explicitly sourced.

#### 6. `entity_has_external_identifier`
- **Direction**: `(Entity:Any)-[:HAS_EXTERNAL_IDENTIFIER]->(ExternalIdentifier:ExternalIdentifier)`
- **Meaning**: Links a domain entity to an authoritative global database identifier (CAS, PubChem, UNII, FDC, ChEBI, INS).
- **Source**: FoodOn, USDA FDC, PubChem, ChEBI.
- **Nature**: Explicitly sourced.

#### 7. `ingredient_substitutes_for`
- **Direction**: `(AlternativeIngredient:Ingredient)-[:SUBSTITUTES_FOR]->(TargetIngredient:Ingredient)`
- **Meaning**: Asserts functional interchangeability within a specified food matrix (e.g., *Pea Protein Isolate substitutes for Soy Protein Isolate in plant-based beverages*).
- **Source**: Peer-Reviewed Food Engineering Literature, Formulation Patents.
- **Evidence Requirement**: Mandatory peer-reviewed formulation trial citation.
- **Nature**: Evidence-derived.

---

### Group B: Nutritional, Chemical and Functional Knowledge

#### 8. `ingredient_has_nutrient_profile`
- **Direction**: `(Ingredient:Ingredient)-[:HAS_NUTRIENT_PROFILE]->(NutrientProfile:NutrientProfile)`
- **Meaning**: Binds an ingredient to an integrated nutritional analysis record envelope from a single release.
- **Source**: USDA FoodData Central, ICMR-NIN IFCT.
- **Nature**: Explicitly sourced.

#### 9. `profile_has_nutrient_measurement`
- **Direction**: `(NutrientProfile:NutrientProfile)-[:HAS_NUTRIENT_MEASUREMENT]->(NutrientMeasurement:NutrientMeasurement)`
- **Meaning**: Groups individual nutrient measurements into the parent profile.
- **Source**: USDA FoodData Central `food_nutrient.csv`.
- **Nature**: Explicitly sourced.

#### 10. `measurement_measures_nutrient`
- **Direction**: `(NutrientMeasurement:NutrientMeasurement)-[:MEASURES_NUTRIENT]->(Nutrient:Nutrient)`
- **Meaning**: Connects a measured observation to the standardized nutrient definition.
- **Source**: USDA FoodData Central `nutrient.csv`, FAO/INFOODS.
- **Nature**: Explicitly sourced.

#### 11. `ingredient_contains_compound`
- **Direction**: `(Ingredient:Ingredient)-[:CONTAINS_COMPOUND]->(Compound:Compound)`
- **Meaning**: Identifies a specific chemical compound naturally occurring in or added to an ingredient (e.g., *Caffeine in Cocoa Powder*).
- **Source**: FooDB, PubChem food associations, Peer-Reviewed Literature.
- **Nature**: Explicitly sourced. Prohibits modulo assignment.

#### 12. `ingredient_has_flavor_molecule`
- **Direction**: `(Ingredient:Ingredient)-[:HAS_FLAVOR_MOLECULE]->(FlavorMolecule:FlavorMolecule)`
- **Meaning**: Connects an ingredient to an aroma molecule identified in its volatile extract.
- **Source**: FlavorDB `natural_source_associations`.
- **Nature**: Explicitly sourced.

#### 13. `molecule_exhibits_descriptor`
- **Direction**: `(FlavorMolecule:FlavorMolecule)-[:EXHIBITS_FLAVOR_DESCRIPTOR]->(SensoryFlavorDescriptor:SensoryFlavorDescriptor)`
- **Meaning**: Links a flavor compound to its recognized organoleptic sensory descriptors (e.g., *Vanillin -> sweet, vanilla, creamy*).
- **Source**: FlavorDB, FEMA Flavor Library.
- **Nature**: Explicitly sourced.

#### 14. `ingredient_has_functional_role`
- **Direction**: `(Ingredient:Ingredient)-[:HAS_FUNCTIONAL_ROLE]->(FunctionalRole:FunctionalRole)`
- **Meaning**: Identifies the techno-functional purpose an ingredient serves in a formulation (e.g., *Soy Lecithin -> Emulsifier*).
- **Source**: Codex INS technological purpose list, Manufacturer Spec Sheets, FoodOn.
- **Nature**: Explicitly sourced.

#### 15. `ingredient_has_allergen`
- **Direction**: `(Ingredient:Ingredient)-[:HAS_ALLERGEN]->(Allergen:Allergen)`
- **Meaning**: Flags statutory allergen presence resulting from botanical or animal origin.
- **Source**: FoodOn taxonomic lineage, FDA FALCPA/FASTER Act, EU Regulation 1169/2011.
- **Nature**: Explicitly sourced.

#### 16. `grade_has_property_measurement`
- **Direction**: `(IngredientGrade:IngredientGrade)-[:HAS_PROPERTY_MEASUREMENT]->(PropertyMeasurement:PropertyMeasurement)`
- **Meaning**: Binds an ingredient grade to measured physical properties (e.g., *viscosity 1500 mPa·s at 1% solution, 25°C*).
- **Source**: Manufacturer Certificate of Analysis / Laboratory Test Reports.
- **Nature**: Explicitly sourced.

---

### Group C: Compatibility, Rules and Matrix Interactions

#### 17. `ingredient_participates_in_interaction`
- **Direction**: `(Ingredient:Ingredient)-[:PARTICIPATES_IN_INTERACTION]->(IngredientInteraction:IngredientInteraction)`
- **Meaning**: Associates an ingredient with a documented multi-ingredient interaction node.
- **Source**: Peer-Reviewed Food Engineering Literature (local PDFs).
- **Nature**: Evidence-derived.

#### 18. `interaction_governed_by_rule`
- **Direction**: `(IngredientInteraction:IngredientInteraction)-[:GOVERNED_BY_RULE]->(CompatibilityRule:CompatibilityRule)`
- **Meaning**: Connects a specific empirical interaction instance to a generalized formulation compatibility rule.
- **Source**: Food Chemistry Textbooks, Scientific Literature Consensus.
- **Nature**: Computationally derived.

#### 19. `subject_supported_by_evidence`
- **Direction**: `(SubjectNode:Any)-[:SUPPORTED_BY_EVIDENCE]->(Evidence:Evidence)`
- **Meaning**: Directly grounds an assertion in a specific verifiable text excerpt, table, or page reference.
- **Source**: Primary Literature, Patents, Official Gazettes.
- **Nature**: Explicitly sourced.

---

### Group D: Recipes, Commercial Products, Formulations and Manufacturing

#### 20. `recipe_has_component`
- **Direction**: `(Recipe:Recipe)-[:HAS_RECIPE_COMPONENT]->(RecipeComponent:RecipeComponent)`
- **Meaning**: Connects a culinary recipe to an ingredient entry.
- **Source**: Culinary Recipe Repositories (Recipe1M+, Food.com).
- **Nature**: Explicitly sourced.

#### 21. `component_uses_ingredient`
- **Direction**: `(RecipeComponent:RecipeComponent)-[:USES_INGREDIENT]->(Ingredient:Ingredient)`
- **Meaning**: Resolves a declared recipe item to a canonical `Ingredient` entity.
- **Source**: Entity Resolution Pipeline.
- **Nature**: Computationally derived.

#### 22. `recipe_has_step`
- **Direction**: `(Recipe:Recipe)-[:HAS_RECIPE_STEP]->(RecipeStep:RecipeStep)`
- **Meaning**: Links a culinary recipe to its sequenced preparation steps.
- **Source**: Culinary Recipe Repositories.
- **Nature**: Explicitly sourced.

#### 23. `product_has_declaration`
- **Direction**: `(CommercialProduct:CommercialProduct)-[:HAS_INGREDIENT_DECLARATION]->(ProductIngredientDeclaration:ProductIngredientDeclaration)`
- **Meaning**: Connects a retail packaged good to a declared ingredient line on its label.
- **Source**: Open Food Facts label crawls.
- **Nature**: Explicitly sourced.

#### 24. `declaration_uses_ingredient`
- **Direction**: `(ProductIngredientDeclaration:ProductIngredientDeclaration)-[:USES_INGREDIENT]->(Ingredient:Ingredient)`
- **Meaning**: Resolves a label declaration item to a canonical `Ingredient` entity.
- **Source**: Entity Resolution Pipeline.
- **Nature**: Computationally derived.

#### 25. `formulation_has_version`
- **Direction**: `(Formulation:Formulation)-[:HAS_VERSION]->(FormulationVersion:FormulationVersion)`
- **Meaning**: Links an industrial product development project to a specific revision.
- **Source**: Pilot Plant Records, Formulation Patents.
- **Nature**: Explicitly sourced.

#### 26. `version_has_component`
- **Direction**: `(FormulationVersion:FormulationVersion)-[:HAS_FORMULATION_COMPONENT]->(FormulationComponent:FormulationComponent)`
- **Meaning**: Connects a formulation revision to a batch slot with exact mass percentage.
- **Source**: Formulation Patents, Pilot Trial Records.
- **Nature**: Explicitly sourced.

#### 27. `component_uses_grade`
- **Direction**: `(FormulationComponent:FormulationComponent)-[:USES_INGREDIENT_GRADE]->(IngredientGrade:IngredientGrade)`
- **Meaning**: Binds an industrial formulation slot to a specific commercial ingredient grade.
- **Source**: Formulation Specifications.
- **Nature**: Explicitly sourced.

#### 28. `version_has_process_sequence`
- **Direction**: `(FormulationVersion:FormulationVersion)-[:HAS_PROCESS_SEQUENCE]->(ProcessStep:ProcessStep)`
- **Meaning**: Connects an industrial formulation to its sequenced manufacturing process steps.
- **Source**: Pilot Plant Batch Records, Patent Flowcharts.
- **Nature**: Explicitly sourced.

#### 29. `step_precedes_step`
- **Direction**: `(StepA:ProcessStep|RecipeStep)-[:PRECEDES]->(StepB:ProcessStep|RecipeStep)`
- **Meaning**: Defines linear execution sequence in preparation instructions or industrial manufacturing stages.
- **Source**: Process Flowcharts, Recipe Instructions.
- **Nature**: Explicitly sourced.

#### 30. `process_step_uses_equipment`
- **Direction**: `(ProcessStep:ProcessStep)-[:USES_EQUIPMENT]->(Equipment:Equipment)`
- **Meaning**: Identifies specific processing machinery required to execute a unit operation stage.
- **Source**: Engineering Literature, Patent Disclosures. Prohibits modulo assignment.
- **Nature**: Evidence-derived.

---

### Group E: Regulatory Governance, Packaging and Commercial

#### 31. `regulation_defines_permission`
- **Direction**: `(Regulation:Regulation)-[:DEFINES]->(RegulatoryPermission:RegulatoryPermission)`
- **Meaning**: Connects a governing legal act to an explicit permission provision.
- **Source**: Codex STAN 192-1995, FSSAI Gazettes, US 21 CFR.
- **Nature**: Explicitly sourced.

#### 32. `permission_permitted_in_category`
- **Direction**: `(RegulatoryPermission:RegulatoryPermission)-[:PERMITTED_IN]->(FoodCategory:FoodCategory)`
- **Meaning**: Establishes the exact food category scope where an additive is legally authorized.
- **Source**: Codex GSFA Table 2 provisions. Prohibits modulo assignment.
- **Nature**: Explicitly sourced.

#### 33. `permission_governs_additive`
- **Direction**: `(RegulatoryPermission:RegulatoryPermission)-[:GOVERNS_ADDITIVE]->(Ingredient:Ingredient)`
- **Meaning**: Links the regulatory permission provision to the target additive substance by INS/CAS.
- **Source**: Codex GSFA / FSSAI Schedules.
- **Nature**: Explicitly sourced.

#### 34. `grade_has_cost_record`
- **Direction**: `(IngredientGrade:IngredientGrade)-[:HAS_COST_RECORD]->(CostRecord:CostRecord)`
- **Meaning**: Binds an ingredient grade to verified commercial price records.
- **Source**: Verified Supplier Quotations, Mandi Commodity Bulletins (AGMARKNET).
- **Nature**: Explicitly sourced.

#### 35. `version_has_shelf_life_study`
- **Direction**: `(FormulationVersion:FormulationVersion)-[:HAS_SHELF_LIFE_STUDY]->(ShelfLifeStudy:ShelfLifeStudy)`
- **Meaning**: Links a formulation batch to an empirical stability study.
- **Source**: Food Science Literature, Stability Trial Reports.
- **Nature**: Explicitly sourced.

#### 36. `version_has_sensory_evaluation`
- **Direction**: `(FormulationVersion:FormulationVersion)-[:HAS_SENSORY_EVALUATION]->(SensoryEvaluation:SensoryEvaluation)`
- **Meaning**: Connects a formulation trial to trained sensory panel evaluation scores.
- **Source**: Sensory Science Research, Pilot Test Reports.
- **Nature**: Explicitly sourced.

#### 37. `packaging_uses_material`
- **Direction**: `(PackagingSpecification:PackagingSpecification)-[:USES_MATERIAL]->(PackagingMaterial:PackagingMaterial)`
- **Meaning**: Identifies the polymer or substrate material used in a packaging format.
- **Source**: Packaging Engineering Datasheets.
- **Nature**: Explicitly sourced.

#### 38. `claim_governed_by_regulation`
- **Direction**: `(Claim:Claim)-[:GOVERNED_BY_REGULATION]->(Regulation:Regulation)`
- **Meaning**: Links a regulated nutrition or health claim to its statutory legal definition.
- **Source**: FDA Nutrition Labeling Regulations, EU Regulation 1924/2006, FSSAI Claims Regs.
- **Nature**: Explicitly sourced.
