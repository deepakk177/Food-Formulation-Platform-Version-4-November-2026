# SECOND-PASS PIPELINE VERIFICATION MATRIX

**Audit Date:** 2026-09-24  
**Audit Target:** [docs/COMPLETE_FORMULATION_PIPELINE_AUDIT.md](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/docs/COMPLETE_FORMULATION_PIPELINE_AUDIT.md)  
**Verification Scope:** Ground-truth code execution tracing across all 15 core architectural components.

---

## 1. Executive Forensic Verification Table

| Component | Claimed in Research / Docs | Actually Implemented | Evidence (Codebase Fact) | Exact File | Exact Function | Actual Algorithm | Actual Library | Implementation Gap |
|---|---|---|---|---|---|---|---|---|
| **1. Constraint Extraction** | AI/NLP Intent Extraction via LLaMA 3.3 70B extracting arbitrary numerical & qualitative constraints | **PARTIALLY** (Rule/Regex only) | `self.llm` initialized in `__init__` but 0 calls in `extract()`. Relies exclusively on `re.search` and substring checks. | [requirements_extractor.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/requirements_extractor.py#L133-L470) | `ProductBriefParser.extract` | Regular Expressions & substring token matching | Python `re`, `pydantic` | LLM is bypassed. Misses explicit numbers not in regex (`≥25% cocoa butter`, `≥8% almond`, `≤28% sugar`). |
| **2. Hard/Soft Classification** | Automated semantic classification based on regulatory, safety, and priority ontologies | **YES** (YAML Configuration) | Reads `config/constraint_priority.yaml` to assign weights and `HARD`/`SOFT` tags. Fallback rule for unlisted items. | [constraint_engine.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/constraint_engine.py#L100-L179) | `ConstraintEngine.prioritize_constraints` | Dictionary lookup & rule-based branching | `pyyaml` | Deterministic configuration lookup, not dynamic ontological reasoning. |
| **3. Constraint Propagation** | Multi-hop graph propagation across categories $\rightarrow$ dietary $\rightarrow$ functional $\rightarrow$ regulatory | **PARTIALLY** (Procedural List Filter) | 5 sequential Python list loops filtering dietary flags, allergen strings, regulatory status, and cost ceilings. | [retrieval_service.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/retrieval_service.py#L185-L280) | `RetrievalOrchestrator.propagate_constraints` | Sequential in-memory list filtering | Python standard library | Procedural in-memory filtering; no graph traversal algorithms. Functional filter step is a no-op (`list(after_allergen)`). |
| **4. Dynamic Subgraph Construction** | Dynamic GraphRAG subgraphs constructed per query via seed expansion & multi-hop traversal | **NO** (Static Cypher Query) | `generate_dynamic_cypher()` creates a query string that is never executed. Real query is static `LIMIT 200`. Fallback iterates CSV. | [retrieval_service.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/retrieval_service.py#L282-L316) | `RetrievalOrchestrator.generate_dynamic_cypher`, `retrieve_kg_ingredients` | Static Cypher retrieval / in-memory CSV parsing | `neo4j`, `pandas` | Dynamic subgraph construction is non-executable presentation code. |
| **5. Four Retrieval Strategies** | Hybrid Cypher KG, SQLite Structured DB, Dense MiniLM Vector Search (Qdrant), Evidence KG | **PARTIALLY** (3 of 4 active, TF-IDF instead of MiniLM) | Qdrant absent. Active vector search uses Scikit-Learn `TfidfVectorizer`. MiniLM in `rag_engine.py` is bypassed. | [retrieval_service.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/retrieval_service.py#L446-L586) | `RetrievalOrchestrator.retrieve_all_multi_dimensional` | TF-IDF Cosine Similarity, SQL `LIKE`, static Cypher | `scikit-learn`, `sqlite3`, `neo4j` | Qdrant is missing. Semantic search is TF-IDF text matching, not dense vector neural search. |
| **6. Candidate Fusion** | Multi-view entity resolution and candidate fusion unifying graph, vector, and structured entities | **PARTIALLY** (Dict Key Deduplication) | Results merged by dictionary key: `candidates[ing.name.lower()] = ing`, updating roles and confidence. | [retrieval_service.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/retrieval_service.py#L473, L520-L547) | `RetrievalOrchestrator.retrieve_all_multi_dimensional` | Lower-case dictionary key deduplication | Python standard library | Simple string-key dictionary deduplication, not entity-resolution or graph-fusion algorithms. |
| **7. Candidate Percentage Generation** | Solved mathematically with mass balance $\sum x_i = 100.0000\%$ | **YES** | `scipy.optimize.minimize` (SLSQP) optimizes percentages against nutrient targets and role bounds. | [models/formulation/model.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/models/formulation/model.py#L152-L181) | `FormulationOptimizationModel.predict_with_uncertainty` | SLSQP constrained nonlinear programming | `scipy.optimize`, `numpy` | Optimization of inclusion percentages is genuinely implemented and verified. |
| **8. Optimization Algorithm** | Multi-objective Pareto optimization, NSGA-II, NSGA-III, Hypervolume maximization | **NO** (Single-Objective SLSQP) | SciPy SLSQP optimizes a single weighted penalty scalar loss with bounds and mass balance equality constraint. | [models/formulation/model.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/models/formulation/model.py#L115-L160) | `FormulationOptimizationModel.predict_with_uncertainty` | SLSQP (Sequential Least Squares Programming) | `scipy.optimize` | False claim of NSGA-II / Pareto optimization. It is single-objective SLSQP. |
| **9. Mass Balance** | Deterministic physical law: $\sum x_i = 100.0000\%$ strictly enforced | **YES** | Equality constraint in SLSQP + normalization and residual absorption on largest ingredient. Checked in gate. | [models/formulation/model.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/models/formulation/model.py#L137, L164-L181), [validation_gate.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/validation_gate.py#L198-L208) | `predict_with_uncertainty`, `validate_candidate_set` | Strict numerical constraint & post-normalization | `numpy` | 100% verified. Zero mass-balance discrepancy. |
| **10. Regulatory Validation** | Binary regulatory multiplier gate (RCS) checking FSSAI / Codex GSFA / FDA limits | **PARTIALLY** (Category permission check, additive score) | Evaluates composition against `foodadditive_allowed_in_foodcategory.csv`. RCS is an additive 15% term in scoring. | [compliance.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/compliance.py#L35-L129), [models/ranking/model.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/models/ranking/model.py#L71-L97) | `evaluate_compliance`, `predict_with_uncertainty` | CSV table lookup & dietary rule checks | `pandas` | Checks category-level permission, not numeric ADI/PPM limits. Regulatory score is additive, not a binary multiplicative gate. |
| **11. Evidence Grounding** | Scientific Evidence Strength (SES) based on DOI citations saturation formula | **PARTIALLY** (Citation existence ratio) | Each ingredient tracks `source_evidence`. Score is `(grounded_count / total) * 100`. Paper's DOI formula is absent. | [models/ranking/model.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/models/ranking/model.py#L59-L64), [validation_gate.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/validation_gate.py#L185-L196) | `predict_with_uncertainty`, `validate_candidate_set` | Citation presence counting | Python standard library | Groundedness is checked, but the claimed mathematical SES formula with DOIs is not implemented. |
| **12. Scoring Engine** | Multi-criteria scoring evaluating FCS, SES, ICS, CSS, RCS, Cost, Macros | **PARTIALLY** (6 heuristic component scores) | Calculates nutrition, functional coverage, evidence ratio, compatibility, regulatory, and cost scores. | [models/ranking/model.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/models/ranking/model.py#L31-L100) | `MultiObjectiveRankingModel.predict_with_uncertainty` | Bounded mathematical heuristic formulas | Python standard library | Individual formulas implemented, but CSS is missing and SES/RCS formulas deviate from paper. |
| **13. Ranking Engine** | Pareto front ranking and TOPSIS multi-criteria decision making | **NO** (Linear Weighted Sort) | Computes `overall_score = sum(w_i * score_i)` and calls `sorted(candidates, key=overall_score, reverse=True)`. | [scoring_engine.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/scoring_engine.py#L44-L54) | `ScoringEngine.rank_candidates` | Standard linear weighted sum descending sort | Python standard library | False claim of Pareto front ranking / TOPSIS. It is a linear weighted sum sort. |
| **14. Iteration & Refinement** | Automated closed-loop iterative backtracking upon validation failure | **NO** (Single-pass or manual CLI loop) | Pipeline runs 1 pass. Multi-iteration loop runs only if user manually passes `--iterations 2` on CLI with hardcoded weight bumps. | [pipeline_runner.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/pipeline_runner.py#L127-L489) | `run_pipeline` | Procedural for-loop over CLI argument | Python standard library | Automated backtracking on validation failure is not implemented. Single-pass execution. |
| **15. LLM Synthesis Generation** | Grounded explanation generation strictly constrained to validated candidate set | **YES** | Calls Groq API (`llama-3.3-70b-versatile`) with prompt prohibiting hallucination and enforcing `DATA_UNAVAILABLE`. | [synthesis_engine.py](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/synthesis_engine.py#L77-L163) | `SynthesisEngine.synthesize` | Prompt-engineered LLM reasoning + fallback | `requests`, `langchain_groq` | 100% verified. Real Groq API integration with strict grounding and deterministic fallback. |

---

## 2. Component-by-Component Forensic Verification Details

### 1. Constraint Extraction
- **Is it actually executable?** Yes.
- **Where is it implemented?** [requirements_extractor.py:L133-L470](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/requirements_extractor.py#L133-L470).
- **What function invokes it?** `product_brief_parser.parse(query)` called by `pipeline_runner.py:L69` and `main.py:L175, L196, L293`.
- **What are its inputs?** `user_prompt: str`.
- **What are its outputs?** `ProductBrief` Pydantic object.
- **What algorithm is actually used?** Regular expressions (`re.search`) and case-insensitive substring checks.
- **What library is actually used?** Python built-in `re`, `pydantic`.
- **Is any part hardcoded?** Yes. Ingredient exclusion lists, category keywords, and regex patterns are hardcoded.
- **Is the implementation deterministic?** Yes (100% deterministic).
- **Is the behavior reproducible?** Yes (Identical output for identical string).
- **Does the implementation match the research paper claim?** **NO.** The paper claims an LLM-based intent extraction engine; the code initializes `ChatGroq` but never calls it.

---

### 2. Hard/Soft Classification
- **Is it actually executable?** Yes.
- **Where is it implemented?** [constraint_engine.py:L100-L179](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/constraint_engine.py#L100-L179).
- **What function invokes it?** `constraint_engine.prioritize_constraints(brief)` called by `pipeline_runner.py:L148` and `validation_gate.py:L41`.
- **What are its inputs?** `ProductBrief` object.
- **What are its outputs?** `Dict` containing `hard_constraints` and `soft_constraints` lists.
- **What algorithm is actually used?** YAML configuration lookup with fallback heuristic rules.
- **What library is actually used?** `pyyaml`.
- **Is any part hardcoded?** Weights and default classifications are specified in [config/constraint_priority.yaml](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/config/constraint_priority.yaml).
- **Is the implementation deterministic?** Yes.
- **Is the behavior reproducible?** Yes.
- **Does the implementation match the research paper claim?** **YES.** Correctly distinguishes veto constraints from soft objectives.

---

### 3. Constraint Propagation
- **Is it actually executable?** Yes.
- **Where is it implemented?** [retrieval_service.py:L185-L280](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/retrieval_service.py#L185-L280).
- **What function invokes it?** `retrieval_orchestrator.propagate_constraints()` called by `pipeline_runner.py:L264`.
- **What are its inputs?** `candidates: List[RetrievedIngredient]`, `brief_dict: Dict[str, Any]`.
- **What are its outputs?** `Dict` containing `eligible_candidates` and `removed_candidates`.
- **What algorithm is actually used?** Procedural Python `for` loops with boolean and substring filtering.
- **What library is actually used?** Python standard library.
- **Is any part hardcoded?** Cost ceiling threshold multiplier (`cost_max * 3.0`) is hardcoded.
- **Is the implementation deterministic?** Yes.
- **Is the behavior reproducible?** Yes.
- **Does the implementation match the research paper claim?** **NO.** Claimed as dynamic graph propagation; implemented as procedural in-memory list filtering.

---

### 4. Dynamic Subgraph Construction
- **Is it actually executable?** **NO.**
- **Where is it implemented?** [retrieval_service.py:L282-L300](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/retrieval_service.py#L282-L300).
- **What function invokes it?** `generate_dynamic_cypher()` called by `retrieve_all_multi_dimensional()` (Line 550).
- **What are its inputs?** `brief_dict: Dict[str, Any]`.
- **What are its outputs?** Cypher query string (returned in response dict, but **never executed** against Neo4j).
- **What algorithm is actually used?** Python string f-string formatting.
- **What library is actually used?** Python standard library.
- **Is any part hardcoded?** The Cypher query template is hardcoded.
- **Is the implementation deterministic?** Yes.
- **Is the behavior reproducible?** Yes.
- **Does the implementation match the research paper claim?** **NO.** It is a presentation artifact; no dynamic graph expansion occurs.

---

### 5. Four Retrieval Strategies
- **Is it actually executable?** Yes.
- **Where is it implemented?** [retrieval_service.py:L446-L586](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/retrieval_service.py#L446-L586).
- **What function invokes it?** `retrieval_orchestrator.retrieve_all_multi_dimensional()` called by `pipeline_runner.py:L202` and `main.py:L182, L200`.
- **What are its inputs?** `brief_dict: Dict[str, Any]`.
- **What are its outputs?** `Dict` with `ingredients`, `evidence`, `intents`, `multi_strategy_breakdown`.
- **What algorithm is actually used?** SQL `LIKE` queries, static Cypher query, Scikit-Learn TF-IDF vectorization + cosine similarity.
- **What library is actually used?** `sqlite3`, `neo4j`, `scikit-learn`.
- **Is any part hardcoded?** Static Cypher query limit (200), TF-IDF similarity threshold (0.05).
- **Is the implementation deterministic?** Yes.
- **Is the behavior reproducible?** Yes.
- **Does the implementation match the research paper claim?** **PARTIALLY.** Qdrant is absent; vector search is TF-IDF text matching rather than dense neural embeddings.

---

### 6. Candidate Fusion
- **Is it actually executable?** Yes.
- **Where is it implemented?** [retrieval_service.py:L473, L520-L547](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/retrieval_service.py#L473).
- **What function invokes it?** `retrieve_all_multi_dimensional()`.
- **What are its inputs?** Entities returned by SQLite, Neo4j, and TF-IDF searches.
- **What are its outputs?** `candidates: Dict[str, RetrievedIngredient]`.
- **What algorithm is actually used?** Dictionary key deduplication on `ingredient.name.lower()`.
- **What library is actually used?** Python standard dictionary.
- **Is any part hardcoded?** None.
- **Is the implementation deterministic?** Yes.
- **Is the behavior reproducible?** Yes.
- **Does the implementation match the research paper claim?** **NO.** Implemented as simple string-key deduplication rather than probabilistic entity resolution.

---

### 7. Candidate Percentage Generation
- **Is it actually executable?** Yes.
- **Where is it implemented?** [models/formulation/model.py:L152-L181](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/models/formulation/model.py#L152-L181).
- **What function invokes it?** `formulation_optimizer.predict_with_uncertainty()` called by `candidate_engine.py:L440`.
- **What are its inputs?** `ingredients: List[Dict]`, `targets: Dict`, `strategy: str`.
- **What are its outputs?** `pcts: List[float]`, `is_feasible: bool`, `nutrition_yield: Dict`.
- **What algorithm is actually used?** Constrained nonlinear optimization via SciPy SLSQP.
- **What library is actually used?** `scipy.optimize`, `numpy`.
- **Is any part hardcoded?** Hardcoded inclusion bounds per ingredient role (e.g. salt $0.05\% - 0.40\%$, emulsifiers $0.15\% - 0.80\%$).
- **Is the implementation deterministic?** Yes.
- **Is the behavior reproducible?** Yes.
- **Does the implementation match the research paper claim?** **YES.** Percentages are genuinely solved through numerical optimization.

---

### 8. Optimization Algorithm
- **Is it actually executable?** Yes.
- **Where is it implemented?** [models/formulation/model.py:L115-L160](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/models/formulation/model.py#L115-L160).
- **What function invokes it?** `predict_with_uncertainty()`.
- **What are its inputs?** Nutrient vectors, cost vector, objective function, equality mass-balance constraint.
- **What are its outputs?** Optimized vector `opt_x`.
- **What algorithm is actually used?** `scipy.optimize.minimize(..., method='SLSQP')`.
- **What library is actually used?** `scipy`.
- **Is any part hardcoded?** Objective loss weights (e.g. `curr_prot * 3.0 + curr_cost * 0.5`).
- **Is the implementation deterministic?** Yes.
- **Is the behavior reproducible?** Yes.
- **Does the implementation match the research paper claim?** **NO.** The paper claims Pareto evolutionary optimization (NSGA-II) and Hypervolume metrics; the code executes single-objective SLSQP.

---

### 9. Mass Balance
- **Is it actually executable?** Yes.
- **Where is it implemented?** [models/formulation/model.py:L137, L164-L181](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/models/formulation/model.py#L137), [validation_gate.py:L198-L208](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/validation_gate.py#L198-L208).
- **What function invokes it?** `FormulationOptimizationModel`, `ValidationGate.validate_candidate_set()`.
- **What are its inputs?** Percentage array `opt_x`.
- **What are its outputs?** Normalized percentages summing to $100.0000\%$, mass balance pass/fail status.
- **What algorithm is actually used?** Solver equality constraint $\sum x_i = 100$, post-normalization `(x / sum) * 100`, rounding residual absorption on max element.
- **What library is actually used?** `numpy`.
- **Is any part hardcoded?** Tolerance `0.01%` is hardcoded.
- **Is the implementation deterministic?** Yes.
- **Is the behavior reproducible?** Yes.
- **Does the implementation match the research paper claim?** **YES.** Strict mass balance is 100% verified.

---

### 10. Regulatory Validation
- **Is it actually executable?** Yes.
- **Where is it implemented?** [compliance.py:L35-L129](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/compliance.py#L35-L129).
- **What function invokes it?** `evaluate_compliance()` called by `validation_gate.py:L127` and `main.py:L243`.
- **What are its inputs?** `composition: Dict`, `constraints: Dict`, `product_category: str`.
- **What are its outputs?** `Dict` with FSSAI, FDA, EFSA statuses (`Passed`, `Warning`, `Failed`, `UNKNOWN`).
- **What algorithm is actually used?** Dietary violation checks + CSV table lookup against Codex GSFA additive permissions.
- **What library is actually used?** `pandas`.
- **Is any part hardcoded?** Additive role categorization strings.
- **Is the implementation deterministic?** Yes.
- **Is the behavior reproducible?** Yes.
- **Does the implementation match the research paper claim?** **PARTIALLY.** It verifies category permission, but does not enforce maximum numerical ADI/PPM limits. RCS is additive rather than a binary multiplicative gate.

---

### 11. Evidence Grounding
- **Is it actually executable?** Yes.
- **Where is it implemented?** [validation_gate.py:L185-L196](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/validation_gate.py#L185-L196), [models/ranking/model.py:L59-L64](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/models/ranking/model.py#L59-L64).
- **What function invokes it?** `ValidationGate.validate_candidate_set()`, `MultiObjectiveRankingModel.predict_with_uncertainty()`.
- **What are its inputs?** `all_components: List[Dict]`.
- **What are its outputs?** `groundedness_results`, `evidence_score`.
- **What algorithm is actually used?** String provenance validation and counting: `(grounded_count / total) * 100`.
- **What library is actually used?** Python standard library.
- **Is any part hardcoded?** Excluded null strings (`["UNKNOWN", "None", "NO_EVIDENCE_RECORDED"]`).
- **Is the implementation deterministic?** Yes.
- **Is the behavior reproducible?** Yes.
- **Does the implementation match the research paper claim?** **NO.** The paper's claimed SES formula ($\sum \frac{P_k}{100} \frac{|DOIs|}{|DOIs|+1}$) is not implemented.

---

### 12. Scoring Engine
- **Is it actually executable?** Yes.
- **Where is it implemented?** [models/ranking/model.py:L31-L100](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/models/ranking/model.py#L31-L100).
- **What function invokes it?** `MultiObjectiveRankingModel.predict_with_uncertainty()` called by `scoring_engine.py:L32`.
- **What are its inputs?** `candidate: Dict`, `brief: Dict`, `profile_name: str`.
- **What are its outputs?** `overall_score`, `radar_scores`, `formulas`, `explanation`.
- **What algorithm is actually used?** Linear weighted utility sum over 6 bounded heuristic scores.
- **What library is actually used?** Python standard library.
- **Is any part hardcoded?** Profile weights (e.g. Balanced: 0.20, 0.20, 0.15, 0.15, 0.15, 0.15), required functional roles set (`{"protein", "emulsifier", "sweetener", "fat", "bulking"}`).
- **Is the implementation deterministic?** Yes.
- **Is the behavior reproducible?** Yes.
- **Does the implementation match the research paper claim?** **PARTIALLY.** Provides measurable multi-objective scoring, but deviates from paper formulas.

---

### 13. Ranking Engine
- **Is it actually executable?** Yes.
- **Where is it implemented?** [scoring_engine.py:L44-L54](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/scoring_engine.py#L44-L54).
- **What function invokes it?** `scoring_engine.rank_candidates()` called by `pipeline_runner.py:L411`.
- **What are its inputs?** `candidates: List[Dict]`, `brief_input`, `profile_name`.
- **What are its outputs?** Sorted list of candidate dictionaries.
- **What algorithm is actually used?** `sorted(candidates, key=lambda x: x["score"]["overall_score"], reverse=True)`.
- **What library is actually used?** Python built-in `sorted()`.
- **Is any part hardcoded?** None.
- **Is the implementation deterministic?** Yes.
- **Is the behavior reproducible?** Yes.
- **Does the implementation match the research paper claim?** **NO.** Claimed as Pareto optimization and TOPSIS; implemented as a standard linear weighted sort.

---

### 14. Iteration & Refinement
- **Is it actually executable?** **NO (as an automated closed loop).**
- **Where is it implemented?** [pipeline_runner.py:L127-L489](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/pipeline_runner.py#L127-L489).
- **What function invokes it?** `run_pipeline(..., iterations=1)`.
- **What are its inputs?** `iterations: int` CLI parameter.
- **What are its outputs?** `iteration_results: List[Dict]`.
- **What algorithm is actually used?** Procedural Python `for iter_idx in range(1, iterations + 1):` with manual weight override on iteration 2.
- **What library is actually used?** Python standard library.
- **Is any part hardcoded?** Iteration 2 boosted weights (`sc["weight"] = 0.95`).
- **Is the implementation deterministic?** Yes.
- **Is the behavior reproducible?** Yes.
- **Does the implementation match the research paper claim?** **NO.** There is no automated feedback loop triggered by validation failure. It executes a single pass unless overridden manually via CLI flags.

---

### 15. LLM Synthesis Generation
- **Is it actually executable?** Yes.
- **Where is it implemented?** [synthesis_engine.py:L77-L163](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/synthesis_engine.py#L77-L163), [groq_client.py:L68-L110](file:///c:/Users/asus/.gemini/antigravity/scratch/FOOD%20FORMULATION%20PLATFORM/Food%20Web%20App%20Core/backend/groq_client.py#L68-L110).
- **What function invokes it?** `synthesis_engine.synthesize()` called by `pipeline_runner.py:L440` and `main.py:L235`.
- **What are its inputs?** `query`, `requirements`, `ranked_candidate`, `evidence_list`.
- **What are its outputs?** JSON report with title, justification summary, ingredient explanations, 3 process steps, and sensory predictions.
- **What algorithm is actually used?** Zero-temperature / low-temperature (0.1) LLM inference via Groq REST API, with fallback to deterministic procedural synthesis.
- **What library is actually used?** `requests`, `json`.
- **Is any part hardcoded?** System prompt text, fallback process steps.
- **Is the implementation deterministic?** Near-deterministic (temperature 0.1); fallback is 100% deterministic.
- **Is the behavior reproducible?** Highly reproducible.
- **Does the implementation match the research paper claim?** **YES.** Real LLM generation grounded strictly in validated candidate sets.

---

## 3. Summary of Aggressively Detected False Claims

1. **False Claim of "Dynamic Scientific Subgraphs / GraphRAG"**:
   - *Verdict:* **UNSUPPORTED**. Cypher queries in the retrieval path are static `LIMIT 200` queries. Dynamic Cypher generation is a formatted string stored in logs, but never executed.
2. **False Claim of "Pareto Optimization / NSGA-II / NSGA-III / TOPSIS"**:
   - *Verdict:* **UNSUPPORTED**. No genetic algorithm or Pareto frontier calculator exists in the codebase. Inclusion percentages are optimized using single-objective SciPy SLSQP, and ranking is a linear weighted sum sort.
3. **False Claim of "Dense Neural Vector Search with Qdrant / MiniLM"**:
   - *Verdict:* **UNSUPPORTED**. Qdrant is completely absent from the repository. Active vector search uses Scikit-Learn `TfidfVectorizer` + Cosine Similarity over in-memory ingredient strings.
4. **False Claim of "LLM-Powered NLP Intent Parser"**:
   - *Verdict:* **UNSUPPORTED**. The parser is 100% regular expressions and keyword checking. The instantiated Groq LLM is never called during brief parsing.
5. **False Claim of "Automated Closed-Loop Iterative Refinement"**:
   - *Verdict:* **UNSUPPORTED**. The pipeline executes a single pass. Multi-iteration re-runs occur only if the user manually passes `--iterations 2` on the CLI.
6. **False Claim of "Scientific Evidence Strength (SES) & Multiplicative Regulatory Gate (RCS)"**:
   - *Verdict:* **UNSUPPORTED**. The paper's claimed mathematical formulas for SES (with DOIs) and RCS (as a binary multiplicative veto gate) are not implemented in the ranking model.
