# External Integrations

**Analysis Date:** 2026-09-16

## Databases & Storage

**Neo4j Graph Database:**
- Purpose: Stores the Food Knowledge Graph including ingredients, functional classes, nutrients, allergens, regulations, and interactions.
- Client: `neo4j.GraphDatabase.driver` implemented in `Food Web App Core/backend/neo4j_client.py`
- Connection: Configured via `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` in `.env`.
- Fallback: Local SQLite / CSV graph fallback in `Food Web App Core/backend/repository.py` and `Food Web App Core/backend/tcs_food_formulator_kg.db`.

**SQLite Database:**
- Purpose: Formulation run history, pipeline task state, session records, local taxonomy caches.
- Implementation: `Food Web App Core/backend/database.py` with SQLAlchemy engines targeting `tcs_food_formulator.db`.

## LLM & AI Services

**Groq Cloud API:**
- Purpose: High-speed LLM inference for requirements extraction, formulation reasoning, and rationale generation.
- Implementation: LangChain Groq client in `Food Web App Core/backend/requirements_extractor.py` and `Food Web App Core/backend/synthesis_engine.py`.
- Key Model: `llama3-70b-8192` / `llama-3.3-70b-versatile` configured via `GROQ_API_KEY`.

**HuggingFace / Local Sentence Transformers:**
- Purpose: Text embeddings for semantic ingredient search, allergen matching, and vector similarity retrieval.
- Implementation: `Food Web App Core/backend/rag_engine.py` and `Food Web App Core/backend/retrieval_service.py`.

## Data Sources & Scraping (Knowledge Graph ETL)

**Food Safety & Regulatory Authorities:**
- Codex Alimentarius GSFA (Codex STAN 192-1995)
- US FDA CFR Title 21 (GRAS notices, 21 CFR 182/184)
- EFSA (European Food Safety Authority) additive approvals
- FSSAI (Food Safety and Standards Authority of India)
- Parsed into `Food Web App Core/backend/data/raw/regulatory_database.csv`.

**Scientific Repositories (`kg_prep`):**
- PubChem Compound & Bioactivity APIs (`kg_prep/src/utils/raw_extractor.py`)
- USDA FoodData Central / OpenFoodFacts scrapers (`kg_prep/src/collectors`)
- Food science compatibility ontologies (`Food Web App Core/backend/config/compatibility_rules.yaml`)

## Frontend-Backend Communication

**FastAPI REST Endpoints:**
- Next.js frontend calls FastAPI backend via HTTP endpoints (`http://localhost:8000/api/...`)
- Primary client: `Food Web App Core/frontend/src/store/useFormulationStore.ts` and fetch calls in `Food Web App Core/frontend/src/components/`.

---

*Integration analysis: 2026-09-16*
