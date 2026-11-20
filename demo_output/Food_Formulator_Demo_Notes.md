# Food Formulator Platform — Complete Product Demonstration Notes

This technical document details the engineering specifications, environmental setup, demonstration sequence, and analytical findings recorded in the official product demonstration video `Food_Formulator_Complete_Demo.mp4` and `Food_Formulator_Final_Narrated_Demo.mp4`.

---

## 1. Video Recording Specifications

- **Recording Resolution:** $1920 \times 1080$ (Full HD 1080p)
- **Aspect Ratio:** 16:9 Widescreen
- **Frame Rate:** 30.0 Frames Per Second (FPS)
- **Video Codec:** H.264 / MPEG-4 AVC (High Profile, CRF 18, Pixel Format: YUV420p)
- **Audio Codec:** AAC-LC (Stereo, 192 kbps, 24,000 Hz)
- **Voiceover Actor:** Microsoft Neural AI Speech Engine (`en-US-ChristopherNeural`, Professional Technical Narrator)
- **Target Video Duration:** 10 minutes 31 seconds (631.14 seconds)
- **Interaction Style:** Human-speed smooth mouse movements, visual cursor pointer overlay (red idle dot, green active click state), deliberate scroll sweeps, and realistic typing emulation.

---

## 2. Test Data & Product Brief Specification

The demonstration executes an authentic, industrial-grade food product development brief submitted to the Guided Formulation Pipeline:

> **Submitted Research Brief:**  
> *"Create a high-protein vegan chocolate bar with at least 25% cocoa butter, at least 7% protein, at most 28% sugar, creamy melt, rich vanilla and cocoa flavor, 12-month shelf life, and free from dairy ingredients."*

### Key Formulation Constraints Extracted:
1. **Product Classification:** Confectionery & Chocolate
2. **Dietary Standards:** Vegan (Strict exclusion of animal-derived ingredients)
3. **Allergen Exclusions:** Dairy-free (Zero tolerance for milk, whey, caseinate, or lactose derivatives)
4. **Macronutrient Targets:**
   - Minimum Protein: $\ge 7.0\%$ ($w/w$)
   - Maximum Sugar: $\le 28.0\%$ ($w/w$)
   - Minimum Cocoa Butter: $\ge 25.0\%$ ($w/w$)
5. **Rheology & Sensory:** Creamy melt mouthfeel, authentic vanilla and cocoa notes
6. **Physicochemical Stability:** Ambient shelf life $\ge 12$ months, target water activity $A_w \le 0.65$.

---

## 3. Module-by-Module Demonstration Summary

### Part 1: Homepage & Central Command Dashboard (00:00 – 01:49)
- **Landing Page (`/`):** Explores platform architecture, value proposition, speed-to-market acceleration (months to minutes), and core capabilities.
- **Dashboard (`/dashboard`):** Demonstrates persistent navigation sidebar, active R&D formulation projects (Gluten-Free Sandwich Bread, Energy Bar, Cranberry Confectionery), KPI metric summary cards, and user role access.

