# PHASE 0.1 / 0.2: CANONICAL NODE SCHEMA DECISIONS & DOMAIN INVENTORY

**Document Version:** 2.0.0 (Phase 0.2 Revision)  
**Status:** FROZEN & RATIFIED  
**Scope:** Evaluation and definitive structural classification of all domain concepts for the Food Formulation Knowledge Graph, with disambiguated entities.

---

## 1. Architectural Principles for Node Classification

A knowledge graph is corrupted when every numerical value, unit of measure, or ephemeral calculation is promoted into an independent node. Conversely, graph utility is destroyed when richly connected, evidence-backed domain concepts are flattened into untraceable string attributes.

Each candidate concept from the domain inventory is classified into one of the following architectural roles:

1. **Canonical Node (`NODE`)**: An entity with persistent independent identity, multi-edge connectivity, and domain-wide relevance across formulations (e.g., `Ingredient`, `FoodCategory`, `Nutrient`, `Compound`, `Process`, `Regulation`, `CommercialProduct`).
2. **Reified Measurement / Assertion Node (`REIFIED_NODE`)**: A contextual record representing an observation, measurement, batch component, product declaration, or legal permission that requires its own provenance, conditions, method, or multi-field attributes (e.g., `NutrientMeasurement`, `FormulationComponent`, `ProductIngredientDeclaration`, `RegulatoryPermission`, `CostRecord`, `PropertyMeasurement`).
3. **Node Property (`NODE_PROPERTY`)**: An intrinsic scalar or vector attribute belonging strictly to a single entity that does not participate in graph traversals (e.g., `CASNumber`, `SMILES`, `MaterialState`, `ConditionsOfUse`).
4. **Relationship Property (`REL_PROPERTY`)**: A qualifying metric or condition describing the edge itself (e.g., `InclusionPercentage`, `SimilarityScore`, `InteractionMechanism`).
5. **Runtime-Only Entity (`RUNTIME_ENTITY`)**: An ephemeral computational artifact generated and consumed during optimization or solver execution in the formulation backend; excluded from the static Knowledge Graph ETL pipeline (e.g., `OptimizationRun`, `OptimizationObjective`, `ConstraintEvaluation`).
6. **Not Required / Deprecated (`DEPRECATED`)**: Concepts that duplicate existing standards or provide no analytical value.

---

## 2. Definitive Classification of Domain Types

### Group A: Ingredient Identity and Classification

| # | Concept Name | Target Classification | Target Artifact / Storage Location | Structural Definition & Justification |
|---|---|---|---|---|
| 1 | `Ingredient` | **Canonical Node** | `Nodes/Ingredients.csv` | **Primary Entity**: The fundamental building block of food formulations. Carries canonical naming, taxonomic grounding, and links to all nutritional, chemical, regulatory, and formulation relationships. |
| 2 | `IngredientGrade` | **Canonical Node** | `Nodes/IngredientGrades.csv` | **Distinguishing Entity**: Distinguishes commercial purity and quality variants (e.g., *Pea Protein Isolate 85%* vs. *Pea Protein Concentrate 60%*; *Food Grade FCC* vs. *USP Pharmaceutical* vs. *Technical*). Essential for accurate cost, rheology, and legal limits. |
| 3 | `IngredientSpecification` | **Canonical Node** | `Nodes/IngredientSpecifications.csv` | **Technical Data Sheet (TDS)**: Captures manufacturer-declared physical specifications (mesh size, maximum moisture, microbial limits, bulk density). Linked to `Supplier` and `IngredientGrade`. Represents acceptable commercial limit envelope. |
| 4 | `FoodCategory` | **Canonical Node** | `Nodes/FoodCategories.csv` | **Hierarchical Taxonomy**: Codex GSFA (Category 01.0 to 16.0) and FoodOn hierarchical food categories. Essential for regulatory limit applicability and category-level formulation priors. |
| 5 | `FoodOnConcept` | **Canonical Node / External Cross-Ref** | `Nodes/ExternalIdentifiers.csv` & `Ingredients.csv` | **Ontological Anchor**: Represents explicit FoodOn OWL class identifiers (`FOODON:00001234`). Stored as `ontology_id` on `Ingredient` and indexed in `ExternalIdentifiers` for cross-ontology alignment. |
| 6 | `ExternalIdentifier` | **Canonical Node** | `Nodes/ExternalIdentifiers.csv` | **Identity Resolution Entity**: Resolves heterogeneous database keys across namespaces: USDA FDC ID, PubChem CID, CAS Registry Number, ChEBI, UNII, FEMA, INS. Enables clean, multi-source disambiguation without polluting domain nodes. |
| 7 | `IngredientAlternative` | **Relationship Property** | Edge `SUBSTITUTES_FOR` | **Functional Edge**: Not a separate node. An ingredient is an alternative to another via a typed relationship `(i1:Ingredient)-[:SUBSTITUTES_FOR {functional_overlap: 0.85, matrix: "bakery"}]->(i2:Ingredient)`. |
| 8 | `MaterialState` | **Node Property** | Property `material_state` on `IngredientGrade` | **Scalar Attribute**: Enum property (`POWDER`, `LIQUID`, `PASTE`, `EMULSION`, `GRANULAR`, `PELLET`). Encapsulated directly on the grade. |

