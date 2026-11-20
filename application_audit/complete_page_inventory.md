# Food Formulation Platform — Complete Page & Route Inventory

This inventory documents every accessible route, subview, modal, and drawer in the platform.

---

## 1. Route Summary Table

| # | Route / URL | Page Name | Primary Purpose | Implemented Status | Screenshot Reference |
|---|---|---|---|---|---|
| 1 | `/` | Homepage / Landing | Product introduction & quick prompt submission | Implemented | `01_homepage.png` |
| 2 | `/dashboard` | Dashboard Overview | Platform KPI overview, quick brief prompt bar, demo launcher | Implemented | `02_dashboard.png` |
| 3 | `/dashboard/formulate` | Formulation Hub | Client redirect to guided formulation workspace | Implemented (Redirect) | `06_formulate_hub.png` |
| 4 | `/dashboard/formulate/guided` (Stage 1) | Product Brief Entry | Natural language brief input, preset selection, category resolution | Implemented | `13_guided_stage1_brief.png` |
| 5 | `/dashboard/formulate/guided` (Stage 2) | Constraint Discovery | Review AI-extracted nutrition targets, dietary rules, and sensory parameters | Implemented | `14_guided_stage2_constraint_discovery.png` |
| 6 | `/dashboard/formulate/guided` (Stage 3) | Hard / Soft Goals Matrix | Interactive toggle between Hard Constraints and Soft Objectives | Implemented | `15_guided_stage3_hard_soft_goals.png` |
| 7 | `/dashboard/formulate/guided` (Stage 4) | Candidate Sets Studio | 4 Pareto-optimized candidate sets, score comparisons, feasibility status | Implemented | `16_guided_stage4_candidate_sets.png` |
| 8 | `/dashboard/formulate/guided` (Modal) | Candidate Set Inspector | Deep-dive modal inspecting ingredients, strategy rationale, and formula | Implemented | `17_guided_stage4_candidate_modal.png` |
| 9 | `/dashboard/formulate/guided` (Stage 5) | Final Formulation Report | Comprehensive 7-tab scientific dossier for selected formulation | Implemented | `18_guided_stage5_final_report_overview.png` |
| 10 | `/dashboard/formulate/guided` (Tab: Ingredients) | Final Ingredients Matrix | Detailed batch scaling, mass share, INS codes, and inclusion % | Implemented | `19_final_report_ingredients.png` |
| 11 | `/dashboard/formulate/guided` (Tab: Process) | Process Recommendations | Unit operations (Dry blending, tempering, cooling, conching) | Implemented | `20_final_report_process.png` |
| 12 | `/dashboard/formulate/guided` (Tab: Cost) | Cost Analysis Studio | Ingredient-by-ingredient cost breakdown ($/kg and $/batch) | Implemented | `21_final_report_cost_analysis.png` |
| 13 | `/dashboard/formulate/guided` (Tab: Nutrition) | Nutrition Profile & Targets | Non-zero calories, carbs, minerals, protein, fat, and target bars | Implemented | `22_final_report_nutrition.png` |
| 14 | `/dashboard/formulate/guided` (Tab: Allergens) | Allergens & Compliance | Dynamic allergen checks, cross-contact matrix, GSFA compliance claims | Implemented | `23_final_report_allergens_compliance.png` |
| 15 | `/dashboard/formulate/guided` (Tab: Rationale) | AI Rationale & Science Trace | Mathematical SLSQP parameters, trade-off analysis, food physics | Implemented | `24_final_report_ai_rationale.png` |
| 16 | `/dashboard/formulate/expert` | Expert Formulation Studio | Manual ingredient composition, sliders, live macro calculations, balance check | Implemented | `07_expert_studio.png` |
| 17 | `/dashboard/ingredients` | Grounded Ingredient Library | Search & filter 23,893 ingredients, dietary tags, cost sliders, compare tray | Implemented | `08_ingredient_library.png` |
| 18 | `/dashboard/ingredients` (Drawer) | Ingredient Details Drawer | Nutritional profile, physical properties (water binding, gelation), subgraphs | Implemented | `25_ingredient_details_drawer.png` |
| 19 | `/dashboard/knowledge-graph` | Knowledge Graph Explorer | Visual graph canvas, node details, depth controls, search, physics layouts | Implemented | `09_knowledge_graph.png`, `26_knowledge_graph_explorer_view.png` |
| 20 | `/dashboard/compliance` | Regional Compliance Matrix | Regulatory audit across FSSAI, FDA, EFSA with project compliance logs | Implemented | `10_compliance_matrix.png` |
| 21 | `/dashboard/profile` | Profile, History & Settings | R&D scientist credentials, project cards, duplicate/delete, preferences | Implemented | `11_profile_settings.png` |
| 22 | `/formulations/new` | Legacy New Formulation | Client redirect to guided formulation workspace | Implemented (Redirect) | `12_formulations_new.png` |
| 23 | `/login` | User Authentication Login | Email/password login with JWT token issuance | Implemented | `03_login.png` |
| 24 | `/register` | Account Registration | User creation with username, email, password, and R&D role | Implemented | `04_register.png` |
| 25 | `/signup` | Alternative Signup Route | Alias registration interface for seamless onboarding | Implemented | `05_signup.png` |

