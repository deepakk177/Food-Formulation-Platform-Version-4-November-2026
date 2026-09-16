# Architecture Overview

**Analysis Date:** 2026-09-16

## System Architecture

The Food Formulation Platform is structured as a multi-tier, data-driven formulation intelligence system combining knowledge graph retrieval, linear programming mathematical optimization, and LLM-assisted reasoning.

```
[ Next.js 14 Frontend UI ]
       |  HTTP / REST
[ FastAPI Application Core (main.py) ]
       |
[ Pipeline Runner (pipeline_runner.py) ]
  ├── 1. Requirements Extraction (requirements_extractor.py)
  ├── 2. Constraint Graph Resolution (constraint_engine.py)
  ├── 3. Context-Aware Retrieval (candidate_engine.py / retrieval_service.py)
  ├── 4. Mathematical LP Optimization (formulation_optimizer.py)
  ├── 5. Validation & Regulatory Gate (validation_gate.py / compliance.py)
  ├── 6. Multi-Criteria Scoring (scoring_engine.py)
  └── 7. Scientific Synthesis & Explanation (synthesis_engine.py)
       |
[ Data & Storage Layer ]
  ├── Neo4j Graph DB (neo4j_client.py)
  ├── SQLite Relational State (database.py / repository.py)
  └── Regulatory & Science Datastores (regulatory_database.csv, compatibility_rules.yaml)
```

## Core Abstractions & Layers

**Pipeline Runner:**
- Location: `Food Web App Core/backend/pipeline_runner.py`
- Role: Coordinates the end-to-end execution flow from a raw text brief to candidate formulation generation and multi-objective scoring.
- State: Emits structured events, step logs, and full formulation result schemas.

**Requirements Extractor:**
- Location: `Food Web App Core/backend/requirements_extractor.py`
- Role: Parses unstructured product briefs into typed requirements (dietary claims, nutritional targets, target cost, shelf life, banned ingredients, sensory goals).

**Constraint Engine:**
- Location: `Food Web App Core/backend/constraint_engine.py`
- Role: Classifies constraints into hard constraints (must satisfy: allergens, regulatory caps, vegan/kosher) and soft constraints (optimizable: cost, protein target, calories).

**Candidate Engine & Retrieval Service:**
- Location: `Food Web App Core/backend/candidate_engine.py`, `retrieval_service.py`, `rag_engine.py`
- Role: Fetches candidate ingredients from the Knowledge Graph based on functional roles (base protein, emulsifier, stabilizer, sweetener, etc.) and filters out hard-violating ingredients.

**Validation & Regulatory Gate:**
- Location: `Food Web App Core/backend/validation_gate.py`, `compliance.py`
- Role: Audits formulations against jurisdiction-specific regulatory databases (Codex GSFA, FDA 21 CFR, EFSA) and verified incompatibility matrices.

**Scoring Engine:**
- Location: `Food Web App Core/backend/scoring_engine.py`
- Role: Computes transparent composite scores across nutritional alignment, cost efficiency, ingredient compatibility, and regulatory confidence.

## Data Flow

1. **User input**: User submits product brief (e.g., "High-protein vegan meal replacement shake under $1.50/serving") in Next.js UI.
2. **Extraction**: `requirements_extractor.py` extracts structured constraints.
3. **Graph Retrieval**: `neo4j_client.py` and `retrieval_service.py` retrieve eligible ingredients matching required functional categories.
4. **Formulation Solving**: Mathematical LP solver calculates percentages satisfying sum-to-100%, nutrition boundaries, and regulatory limits.
5. **Validation**: Candidate recipes pass through `validation_gate.py` for allergen, regulatory, and synergy compliance.
6. **Synthesis & Delivery**: `synthesis_engine.py` synthesizes scientific rationale; `main.py` returns full payload to Zustand store and Next.js view.

## Error Handling & Fallbacks

- **Database Fallback**: When Neo4j is unavailable or offline, the platform falls back to SQLite (`tcs_food_formulator_kg.db`) and CSV repository access (`Food Web App Core/backend/repository.py`).
- **LLM Fallback**: When LLM calls fail or timeout, deterministic fallback extractors and template-driven rationale generators provide graceful degradation without crashing the API.

---

*Architecture analysis: 2026-09-16*
