# PHASE 0.1 / 0.2: RECIPE AND INDUSTRIAL FORMULATION EXTRACTION CONTRACTS

**Document Version:** 2.0.0 (Phase 0.2 Revision)  
**Status:** FROZEN & RATIFIED  
**Scope:** Extraction contracts and structural separation for Culinary Recipes, Commercial Product Declarations, Industrial Patent Formulations, Research Paper Experiments, and AI-Generated Candidates.

---

## 1. The Five Distinct Extraction Contracts

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               THE FIVE EXTRACTION CONTRACTS                            │
├──────────────────────────┬──────────────────────────┬──────────────────────────────────┤
│ Contract Type            │ Quantities & Inclusions  │ Processing Context               │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ 1. Culinary Recipe       │ Disclosed kitchen units  │ Sequenced kitchen steps          │
│                          │ Volumetric -> Mass calc  │ (e.g. "whisk at high speed")     │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ 2. Product Declaration   │ Rank order (1, 2, ... n) │ No unit operations               │
│                          │ Exact % STRICTLY NULL    │ Package claims & allergens only  │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ 3. Industrial Patent     │ Exact % w/w (sum = 100%) │ Factory unit operations          │
│                          │ Batch scaling basis      │ (shear, rpm, barrel temperature) │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ 4. Research Experiment   │ Experimental dosage      │ Analytical testing conditions    │
│                          │ (e.g. 0.5% vs 1.0% w/w)  │ (rheometer, texture analyzer)    │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ 5. AI-Generated Candidate│ Optimized percentages    │ Predicted unit operations        │
│                          │ Downstream solver output │ Virtual state (excluded from KG) │
└──────────────────────────┴──────────────────────────┴──────────────────────────────────┘
```

---

## 2. Extraction Contract 1: Culinary Recipes (`Recipe`)

- **Applicable Sources**: Recipe1M+, Food.com, authentic digital cookbooks.
- **Node Targets**: `Recipe`, `RecipeComponent`, `RecipeStep`.
- **Extraction Rules**:
  1. Extract verbatim component string into `raw_text` (e.g., *"2 1/2 cups unbleached all-purpose flour"*).
  2. Parse numerical quantity and unit deterministically into `quantity_numeric` (`2.5`) and `quantity_unit` (`cup`).
  3. If volumetric units are present, standard bulk density tables may be used to compute `estimated_mass_grams` ($300.0\text{ g}$). This field is tagged with `verification_status = CALCULATION_VERIFIED`.
  4. Parse preparation techniques (*"sifted"*, *"melted"*, *"diced"*) into `preparation_notes`.
  5. Parse preparation instructions into sequenced `RecipeStep` records linked by `PRECEDES` edges.

---

## 3. Extraction Contract 2: Commercial Product Declarations (`CommercialProduct`)

- **Applicable Sources**: Open Food Facts, retail supermarket label crawls.
- **Node Targets**: `CommercialProduct`, `ProductIngredientDeclaration`.
- **Extraction Rules**:
  1. Extract retail GTIN barcode, brand owner, product name, net contents, and complete verbatim statutory ingredient statement.
  2. Segment ingredient declaration by commas and parenthetical sub-clauses into discrete items.
  3. Assign statutory `declaration_order` ($1, 2, \dots, n$, where $1$ is greatest weight).
  4. **PERCENTAGE EXTRACTION RULE**:
     - `declared_percentage` is populated **ONLY** if an explicit percentage is printed on the package (e.g., *"hazelnuts (13%)"* $\rightarrow 13.0\%$).
     - If no percentage is printed, `declared_percentage` is strictly `NULL`.
     - **ABSOLUTE PROHIBITION**: The pipeline shall **never** synthesize, estimate, or infer exact formulation percentages from ingredient rank order. A consumer packaging label is not a factory recipe.
  5. Flag characterizing ingredients (`is_characterizing = true`) when ingredients are highlighted in product branding or marketing copy.

---

## 4. Extraction Contract 3: Industrial Patent Formulations (`Formulation`)

- **Applicable Sources**: USPTO, EPO, and WIPO patent disclosures, pilot plant batch logs.
- **Node Targets**: `Formulation`, `FormulationVersion`, `FormulationComponent`, `ProcessStep`.
- **Extraction Rules**:
  1. Extract target food matrix title, patent grant number, example number (e.g., *Example 1, Formulation B*), and reference batch mass.
  2. Extract tabular component inclusion levels. Inclusion levels must be converted to **percentage of total formulation mass** ($\% \text{ w/w}$).
  3. **MATHEMATICAL INVARIANT**: The sum of all component inclusion percentages must satisfy mass balance:
     $$\sum_{i=1}^n x_i = 100.000\% \pm 0.005\%$$
     If mass balance does not sum to 100%, components must be audited for missing solvent/water carriers before normalization.
  4. Extract manufacturing process parameters (`temperature_celsius`, `pressure_bar`, `shear_rpm`, `holding_time_seconds`) into sequenced `ProcessStep` nodes linked to `Equipment`.

---

## 5. Extraction Contract 4: Research Paper Experiments (`IngredientInteraction`)

- **Applicable Sources**: Peer-reviewed food science literature (Elsevier, Wiley, Springer).
- **Node Targets**: `IngredientInteraction`, `PropertyMeasurement`, `ShelfLifeStudy`, `Evidence`.
- **Extraction Rules**:
  1. Identify experimental factors: ingredient pair, concentration range, solution pH, ionic strength, and thermal history.
  2. Extract measured rheological or physical response: apparent viscosity, storage modulus ($G'$), loss modulus ($G''$), syneresis percentage, or particle size distribution ($D[4,3]$).
  3. Formulate `IngredientInteraction` record with explicit matrix conditions.
  4. Binds directly to an `Evidence` node containing verbatim excerpt, DOI, page number, and table number.

---

## 6. Extraction Contract 5: AI-Generated Formulation Candidates

- **Applicable Sources**: Downstream backend formulation optimization engine (`candidate_engine.py` / `scipy.optimize`).
- **Entity**: `AICandidateFormulation`.
- **Rules**:
  1. Generated downstream during user session execution; **excluded from the static Knowledge Graph preparation ETL pipeline**.
  2. Bounded by strict equality constraint $\sum x_i = 100.000\%$.
  3. Outputs carry solver convergence metadata, mass balance slack, constraint satisfaction score, and validation gate audit status.
  4. **ABSOLUTE PROHIBITION**: Generated AI formulation candidates must **never** be saved into the Knowledge Graph as historical recipe priors or ground truth formulations.