---

## 2. Detailed Page-by-Page Specifications

### Page 1: Homepage (`/`) & Dashboard Overview (`/dashboard`)
- **Navigation Location**: Top brand logo & Sidebar `Dashboard` link.
- **Purpose**: Serves as the primary executive overview and entry point for instant formulation generation.
- **Main Sections & Layout**:
  - Top canonical header with brand icon, search bar (`⌘K`), notification bell, settings link, and profile menu.
  - Left persistent sidebar with `MAIN MENU`, `PROJECTS` quick links, and `ENTERPRISE PLAN` storage monitor.
  - Center hero banner with value proposition and capability tags.
  - Natural language formulation input card (`textarea`, submit button with live spinner).
  - Quick action CTA buttons (`Start Formulating` -> `/dashboard/formulate/guided`, `Watch Platform Demo`).
  - Inline AI Processing animation state and embedded `FormulationResults` container upon execution.
- **Backend APIs Triggered**:
  - `POST /api/formulation/generate` on form submit.
- **Data Displayed**:
  - Real-time formulation result if generated inline; otherwise executive prompts.

---

### Page 2: Guided Formulation Pipeline (`/dashboard/formulate/guided`)
This is the core 5-stage formulation workspace. It features a **pinned, sticky navigation bar** docked at `top-0` that allows users to freely jump back and forth to any reached stage.

#### Stage 1: Product Brief Submission
- **Visuals**: `13_guided_stage1_brief.png`.
- **Purpose**: Capture natural language product briefs from food developers.
- **Components**:
  - Multi-line text input with rich placeholder guidance.
  - 3 clickable preset briefs (`EXP-001 High-Protein Vegan Chocolate Bar`, `Low-Sugar Prebiotic Citrus Beverage`, `High-Fibre Gluten-Free Digestive Oat Bar`).
  - Primary CTA button: `Analyze Brief & Recommend Constraints →`.
- **APIs Triggered**: `POST /api/formulation/parse-brief`.

#### Stage 2: Constraint Discovery
- **Visuals**: `14_guided_stage2_constraint_discovery.png`.
- **Purpose**: Display transparent, structured extraction of requirements from the brief.
- **Components**:
  - Extracted constraint cards categorized by type: `NUTRITION`, `DIETARY`, `ALLERGEN`, `SENSORY`, `SHELF_LIFE`, `PROCESSING`.
  - Priority pills (`CRITICAL`, `HIGH`, `MEDIUM`).
  - Extracted parameter badges showing numerical target, unit, and source text span.
  - Action buttons: `Back to Brief` and `Configure Hard & Soft Constraints →`.

#### Stage 3: Hard vs. Soft Goals Matrix
- **Visuals**: `15_guided_stage3_hard_soft_goals.png`.
- **Purpose**: Enable food developers to configure the optimization boundary conditions.
- **Components**:
  - Interactive toggle switches converting constraints between `HARD CONSTRAINT` (must be 100% satisfied or candidate is disqualified) and `SOFT OBJECTIVE` (optimized for highest score).
  - Add Custom Constraint modal (`Name`, `Attribute`, `Operator`, `Target Value`, `Category`).
  - Delete constraint button per row.
  - Primary CTA button: `Run AI Formulation Search →`.
- **APIs Triggered**: `POST /api/formulation/generate`.

