# 🍔 The TCS Food Formulator — A Simple Explanation

Welcome! If you are not a software engineer, this document is for you. It explains how the **TCS Food Formulator** works behind the scenes using simple real-world analogies. 

Think of this system as a **Smart Digital Kitchen** that helps food companies and scientists design new food recipes (like a vegan chocolate beverage or gluten-free bread), calculate their nutritional value, and automatically check if they follow health and food safety rules.

---

## 🍽️ The Restaurant Analogy: How the System is Organized

To understand how the code files work together, let's imagine a modern restaurant:

```
                  ┌───────────────────────────────┐
                  │      Traffic Controller       │
                  │            (Nginx)            │
                  └───────────────┬───────────────┘
                                  │
                 ┌────────────────┴────────────────┐
                 ▼                                 ▼
       ┌───────────────────┐             ┌───────────────────┐
       │   The Dining Room │             │    The Kitchen    │
       │    (Frontend UI)  │             │   (Backend API)   │
       └───────────────────┘             └─────────┬─────────┘
                                                   │
                        ┌──────────────────────────┼──────────────────────────┐
                        ▼                          ▼                          ▼
             ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
             │  The Recipe Analyst │    │  Quality Inspector  │    │    The Warehouse    │
             │     (AI Engine)     │    │ (Compliance Engine) │    │     (Database)      │
             └─────────────────────┘    └─────────────────────┘    └─────────────────────┘
```

### 1. The Traffic Controller (Nginx)
When a customer approaches the restaurant, a host stands at the door to direct them. 
* **In this App:** [nginx.conf](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/nginx.conf) is the host. It listens on the main web address (Port 80) and sends requests to the right place: if you want to look at the screen, it sends you to the **Dining Room** (Frontend); if you ask for recipe generation or compliance checking, it sends you to the **Kitchen** (Backend).

### 2. The Dining Room (Frontend / Customer Screen)
This is what the user sees and interacts with. It contains tables, buttons, sliders, and charts.
* **In this App:** The [frontend/](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/frontend) folder is the dining room. It is built using **Next.js** (a tool for building modern websites) and styled with **Tailwind CSS**. 
* **Key Areas in the Dining Room:**
  * **The Host Desk (Login/Registration):** Where users sign in ([login page](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/frontend/src/app/login/page.tsx) and [register page](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/frontend/src/app/register/page.tsx)).
  * **The Main Dashboard:** Shows general statistics, ongoing projects, and alert messages ([dashboard page](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/frontend/src/app/dashboard/page.tsx)).
  * **Guided Assistant (For Beginners):** A wizard that guides users step-by-step to input what kind of food they want to make ([guided formulator](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/frontend/src/app/dashboard/formulate/guided/page.tsx)).
  * **Expert Canvas (For Food Scientists):** A workspace where scientists drag and drop ingredients, slide sliders to change ingredient percentages, and see nutrient numbers calculate in real-time ([expert formulator](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/frontend/src/app/dashboard/formulate/expert/page.tsx)).
  * **Ingredient Pantry:** A searchable library of ingredients with their USDA nutrients ([ingredients page](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/frontend/src/app/dashboard/ingredients/page.tsx)).

### 3. The Kitchen (Backend / Core Logic)
This is where the actual cooking, calculations, and thinking happen. The user never sees the kitchen directly, but they receive the "dishes" (data) cooked here.
* **In this App:** The [backend/](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend) folder is the kitchen. It is built with **FastAPI**, a Python-based tool designed to serve data quickly.
* The main hub in the kitchen is [main.py](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/main.py). It acts as the head chef, receiving orders from the frontend, delegating work to the AI Engine and Safety Inspector, and saving recipes.

### 4. The Recipe Analyst (AI RAG Engine)
When a user asks for a recipe like *"Generate a vegan high-protein chocolate beverage"*, the kitchen asks the **Recipe Analyst** to write it.
* **In this App:** This is [rag_engine.py](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/rag_engine.py). It uses a technique called **RAG** (Retrieval-Augmented Generation):
  1. **Retrieval (Open-book Search):** First, it searches a catalog of clean ingredients ([food_ingredients_clean.csv](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/food_ingredients_clean.csv)) for things related to the request. It filters out allergens (like milk or egg for a vegan request, or wheat for a gluten-free request).
  2. **Generation (Writing the Report):** Next, it hands those ingredients to a smart AI Brain (**LLaMA 3.3** hosted on a service called **Groq**). The AI writes a detailed recipe report containing:
     * Ingredient percentages (adding up to exactly 100%).
     * Coverage of key roles (protein source, sweetener, stabilizer, etc.).
     * Nutrition predictions (protein, fat, carbs, calories).
     * Processing instructions (how fast to blend, what temperature to heat it to).
  3. **Translation (Parsing):** Finally, it translates the text report into structured computer data (JSON) so the frontend can display it in neat tables and graphs.

