# Complete System & Project Requirements (Porting to Another Device)

Everything required to install, configure, and run the **Food Formulation Platform** (Web App + Formulation Pipeline + Exhaustive Search + Knowledge Graph Scripts) on a new machine.

---

## 1. System & Runtime Prerequisites

| Component | Required / Tested Version | Notes |
| :--- | :--- | :--- |
| **Python** | `3.11+` (tested on `3.14.0`) | Used for FastAPI backend, SciPy SLSQP optimizer, Scikit-Learn ML/TF-IDF, and CLI scripts |
| **Node.js** | `20+` (tested on `v21.6.2`) | Used for Next.js 14 frontend |
| **npm** | `10+` (tested on `10.2.4`) | Included with Node.js |
| **OS** | Windows 10/11, Linux, or macOS | Developed on Windows; `backend/Dockerfile` targets `python:3.11-slim` and `frontend/Dockerfile` targets `node:20-alpine` |
| **Docker & Docker Compose** *(Optional)* | Docker Desktop / Compose v2+ | Only needed if running via `Food Web App Core/docker-compose.yml` |
| **Neo4j** *(Optional)* | `5.x` (`bolt://localhost:7687`) | Optional; when offline or `NEO4J_ENABLED=0`, the backend uses the grounded SQLite + CSV KG index |
| **PostgreSQL** *(Optional)* | `15-alpine` (`port 5432`) | Optional; when `DATABASE_URL` is blank, the backend uses local SQLite (`tcs_food_formulator.db`) |

---

## 2. Python Backend & Pipeline Dependencies

Create a virtual environment inside `Food Web App Core/backend/`:

```powershell
# Windows PowerShell
cd "Food Web App Core\backend"
python -m venv venv
.\venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
cd "Food Web App Core/backend"
python3 -m venv venv
source venv/bin/activate
```

### A. Core Packages (from `Food Web App Core/backend/requirements.txt`)
```text
fastapi>=0.100.0
uvicorn>=0.22.0
pydantic>=2.0
pydantic-settings>=2.0
sqlalchemy>=2.0
pandas>=2.0
numpy>=1.24.0
python-dotenv>=1.0.0
requests>=2.31.0
tqdm>=4.65.0
langchain>=0.1.0
langchain-core>=0.1.0
langchain-groq>=0.1.0
langchain-huggingface>=0.0.1
langgraph>=0.0.15
sentence-transformers>=2.2.2
email-validator>=2.0.0
neo4j>=5.14.0
```

### B. Additional Required Packages (Imported by Pipeline, Optimizer & ML — Missing from `requirements.txt`)
Install these as well so all formulation, optimization, ML, and CLI scripts run without `ModuleNotFoundError`:

```text
scipy>=1.11.0          # Constrained SLSQP optimization (models/formulation/model.py)
scikit-learn>=1.3.0    # TF-IDF semantic search & HistGradientBoosting role classifier
joblib>=1.3.0          # Loading ml/artifacts/functional_role_classifier.joblib
PyYAML>=6.0            # Loading backend/config/constraint_priority.yaml
groq>=0.11.0           # Groq LLM client
networkx>=3.0          # Graph utilities
pytest>=8.0.0          # Test suites
```

**Single-command install (exact tested versions in `venv`):**
```bash
pip install -r requirements.txt scipy==1.17.1 scikit-learn==1.9.0 joblib==1.5.3 PyYAML==6.0.3 groq==0.37.1 networkx==3.6.1 pytest==9.2.0
```
*(Tested working versions for key core packages: `fastapi==0.136.3`, `uvicorn==0.49.0`, `pydantic==2.13.4`, `SQLAlchemy==2.0.50`, `pandas==3.0.3`, `numpy==2.4.6`, `neo4j==6.2.0`, `torch==2.12.0`, `transformers==5.10.2`, `sentence-transformers==5.5.1`.)*

---

## 3. Frontend (Next.js) Dependencies

Defined in `Food Web App Core/frontend/package.json`:

