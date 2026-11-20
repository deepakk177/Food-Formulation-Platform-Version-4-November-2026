# 🍔 TCS Food Formulator - Quickstart & Usage Guide

Welcome to the **TCS Food Formulator**! This project is an AI-driven, compliance-aware RAG platform designed to assist food scientists and product developers in formulating new recipes (e.g., vegan beverages, gluten-free bread), validating nutrition metrics, and verifying regional food compliance against global regulations in real time.

---

## 📌 Table of Contents
1. [System Architecture](#-system-architecture)
2. [Prerequisites](#-prerequisites)
3. [Configuration & Environment Variables](#-configuration--environment-variables)
4. [Running the Application](#-running-the-application)
   * [Method A: Automated PowerShell Launcher (Windows Local Dev)](#method-a-automated-powershell-launcher-windows-local-dev)
   * [Method B: Docker Compose (Fully Orchestrated Stack)](#method-b-docker-compose-fully-orchestrated-stack)
   * [Method C: Manual Cross-Platform Launch (Mac/Linux/Windows)](#method-c-manual-cross-platform-launch-maclinuxwindows)
5. [Feature & UI Walkthrough](#-feature--ui-walkthrough)
   * [1. User Registration & Default Credentials](#1-user-registration--default-credentials)
   * [2. Project Dashboard](#2-project-dashboard)
   * [3. Guided Formulator (AI Stepper)](#3-guided-formulator-ai-stepper)
   * [4. Expert Canvas (Live Editor & Sliders)](#4-expert-canvas-live-editor--sliders)
   * [5. Ingredient Pantry (USDA Search)](#5-ingredient-pantry-usda-search)
6. [Directory Code Map](#-directory-code-map)
7. [Troubleshooting & FAQ](#-troubleshooting--faq)

---

## 🏗️ System Architecture

The application is structured as a full-stack web utility orchestrated with the following layers:

* **Frontend UI (Next.js 14 + Tailwind CSS + Zustand)**: A premium interactive dashboard, featuring a guided formulation stepper, a drag-and-drop / slider-based expert recipe canvas, and Recharts-based nutritional charts.
* **Backend API (FastAPI + SQLAlchemy)**: Manages authentication, formulation history, USDA ingredient cache, and coordinates AI/compliance operations.
* **AI Graph Engine (LangGraph + Groq LLaMA 3.3)**: Executes a Retrieval-Augmented Generation (RAG) workflow to retrieve ingredients from [food_ingredients_clean.csv](file:///backend/food_ingredients_clean.csv), queries LLaMA 3.3 via Groq API for precise percentages and processing instructions, and parses the outputs.
* **Compliance Auditor (Rule-based Engine)**: Evaluates formulations in real time against FDA (US), EFSA (Europe), and FSSAI (India) parameters, flags allergens, and audits chemical/preservative limits.
* **Database (SQLite for Dev / PostgreSQL for Prod)**: Stores user credentials, development projects, formulation versions, and compliance logs.
* **Orchestrator / Proxy (Nginx + Docker Compose)**: Nginx listens on port 80 and routes API routes (`/api/`) and documentation (`/docs`) to the backend, forwarding web pages (`/`) to the frontend.

---

## 📋 Prerequisites

Before running the application locally, ensure you have the following installed on your machine:

| Component | Required Version | Purpose |
| :--- | :--- | :--- |
| **Node.js** | v18.0.0 or higher | Frontend build and Next.js development server |
| **Python** | v3.9 to v3.12 | Backend FastAPI server, SQLAlchemy, and LangGraph |
| **Docker & Docker Desktop** | Latest (Optional) | For running the entire multi-service stack with a single command |
| **PowerShell** | v5.1+ (Windows Only) | For running the quickstart development launcher script |

You will also need a **Groq API Key** to run the formulation generator. You can generate one for free at the [Groq Console](https://console.groq.com/).

---

## ⚙️ Configuration & Environment Variables

### 1. Backend Environment Setup (`backend/.env`)
Copy [backend/.env.example](file:///backend/.env.example) to a new file named `backend/.env` and fill in the values:

```bash
# FastAPI Server Port & Bindings
PORT=8000
HOST=0.0.0.0

# Database URL (Relational DB for users/projects)
# Leave blank to automatically fallback to the local SQLite database file (./tcs_food_formulator.db)
DATABASE_URL=

# Neo4j Knowledge Graph Configuration (Live DB with 24,930 nodes & 5,265 relationships)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=Food@123
NEO4J_DATABASE=neo4j

# Groq API Configuration (Fast high-throughput LLM reasoning)
GROQ_API_KEY=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
GROQ_MODEL=openai/gpt-oss-20b

# USDA API Keys (Optional - default is DEMO_KEY)
USDA_API_KEY=DEMO_KEY

# Pinecone Key (Optional - Fallback is InMemoryVectorStore)
PINECONE_API_KEY=
PINECONE_ENV=us-east-1

# JWT Secret Signing Key (Used to sign session tokens)
JWT_SECRET=tcs_secret_key_67890
```

> [!IMPORTANT]
> - **Neo4j Knowledge Graph**: Operates on `bolt://localhost:7687` with verified credentials (`neo4j:Food@123`).
> - **Groq LLM Engine**: Connected via `GROQ_API_KEY` using active model `openai/gpt-oss-20b` for formulation synthesis and reasoning.


### 2. Frontend Environment Setup (`frontend/.env.local`)
Create or edit [frontend/.env.local](file:///frontend/.env.local) to point the Next.js app to your backend API URL:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🚀 Running the Application

### Method A: Automated PowerShell Launcher (Windows Local Dev)
This is the easiest way to launch the application for local development on a Windows machine. It automatically creates the Python virtual environment, installs all frontend and backend dependencies, and opens both servers in separate PowerShell terminal windows.

1. Open a PowerShell terminal as an Administrator or with Execution Policy bypassed.
2. Navigate to the `Food web App` folder.
3. Run the startup script:
   ```powershell
   powershell -ExecutionPolicy Bypass -File start_dev.ps1
   ```
4. The script will:
   * Create `backend/venv` and install `requirements.txt`.
   * Create `backend/.env` (if not present) and prompt you to input your Groq API Key.
   * Run `npm install` inside the `frontend` folder.
   * Start the Backend Server on [http://localhost:8000](http://localhost:8000) and Frontend on [http://localhost:3000](http://localhost:3000).

---

### Method B: Docker Compose (Fully Orchestrated Stack)
Use this option to run the application in isolated Docker containers, simulating a production deployment with a PostgreSQL database and an Nginx reverse proxy routing traffic on port 80.

1. Set your `GROQ_API_KEY` as an environment variable in your terminal, or create a `.env` file in the **root** folder containing:
   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   ```
2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
3. Docker will orchestrate four services:
   * **`postgres`** (Port `5432`): High-performance database.
   * **`backend`** (Port `8000`): FastAPI engine.
   * **`frontend`** (Port `3000`): Next.js app.
   * **`nginx`** (Port `80`): Main load balancer / proxy.
4. Access the web interface on: **[http://localhost](http://localhost)** (Port 80).
5. Access API Swagger Docs on: **[http://localhost/docs](http://localhost/docs)**.

---

### Method C: Manual Cross-Platform Launch (Mac/Linux/Windows)
If you prefer to start the services manually or are running on macOS or Linux, follow these steps:

#### Step 1: Start the FastAPI Backend
1. Open a new terminal and navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Make sure your `backend/.env` file is set up.
5. Run the Uvicorn reload server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Step 2: Start the Next.js Frontend
1. Open a second terminal window and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install Node.js dependencies:
   ```bash
   npm install
   ```
3. Run the Next.js development server:
   ```bash
   npm run dev
   ```
4. Open your browser and navigate to **[http://localhost:3000](http://localhost:3000)**.

---

## 🍽️ Feature & UI Walkthrough

### 1. User Registration & Default Credentials
On startup, the system automatically checks the database and seeds a default administrative expert account. 

* **Default Admin Email:** `admin@tcs.com`
* **Default Admin Password:** `admin123`

You can also use the registration form to create new accounts with roles like **"Expert User"** (food scientist) or **"Beginner User"** (product manager).

---

### 2. Project Dashboard
After signing in, you will be taken to the Dashboard. Here, you will find:
* **Overall Formulation Analytics**: Quick stats showing the total number of projects, generated formulations, and compliance validations.
* **Active Projects List**: A chronological table of your ongoing food development products (e.g. Gluten-Free Bread). Clicking on a project opens its active formulation history.
* **Pre-seeded Sample Project**: The database comes pre-populated with a sample *"Gluten-Free Sandwich Bread"* project so that the charts and compliance metrics are visible immediately.

---

### 3. Guided Formulator (AI Stepper)
This wizard directs you step-by-step through generating a new formulation using the AI RAG workflow:

```
Step 1: Category Selection (Beverage, Bakery, Snack, etc.)
               │
               ▼
Step 2: Dietary Constraints (Vegan, Gluten-Free, Low-Sugar, Allergen Exclusions)
               │
               ▼
Step 3: Nutrient Targets (Set target grams for Protein, Fats, Carbs per 100g)
               │
               ▼
Step 4: AI Generation (Sends parameters to LLaMA 3.3 and builds initial recipe)
```

1. Click **"New Formulation"** or go to `/dashboard/formulate/guided`.
2. Select your product category and write a short description (e.g. *"High-protein vegan cocoa drink"*).
3. Toggle dietary restrictions. If you select **"Vegan"**, the RAG search filter will prevent the AI from retrieving animal-derived ingredients (milk, eggs, gelatin).
4. Set nutrient target range sliders.
5. Click **"Generate Formulation"**. The RAG pipeline will filter ingredients, invoke LLaMA 3.3, parse the recipe text into a structured dataset, evaluate compliance, and render the results screen.

---

### 4. Expert Canvas (Live Editor & Sliders)
Designed for food scientists, the Expert Canvas offers fine-grained manual control over the recipe composition.

* **Interactive Composition Sliders**: Every ingredient in the formulation has a slider showing its weight percentage. Adjusting a slider automatically updates the other ingredients and locks in a total sum of exactly **100%**.
* **Live Nutritional Panel**: As you adjust ingredient percentages, the system re-calculates the macronutrient composition (Protein, Fat, Carbohydrates, Calories) in real time using the USDA nutrition profiles.
* **Real-time Compliance Panel**: Audits the recipe instantly against three regulatory regions:
  * **FDA (US)**: Warns if sweetener limits are exceeded or allergens are detected.
  * **EFSA (Europe)**: Flags safety limits, E-number food additives, or allergen labeling guidelines.
  * **FSSAI (India)**: Evaluates regional food standard criteria.
* **Version Save**: Save your tweaked recipe as a new iteration (e.g., V1.1, V1.2) under the current project.

---

### 5. Ingredient Pantry (USDA Search)
Use the pantry workspace to manage the system's available raw materials:
* **Search Ingredient Library**: Search for bulk and functional ingredients.
* **USDA Nutrient Query**: View exact nutritional values (calories, protein, fats, fibers) mapped to USDA database codes.
* **Add Custom Ingredients**: Input custom ingredients with their cost per kg and nutritional composition to be used in future AI generations or manual expert canvas formulations.

---

## 📁 Directory Code Map

Here is a map of the important code files in the repository:

```
Food web App/
│
├── backend/                   # FastAPI Backend
│   ├── main.py                # Main API coordinator and routes
│   ├── models.py              # SQLAlchemy database tables (User, Project, Formulation, etc.)
│   ├── schemas.py             # Pydantic validation schemas
│   ├── compliance.py          # Rule-based FDA, EFSA, FSSAI compliance logic
│   ├── rag_engine.py          # LangGraph recipe generation + Groq prompt engineering
│   ├── database.py            # SQLite/PostgreSQL connection engine
│   ├── food_ingredients_clean.csv # Clean ingredient reference dataset
│   └── requirements.txt       # Backend python package lists
│
├── frontend/                  # Next.js Frontend
│   ├── src/app/               # Web application router pages
│   │   ├── page.tsx           # Product landing page
│   │   ├── login/page.tsx     # Session sign-in
│   │   ├── dashboard/page.tsx # Central dashboard layout
│   │   └── dashboard/formulate/expert/page.tsx # Live slider canvas
│   ├── src/components/        # Reusable Tailwind UI components
│   └── package.json           # Node dependency configuration
│
├── docker-compose.yml         # Containerized services orchestrator
├── nginx.conf                 # Nginx proxy mapping routes on Port 80
└── start_dev.ps1              # Local development launcher script (PowerShell)
```

---

## ❓ Troubleshooting & FAQ

### Q1: The formulation generation gets stuck or returns a `500 Server Error`
**A:** This is almost always caused by a missing or invalid `GROQ_API_KEY` in [backend/.env](file:///backend/.env).
1. Open the [backend/.env](file:///backend/.env) file.
2. Verify that `GROQ_API_KEY` is not empty and is a valid key from your Groq console.
3. Restart the backend server.

### Q2: I get an execution policy error when running `start_dev.ps1`
**A:** Windows restricts running scripts by default. You can bypass this restriction for the session by running:
```powershell
powershell -ExecutionPolicy Bypass -File start_dev.ps1
```
Alternatively, open PowerShell as an administrator and run:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q3: How do I change the database from SQLite to PostgreSQL?
**A:** 
* **If running via Docker Compose**: The stack automatically configures PostgreSQL (`tf_postgres`) as the default database. You do not need to do anything.
* **If running manually**: Install PostgreSQL locally, create a database, and update the `DATABASE_URL` in [backend/.env](file:///backend/.env):
  ```bash
  DATABASE_URL=postgresql://your_username:your_password@localhost:5432/your_database_name
  ```

### Q4: Nginx fails to start due to port 80 being in use
**A:** Port 80 is sometimes used by other server software or IIS on Windows. You can change Nginx's external port in [docker-compose.yml](file:///docker-compose.yml):
```yaml
  nginx:
    # ...
    ports:
      - "8080:80"  # Change "80:80" to "8080:80"
```
You can then access the application at `http://localhost:8080`.