### 5. The Food Safety Inspector (Compliance Engine)
Before a recipe is allowed out of the kitchen, it must pass a safety audit.
* **In this App:** This is [compliance.py](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/compliance.py). It reviews the recipe against food rules in three major regions:
  * **FDA** (United States)
  * **EFSA** (Europe)
  * **FSSAI** (India)
* **What it looks for:**
  * Did a *Vegan* recipe accidentally include egg or milk? (If yes $\rightarrow$ **Failed**)
  * Did a *Gluten-Free* recipe include gluten? (If yes $\rightarrow$ **Failed**)
  * Are there too many preservatives? (More than 0.1% $\rightarrow$ **Warning**)
  * Is the artificial sweetener concentration too high? (More than 0.05% $\rightarrow$ **Warning**)

### 6. The Warehouse (Database)
A restaurant needs a cellar or pantry to store customer receipts, staff logs, and dry inventory.
* **In this App:** The database stores information in structured "filing cabinets" (tables) managed by [database.py](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/database.py) and [models.py](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/models.py):
  * **Users Table:** Stores names, emails, passwords (securely hashed), and roles (e.g., Expert vs. Beginner).
  * **Projects Table:** Stores the folder name, category, and prompt query for each food product you are developing.
  * **Formulations Table:** Stores the recipe ingredients, percentages, nutrients, and step-by-step instructions for each version (e.g. V1.0, V1.1).
  * **Compliance Logs Table:** Stores the results of the FDA, EFSA, and FSSAI safety checks.
* **Database Engine:** In the development version, we use a simple file-based database called **SQLite** ([tcs_food_formulator.db](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/tcs_food_formulator.db)). When deployed in production, it automatically connects to a heavy-duty database system called **PostgreSQL**.

### 7. The Shipping Crates (Docker Containerization)
How do we ensure that the restaurant runs identically, whether it is set up in New York, London, or Mumbai?
* **In this App:** We pack the components into "Docker containers" (virtual software crates). 
  * The [docker-compose.yml](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/docker-compose.yml) file acts as the shipping manifest. It coordinates four crates:
    1. **`postgres`:** The storage warehouse.
    2. **`backend`:** The kitchen logic.
    3. **`frontend`:** The dining room screen.
    4. **`nginx`:** The traffic router.
  * By running one command (`docker-compose up`), all four containers start, connect to each other, and run in perfect harmony.

---

## 🔄 The Journey of a Request: Step-by-Step

Here is exactly what happens when you type *"I want a vegan chocolate protein shake"* and click **Generate**:

```
 ┌───┐                  ┌───┐                 ┌───┐                 ┌─────────┐
 │   │ -- 1. Request -> │   │ -- 2. Route --> │   │ -- 3. Search -> │ Vector  │
 │   │                  │   │                 │   │                 │ Store   │
 │   │                  │   │                 │   │                 └────┬────┘
 │ U │                  │ N │                 │ B │                      │
 │ S │                  │ G │                 │ A │                      │ 4. Ingredients
 │ E │                  │ I │                 │ C │                      ▼
 │ R │                  │ N │                 │ K │                 ┌─────────┐
 │   │                  │ X │                 │ E │                 │ Groq LLM│
 │   │                  │   │                 │ N │                 │ (AI)    │
 │   │                  │   │                 │ D │                 └────┬────┘
 │   │                  │   │                 │   │                      │
 │   │                  │   │                 │   │                      │ 5. Recipe text
 │   │                  │   │                 │   │                      ▼
 │   │                  │   │                 │   │                 ┌─────────┐
 │   │                  │   │                 │   │ < - 6. Parse -- │ Parser  │
 │   │                  │   │                 │   │                 └─────────┘
 │   │                  │   │                 │   │
 │   │                  │   │                 │   │ -- 7. Check --> ┌─────────┐
 │   │                  │   │                 │   │                 │ Compl.  │
 │   │                  │   │                 │   │                 │ Engine  │
 │   │                  │   │                 │   │                 └────┬────┘
 │   │                  │   │                 │   │                      │
 │   │                  │   │                 │   │                      │ 8. Audit logs
 │   │                  │   │                 │   │                      ▼
 │   │                  │   │                 │   │ -- 9. Save ---> ┌─────────┐
 │   │                  │   │                 │   │                 │ Database│
 │   │                  │   │                 │   │                 └────┬────┘
 │   │                  │   │                 │   │                      │
 │   │ < - 11. Render - │   │ < - 10. Data -- │   │ <─── 10. Done ───────┘
 └───┘                  └───┘                 └───┘
```