- **Runtime dependencies**: `next@^14.0.0`, `react@^18.2.0`, `react-dom@^18.2.0`, `zustand@^4.4.0`, `recharts@^2.10.0`, `reactflow@^11.10.0`, `cytoscape@^3.34.1`, `lucide-react@^0.290.0`, `clsx@^2.0.0`, `tailwind-merge@^2.0.0`, `@types/cytoscape@^3.31.0`, `playwright-core@^1.65.0`
- **Dev dependencies**: `typescript@^5.2.0`, `tailwindcss@^3.3.0`, `postcss@^8.4.0`, `autoprefixer@^10.4.0`, `@types/node@^20.0.0`, `@types/react@^18.2.0`, `@types/react-dom@^18.2.0`

Install command:
```bash
cd "Food Web App Core/frontend"
npm install
```

---

## 4. Required Data Files, Databases & ML Artifacts

Ensure these repository files are copied/present on the target device (do **not** omit them via `.gitignore` when transferring):

| File Path | Purpose |
| :--- | :--- |
| `Food Web App Core/backend/tcs_food_formulator_kg.db` | Master SQLite Knowledge Graph DB (**23,893** ingredient records + `ingredient_learning_store`) |
| `Food Web App Core/backend/tcs_food_formulator.db` | Application SQLite DB (users, projects, formulations, compliance logs; auto-initialized if absent) |
| `Food Web App Core/backend/food_ingredients_clean.csv` | Offline fallback index for `neo4j_client.py` |
| `Food Web App Core/backend/config/constraint_priority.yaml` | Hard/soft constraint classification weights |
| `ml/artifacts/functional_role_classifier.joblib` | Pre-trained functional role classifier (`ml/inference/predictor.py`) |
| `kg_prep/data/output/Relationships/foodadditive_allowed_in_foodcategory.csv` | Codex GSFA additive-category compliance table (`compliance.py`) |
| `kg_prep/data/output/graph_statistics.csv` | KG node/edge/reachability statistics (`26,668` nodes, `63,758` edges, `15,271` reachable) |

---

## 5. Environment Configuration

### Backend (`Food Web App Core/backend/.env`)
Copy `Food Web App Core/backend/.env.example` to `.env`:

```env
PORT=8000
HOST=0.0.0.0

# Leave blank to use local SQLite (./tcs_food_formulator.db)
DATABASE_URL=

# Optional: Groq API key for LLM synthesis (falls back deterministically if blank)
GROQ_API_KEY=

# Optional: USDA FoodData Central key
USDA_API_KEY=DEMO_KEY

# Optional: Pinecone (falls back to in-memory)
PINECONE_API_KEY=
PINECONE_ENV=us-east-1

# JWT signing secret
JWT_SECRET=tcs_secret_key_67890

# Set to 0 when Neo4j is not running locally (avoids 20s startup timeout)
NEO4J_ENABLED=0
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=Food@123
NEO4J_DATABASE=neo4j
```

### Frontend (`Food Web App Core/frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 6. Running on the New Device

### Option A: Local Development (Recommended)

**Terminal 1 — Backend (Port `8000`):**
```powershell
cd "Food Web App Core\backend"
$env:NEO4J_ENABLED="0"
.\venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 — Frontend (Port `3000`):**
```powershell
cd "Food Web App Core\frontend"
npm run dev
```

- Web App UI: `http://localhost:3000`
- Backend API & Swagger Docs: `http://localhost:8000/docs`

### Option B: CLI Formulation & Pruning Scripts
```powershell
cd "Food Web App Core\backend"
.\venv\Scripts\python.exe pipeline_runner.py --brief "Create a dairy-free chocolate..."
.\venv\Scripts\python.exe run_kg_pruning_briefs.py
.\venv\Scripts\python.exe run_white_001_exhaustive.py
```

### Option C: Docker Compose
```bash
cd "Food Web App Core"
docker compose up --build
```
*(Starts PostgreSQL on `5432`, FastAPI backend on `8000`, Next.js frontend on `3000`, and Nginx on `80`. Note: update `Food Web App Core/backend/requirements.txt` to include `scipy`, `scikit-learn`, `joblib`, `PyYAML`, `groq`, and `networkx` before building the Docker image.)*