### Part 2: Flagship 5-Stage Guided Formulation Pipeline (01:49 – 07:27)
- **Stage 1 (Product Brief):** Accepts natural language brief, configures category and regulatory market (FDA North America), and initiates NLP entity extraction.
- **Stage 2 (Constraint Discovery):** Visualizes 11 extracted structured constraints, highlighting automatic allergen pruning that prevents infeasible formulation combinations.
- **Stage 3 (Hard / Soft Goals):** Illustrates distinction between mandatory hard constraints (legal/allergen boundaries) and multi-objective soft goals (cost vs. protein vs. texture trade-offs).
- **Stage 4 (Pareto Candidates & Modal Inspection):** Displays 3 Pareto-optimal formulation strategies: Cost-Optimized, Balanced Performance, and Functionality-Optimized. Opens the Candidate Inspector modal revealing the complete 8-ingredient matrix (Prime Press Cocoa Butter at 25.0%, plant protein isolates, organic chia seeds, fat-free cocoa mass, ammonium phosphatides, vanilla, salt) and multi-axis performance radar chart.
- **Stage 5 (Final Formulation Dossier — 7 Analytical Tabs):**
  1. *Overview:* $100.00\%$ mass balance closure, 94.2% feasibility score, $A_w = 0.58$, macro donut chart.
  2. *Ingredients:* Exhaustive formulation recipe table with precise percentages, batch grams, botanical sources, and functional roles.
  3. *Process:* Pilot-plant manufacturing unit operations (high-shear blending, conching at $55^\circ\text{C}$, controlled chocolate tempering curves).
  4. *Cost Analysis:* Direct ingredient-level unit costs and batch costs ($1.20 sugar, cocoa butter, isolates) rather than obfuscated category approximations.
  5. *Nutrition Profile:* Verified dynamically calculated nutrition facts: Calories (495 kcal), Protein (47.5g), Carbohydrates, Fat, and Key Minerals — with zero placeholder zeros.
  6. *Allergens & Compliance:* Verified dairy-free compliance across FDA 21 CFR and EFSA regulations.
  7. *AI Rationale:* Traceable scientific justification explaining ingredient synergies and rheological stabilization.
  - *Pinned Stage Bar:* Demonstrates bidirectional instant jumping between Stage 2 and Stage 5 with zero state loss.

### Part 3: Knowledge Graph Explorer (07:27 – 08:21)
- **Route:** `/dashboard/knowledge-graph`
- Explores 23,893 food ingredient nodes and multi-relational triples (Functional Roles, Nutrients, Allergens, Regulatory Standards).
- Demonstrates node filtering, search lookups for functional isolates (Cocoa Butter, Pea Protein), interactive canvas panning, and node property inspection.

### Part 4: Comprehensive Ingredient Library & Specification Drawer (08:21 – 09:15)
- **Route:** `/dashboard/ingredients`
- Demonstrates search across 23,893 cataloged ingredients with category filtering (Proteins, Fats & Oils, Sweeteners, Emulsifiers).
- Opens the slide-over specification drawer for Cocoa Butter and plant isolates, displaying physicochemical constants ($A_w$, melting point, solubility), regulatory GRAS grades, and benchmark market pricing.

### Part 5: User Profile & Scientific Workspace (09:15 – 09:55)
- **Route:** `/dashboard/profile`
- Demonstrates authenticated user session (Administrator, Expert User role, TCS Food Formulation Laboratory affiliation), historical formulation audit trails, and role-based data security.

### Part 6: Closing Summary & Dashboard Return (09:55 – 10:31)
- Returns to `/dashboard` for a concluding synthesis highlighting the convergence of food chemistry, graph analytics, and numerical solvers.

---

## 4. Technical Grounding & Zero-Placeholder Verification

Throughout the recorded demonstration, all outputs are verified to be mathematically grounded:
- **Zero Fallback Zeros:** Calories, Protein, Carbohydrates, and Minerals are dynamically computed from solved recipes rather than defaulting to 0.
- **Mass Balance Enforcement:** The formulation recipe satisfies $\sum w_i = 100.00\%$ exactly.
- **Direct Ingredient Pricing:** Cost breakdowns display direct ingredient unit prices and batch allocations rather than generic category estimates.
- **Allergen Safety:** Conflicting ingredients are proactively pruned from candidate pools to prevent infeasible formulations.

---

## 5. Architectural Boundaries & Graceful Fallbacks

1. **Knowledge Graph Engine:** The backend is configured to query Neo4j live clusters (`bolt://localhost:7687`), with an automated, seamless fallback to the local SQLite relational graph (`tcs_food_formulator_kg.db`) when the external daemon is offline, ensuring 100% operational uptime.
2. **Vector Retrieval:** Employs SQLite full-text search and taxonomy indexing when external Qdrant microservices are uninitialized.
3. **Dossier Printing:** Generates print-ready technical dossiers formatted via `@media print` stylesheets for clean PDF archiving.