---

### Group B: Nutritional, Chemical and Functional Knowledge

| # | Concept Name | Target Classification | Target Artifact / Storage Location | Structural Definition & Justification |
|---|---|---|---|---|
| 9 | `Nutrient` | **Canonical Node** | `Nodes/Nutrients.csv` | **Standardized Nutrient**: Controlled vocabulary of macro- and micronutrients standardized against INFOODS tags and USDA FDC nutrient IDs (e.g., *Protein [INFOODS: PROCNT]*, *Calcium [INFOODS: CA]*). |
| 10 | `NutrientProfile` | **Reified Node** | `Nodes/NutrientProfiles.csv` | **Composite Nutritional Envelope**: Groups a coherent set of nutrient measurements for a single food item from a specific analytical source release (e.g., `NP-FDC-167512-2024`). Prevents temporal or methodological mixing. |
| 11 | `NutrientMeasurement` | **Reified Node** | `Nodes/NutrientMeasurements.csv` | **Quantitative Observation**: Atomic measurement record containing `value`, `unit`, `basis` (per 100g finished product vs. dry weight), `derivation_method`, `min_val`, `max_val`, and `evidence_id`. Prevents dimensional collapse. |
| 12 | `Compound` | **Canonical Node** | `Nodes/Compounds.csv` | **Chemical Entity**: Discrete molecular substance defined by `SMILES`, `InChIKey`, `MolecularWeight`, and `MolecularFormula`. Linked to ingredients via verified literature extraction. |
| 13 | `FlavorMolecule` | **Canonical Node** | `Nodes/FlavorMolecules.csv` | **Organoleptic Entity**: Aroma-active compound possessing specific odor threshold values and chemical identifiers (e.g., *Vanillin [CAS: 121-33-5]*, *Limonene [CAS: 5989-27-5]*). Linked to FlavorDB and PubChem. |
| 14 | `SensoryFlavorDescriptor` | **Canonical Node** | `Nodes/SensoryFlavorDescriptors.csv` | **Sensory Descriptor**: Controlled vocabulary of sensory aroma descriptors (e.g., *citrus*, *caramel*, *woody*, *green*, *sweet*). Connects flavor molecules to human perceptual qualities. (Replaces legacy ambiguous `Flavors.csv`). |
| 15 | `FunctionalRole` | **Canonical Node** | `Nodes/FunctionalRoles.csv` | **Techno-Functional Purpose**: Standardized techno-functional classification based on Codex INS and FoodOn (e.g., *Emulsifier*, *Stabilizer*, *Thickener*, *Acidulant*, *Antioxidant*, *Sweetener*). |
| 16 | `PropertyMeasurement` | **Reified Node** | `Nodes/PropertyMeasurements.csv` | **Empirical Physical Observation**: Measured rheological, thermal, or physical parameters (e.g., viscosity, water holding capacity, gel strength, melting profile) with explicit testing conditions (`temperature`, `shear_rate`, `pH`). Distinct from manufacturer acceptance limits (`IngredientSpecification`). |
| 17 | `MeasurementMethod` | **Node Property / Citation** | Property `method_reference` on Measurements | **Analytical Standard**: Standardized test method string (e.g., *AOAC 991.43*, *Karl Fischer Titration*, *Brookfield Viscometry RV-4*). Embedded in measurement records. |
| 18 | `Allergen` | **Canonical Node** | `Nodes/Allergens.csv` | **Regulatory Safety Entity**: Major statutory allergen classes (US Big 9, EU 14, FSSAI Schedule): *Milk, Eggs, Peanuts, Tree Nuts, Fish, Crustacean Shellfish, Wheat, Soy, Sesame, Celery, Mustard, Lupin, Molluscs, Sulphites*. |

