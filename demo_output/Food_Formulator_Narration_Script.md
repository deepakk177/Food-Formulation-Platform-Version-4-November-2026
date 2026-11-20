# Food Formulator Platform — Narration Script & Scene Guide

## Scene 1: Platform Introduction & Landing Page
- **Timestamp:** `00:00 – 00:55 (55.0s)` | **Route:** `/`
- **Visual Demonstration:** Full browser capture on http://localhost:3000/. Smooth mouse pointer hovers over platform hero section, scrolls deliberately down through computational architecture diagrams, feature highlight cards, and regulatory compliance standards, then scrolls back to top and clicks 'Go to Dashboard'.
- **Technical Notes:** Highlights the business problem (long R&D cycles, ingredient substitution costs) and positions the platform's multi-layered architecture: NLP parsing, Knowledge Graph triples, and SLSQP numerical solver.

> **Narration:**
> "Welcome to the Food Formulation AI Platform — an enterprise-grade computational intelligence system engineered for food scientists, research chefs, and product development engineers. In modern industrial food manufacturing, developing new formulations has historically been a lengthy, trial-and-error endeavor, often demanding dozens of bench-top kitchen trials, pilot-plant test runs, and extensive sensory panels that can span six to eighteen months. The Food Formulator platform transforms this paradigm by combining an extensive knowledge graph of nearly twenty-four thousand characterized ingredients with automated constraint discovery, numerical mass balance optimization, and multi-jurisdictional regulatory compliance. In this comprehensive demonstration, we will explore the complete end-to-end capabilities of the platform, from unstructured brief submission to final manufacturing specification."

## Scene 2: Central Command Dashboard & Workspace Overview
- **Timestamp:** `00:55 – 01:49 (54.0s)` | **Route:** `/dashboard`
- **Visual Demonstration:** Cursor demonstrates persistent left-hand navigation sidebar (Dashboard, Guided Formulator, Expert Studio, Ingredient Catalog, Knowledge Graph, Compliance, Profile). Hovers across KPI summary cards (Active Formulations, 23,893 Indexed Nodes, Compliance Pass Rate). Scrolls down to view existing research projects (Gluten-Free Sandwich Bread, Energy Bar, Cranberry Delight), then navigates to the Guided Formulator.
- **Technical Notes:** Demonstrates enterprise project management, multi-formulation tracking, and role-based laboratory organization.

> **Narration:**
> "We begin on the central application dashboard. The persistent left-hand navigation sidebar provides seamless access to all platform modules: the Five-Stage Guided Formulation Wizard, the Expert Studio for manual formulation adjustments, the comprehensive Ingredient Catalog, the interactive Knowledge Graph Explorer, and the Multi-Jurisdictional Regulatory Matrix. On the main dashboard canvas, formulation teams can monitor active research and development projects, overall compliance pass rates, total ingredient nodes indexed in the system, and cost optimization benchmarks. We can also review existing projects in the laboratory database, such as Gluten-Free Sandwich Bread, Energy Bars, and Cranberry Protein Confectionery. Each project maintains its own formulation iterations, target parameters, and regulatory audit trail."

## Scene 3: Stage 1: Natural Language Product Brief Submission
- **Timestamp:** `01:49 – 02:49 (60.8s)` | **Route:** `/dashboard/formulate/guided (Stage 1)`
- **Visual Demonstration:** Highlights the persistent pinned progress stepper bar at top. Selects category 'Confectionery & Chocolate', focuses on brief textarea, and types the exact user brief at realistic typing speed. Sets target market to North America FDA, scrolls down, and clicks 'Analyze Brief & Recommend Constraints'.
- **Technical Notes:** Demonstrates natural language processing (NLP) extracting multi-modal constraints from freeform industrial text.

