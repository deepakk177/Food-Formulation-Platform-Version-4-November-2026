# Feature Inventory — Food Formulation AI Platform

This document categorizes all discovered platform features into four verified status tiers: **Implemented (Production Ready)**, **Partially Implemented (Operational with Fallbacks)**, **UI-Only / Static Demonstrations**, and **Unavailable / Future Enhancements**.

---

## 1. Implemented Features (Fully Functional & Grounded)

| Category | Feature Name | Description | Verified Backend / Frontend Binding |
| :--- | :--- | :--- | :--- |
| **Pipeline** | 5-Stage Guided Formulation Pipeline | Complete end-to-end wizard guiding users from brief to final formulation dossier | React state + FastAPI `/api/pipeline/*` routes |
| **Pipeline** | Pinned Stage Progress Navigation Bar | Persistent, clickable step navigation bar allowing instantaneous jumping back and forth across all 5 stages | Pinned sticky header with completed step checkmarks |
| **Extraction** | Natural Language Constraint Extraction | Parses freeform user briefs into structured targets (nutritional, allergen, physicochemical, regulatory) | `POST /api/pipeline/extract-constraints` (NLP parser) |
| **Extraction** | Infeasible Allergen Pruning | Dynamically removes conflicting ingredients that cause formulation infeasibility while maintaining allergen declarations | Allergen filtration engine in formulation optimizer |
| **Optimization** | SLSQP Multi-Objective Optimization | SciPy Sequential Least Squares Programming solver balancing macro targets, ingredient bounds, and $\sum w_i = 100\%$ | `scipy.optimize.minimize(method='SLSQP')` |
| **Optimization** | Multi-Strategy Pareto Candidate Sets | Generates three distinct formulation trade-offs: Cost-Optimized, Balanced Performance, and Premium Nutrition | `POST /api/pipeline/generate-candidates` |
| **Optimization** | Candidate Set Inspection Modal | Deep-dive modal showing full 8-ingredient breakdown, mass percentages, functional roles, and score radar | Frontend interactive dialog component |
| **Reporting** | 7-Tab Analytical Dossier | Comprehensive technical report containing Overview, Ingredients, Process, Cost Analysis, Nutrition, Allergens, AI Rationale | Dynamic tab switcher on Stage 5 |
| **Reporting** | Direct Ingredient Cost Breakdown | Direct ingredient-level unit cost and batch cost display instead of aggregate category approximations | Formulated ingredient cost aggregation engine |
| **Reporting** | Dynamic Nutrition Engine | Calculates Calories, Protein, Carbohydrates, Fat, Aw, and Key Minerals dynamically without zero-value placeholders | `POST /api/pipeline/finalize-formulation` |
| **Reporting** | AI Formulation Rationale | Explainable AI narrative detailing substitution logic, functional synergy, and stability tradeoffs | Structured justification engine |
| **Learning** | Cross-Formulation Learning Store | Persistent SQLite store recording formulation patterns and learned ingredient values across sessions | SQLite `ingredient_learning_store` table |
| **Catalog** | 23,893-Ingredient Knowledge Base | Searchable, paginated ingredient database with categorical filtering (Proteins, Sweeteners, Emulsifiers, etc.) | SQLite `ingredients` table with full-text indexing |
| **Catalog** | Ingredient Detail Slide-Over Drawer | Deep-dive panel displaying physicochemical constants, allergen profile, regulatory grades, and usage levels | Dynamic slide-over drawer component |
| **Graph** | Interactive Knowledge Graph Explorer | Node-link graph visualization illustrating ingredient classes, functional roles, and replacement edges | Interactive graph canvas with SQLite graph traversal |
| **Studio** | Expert Manual Formulation Builder | Real-time interactive formulation workspace with percentage sliders and live mass balance normalization | `/dashboard/formulate/expert` with live recalculation |
| **Compliance** | Multi-Jurisdictional Regulatory Matrix | Compliance auditing across US FDA 21 CFR, EU EFSA, and India FSSAI standards | `/dashboard/compliance` with GSFA rule checker |
| **Auth** | User Authentication & Session Security | Secure login, registration, JWT bearer token issuance, and protected route guards | FastAPI JWT authentication + Bcrypt hashing |
| **Projects** | Project & Formulation Management | Create, edit, clone, and manage formulation projects and version histories | SQLite `projects` and `formulations` tables |

---

## 2. Partially Implemented Features (Operational with Fallbacks)

| Feature Name | Current Implementation | Fallback Mechanism | Status / Notes |
| :--- | :--- | :--- | :--- |
| **Neo4j Enterprise Graph Engine** | Full Cypher query client configured in backend | Automatic SQLite relational graph fallback | When standalone Neo4j daemon is offline, backend seamlessly routes graph queries through `tcs_food_formulator_kg.db` without crashing or dropping relationships. |
| **Technical Dossier PDF Export** | Integrated browser print and layout stylesheet (`@media print`) | Client-side `window.print()` triggers clean PDF generation | Formatted specifically for A4/Letter print; server-side headless Chromium PDF generation endpoint is omitted in favor of zero-dependency client printing. |
| **Vector Similarity Retrieval (Qdrant)** | Qdrant client interfaces defined in architecture | SQLite trigram & lexical fuzzy matching | For lightweight local operation, semantic lookups default to optimized SQL query indexes when remote Qdrant vector database is uninitialized. |

---

## 3. UI-Only / Static Demonstrations

| Feature Name | UI Appearance | Underlying Reality |
| :--- | :--- | :--- |
| **Pilot Plant Process Parameters** | Displays thermal curves, shear rate values, and stage-by-stage mixing sequences | Values are deterministically generated from product category heuristics (e.g. snack bar extrusion vs. beverage retort) rather than live factory SCADA/IoT sensor telemetry. |
| **Packaging Barrier Atmosphere** | Displays recommended gas flush ($N_2/CO_2$) and water vapor transmission rate (WVTR) | Algorithmic heuristic based on formulated $A_w$; does not integrate directly with packaging vendor ERP catalogs. |
| **Raw Material Vendor Pricing Feed** | Displays market pricing per kg for ingredients | Sourced from static internal benchmark pricing table; does not execute live Commodity Exchange (CBOT) API queries. |

---

## 4. Unavailable / Not Implemented Features

| Feature Name | Category | Reason for Non-Inclusion |
| :--- | :--- | :--- |
| **Direct ERP Supply Chain Ordering** | Enterprise Integration | Platform scope focuses on formulation R&D and regulatory compliance; SAP/Oracle procurement connectors are outside current architecture. |
| **Factory Equipment SCADA Integration** | Manufacturing Execution | Platform produces master formulation records (MFR); does not connect directly to factory PLC controllers. |
| **Enterprise SSO (SAML 2.0 / Okta)** | Security | Current authentication utilizes standard JWT bearer tokens with bcrypt hashing; federated SAML/OIDC is not configured. |
| **Physical Sensory Panel Mobile App** | Sensory Evaluation | Sensory metrics are modeled mathematically; human consumer panel mobile data collection is not bundled. |