---

### Group C: Ingredient Compatibility and Constraints

| # | Concept Name | Target Classification | Target Artifact / Storage Location | Structural Definition & Justification |
|---|---|---|---|---|
| 19 | `IngredientInteraction` | **Reified Node** | `Nodes/IngredientInteractions.csv` | **Bilateral Matrix Interaction**: Reified node capturing documented matrix interactions between ingredient pairs (e.g., *Xanthan Gum + Locust Bean Gum synergistic gelation*; *Milk Protein + Anthocyanin precipitation*). Stores matrix conditions, pH, and observed effect. |
| 20 | `CompatibilityRule` | **Canonical Node** | `Nodes/CompatibilityRules.csv` | **Declarative Expert Rule**: Generalized formulation rule governing chemical/physical compatibility (e.g., *Do not combine high-calcium salts with sodium alginate in pre-mix liquids without sequestering agents*). |
| 21 | `InteractionMechanism` | **Relationship Property** | Property on `IngredientInteraction` | **Physical Description**: Scientific explanation of interaction (e.g., *electrostatic cross-linking*, *hydrophobic association*, *Maillard condensation*). Stored as an attribute on the interaction node. |
| 22 | `Constraint` | **Canonical Node** | `Nodes/Constraints.csv` | **Bounded Technical Requirement**: Formalized numerical or categorical bounds (`parameter`, `operator`, `limit_value`, `unit`, `basis`, `scope`). Enforces regulatory limits, client brief limits, and physical stability thresholds. |
| 23 | `ConstraintEvaluation` | **Runtime-Only Entity** | Backend Formulation Engine | **Downstream Runtime Artifact**: Result of evaluating a candidate formulation against a `Constraint` (pass, fail, slack value). Generated during solver execution; excluded from the static Knowledge Graph CSV preparation. |

---

### Group D: Recipes, Commercial Products and Formulation

| # | Concept Name | Target Classification | Target Artifact / Storage Location | Structural Definition & Justification |
|---|---|---|---|---|
| 24 | `Recipe` | **Canonical Node** | `Nodes/Recipes.csv` | **Culinary Recipe**: Home, commercial, or benchmark food preparation record derived from recipe repositories (e.g., Recipe1M+, open food collections). Preserves kitchen preparation units and human instructions. |
| 25 | `RecipeComponent` | **Reified Node** | `Nodes/RecipeComponents.csv` | **Culinary Ingredient Item**: Represents an ingredient entry in a culinary recipe with declared raw quantities (e.g., *2 cups all-purpose flour*, *1 tsp vanilla extract*). |
| 26 | `RecipeStep` | **Canonical Node** | `Nodes/RecipeSteps.csv` | **Culinary Instruction Step**: Sequenced culinary preparation instruction (e.g., *Beat eggs and sugar until frothy*). Linked via `PRECEDES` edges. |
| 27 | `CommercialProduct` | **Canonical Node** | `Nodes/CommercialProducts.csv` | **Retail Packaged Good**: Packaged commercial food product (e.g., *Nutella*, *Coca-Cola*) with GTIN barcode, brand name, net weight, and packaging statement. (Disambiguated from recipes and formulations). |
| 28 | `ProductIngredientDeclaration` | **Reified Node** | `Nodes/ProductIngredientDeclarations.csv` | **Statutory Label Ingredient Item**: Reified declaration of an ingredient on a commercial product package. Stores `declaration_order` ($1, 2, \dots$) and `declared_percentage` (strictly `NULL` if not disclosed on the package). |
| 29 | `Formulation` | **Canonical Node** | `Nodes/Formulations.csv` | **Industrial Product Batch**: Factory formulation distinct from culinary recipes. Governed by 100.000% mass balance, commercial ingredient grades, and industrial process specifications. |
| 30 | `FormulationVersion` | **Canonical Node** | `Nodes/FormulationVersions.csv` | **Formulation Revision**: Specific iteration (e.g., *Rev 1.2 Cost Optimized*, *Rev 2.0 Dairy-Free*) tracking changes in component inclusion, batch size, and pilot test results. |
| 31 | `FormulationComponent` | **Reified Node** | `Nodes/FormulationComponents.csv` | **Industrial Batch Slot**: Precise batch component with `inclusion_percentage` (strictly bounded $x_i \in [0, 100]$ summing to 100%), `min_percentage`, `max_percentage`, `batch_phase`, and links to `IngredientGrade` and `FunctionalRole`. |
| 32 | `OptimizationRun` | **Runtime-Only Entity** | Backend Optimization Log | **Downstream Solver Run**: Log of mathematical optimizer execution (SLSQP iterations, objective values, convergence status). Managed by backend; excluded from ETL preparation CSVs. |
| 33 | `OptimizationObjective` | **Runtime-Only Entity** | Backend Solver Config | **Downstream Mathematical Objective**: Objective function weights (minimize cost, maximize protein, minimize carbon score). Managed by backend solver. |