#### Stage 4: Candidate Sets Selection Studio
- **Visuals**: `16_guided_stage4_candidate_sets.png`.
- **Purpose**: Compare 4 distinct formulation candidate sets generated by the mathematical optimizer.
- **Components**:
  - 3-column / grid cards for candidate sets:
    1. **Candidate Set A**: Nutrition-Maximized Strategy.
    2. **Candidate Set B**: Cost-Optimized Strategy.
    3. **Candidate Set C**: Functionality & Texture Strategy.
    4. **Candidate Set D**: Balanced Strategy.
  - Candidate metrics: Overall score percentage, Rank #1 badge, Strategy rationale callout ("Why this strategy?").
  - Grounded KPI pills: Protein ($g$), Carbs ($g$), Calories ($kcal$), Minerals ($mg$), Cost/kg ($\$$), Water Activity ($A_w$).
  - Core ingredients preview list with percentage breakdown.
  - Compliance badges: `✓ Hard Constraints Pass`, `Pareto Feasible`.
  - Button 1: `Inspect Candidate Set (Ingredients & Scores)` -> Opens deep-dive modal.
  - Button 2: `Select Candidate Set & View Final Report →` -> Advances to Stage 5.

#### Candidate Inspection Modal (Stage 4 Subview)
- **Visuals**: `17_guided_stage4_candidate_modal.png`.
- **Purpose**: Diagnostic modal enabling full transparency before finalizing candidate selection.
- **Tabs**:
  1. `Ingredients`: Batch scaling calculator (adjust batch from 100g to 1000kg), complete raw materials table with mass balance verification.
  2. `Strategy Rationale`: Explains algorithmic trade-offs, objective scalarization, and target advantages.
  3. `Pareto Scoring`: Shows exact mathematical formula, dimension weights, and radar score breakdown.
- **Footer Buttons**: `Close Inspector`, `Select This Candidate Set & View Final Report`.

#### Stage 5: Final Formulation Report Dossier
- **Visuals**: `18_guided_stage5_final_report_overview.png` through `24_final_report_ai_rationale.png`.
- **Purpose**: Complete scientific specification sheet ready for pilot-plant trials and regulatory approval.
- **Pinned Workspace Tab Navigation**:
  1. **Overview Tab** (`18_...`): Formula summary, batch yield, moisture retention, completeness index, and key indicators.
  2. **Ingredients Tab** (`19_...`): Full ingredient composition matrix with INS numbers, inclusion %, batch weight in grams, addition sequence, and functional roles.
  3. **Process Tab** (`20_...`): Process unit operations (Mixing, conching, tempering, extrusion), temperatures, shear rates, and dwell times.
  4. **Cost Analysis Tab** (`21_...`): Unit raw material cost ($/kg), ingredient-level cost contributions, batch cost total, and Pareto efficiency index.
  5. **Nutrition Tab** (`22_...`): Calories donut chart, macro split (protein, carbs, fat), sodium, fiber, key minerals (Calcium, Iron, Potassium, Magnesium), and compliance progress bars against targets.
  6. **Allergens & Compliance Tab** (`23_...`): Dynamic allergen identification, cross-contact risk matrix (peanuts, tree nuts, gluten, dairy, soy), and regulatory claim support (High Protein, Low Sugar, Gluten Free, GSFA Additive Clearance).
  7. **AI Rationale Tab** (`24_...`): SLSQP optimizer solver diagnostics, constraint tolerance proof, and scientific literature citations.

---

### Page 3: Expert Formulation Studio (`/dashboard/formulate/expert`)
- **Visuals**: `07_expert_studio.png`.
- **Purpose**: Direct manual recipe builder for experienced food scientists who wish to author custom ingredient ratios and benchmark them against the solver.
- **Components**:
  - Live ingredient selector from grounded database.
  - Inclusion % slider and numeric input per ingredient.
  - Dynamic mass balance indicator (must equal exactly 100.00%).
  - Auto-distribute equally utility button.
  - Live reactive macro calculations (protein, fat, carbs, calories).
  - Validation CTA: `Run Compliance & Validation Audit`.
- **APIs Triggered**: `GET /api/ingredients`, `POST /api/formulate`.

---

### Page 4: Grounded Ingredient Library (`/dashboard/ingredients`)
- **Visuals**: `08_ingredient_library.png`, `25_ingredient_details_drawer.png`.
- **Purpose**: Search, filter, and inspect the platform's 23,893 food ingredients.
- **Components**:
  - Search input with instantaneous debounce.
  - Category selector pills (`Proteins`, `Fats & Lipids`, `Sweeteners`, `Fibres & Texturizers`, `Emulsifiers`).
  - Functional property sliders (Water binding, Emulsification, Gelation, Thickening).
  - Dietary requirement filter checkboxes (`Vegan`, `Gluten-Free`, `Dairy-Free`, `Non-GMO`, `Organic`).
  - Max cost range slider ($0 - $500/kg).
  - View toggle: Grid view cards vs. Compact tabular list view.
  - Selected item comparison tray.
