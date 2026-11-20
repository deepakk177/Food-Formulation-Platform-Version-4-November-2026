# Food Formulation Platform — Model & Computational Architecture

This document defines the computational paradigm for every functional requirement in the platform. Rather than naively applying Machine Learning everywhere, each component is strictly assigned to one of five paradigms based on physical laws, mathematical determinism, graph topology, empirical data availability, and causal reasoning.

---

## The 5 Computational Paradigms

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FOOD FORMULATION COMPUTATIONAL ENGINE                    │
├─────────────────┬─────────────────┬─────────────────┬───────────────────────┤
│ A. DETERMINISTIC│ B. DATABASE/KG  │ C. OPTIMIZATION │ D. MACHINE LEARNING   │
│    COMPUTATION  │    RETRIEVAL    │                 │    PREDICTION         │
├─────────────────┼─────────────────┼─────────────────┼───────────────────────┤
│ Mass Balance    │ INS / E-Numbers │ Ingredient Pct  │ Functional Role Class.│
│ Macro Yield     │ Regulatory Perm.│ Multi-Objective │ Matrix Compatibility  │
│ Percentage Norm.│ Allergen Flags  │ Target Distance │ Shelf-Life Kinetics*  │
│ Unit Batch Cost │ Physical Props  │ Gating Bounds   │ Sensory Profiling*    │
└─────────────────┴─────────────────┴─────────────────┴───────────────────────┘
                     │ E. LLM / AGENT REASONING
                     ├─────────────────────────
                     │ Brief Interpretation
                     │ Constraint Parsing
                     │ Scientific Explanations