---

### Group E: Manufacturing and Processing

| # | Concept Name | Target Classification | Target Artifact / Storage Location | Structural Definition & Justification |
|---|---|---|---|---|
| 34 | `Process` | **Canonical Node** | `Nodes/Processes.csv` | **Industrial Unit Operation**: Standard food engineering unit operation (e.g., *High-Shear Mixing*, *High-Pressure Homogenization*, *Direct Steam Injection UHT*, *Twin-Screw Extrusion*, *Fluid Bed Spray Drying*). |
| 35 | `ProcessStep` | **Reified Node** | `Nodes/ProcessSteps.csv` | **Sequenced Manufacturing Stage**: Concrete step in a manufacturing schedule with explicit execution order, target duration, and linked operating parameters. Form a DAG via `PRECEDES` edges. |
| 36 | `ProcessParameter` | **Node Property / Measurement** | Properties on `ProcessStep` | **Operating Setting**: Numerical physical settings (`temperature_celsius`, `pressure_bar`, `rpm`, `residence_time_seconds`). Encapsulated in the `ProcessStep` record. |
| 37 | `Equipment` | **Canonical Node** | `Nodes/Equipment.csv` | **Processing Machinery**: Industrial equipment unit required for processing (e.g., *Twin-Screw Extruder*, *Colloid Mill*, *Pate-Type Heat Exchanger*, *Ribbon Blender*). |
| 38 | `PackagingSpecification` | **Canonical Node** | `Nodes/PackagingSpecifications.csv` | **Container & Barrier Specification**: Industrial packaging system specification (e.g., *Multilayer Barrier Pouch [PET/Alu/PE]*, *Aseptic Carton Tetra Pak*). Stores barrier metrics (OTR, WVTR). |
| 39 | `PackagingMaterial` | **Canonical Node** | `Nodes/PackagingMaterials.csv` | **Substrate Material**: Packaging component material (e.g., *HDPE*, *LDPE*, *PET*, *Glass*, *Aluminum*, *PLA*). Linked to `PackagingSpecification`. |

---

### Group F: Supporting and Governance Node Types

