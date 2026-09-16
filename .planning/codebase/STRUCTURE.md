# Codebase Structure

**Analysis Date:** 2026-09-16

## Directory Layout

```
FOOD FORMULATION PLATFORM/
├── Food Web App Core/
│   ├── backend/                 # FastAPI server, formulation engines & algorithms
│   │   ├── config/              # YAML rules, settings, compatibility matrices
│   │   ├── data/                # Raw ingredient CSVs, taxonomy, regulatory databases
│   │   ├── docs/                # Architecture specifications & forensic audit logs
│   │   ├── outputs/             # Generated formulation reports and logs
│   │   ├── tests/               # Pytest test suite for backend engines
│   │   ├── candidate_engine.py  # Candidate generation & percentage allocation
│   │   ├── constraint_engine.py # Hard/soft constraint graph evaluator
│   │   ├── main.py              # FastAPI application router & endpoints
│   │   ├── neo4j_client.py      # Neo4j Cypher client
│   │   ├── pipeline_runner.py   # Orchestrator for end-to-end pipeline
│   │   ├── repository.py        # SQLite / CSV data access repository
│   │   ├── requirements_extractor.py # NLP brief parser
│   │   ├── scoring_engine.py    # Multi-factor formulation scoring
│   │   ├── synthesis_engine.py  # Scientific rationale generator
│   │   └── validation_gate.py   # Formulation safety & regulatory validator
│   └── frontend/                # Next.js 14 React user interface
│       ├── src/
│       │   ├── app/             # App Router pages and layouts
│       │   ├── components/      # React UI components (Chat, Graphs, Formulations)
│       │   ├── store/           # Zustand state management
│       │   └── types/           # TypeScript interfaces and types
│       ├── package.json         # Frontend dependencies and npm scripts
│       └── tailwind.config.ts   # Tailwind CSS configuration
├── kg_prep/                     # Knowledge Graph extraction, ETL & validation
│   ├── src/
│   │   ├── collectors/          # Scrapers for PubChem, USDA, OpenFoodFacts
│   │   ├── profiler/            # Ingredient profiling & normalization
│   │   ├── relationship_builder/# Graph relationship construction
│   │   ├── semi_structured_processor/
│   │   ├── structured_processor/
│   │   ├── unstructured_processor/
│   │   ├── utils/               # HTTP client, mock generator, raw extractors
│   │   └── validator/           # Schema & integrity validation
│   ├── tests/                   # Pytest test suite for KG pipeline
│   └── requirements.txt         # KG Python dependencies
└── .planning/                   # GSD project plans, roadmap, and codebase maps
    └── codebase/                # Codebase intelligence and architecture maps
```

## Key File Locations

**Entry Points:**
- `Food Web App Core/backend/main.py`: Backend FastAPI server entry point.
- `Food Web App Core/frontend/src/app/page.tsx`: Frontend web application main landing page.
- `Food Web App Core/backend/pipeline_runner.py`: Formulation pipeline execution entry point.

**Configuration:**
- `Food Web App Core/backend/config/compatibility_rules.yaml`: Known ingredient incompatibilities and interaction rules.
- `Food Web App Core/backend/data/raw/regulatory_database.csv`: Real regulatory limits across jurisdictions.
- `Food Web App Core/frontend/next.config.js`: Next.js web application configuration.

**Core Formulation Logic:**
- `Food Web App Core/backend/requirements_extractor.py`: Natural language brief analysis.
- `Food Web App Core/backend/constraint_engine.py`: Constraint model building and validation.
- `Food Web App Core/backend/candidate_engine.py`: Ingredient candidate retrieval and weighting.
- `Food Web App Core/backend/validation_gate.py`: Formulation safety checks and regulatory audit.
- `Food Web App Core/backend/scoring_engine.py`: Quality, cost, nutrition, and feasibility scoring.

**Testing:**
- `Food Web App Core/backend/tests/`: Unit and end-to-end integration tests.
- `kg_prep/tests/`: Knowledge Graph scraper and profiler tests.

## Where to Add New Code

**New Formulation Constraint or Rule:**
- Rule definition: `Food Web App Core/backend/config/`
- Parsing & Evaluation: `Food Web App Core/backend/constraint_engine.py`

**New Optimization Algorithm:**
- Implementation: `Food Web App Core/backend/candidate_engine.py` or new `formulation_optimizer.py`
- Test: `Food Web App Core/backend/tests/`

**New Frontend View or Widget:**
- UI Component: `Food Web App Core/frontend/src/components/`
- State Slice: `Food Web App Core/frontend/src/store/`
- Route: `Food Web App Core/frontend/src/app/`

---

*Structure analysis: 2026-09-16*