> **Narration:**
> "We now enter the Guided Formulator to begin our flagship five-stage workflow. Stage 1 accepts unstructured natural-language product specifications directly from marketing or culinary briefs. For this demonstration, we submit a rigorous commercial requirement: Create a high-protein vegan chocolate bar with at least 25% cocoa butter, at least 7% protein, at most 28% sugar, creamy melt, rich vanilla and cocoa flavor, 12-month shelf life, and free from dairy ingredients. Notice how this brief encapsulates multiple interdependent constraints: compositional floors for cocoa butter, nutritional thresholds for protein and sugar, strict vegan and dairy-free dietary standards, rheological texture preferences, and ambient shelf-life stability. We select Confectionery and Chocolate as our target category, designate North America FDA as our target market, and click Analyze Brief to trigger the natural language processing engine."

## Scene 4: Stage 2: Automated Constraint Discovery & Entity Extraction
- **Timestamp:** `02:49 – 03:45 (55.4s)` | **Route:** `/dashboard/formulate/guided (Stage 2)`
- **Visual Demonstration:** Displays the 11 discovered structured constraints. Cursor moves over parameter rows: vegan dietary status, dairy allergen prohibition, protein floor >= 7%, sugar ceiling <= 28%, cocoa butter >= 25%, creamy melt mouthfeel, and 12-month shelf life. Scrolls down to inspect the full list, highlighting allergen pruning, and clicks 'Configure Hard & Soft Constraints'.
- **Technical Notes:** Explains automated entity classification, confidence scores, and safety pruning preventing conflicting or infeasible candidate generation.

> **Narration:**
> "In Stage 2, the extraction engine has parsed the brief and successfully discovered eleven distinct structured constraints. The system maps the requirements into actionable parameters: mandatory vegan dietary status, complete dairy allergen exclusion, a minimum protein target of 7%, a maximum sugar ceiling of 28%, and a critical minimum of 25% cocoa butter to ensure authentic chocolate crystallization and snap. Sensory attributes including creamy melt mouthfeel and rich vanilla and cocoa flavor profiles are identified as functional targets, alongside a 12-month ambient shelf-life requirement. Crucially, the platform automatically prunes conflicting ingredients and impossible allergen constraints before solving, preventing infeasible formulation sets. With all discovered constraints verified, we advance to goal prioritization."

## Scene 5: Stage 3: Hard Constraints & Soft Objectives Prioritization
- **Timestamp:** `03:45 – 04:37 (52.7s)` | **Route:** `/dashboard/formulate/guided (Stage 3)`
- **Visual Demonstration:** Inspects Hard Constraints table (binary boundary conditions) and Soft Objectives table. Moves cursor to demonstrate toggling constraints between hard and soft modes and tuning multi-objective priority sliders (cost vs. protein vs. texture). Clicks 'Run AI Formulation Search' to execute the solver.
- **Technical Notes:** Details the mathematical distinction between equality/inequality hard boundary conditions vs. multi-objective soft cost functions.

> **Narration:**
> "Stage 3 demonstrates the platform's flexible constraint management interface. Here, constraints are divided into two distinct operational classes: Hard Constraints and Soft Objectives. Hard constraints represent non-negotiable feasibility boundaries — including food safety regulations, legal maximums, and zero-tolerance allergen exclusions. If a formulation candidate violates even one hard constraint, it is mathematically disqualified. In contrast, soft objectives guide the multi-objective Pareto solver, allowing the formulator to adjust priority weights between ingredient cost minimization, nutritional density, and sensory texture scores. Formulators can seamlessly toggle constraints between hard and soft tiers or fine-tune slider weights before triggering the numerical optimization solver."

## Scene 6: Stage 4: Pareto Candidate Generation & Deep-Dive Inspection
- **Timestamp:** `04:37 – 05:45 (68.0s)` | **Route:** `/dashboard/formulate/guided (Stage 4)`
- **Visual Demonstration:** Displays the 3 synthesized Pareto strategy cards: Cost-Optimized, Balanced Performance, and Functionality & Texture Optimized. Clicks 'Inspect Candidate Set' on Candidate 1 to open the deep-dive modal dialog. Scrolls through the complete 8-ingredient table (Prime Press Cocoa Butter at 25.0%, plant protein isolates, organic chia seeds, fat-free cocoa mass, ammonium phosphatides, vanilla, salt). Switches to the radar chart tab. Clicks 'Select This Candidate Set & View Final Report'.
- **Technical Notes:** Validates exact compliance with user brief: Prime Press Cocoa Butter at exactly 25.0%, plant proteins, zero dairy, and Pareto score evaluation.