| # | Concept Name | Target Classification | Target Artifact / Storage Location | Structural Definition & Justification |
|---|---|---|---|---|
| 40 | `Supplier` | **Canonical Node** | `Nodes/Suppliers.csv` | **Commercial Vendor**: Commercial manufacturer or distributor of food ingredients and industrial additives (e.g., *Cargill*, *Tate & Lyle*, *Ingredion*, *ADM*, *Kerry*). |
| 41 | `CostRecord` | **Reified Node** | `Nodes/CostRecords.csv` | **Temporal Commercial Price**: Real supplier quotation or market commodity price with `price_value`, `currency`, `pricing_unit`, `price_type` (`COMMODITY_MANDI`, `SUPPLIER_QUOTE`), `region`, `price_date`, `valid_until`, and `supplier_id`. |
| 42 | `Regulation` | **Canonical Node** | `Nodes/Regulations.csv` | **Statutory Legal Instrument**: Governing regulatory law (e.g., *Codex STAN 192-1995*, *FSSAI Food Products Standards 2011*, *US 21 CFR Part 172*, *EU Regulation 1333/2008*). |
| 43 | `RegulatoryPermission` | **Reified Node** | `Nodes/RegulatoryPermissions.csv` | **Legal Provision Assertion**: Explicit statutory authorization connecting an additive to a food category with `max_level_numeric`, `unit`, `jurisdiction`, `status` (*Permitted*, *Prohibited*, *GMP*), and specific legal conditions. Must NOT be inferred from mere additive index listing! |
| 44 | `UseCondition` | **Node Property** | Property `conditions_of_use` on `RegulatoryPermission` | **Legal Restriction Text**: Qualifying statutory conditions (e.g., *"Singularly or in combination with other benzoates calculated as benzoic acid"*, *"GMP only"*). Stored as an attribute on permissions. |
| 45 | `ProcessCondition` | **Node Property** | Embedded in `ProcessSteps` / `PropertyMeasurement` | **Physical Environment**: Environmental operating conditions (e.g., *ambient humidity < 40%*, *inert nitrogen blanketing*). Embedded in step properties. |
| 46 | `ProcessOutcome` | **Node Property** | Property `expected_outcome` on `ProcessStep` | **Physical Transformation**: Declared physical result (e.g., *emulsion droplet size D[4,3] < 2.0 microns*, *commercial sterility Fo = 6.0*). |
| 47 | `ShelfLifeStudy` | **Canonical Node** | `Nodes/ShelfLifeStudies.csv` | **Stability Study Record**: Documented stability study extracted from literature or internal trials with `temperature_celsius`, `relative_humidity`, `duration_days`, and observed failure modes. |
| 48 | `StabilityParameter` | **Node Property / Measurement** | Embedded in `ShelfLifeStudy` | **Kinetic Stability Metric**: Parameters monitored over time (`peroxide_value`, `water_activity`, `ph_drift`, `microbial_cfu_g`). Embedded as measurement records. |
| 49 | `SensoryAttribute` | **Canonical Node** | `Nodes/SensoryAttributes.csv` | **Organoleptic Property**: Quantitative sensory descriptive attributes (e.g., *sweetness_intensity*, *sandiness*, *chalkiness*, *melt_rate*, *grittiness*, *astringency*). |
| 50 | `SensoryEvaluation` | **Reified Node** | `Nodes/SensoryEvaluations.csv` | **Trained Panel Test**: Formal sensory evaluation test on a recipe or formulation version, recording mean attribute scores across a trained panel. |
| 51 | `Evidence` | **Canonical Node** | `Nodes/Evidence.csv` | **Traceable Scientific Citation**: Verifiable excerpt, table reference, or experimental claim extracted from a primary authoritative document (DOI, Patent Number, Legal Gazette, TDS). |
| 52 | `Source` | **Canonical Node** | `Nodes/Sources.csv` | **Authoritative Institution / Database**: Originating organization or repository (e.g., *Codex Alimentarius Commission*, *USDA ARS*, *FSSAI*, *NCBI PubChem*, *FoodOn Consortium*). |
| 53 | `Dataset` | **Canonical Node** | `Nodes/Datasets.csv` | **Concrete Dataset Release**: Versioned release of a source dataset (e.g., *USDA FoodData Central April 2024*, *FoodOn Release 2024-03-15*). Houses SHA-256 integrity hashes. |
| 54 | `Claim` | **Canonical Node** | `Nodes/Claims.csv` | **Standardized Nutrition / Health Claim**: Statutorily regulated label claims (e.g., *High Protein [≥20% energy from protein]*, *Sugar Free [<0.5g/100g]*, *Source of Fiber*). Linked to qualifying criteria. |
