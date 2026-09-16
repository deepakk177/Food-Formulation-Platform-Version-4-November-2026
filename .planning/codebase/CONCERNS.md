# Codebase Concerns & Technical Debt

**Analysis Date:** 2026-09-16

## Technical Debt & Hardcoding Audit

**Hardcoded / Fabricated Logic:**
- Issue: A forensic code audit identified 69 hardcoded or simulated values across scoring, candidate percentage allocation, shelf-life prediction, regulatory status, and cost approximations.
- Files:
  - `Food Web App Core/backend/candidate_engine.py`: Static heuristic percentage allocation instead of mathematical linear programming optimization.
  - `Food Web App Core/backend/scoring_engine.py`: Hardcoded fallback scores (e.g. `0.85`, `0.78`) when attribute data is sparse.
  - `Food Web App Core/backend/repository.py`: Synthetic metadata and placeholder shelf-life values.
  - `Food Web App Core/backend/docs/HARDCODING_AUDIT.md`: Complete register of all 69 identified issues.
- Impact: Formulations may appear plausible on demo data but lack grounded scientific precision and dynamic responsiveness to novel product briefs.
- Fix Approach: Transition to deterministic linear programming formulation solvers (`scipy.optimize.linprog`), real regulatory limits (`regulatory_database.csv`), and scientific compatibility rules (`compatibility_rules.yaml`).

## Fragile Areas & Edge Cases

**Sparse Ingredient Metadata:**
- Files: `Food Web App Core/backend/repository.py`, `Food Web App Core/backend/candidate_engine.py`
- Why Fragile: When an ingredient is retrieved that lacks specific micronutrient or density metrics, fallbacks may either raise exceptions or default to zero, skewing optimization.
- Safe Modification: Ensure strict schema validation with `Optional[float]` and explicit imputation policies (or flagging missing data to the user) rather than silently inventing default values.

**Neo4j Connectivity & Offline Operation:**
- Files: `Food Web App Core/backend/neo4j_client.py`, `Food Web App Core/backend/pipeline_runner.py`
- Why Fragile: If Neo4j is not running locally, queries must fall back cleanly to the embedded SQLite/CSV knowledge graph without degradation of constraint validation.
- Safe Modification: Centralize fallback retrieval pathways so that all queries route through `repository.py` consistently.

## Security Considerations

**API Key Management:**
- Risk: Potential leakage of `GROQ_API_KEY` or Neo4j credentials if committed to version control.
- Files: `Food Web App Core/backend/.env`, `Food Web App Core/backend/.env.example`
- Current Mitigation: `.gitignore` excludes `.env`. `.env.example` contains only blank template keys.
- Recommendation: Maintain zero secrets in code, use environment variable injection in CI/CD and deployment.

## Performance Bottlenecks

**Semantic Search & LLM Inference Latency:**
- Files: `Food Web App Core/backend/requirements_extractor.py`, `Food Web App Core/backend/synthesis_engine.py`
- Cause: Cold starts on embedding models and network round-trips to external LLM providers during pipeline execution.
- Improvement Path: Cache embeddings for seed ingredients; support asynchronous background job execution with polling/streaming for the frontend.

---

*Concerns audit: 2026-09-16*