- **Ingredient Detail Drawer / Modal**:
  - 5 tabs: `OVERVIEW`, `NUTRITION`, `PROPERTIES`, `COMPLIANCE`, `KG RELATIONS`.
  - Interactive embedded subgraph centered on selected ingredient.
- **APIs Triggered**: `GET /api/ingredients`, `GET /api/ingredients/{id}`.

---

### Page 5: Knowledge Graph Explorer (`/dashboard/knowledge-graph`)
- **Visuals**: `09_knowledge_graph.png`, `26_knowledge_graph_explorer_view.png`.
- **Purpose**: Direct interactive visual navigation of the food science knowledge graph.
- **Components**:
  - Visual Canvas with interactive force-directed graph rendering (nodes and typed edges).
  - Toolbar with Zoom in, Zoom out, Fit view, Reset, and Layout selectors (`cose`, `circle`, `grid`, `concentric`).
  - Search bar to query nodes (`/api/knowledge-graph/search`).
  - Subgraph traversal depth selector (`Depth: 1`, `Depth: 2`, `Depth: 3`).
  - Node category filter dropdown (`All`, `Ingredient`, `Nutrient`, `Allergen`, `Category`).
  - Graph Statistics HUD (Node count, Edge count, Graph density, Cluster coefficient).
  - Visual legend explaining node color coding.
  - Slide-out Node Details inspector displaying grounded attributes, provenance, and outgoing relationships.
- **APIs Triggered**:
  - `GET /api/knowledge-graph`
  - `GET /api/knowledge-graph/health`
  - `GET /api/knowledge-graph/search?q={query}`
  - `GET /api/knowledge-graph/node/{id}`
  - `GET /api/knowledge-graph/neighbors/{id}`

---

### Page 6: Compliance Audit Dashboard (`/dashboard/compliance`)
- **Visuals**: `10_compliance_matrix.png`.
- **Purpose**: Regulatory safety validation across regional jurisdictions (FSSAI, FDA, EFSA).
- **Components**:
  - KPI summary counters: `Fully Compliant` (green), `With Warnings` (amber), `Violations Found` (red).
  - Audit Log Records master list with project name, category, formulation ID, and overall badge.
  - Detailed Regulatory Breakdown pane showing regional clearance status, additive permission status, and required technical dossiers.
- **APIs Triggered**: `GET /api/projects`, `GET /api/projects/{id}`.

---

### Page 7: Profile, Project History & Settings (`/dashboard/profile`)
- **Visuals**: `11_profile_settings.png`.
- **Purpose**: Manage scientist account profile, formulation project history, and platform preferences.
- **Components**:
  - User identity badge: Avatar initials, scientist name, verified R&D credential badge, organization, and department.
  - Project stats HUD: Total Projects, Active Formulations, Compliance Pass Rate, Ingredients Utilized.
  - Project Management Console:
    - Search input.
    - Category filter dropdown & Status filter dropdown (`Approved`, `Formulated`, `In Development`, `Archived`).
    - Sort selector (`Recently Modified`, `Date Created`, `Project Name`).
    - Project cards with formulation ID, version tag, last modified date, and duplicate/delete actions.
  - Platform Preferences:
    - Measurement units selector (`Metric`, `Imperial`).
    - Automatic compliance pre-flight checks toggle.
    - Draft auto-save toggle.
    - RAG Embedding Model configuration selector (`Deep KG Embedding`, `Hybrid Graph-Dense`, `Standard Vector RAG`).
- **APIs Triggered**: `GET /api/projects`, `POST /api/projects`, `DELETE /api/projects/{id}`, `POST /api/projects/{id}/duplicate`.

---

### Page 8: Authentication Suite (`/login`, `/register`, `/signup`)
- **Visuals**: `03_login.png`, `04_register.png`, `05_signup.png`.
- **Purpose**: Secure user sign-in and new account onboarding.
- **Components**:
  - Brand header and illustration.
  - Form inputs: Username, Email, Password, Role selector (`Guided User`, `Expert Formulator`).
  - Error alert banners for invalid credentials or existing user collisions.
  - JWT token storage into client store upon successful authentication.
- **APIs Triggered**: `POST /api/auth/login`, `POST /api/auth/register`.