> **Narration:**
> "In Stage 4, the platform delivers distinct candidate formulation sets synthesized by our numerical engine. Under the hood, the backend queries our 23,893-ingredient knowledge base and executes a Sequential Least Squares Programming algorithm to optimize the recipe subjected to exact mass balance and nutritional target equations. The system generates three distinct strategic formulation variants: a Cost-Optimized Strategy, a Balanced Performance Strategy, and a Functionality and Texture-Optimized Strategy. Opening the Candidate Inspector modal provides complete transparency into the formulated recipe: Prime Press Cocoa Butter at exactly 25.0% satisfying our brief, high-purity plant protein isolates, organic chia seeds providing rheological viscosity, fat-free cocoa mass, ammonium phosphatides as an emulsifier, and natural vanilla flavor systems. We also inspect the multi-axis performance radar chart evaluating cost, nutrition, stability, and clean-label index before selecting this candidate set for final reporting."

## Scene 7: Stage 5: Final Formulation Dossier (All 7 Analytical Tabs)
- **Timestamp:** `05:45 – 07:27 (101.6s)` | **Route:** `/dashboard/formulate/guided (Stage 5)`
- **Visual Demonstration:** Demonstrates all seven analytical tabs systematically: (1) Overview: 100.00% mass balance, 94.2% score, Aw=0.58, donut chart. (2) Ingredients: full recipe table with exact percentages, grams, and botanical roles. (3) Process: blending, refining, conching at 55C, tempering curves, CCPs. (4) Cost Analysis: direct raw material unit prices ($1.20 sugar, cocoa butter, isolates). (5) Nutrition Profile: Calories (495 kcal), Protein (47.5g), Carbs, Minerals. (6) Allergens & Compliance: vegan confirmed, zero dairy cross-contact, FDA/EFSA badges. (7) AI Rationale: substitution logic. Clicks persistent stage bar back to Stage 2 and forward to Stage 5.
- **Technical Notes:** Highlights complete zero-placeholder enforcement, true mass-balance closure, direct ingredient costing, and state persistence via the pinned navigation bar.

> **Narration:**
> "Stage 5 presents the complete seven-tab Technical Formulation Dossier — an industrial-grade manufacturing specification. In Tab 1, Overview, we confirm complete 100.00% mass balance closure, a high feasibility score of 94%, a water activity of 0.58 guaranteeing shelf-stability without artificial preservatives, and an interactive macronutrient donut chart. In Tab 2, Ingredients, we examine the complete production recipe with exact percentages, gram allocations, and botanical functional roles. Tab 3, Process, outlines the pilot-plant manufacturing protocol, detailing high-shear dry blending, fat melting, refining, conching at 55 degrees Celsius, and controlled tempering curves. In Tab 4, Cost Analysis, costs are presented directly per individual raw material — avoiding vague category approximations. Tab 5, Nutrition Profile, displays dynamically calculated values: 495 kilocalories, 47.5 grams of protein, carbohydrates, and key minerals with zero placeholder values. Tab 6, Allergens and Compliance, verifies full compliance with FDA 21 CFR and EFSA standards, confirming zero dairy cross-contact risk. Finally, Tab 7, AI Rationale, details the scientific justification behind each ingredient substitution. Notice also the pinned stage bar at the top, enabling instant bidirectional navigation across all stages without data loss."

## Scene 8: Knowledge Graph Explorer & Semantic Traversal
- **Timestamp:** `07:27 – 08:21 (53.9s)` | **Route:** `/dashboard/knowledge-graph`
- **Visual Demonstration:** Loads interactive Knowledge Graph module. Highlights total node count: 23,893 nodes indexed. Clicks node type filters (Ingredients, Functional Roles, Allergens, Nutrients). Types 'Cocoa Butter' into graph search. Panning across force-directed canvas. Clicks node to inspect metadata and connected edges.
- **Technical Notes:** Explains semantic graph modeling, ontological triple structure, and fallback mechanism ensuring 100% local uptime.

