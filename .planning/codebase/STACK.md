# Technology Stack

**Analysis Date:** 2026-09-16

## Languages

**Primary:**
- Python 3.10+ — Backend services, formulation pipeline, knowledge graph ETL, NLP/LLM integration (`Food Web App Core/backend`, `kg_prep`)
- TypeScript 5.2+ — Frontend user interface, state management, graph visualization (`Food Web App Core/frontend`)

**Secondary:**
- Cypher / SQL — Graph database queries and relational persistence (`Food Web App Core/backend/neo4j_client.py`, `Food Web App Core/backend/database.py`)
- HTML5 / CSS3 (Tailwind) — UI styling and layout (`Food Web App Core/frontend/src/app/globals.css`)

## Runtime & Engines

- Node.js (v18+ / v20+) — Frontend runtime for Next.js 14
- CPython 3.10 - 3.14 — Backend execution environment and data processing pipelines

## Frameworks & Core Libraries

**Backend (`Food Web App Core/backend`):**
- FastAPI (`fastapi>=0.100.0`) — REST API server and request routing (`Food Web App Core/backend/main.py`)
- Uvicorn (`uvicorn>=0.22.0`) — ASGI server
- Pydantic v2 (`pydantic>=2.0`, `pydantic-settings>=2.0`) — Data validation and configuration schemas (`Food Web App Core/backend/schemas.py`)
- LangChain / LangGraph (`langchain>=0.1.0`, `langgraph>=0.0.15`) — Agentic reasoning and formulation workflows
- Groq / HuggingFace (`langchain-groq`, `langchain-huggingface`) — LLM generation and sentence embeddings
- Sentence Transformers (`sentence-transformers>=2.2.2`) — Semantic retrieval and embedding matching
- Neo4j Python Driver (`neo4j>=5.14.0`) — Cypher graph traversal and querying
- SQLAlchemy (`sqlalchemy>=2.0`) — SQLite local persistence (`Food Web App Core/backend/database.py`)
- Pandas & NumPy (`pandas>=2.0`, `numpy>=1.24.0`) — Ingredient tabular processing and matrix computations
- SciPy (`scipy>=1.11.0`) — Linear programming formulation optimization

**Frontend (`Food Web App Core/frontend`):**
- Next.js 14 (`next: ^14.0.0`) — React application framework with App Router (`Food Web App Core/frontend/src/app`)
- React 18 (`react: ^18.2.0`, `react-dom: ^18.2.0`) — UI component library
- Zustand (`zustand: ^4.4.0`) — Global state management (`Food Web App Core/frontend/src/store`)
- Cytoscape.js & ReactFlow (`cytoscape: ^3.34.1`, `reactflow: ^11.10.0`) — Graph and pipeline visualization
- Recharts (`recharts: ^2.10.0`) — Nutritional and radar metric visualization
- Tailwind CSS 3.3 (`tailwindcss: ^3.3.0`, `tailwind-merge: ^2.0.0`) — Utility-first styling
- Lucide React (`lucide-react: ^0.290.0`) — Icons

**Knowledge Graph Pipeline (`kg_prep`):**
- Requests & aiohttp (`requests>=2.31.0`, `aiohttp>=3.9.0`) — Synchronous and async scraping
- BeautifulSoup4 & lxml (`beautifulsoup4>=4.12.0`, `lxml>=5.1.0`) — HTML / XML document parsing
- PyYAML (`pyyaml>=6.0.1`) — Taxonomy and ontology configuration parsing

## Configuration & Environment

- Environment Variables: `.env` loaded via `python-dotenv` in backend (`Food Web App Core/backend/config/settings.py` / `.env`)
- Backend Config: `Food Web App Core/backend/config/compatibility_rules.yaml`
- Frontend Config: `Food Web App Core/frontend/next.config.js`, `Food Web App Core/frontend/tailwind.config.ts`

---

*Stack analysis: 2026-09-16*
