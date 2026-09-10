# 🚀 TCS Food Formulator - local Development Run & Usage Guide

This guide details how to configure, start, and run the **TCS Food Formulator** application locally using **PowerShell** commands (without Docker).

---

## ⚙️ 1. Environment & API Configuration

Before running the services, you must configure the backend environment file with your credentials (specifically the Groq API key).

1. Open a PowerShell window and navigate to the `backend` folder:
   ```powershell
   cd backend
   ```
2. Copy the environment configuration template:
   ```powershell
   Copy-Item .env.example .env
   ```
3. Open the newly created `backend/.env` file in Notepad or VS Code and set your Groq API key:
   ```env
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```
   *(Note: Leave `DATABASE_URL` empty to automatically default to a local SQLite database).*

---

## 🛠️ 2. PowerShell Run Commands

To run the application, you must start the backend API and the frontend Next.js server in **two separate PowerShell terminals**.

### Terminal 1: Run the Backend API
Navigate to the root directory `Food Web App Core` in a new PowerShell window, then execute:

```powershell
# 1. Navigate to the backend directory
cd backend

# 2. Set up the Python virtual environment
python -m venv venv

# 3. Choose ONE of the following methods to install dependencies and run:

# --- METHOD A (Recommended - completely avoids script execution errors) ---
# Run directly using the virtual environment's executables (no activation needed):
.\venv\Scripts\pip.exe install -r requirements.txt
.\venv\Scripts\uvicorn.exe main:app --reload --host 0.0.0.0 --port 8000

# --- METHOD B (Alternative - requires changing PowerShell policy) ---
# Bypass execution policy for this terminal session, activate venv, and run:
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
*Keep this terminal open. The backend API is now running at **http://localhost:8000**.*

---

### Terminal 2: Run the Frontend Next.js Web App
Open a **SECOND** separate PowerShell window and navigate to the `Food Web App Core` root directory:

```powershell
# 1. Navigate to the frontend directory
cd frontend

# 2. Install Node.js frontend dependencies
npm install

# 3. Start the Next.js development server
npm run dev
```
*Keep this terminal open. The frontend web portal is now running at **http://localhost:3000**.*

---

## 🔑 3. Accessing the Application

Once both terminals are running, open your web browser and navigate to:

* **Frontend Web Application**: [http://localhost:3000](http://localhost:3000)
* **Backend Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Default Login Credentials
* **Email**: `admin@tcs.com`
* **Password**: `admin123`


---

## 🌟 4. Core Features Walkthrough

### A. Dashboard View
Displays total formulation metrics, ongoing product lists, and quick shortcuts. You can see a seeded *"Gluten-Free Sandwich Bread"* project immediately on login.

### B. Guided Formulator (AI-Stepping Assistant)
Navigate to **Formulate** -> **Guided Formulator** in the menu:
1. Select food category (Beverage, Bakery, Snack, Dairy, etc.) and write a brief description.
2. Toggle dietary rules (such as checking **Vegan** to filter out animal-product ingredients in the search database).
3. Set your target protein, fat, carbohydrates, and calorie metrics.
4. Click **Generate** to call the AI RAG engine and render the results dashboard.

### C. Expert Canvas (Manual & Live Formulation)
Navigate to **Expert Formulator** to adjust recipe fractions manually:
1. Drag sliders to adjust ingredient percentages. The canvas will validate that they sum to exactly 100%.
2. View the **Live Nutrition Panel** recalculating calories, protein, and other nutrient profiles in real time.
3. Read the **Compliance Warnings** highlighting violations against **FDA**, **EFSA**, or **FSSAI** guidelines.

### D. Ingredient Pantry
Search raw materials, query USDA database items, and add custom entries with cost metrics.

---

## ❌ 5. Common Troubleshooting

* **FastAPI Backend displays 500 error on formulation generation:**
  * **Cause:** Missing or expired `GROQ_API_KEY` in `backend/.env`.
  * **Solution:** Create the key on [Groq Console](https://console.groq.com/) and verify it is correctly configured in your `backend/.env` file, then restart Terminal 1.
* **Powershell throws script execution warnings:**
  * **Solution:** If running `.ps1` files triggers permissions errors, run PowerShell as Administrator and execute:
    ```powershell
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```
