# Demo Recording Plan — Food Formulation AI Platform Walkthrough

This document outlines a professional, page-by-page screen recording sequence covering every accessible screen, subview, modal, and analytical tab of the Food Formulation AI Platform. It is engineered for a cohesive 8-to-10 minute comprehensive product demonstration video.

---

## Recording Sequence Summary Table

| Scene # | Screen / Route | Target View / Component | Duration | Key Demonstrations & Actions |
| :---: | :--- | :--- | :---: | :--- |
| **01** | `/` | Homepage / Landing Page | 0:35 | Hero section, problem statement, key metrics banner, navigation bar |
| **02** | `/login` & `/register` | Authentication Flow | 0:25 | Show clean auth forms, secure login, role-based access reassurance |
| **03** | `/dashboard` | Central Command Dashboard | 0:45 | Project overview cards, recent formulation activity, quick metrics |
| **04** | `/dashboard/formulate/guided` (Stage 1) | Product Brief Submission | 0:40 | Select preset "High-Protein Snack Bar", review natural language brief, click Extract Constraints |
| **05** | `/dashboard/formulate/guided` (Stage 2) | Constraint Discovery | 0:45 | Show extracted nutritional targets, water activity ($A_w \le 0.65$), allergen exclusions, infeasible pruning |
| **06** | `/dashboard/formulate/guided` (Stage 3) | Hard vs. Soft Goals | 0:40 | Demonstrate hard constraint toggles and soft multi-objective priority sliders (cost vs. protein) |
| **07** | `/dashboard/formulate/guided` (Stage 4) | Candidate Sets Overview | 0:50 | Highlight 3 Pareto candidates (Cost, Balanced, Premium), scores, Aw badges, and core preview |
| **08** | `/dashboard/formulate/guided` (Modal) | Candidate Deep-Dive Inspector | 0:50 | Click "Inspect Candidate Set", showcase 8-ingredient table, percentages, and multi-axis radar chart |
| **09** | `/dashboard/formulate/guided` (Stage 5 - Tab 1) | Final Report: Overview | 0:45 | Overall score (94.2%), mass balance check (100.00g), macro donut chart, executive summary |
| **10** | `/dashboard/formulate/guided` (Stage 5 - Tab 2) | Final Report: Ingredients | 0:45 | Full formulation recipe table, exact percentages, botanical sources, functional roles |
| **11** | `/dashboard/formulate/guided` (Stage 5 - Tab 3) | Final Report: Process | 0:35 | Unit operations sequence, mixing order, thermal treatment, shear rates, HACCP control points |
| **12** | `/dashboard/formulate/guided` (Stage 5 - Tab 4) | Final Report: Cost Analysis | 0:40 | Direct ingredient-level costs ($1.20 sugar, isolates), cost share %, cost/kg comparisons |
| **13** | `/dashboard/formulate/guided` (Stage 5 - Tab 5) | Final Report: Nutrition Profile | 0:45 | Verified non-zero metrics: Calories (495 kcal), Protein (47.5g), Carbs, Key Minerals, Aw |
| **14** | `/dashboard/formulate/guided` (Stage 5 - Tab 6) | Final Report: Allergens & Compliance | 0:40 | Declared allergens, cross-contact risk matrix, FDA/EFSA/FSSAI regulatory claim badges |
| **15** | `/dashboard/formulate/guided` (Stage 5 - Tab 7) | Final Report: AI Rationale | 0:35 | Explainable AI justification, substitution logic, and stability tradeoff explanations |
| **16** | Pinned Stage Bar | Navigation Jump | 0:25 | Click backwards to Stage 2 and forward to Stage 5 to demonstrate the persistent pinned bar |
| **17** | `/dashboard/formulate/expert` | Expert Manual Studio | 0:50 | Add ingredients manually, move percentage sliders, observe live mass-balance recalculation |
| **18** | `/dashboard/ingredients` | Ingredient Catalog & Drawer | 0:45 | Search 23,893 ingredients, filter by category, open slide-over drawer for physicochemical specs |
| **19** | `/dashboard/knowledge-graph` | Knowledge Graph Visualizer | 0:45 | Explore force-directed node-link graph, click relationships, demonstrate SQLite graph query |
| **20** | `/dashboard/compliance` | Regulatory Audit Matrix | 0:40 | Switch between FDA, EFSA, and FSSAI standards, verify additive GSFA maximum levels |
| **21** | `/dashboard/profile` | Settings & User Profile | 0:20 | Display user organization, role settings, and clean wrap-up |

**Total Estimated Duration:** **13 minutes 40 seconds** (can be smoothly edited to an 8-minute highlight reel or 12-minute deep-dive).

---

## Detailed Scene-by-Scene Script & Cues

### Scene 1: Platform Introduction & Landing Page (0:00 - 0:35)
- **Visual:** Smooth scroll on `http://localhost:3000/`.
- **Narration Hook:** "Welcome to the Food Formulation AI Platform — an enterprise-grade food science intelligence platform combining knowledge graphs, multi-objective optimization, and regulatory compliance to accelerate food product development from months to minutes."
- **Action:** Highlight the clean interface, enterprise branding, and click "Launch Platform / Go to Dashboard".

### Scene 2: Authentication & User Workspace (0:35 - 1:00)
- **Visual:** Display `/login` and `/dashboard`.
- **Narration Hook:** "Built with role-based security, formulation scientists can securely log in to access proprietary project databases and regulatory audit histories."
- **Action:** Quick demonstration of dashboard KPI tiles and recent projects list.