> **Narration:**
> "We now transition to the Knowledge Graph Explorer — the semantic intelligence core powering the platform. This module maps 23,893 food ingredients connected through complex multi-relational triples, including functional class memberships, compatibility edges, nutrient relationships, and allergen taxonomies. Using the interactive force-directed canvas, food scientists can filter node types, inspect ingredient clusters, and examine bidirectional relationships. Searching for key functional components such as Pea Protein Isolate or Cocoa Butter reveals rich node metadata, including chemical identifiers, regulatory GRAS status, and connected replacement nodes. By adjusting graph traversal depth, researchers can explore ingredient substitution pathways that maintain emulsion stability and flavor harmony."

## Scene 9: Comprehensive Ingredient Library & Specification Drawer
- **Timestamp:** `08:21 – 09:15 (53.8s)` | **Route:** `/dashboard/ingredients`
- **Visual Demonstration:** Demonstrates 23,893-ingredient catalog table. Toggles category filters: Proteins, Fats & Oils, Sweeteners. Searches for 'Cocoa Butter'. Clicks ingredient row to open the slide-over specification drawer. Scrolls through physicochemical constants (Aw, melting point, pH, solubility), allergen matrix, safety ratings, and market cost.
- **Technical Notes:** Showcases physical-chemical characterization data, commercial sourcing feasibility, and full-text search indexing.

> **Narration:**
> "Next, we inspect the Ingredient Library, which provides an exhaustive, searchable repository of all 23,893 cataloged ingredients. Formulators can search by common name, CAS number, or filter by functional classifications such as Proteins, Sweeteners, Emulsifiers, Hydrocolloids, and Fats and Oils. Clicking any ingredient card expands the slide-over specification drawer. Here, we can inspect verified physicochemical parameters — such as water activity, pH, and solubility — alongside macro and micronutrient distributions, allergen warnings, and benchmark market pricing. This grounded database ensures that every formulation synthesized by our AI is immediately reproducible on the factory floor using real, commercially available ingredients."

## Scene 10: User Profile, Laboratory Settings & Formulation History
- **Timestamp:** `09:15 – 09:55 (40.6s)` | **Route:** `/dashboard/profile`
- **Visual Demonstration:** Navigates to user profile page. Displays logged-in demonstration profile (Administrator, Expert User role, TCS Food Formulation Laboratory affiliation). Scrolls down through formulation history, saved project versions, and account settings.
- **Technical Notes:** Covers authentication security, JWT session token management, and audit traceability.

> **Narration:**
> "In the User Profile and Project History module, researchers and enterprise administrators can manage their scientific workspace. We observe the logged-in demonstration profile with Expert User privileges, organizational affiliation with the TCS Food Formulation Laboratory, and comprehensive formulation history logs. Formulators can review previously archived projects, compare iteration histories, and safely export technical audit dossiers. The platform enforces strict role-based access control and credential hashing, ensuring proprietary formulation recipes and intellectual property remain securely compartmentalized."

## Scene 11: Closing Summary & Dashboard Return
- **Timestamp:** `09:55 – 10:31 (35.2s)` | **Route:** `/dashboard`
- **Visual Demonstration:** Returns to main dashboard. Panning across completed formulation metrics, platform health badge, and Food Formulator platform branding for a professional closing view.
- **Technical Notes:** Final executive recap summarizing the technological convergence of food biochemistry, knowledge graphs, and mathematical optimization.

> **Narration:**
> "Returning to the central command dashboard, we conclude this demonstration of the Food Formulation AI Platform. By seamlessly integrating natural language brief interpretation, automated constraint extraction, a 23,893-ingredient knowledge graph, SciPy numerical optimization, and multi-jurisdictional regulatory compliance, the platform transforms food product development from an empirical trial-and-error cycle into a predictable, mathematically grounded digital science. Thank you for your time and interest in the Food Formulator platform."