1. **You make a request:** You fill out your constraints (e.g. check "Vegan", set protein slider to 20g) on the [guided stepper website](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/frontend/src/app/dashboard/formulate/guided/page.tsx) and click **"Generate Formulation"**.
2. **Nginx routes it:** The request goes to [nginx.conf](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/nginx.conf), which recognizes the `/api/formulate` URL and forwards it to the Python backend in [main.py](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/main.py).
3. **AI Engine Retrieves Ingredients:** The backend starts the AI Graph workflow inside [rag_engine.py](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/rag_engine.py). It reads the clean ingredients CSV file and selects the best ingredients matching your product request (filtering out animal products like milk or egg since you checked "Vegan").
4. **AI Engine Generates Recipe:** The selected ingredients are formatted and sent to the **LLaMA 3.3 AI Model** via Groq. The AI model carefully drafts a text-based recipe report matching all parameters.
5. **Parser Structures Recipe:** The backend takes the plain text report generated by the AI and uses search patterns (regular expressions) in [rag_engine.py:L309](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/rag_engine.py#L309) to convert it into structured columns and clean numbers.
6. **Safety Check:** The structured recipe is passed to [compliance.py](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/compliance.py) which cross-references ingredients and percentages against FDA, EFSA, and FSSAI rulebooks, generating a compliance report status (**Passed**, **Warning**, or **Failed**).
7. **Saved to Database:** The backend saves the recipe version and safety logs to the database file ([tcs_food_formulator.db](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/tcs_food_formulator.db)) via [database.py](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/database.py).
8. **Displayed on Screen:** The backend sends the recipe data and compliance status back through Nginx to the website. The [formulation-results.tsx](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/frontend/src/components/formulation-results.tsx) component renders colorful composition charts, calorie predictions, and compliance check alert cards.

---

## 🛠️ Code Map (For Technical Users)

If you are a developer looking to edit the project, here is how the folders map to the Restaurant Analogy:

* **The Face / UI:**
  * `frontend/src/app/` $\rightarrow$ Web routing pages
    * [page.tsx](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/frontend/src/app/page.tsx) $\rightarrow$ Landing landing page
    * [dashboard/page.tsx](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/frontend/src/app/dashboard/page.tsx) $\rightarrow$ Central control dashboard
    * [dashboard/formulate/guided/page.tsx](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/frontend/src/app/dashboard/formulate/guided/page.tsx) $\rightarrow$ Guided user wizard
    * [dashboard/formulate/expert/page.tsx](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/frontend/src/app/dashboard/formulate/expert/page.tsx) $\rightarrow$ Live formula editor
  * `frontend/src/components/` $\rightarrow$ UI components
    * [formulation-results.tsx](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/frontend/src/components/formulation-results.tsx) $\rightarrow$ Nutrients, instructions, and compliance output UI
  * `frontend/src/store/` $\rightarrow$ Shared browser state
    * [useStore.ts](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/frontend/src/store/useStore.ts) $\rightarrow$ Store for saving logins and active recipes

* **The Logic / Backend:**
  * `backend/` $\rightarrow$ Core python services
    * [main.py](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/main.py) $\rightarrow$ API routing and central coordinator
    * [rag_engine.py](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/rag_engine.py) $\rightarrow$ Vector search and LangGraph AI agent logic
    * [compliance.py](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/compliance.py) $\rightarrow$ Compliance safety checking rules
    * [database.py](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/database.py) $\rightarrow$ Database connection settings
    * [models.py](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/models.py) $\rightarrow$ SQL table structures
    * [schemas.py](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/schemas.py) $\rightarrow$ Network request input/output definitions
    * [food_ingredients_clean.csv](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/backend/food_ingredients_clean.csv) $\rightarrow$ Clean ingredient pantry file

* **Deployment Configuration:**
  * [docker-compose.yml](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/docker-compose.yml) $\rightarrow$ Coordinates all service containers
  * [nginx.conf](file:///c:/Users/asus/.gemini/antigravity/scratch/Food%20web%20App/nginx.conf) $\rightarrow$ Proxy traffic routing rules