### Scene 3: The 5-Stage Guided Formulation Wizard (1:00 - 1:40)
- **Visual:** Navigate to `/dashboard/formulate/guided` (Stage 1).
- **Narration Hook:** "Our flagship capability is the 5-Stage Guided Formulation Pipeline. It begins with a natural language product brief."
- **Action:** Click the "High-Protein Snack Bar" preset. Point out the category selector, target market (North America FDA), and click "Extract Constraints & Analyze Brief".

### Scene 4: NLP Constraint Discovery & Entity Extraction (1:40 - 2:25)
- **Visual:** Stage 2 screen.
- **Narration Hook:** "Instantly, our NLP parser extracts critical parameters: target protein, maximum sugar, sodium limits, and strict water activity thresholds ($A_w \le 0.65$) essential for microbial shelf-stability."
- **Action:** Show the interactive thresholds. Highlight the intelligent allergen handling that prunes conflicting ingredients before solving.

### Scene 5: Hard vs. Soft Goals Prioritization (2:25 - 3:05)
- **Visual:** Stage 3 screen.
- **Narration Hook:** "Formulators maintain full control over trade-offs, designating non-negotiable legal limits as Hard Constraints while tuning Soft Goals like cost minimization vs. sensory texture."
- **Action:** Adjust the sliders slightly, then click "Generate Candidate Formulations".

### Scene 6: Candidate Set Generation & Pareto Optimization (3:05 - 3:55)
- **Visual:** Stage 4 screen with 3 candidate cards.
- **Narration Hook:** "Under the hood, the platform queries our 23,893-ingredient knowledge graph and runs a Sequential Least Squares Programming (SLSQP) solver to generate three Pareto-optimal formulations: Cost-Optimized, Balanced, and Premium Nutrition."
- **Action:** Hover over the Rank #1 card, showing the 88.8% score, Aw of 0.58, and cost/kg.

### Scene 7: Deep-Dive Candidate Inspector Modal (3:55 - 4:45)
- **Visual:** Click "Inspect Candidate Set" to trigger the modal.
- **Narration Hook:** "Opening the Candidate Inspector reveals the complete ingredient matrix, exact percentages, functional classifications, and a multi-dimensional performance radar chart."
- **Action:** Scroll through the 8 ingredients (Certified Gluten-Free Flour, Refined Cane Sugar, Soy Protein Isolate, etc.). Click "Select This Candidate Set & View Final Report".

### Scene 8: The 7-Tab Analytical Dossier (4:45 - 8:30)
- **Visual:** Step through all 7 tabs on Stage 5:
  1. **Overview:** Show the overall score (94.2%), mass balance check (100.00g), and macronutrient donut chart.
  2. **Ingredients:** Highlight the complete recipe table with percentages and functional roles.
  3. **Process:** Walk through the manufacturing instructions, mixing sequence, and critical control points.
  4. **Cost Analysis:** Emphasize that costs are provided **directly per ingredient** (e.g. `$1.20` for Refined Cane Sugar) rather than broad category guesses.
  5. **Nutrition Profile:** Showcase the dynamically calculated nutrition facts: Calories (495 kcal), Protein (47.5g), Carbohydrates, and Key Minerals — with **zero placeholder zeros**.
  6. **Allergens & Compliance:** Display the multi-jurisdiction compliance checks and cross-contact allergen risks.
  7. **AI Rationale:** Review the explainable AI narrative explaining why these specific ingredients were paired for maximum stability.

### Scene 9: Pinned Navigation Bar Demonstration (8:30 - 8:55)
- **Visual:** Use the pinned navigation bar at the top of the screen.
- **Narration Hook:** "Notice the persistent stage navigation bar pinned at the top. Formulators can easily jump back to Stage 2 or Stage 3 to tweak constraints and return immediately to the final report without page reloads."
- **Action:** Click Stage 2, show the state is preserved, then click Stage 5 to return.

### Scene 10: Expert Studio Manual Formulation (8:55 - 9:45)
- **Visual:** Navigate to `/dashboard/formulate/expert`.
- **Narration Hook:** "For experienced food scientists wanting complete hands-on control, the Expert Studio offers a real-time manual formulation workspace."
- **Action:** Search and add an ingredient, drag the percentage slider, and demonstrate the real-time mass balance bar enforcing 100%.

### Scene 11: 23,893-Ingredient Knowledge Base & Explorer (9:45 - 10:30)
- **Visual:** Navigate to `/dashboard/ingredients`.
- **Narration Hook:** "The platform is backed by an extensive repository of nearly 24,000 food ingredients."
- **Action:** Filter by "Sweetener" or "Protein", click an ingredient row to slide open the detail drawer showing physicochemical constants and safety grades.

### Scene 12: Knowledge Graph Visualization (10:30 - 11:15)
- **Visual:** Navigate to `/dashboard/knowledge-graph`.
- **Narration Hook:** "Our Knowledge Graph maps complex functional relationships, substitute ingredients, and compatibility synergies, powering semantic discovery across the formulation lifecycle."
- **Action:** Pan and zoom the force-directed graph canvas, click on an ingredient node to show its connected classes.

### Scene 13: Regulatory Compliance Matrix (11:15 - 11:55)
- **Visual:** Navigate to `/dashboard/compliance`.
- **Narration Hook:** "Finally, the Regulatory Compliance engine evaluates formulations against global food safety standards, including FDA 21 CFR, EFSA, and FSSAI, checking maximum additive limits and labeling requirements."
- **Action:** Switch jurisdictions and review the pass/review status badges.

### Scene 14: Conclusion (11:55 - 12:15)
- **Visual:** Return to `/dashboard`.
- **Narration Hook:** "The Food Formulation AI Platform transforms formulation R&D into a rapid, mathematically grounded, and regulatory-compliant digital workflow."