```
*\*Note: Shelf-life kinetics and sensory profiling are designated ML targets where available, but will report `INSUFFICIENT LABELED DATA` / `DATA_UNAVAILABLE` until experimental ground-truth calibration datasets are loaded.*

---

## Classification Matrix

### Category A: Deterministic Computation

**Definition**: Operations governed by conservation of mass, arithmetic identity, linear algebra, or definitive unit accounting. Adding ML or stochastic heuristics here introduces error, violates physical laws, and is scientifically invalid.

| Component | Input Features | Exact Computation | Why Deterministic? | Output |
|---|---|---|---|---|
| **Formulation Mass Balance** | Ingredient mass percentages $x_i$ | $\sum_{i=1}^n x_i = 100.0000\%$ | Conservation of mass is an absolute physical law. A formulation cannot sum to 98% or 102%. | Feasibility boolean, normalization factor |
| **Nutritional Macro Yield** | Formulation percentages $x_i$, ingredient nutrition per 100g $N_{i,m}$ | $Y_m = \sum_{i=1}^n \left(\frac{x_i}{100} \times N_{i,m}\right)$ | Macronutrient content in a compound mixture is the exact weighted linear sum of constituent nutrients. | Protein, Fat, Carbs, Energy, Sodium per 100g |
| **Batch Cost Calculation** | Formulation percentages $x_i$, verified unit costs $C_i$ ($/kg) | $\text{Cost}_{\text{raw}} = \sum_{i=1}^n \left(\frac{x_i}{100} \times C_i\right)$ | Financial raw material cost is exact multiplication. If any $C_i$ is missing, status must be `COST_UNKNOWN`. | Exact $/kg, or `COST_UNKNOWN` |
| **Percentage Normalization** | Raw mass weights $w_i$ | $x_i = \frac{w_i}{\sum w_k} \times 100\%$ | Standard unit conversion preserving minor precision down to 0.0001%. | Standardized percentage array |
| **Nutritional Compliance Score** | Actual yield $Y_{\text{prot}}$, target $T_{\text{prot}}$ | $\min\left(100, \frac{Y_{\text{prot}}}{\max(1, T_{\text{prot}})} \times 100\right)$ | Exact mathematical distance to target objective. | 0.0 – 100.0 score |

---

### Category B: Database / Knowledge Graph Retrieval

**Definition**: Grounded factual truths that already exist in verified biological, chemical, or regulatory registries. Predicting these with ML risks hallucinations and severe regulatory non-compliance.

| Component | Database / KG Source | Query / Retrieval Method | Why DB/KG? | Output |
|---|---|---|---|---|
| **INS / E-Number Codes** | Codex Alimentarius / CXG 036e table (`INS.csv`) | Direct lookup by canonical chemical entity ID / CAS | INS numbers are globally standardized international codes, not predictable variables. | INS string or `None` |
| **Regional Regulatory Permissions** | Codex GSFA, FSSAI regulations, EU 231/2012 (`foodadditive_allowed_in_foodcategory.csv`) | Composite join on `(additive_id, food_category_id, jurisdiction)` | Legal legality is a codified statute. Predicting legal status with ML creates legal liability. | `PERMITTED`, `PROHIBITED`, `UNKNOWN` + Max Level |
| **Allergen Declarations** | FALCPA / EU FIC 1169 Allergen tables (`Allergens.csv`, `ingredient_has_allergen.csv`) | Graph traversal `(Ingredient)-[:HAS_ALLERGEN]->(Allergen)` | Food allergens are biochemical facts of raw material species origin. | Allergen list or `None` / `UNKNOWN` |
| **Verified Physicochemical Properties** | FooDB / USDA FDC compound tables (`Properties.csv`, `ingredient_has_property.csv`) | Property lookup by ingredient ID | Density, water-solubility, melting point are experimentally measured constants. | Property dictionary or `UNKNOWN` |
| **Scientific Literature Evidence** | Peer-reviewed citations, patent sources (`Evidence.csv`, `Sources.csv`) | Provenance lineage join `(Entity)-[:SUPPORTED_BY]->(Evidence)` | Evidence provenance must cite verified scientific publications. | Citation string, DOI, source ID |

---

### Category C: Numerical Formulation Optimization

**Definition**: Multi-variable continuous decision problems where ingredient percentages must be chosen to satisfy conflicting constraints (e.g. target protein $\ge 30\%$, max sugar $\le 5\%$, cost $\le \$10/\text{kg}$, mass sum $= 100\%$).

| Component | Objective Function | Constraints | Solver Engine | Why Optimization? |
|---|---|---|---|---|
| **Candidate Formulation Generator** | $\min_{x} w_{\text{nutr}}\|N x - T\|^2 + w_{\text{cost}} C^T x - w_{\text{func}} F^T x$ | $\sum x_i = 100\%$, $l_i \le x_i \le u_i$, $A_{\text{diet}} x = 0$ | `scipy.optimize.minimize` (SLSQP / Trust-Constr) | Ingredient percentages must not be hardcoded or guessed; they must solve the multi-objective Pareto front. |
| **Strategy Multi-Candidate Profiler** | Tailored weights: Nutrition-Maximized, Cost-Minimizing, Balanced | Category-specific inclusion bounds, functional minimum thresholds | Sequential Quadratic Programming with variable penalty factors | Produces genuinely distinct, mathematically feasible candidates. |

---

### Category D: Machine Learning Prediction

**Definition**: Complex nonlinear relationships where first-principles physics is intractable or high-dimensional, but empirical data or structural similarities provide predictive power.

| Component | Model Family | Input Features | Ground Truth Target | Status / Data Availability |
|---|---|---|---|---|
| **Ingredient Functional Role Classifier** | LightGBM / Random Forest Classifier | Macro profile (protein, fat, carbs, calories), physical category, physicochemical descriptors | Functional role (`Protein Source`, `Emulsifier`, `Bulking Agent`, `Stabilizer`, etc.) | **REAL DATASET AVAILABLE** (23,876 ingredients). Model will be trained, evaluated, and deployed. |
| **Pairwise Ingredient Compatibility Predictor** | Gradient Boosted Classifier / Graph Neural Similarity | Compound co-occurrence, pH delta, ionic interaction, polarity similarity | Compatibility class (`COMPATIBLE`, `INCOMPATIBLE`, `NEUTRAL`) | **REAL SEED DATASET AVAILABLE** (`ingredient_interactions.csv`, FooDB co-occurrence). |
| **Formulation Shelf-Life Estimator** | ElasticNet / Gradient Boosted Regressor | Formulation water activity ($a_w$), pH, preservative concentration, packaging transmission rate | Measured shelf life in days/months | **INSUFFICIENT LABELED DATA**: No experimental storage testing labels exist in repository. Will report `INSUFFICIENT LABELED DATA` / `DATA_UNAVAILABLE`. |
| **Descriptive Sensory Texture Predictor** | Multi-output Random Forest Regressor | Viscosity modifiers, lipid fraction, hydrocolloid ratio, total soluble solids | Descriptive sensory panel ratings (firmness, adhesiveness, creaminess) | **INSUFFICIENT LABELED DATA**: No trained sensory panel dataset present. Will report `INSUFFICIENT LABELED DATA` / `DATA_UNAVAILABLE`. |

---

### Category E: LLM / Agent Reasoning

**Definition**: Unstructured natural language comprehension, semantic intent translation, and synthesis of human-readable scientific justifications grounded strictly in retrieved facts.

| Component | Prompt / Model | Input | Validation Gate | Why LLM? |
|---|---|---|---|---|
| **Product Brief NLP Parser** | Structured Schema LLM / Few-Shot Pydantic | User natural language prompt (e.g. "vegan protein bar with 30g protein, no added sugar") | Pydantic validation of `ProductBrief` | Humans specify food goals in freeform language with colloquial terms. |
| **Formulation Scientific Dossier Synthesizer** | Grounded Groq Llama-3.3 / Deterministic Fallback | Validated candidate set + retrieved evidence citations | Strict anti-hallucination validation (rejects any ingredient not in candidate set) | Translates mathematical optimization results into professional food science technical reports. |

---

## Architectural Decision Summary

1. **Mass balance, macros, costs, and percentage normalizations** will NEVER use ML or heuristic estimations. They are 100% deterministic code in `candidate_engine.py` and `scoring_engine.py`.
2. **Ingredient percentages** will NEVER be hardcoded constants. They are generated via `scipy.optimize` numerical optimization.
3. **INS codes, allergen tags, regulatory max levels, and evidence citations** will NEVER be fabricated or hallucinated. They are queried from KG SQLite tables.
4. **Machine Learning** is trained and evaluated with real train/val/test splits on 23,876 verified food ingredients for Functional Role & Matrix Classification.
5. **Shelf life and sensory prediction** will return `DATA_UNAVAILABLE / INSUFFICIENT_LABELED_DATA` with confidence = None rather than faking 9 months or smooth texture.
