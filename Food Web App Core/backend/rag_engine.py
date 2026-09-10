# Auto-reload trigger: Groq API Key updated in env
import os
import re
import time
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple, Optional
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.documents import Document as LCDocument
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict

# Load backend-specific environmental configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, '.env'))

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
USDA_API_KEY = os.getenv("USDA_API_KEY", "DEMO_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")

ALL_FUNCTIONAL_ROLES = [
    "Protein Source",
    "Bulking Agent",
    "Emulsifier",
    "Stabilizer",
    "Sweetener",
    "Flavor System",
    "Acidity Control",
    "Preservation",
]

class AgentState(TypedDict):
    query: str
    context_docs: List[LCDocument]
    raw_response: str

# Lazy load references
_embeddings = None
_vector_store = None
_llm = None
_fallback_llm = None

def get_embeddings():
    global _embeddings
    if not _embeddings:
        _embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return _embeddings

class InMemoryVectorStore:
    def __init__(self, documents: List[LCDocument], embeddings: HuggingFaceEmbeddings):
        self.documents = documents
        self.embeddings = embeddings
        texts = [d.page_content for d in documents]
        self.doc_embeddings = np.array(self.embeddings.embed_documents(texts))

    def _cosine_search(self, query: str, k: int, role_filter: Optional[str] = None) -> List[LCDocument]:
        q_emb = np.array(self.embeddings.embed_query(query))

        if role_filter:
            indices = [i for i, d in enumerate(self.documents)
                       if d.metadata.get("functional_role") == role_filter]
            if not indices:
                indices = list(range(len(self.documents)))
        else:
            indices = list(range(len(self.documents)))

        sub_embs = self.doc_embeddings[indices]
        dots = sub_embs @ q_emb
        norms = np.linalg.norm(sub_embs, axis=1) * np.linalg.norm(q_emb) + 1e-9
        sims = dots / norms
        top_k = np.argsort(sims)[::-1][:k]
        return [self.documents[indices[i]] for i in top_k]

    def category_aware_search(self, query: str, k_per_role: int = 2) -> List[LCDocument]:
        results: List[LCDocument] = []
        seen_names: set = set()
        for role in ALL_FUNCTIONAL_ROLES:
            role_docs = self._cosine_search(query, k=k_per_role, role_filter=role)
            for doc in role_docs:
                name = doc.metadata.get("name", "")
                if name not in seen_names:
                    results.append(doc)
                    seen_names.add(name)
        return results

def get_vector_store():
    global _vector_store
    if not _vector_store:
        csv_path = os.path.join(script_dir, "food_ingredients_clean.csv")
        if not os.path.exists(csv_path):
            # Create a backup csv in case it is run from another directory context
            raise FileNotFoundError(f"Clean ingredients database not found at: {csv_path}")
        df = pd.read_csv(csv_path)
        docs = []
        for _, row in df.iterrows():
            page_content = (
                f"Ingredient Name: {row['name']}\n"
                f"Category: {row['category']}\n"
                f"Functional Role: {row['functional_role']}\n"
                f"Allergen: {row['allergen']}\n"
                f"Protein: {row['protein']} g per 100g\n"
                f"Fat: {row['fat']} g per 100g\n"
                f"Carbohydrates: {row['carbs']} g per 100g\n"
                f"Calories: {row['calories']} kcal per 100g\n"
                f"Use cases: This ingredient is commonly used as a {row['functional_role'].lower()} "
                f"in food formulations."
            )
            metadata = {
                "name": str(row["name"]),
                "category": str(row["category"]),
                "functional_role": str(row["functional_role"]),
                "allergen": str(row["allergen"]),
                "protein": float(row["protein"]),
                "fat": float(row["fat"]),
                "carbs": float(row["carbs"]),
                "calories": float(row["calories"]),
            }
            docs.append(LCDocument(page_content=page_content, metadata=metadata))
        
        _vector_store = InMemoryVectorStore(docs, get_embeddings())
    return _vector_store

def get_llms():
    global _llm, _fallback_llm
    if not _llm:
        # Check API key presence
        if not GROQ_API_KEY:
            print("[WARNING] GROQ_API_KEY is not defined. API requests will fail.")
        
        try:
            _llm = ChatGroq(
                model_name="llama-3.3-70b-versatile",
                temperature=0.1,
                groq_api_key=GROQ_API_KEY,
            )
        except Exception:
            # Fallback immediately to standard model if initializer fails
            _llm = ChatGroq(
                model_name="llama-3.1-8b-instant",
                temperature=0.1,
                groq_api_key=GROQ_API_KEY,
            )
            
        _fallback_llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            temperature=0.1,
            groq_api_key=GROQ_API_KEY,
        )
    return _llm, _fallback_llm

def retrieve_node(state: AgentState) -> Dict[str, Any]:
    query = state["query"]
    store = get_vector_store()
    docs = store.category_aware_search(query, k_per_role=2)
    return {"context_docs": docs}

SYSTEM_PROMPT = """\
You are a Senior Food Scientist at TCS Research designing formulation reports for clients.
Generate a recipe formulation report in the EXACT plain-text format below.
Rules:
  1. All percentages must sum to exactly 100.00%.
  2. Use ONLY ingredients from the provided context list.
  3. Allergen filtering: if the query says vegan, exclude Milk/Egg. If gluten-free, exclude Gluten.
  4. Calculate Protein (g), Sugar (g), and Calories (kcal) from the formulation percentages and
     the per-100g macros supplied in the ingredient context.
     Formula: macro_contribution = (ingredient_concentration_pct / 100) * ingredient_macro_per_100g
     Sum contributions from all ingredients for total macros.
  5. Output raw plain text ONLY — no markdown, no asterisks, no backticks.

Format Template:
====================================================================
TCS FOOD FORMULATOR – GENERATED FORMULATION REPORT
Constraint-Driven Multi-Objective Recipe Generation
====================================================================

Recipe ID      : <e.g. CHOC_BEV_001>
Recipe Name    : <Descriptive Name>
Category       : <Product Category>
Version        : V1.0

====================================================================
1. COMPLETE FORMULATION COMPOSITION
====================================================================

BULK INGREDIENTS
--------------------------------------------------------------------
Ingredient                     Category           Conc. (%)

<Ingredient 1>                 <Category>         <XX.XX>
<Ingredient 2>                 <Category>         <XX.XX>

Subtotal (Bulk)                                   <XX.XX> %

--------------------------------------------------------------------

FUNCTIONAL INGREDIENTS
--------------------------------------------------------------------
Ingredient                     Functional Role    Conc. (%)

<Ingredient 1>                 <Role>             <XX.XX>
<Ingredient 2>                 <Role>             <XX.XX>

Subtotal (Functional)                              <XX.XX> %

====================================================================
TOTAL FORMULATION = 100.00 %
====================================================================

====================================================================
2. FUNCTIONAL ROLE COVERAGE
====================================================================

Role                     Ingredient               Coverage

Protein Source           <Ingredient>              [YES/NO]
Bulking Agent            <Ingredient>              [YES/NO]
Emulsifier               <Ingredient>              [YES/NO]
Stabilizer               <Ingredient>              [YES/NO]
Sweetener                <Ingredient>              [YES/NO]
Flavor System            <Ingredient>              [YES/NO]
Acidity Control          <Ingredient>              [YES/NO]
Preservation             <Ingredient>              [YES/NO]

Functional Completeness Score (FCS): <XX.X> % (<X>/8 roles covered)
Assessment: <FUNCTIONALLY COMPLETE (>=90%) / NEEDS REVIEW (<90%)>

====================================================================
3. PRODUCT PERFORMANCE PREDICTION
====================================================================

Protein                 : <XX.X> g / 100g product
Total Fat               : <XX.X> g / 100g product
Carbohydrates           : <XX.X> g / 100g product
Calories                : <XXX> kcal / 100g product

Texture                 : <Description>
Mouthfeel               : <Description>
Viscosity               : <Description>
Shelf-life              : ~<X> months

====================================================================
4. PROCESS RECOMMENDATION
====================================================================

STEP 1: <Description>
STEP 2: <Description>
STEP 3: <Description>
STEP 4: Homogenization: <RPM> rpm x <duration> min
STEP 5: Heat treatment: <temp>C x <duration> sec

====================================================================
FINAL STATUS
====================================================================

Recipe Status: READY FOR VIRTUAL VALIDATION
====================================================================
"""

def generate_node(state: AgentState) -> Dict[str, Any]:
    query = state["query"]
    docs = state["context_docs"]

    context_lines = []
    for i, doc in enumerate(docs, 1):
        m = doc.metadata
        context_lines.append(
            f"[{i}] Name: {m['name']} | Role: {m['functional_role']} | "
            f"Protein: {m['protein']}g | Fat: {m['fat']}g | "
            f"Carbs: {m['carbs']}g | Calories: {m['calories']} kcal | "
            f"Allergen: {m['allergen']}"
        )
    context_str = "\n".join(context_lines)

    user_msg = (
        f"Product Request: {query}\n\n"
        f"Available Ingredients (use ONLY these):\n{context_str}\n\n"
        f"Generate the formulation report now."
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_msg),
    ]

    primary, fallback = get_llms()
    try:
        response = primary.invoke(messages)
    except Exception as e:
        print(f"[RAG ENGINE] Primary Groq LLM failed: {e}. Falling back...")
        response = fallback.invoke(messages)

    return {"raw_response": response.content}

def build_graph() -> Any:
    graph = StateGraph(AgentState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()


def parse_formulation_report(report_text: str) -> Dict[str, Any]:
    """
    Parses the plain text generated output of the Groq LLM formulation
    report and structures it into structured JSON representation.
    """
    data = {
        "recipe_id": "REC_GEN_001",
        "recipe_name": "AI Formulation Project",
        "category": "General",
        "composition": {
            "bulk_ingredients": [],
            "functional_ingredients": []
        },
        "functional_coverage": {
            "roles": {},
            "completeness_score": 0.0,
            "assessment": "NEEDS REVIEW"
        },
        "performance_prediction": {
            "protein": 0.0,
            "fat": 0.0,
            "carbohydrates": 0.0,
            "calories": 0.0,
            "texture": "N/A",
            "mouthfeel": "N/A",
            "viscosity": "N/A",
            "shelf_life": 6
        },
        "process_recommendations": [],
        "status": "DRAFT"
    }

    try:
        # Extract ID, Name, Category
        id_match = re.search(r"Recipe ID\s*:\s*([^\n]+)", report_text)
        name_match = re.search(r"Recipe Name\s*:\s*([^\n]+)", report_text)
        cat_match = re.search(r"Category\s*:\s*([^\n]+)", report_text)
        
        if id_match: data["recipe_id"] = id_match.group(1).strip()
        if name_match: data["recipe_name"] = name_match.group(1).strip()
        if cat_match: data["category"] = cat_match.group(1).strip()

        # Parse Composition: Bulk
        bulk_block = re.search(
            r"BULK INGREDIENTS\s*[-]+\s*Ingredient\s+Category\s+Conc\.\s*\(\%\)\s*(.*?)(?=-{10,}|FUNCTIONAL INGREDIENTS)", 
            report_text, re.DOTALL | re.IGNORECASE
        )
        if bulk_block:
            lines = bulk_block.group(1).strip().split("\n")
            for line in lines:
                if not line.strip() or "Subtotal" in line:
                    continue
                # Split by double spaces or tab characters
                parts = [p.strip() for p in re.split(r"\s{2,}", line) if p.strip()]
                if len(parts) >= 3:
                    try:
                        conc_pct = float(re.sub(r"[^\d\.]", "", parts[2]))
                        data["composition"]["bulk_ingredients"].append({
                            "name": parts[0],
                            "category": parts[1],
                            "percentage": conc_pct
                        })
                    except ValueError:
                        pass

        # Parse Composition: Functional
        func_block = re.search(
            r"FUNCTIONAL INGREDIENTS\s*[-]+\s*Ingredient\s+(?:Functional Role|Category)\s+Conc\.\s*\(\%\)\s*(.*?)(?=-{10,}|TOTAL FORMULATION|=)", 
            report_text, re.DOTALL | re.IGNORECASE
        )
        if func_block:
            lines = func_block.group(1).strip().split("\n")
            for line in lines:
                if not line.strip() or "Subtotal" in line:
                    continue
                parts = [p.strip() for p in re.split(r"\s{2,}", line) if p.strip()]
                if len(parts) >= 3:
                    try:
                        conc_pct = float(re.sub(r"[^\d\.]", "", parts[2]))
                        data["composition"]["functional_ingredients"].append({
                            "name": parts[0],
                            "functional_role": parts[1],
                            "percentage": conc_pct
                        })
                    except ValueError:
                        pass

        # Parse Functional Role Coverage Roles
        coverage_block = re.search(
            r"2\.\s*FUNCTIONAL\s*ROLE\s*COVERAGE\s*=+\s*Role\s+Ingredient\s+Coverage\s*(.*?)(?==+|Functional Completeness Score)",
            report_text, re.DOTALL | re.IGNORECASE
        )
        if coverage_block:
            lines = coverage_block.group(1).strip().split("\n")
            for line in lines:
                if not line.strip():
                    continue
                parts = [p.strip() for p in re.split(r"\s{2,}", line) if p.strip()]
                if len(parts) >= 2:
                    role = parts[0]
                    ing_with_cov = parts[1]
                    # Check if YES/NO is appended at the end
                    cov_yes = "YES" in line.upper()
                    # Clean ingredient name (strip YES/NO)
                    ing_name = re.sub(r"\s+\[?YES\]?$", "", ing_with_cov, flags=re.IGNORECASE).strip()
                    ing_name = re.sub(r"\s+\[?NO\]?$", "", ing_name, flags=re.IGNORECASE).strip()
                    if cov_yes and ing_name and ing_name.lower() != "none" and ing_name.lower() != "n/a":
                        data["functional_coverage"]["roles"][role] = ing_name

        # Parse FCS Score & Assessment
        fcs_match = re.search(r"Functional Completeness Score\s*\(FCS\):\s*([\d\.]+)\s*%", report_text, re.IGNORECASE)
        assess_match = re.search(r"Assessment:\s*([^\n]+)", report_text, re.IGNORECASE)
        if fcs_match:
            data["functional_coverage"]["completeness_score"] = float(fcs_match.group(1))
        if assess_match:
            data["functional_coverage"]["assessment"] = assess_match.group(1).strip()

        # Parse Performance Predictions
        prot_match = re.search(r"Protein\s*:\s*([\d\.]+)\s*g", report_text, re.IGNORECASE)
        fat_match = re.search(r"Total Fat\s*:\s*([\d\.]+)\s*g", report_text, re.IGNORECASE)
        carb_match = re.search(r"Carbohydrates\s*:\s*([\d\.]+)\s*g", report_text, re.IGNORECASE)
        cal_match = re.search(r"Calories\s*:\s*([\d\.]+)\s*kcal", report_text, re.IGNORECASE)
        
        if prot_match: data["performance_prediction"]["protein"] = float(prot_match.group(1))
        if fat_match: data["performance_prediction"]["fat"] = float(fat_match.group(1))
        if carb_match: data["performance_prediction"]["carbohydrates"] = float(carb_match.group(1))
        if cal_match: data["performance_prediction"]["calories"] = float(cal_match.group(1))

        tex_match = re.search(r"Texture\s*:\s*([^\n]+)", report_text, re.IGNORECASE)
        mouth_match = re.search(r"Mouthfeel\s*:\s*([^\n]+)", report_text, re.IGNORECASE)
        visc_match = re.search(r"Viscosity\s*:\s*([^\n]+)", report_text, re.IGNORECASE)
        shelf_match = re.search(r"Shelf-life\s*:\s*~?([\d]+)", report_text, re.IGNORECASE)

        if tex_match: data["performance_prediction"]["texture"] = tex_match.group(1).strip()
        if mouth_match: data["performance_prediction"]["mouthfeel"] = mouth_match.group(1).strip()
        if visc_match: data["performance_prediction"]["viscosity"] = visc_match.group(1).strip()
        if shelf_match: data["performance_prediction"]["shelf_life"] = int(shelf_match.group(1))

        # Parse processing steps
        steps = re.findall(r"STEP \d+:\s*([^\n]+)", report_text)
        if steps:
            data["process_recommendations"] = [step.strip() for step in steps]
        else:
            # Fallback parsing in case of formatting anomalies
            lines = report_text.split("\n")
            for line in lines:
                if line.strip().upper().startswith("STEP"):
                    data["process_recommendations"].append(line.split(":", 1)[-1].strip())

        # Status
        status_match = re.search(r"Recipe Status:\s*([^\n]+)", report_text, re.IGNORECASE)
        if status_match:
            data["status"] = status_match.group(1).strip()

    except Exception as e:
        print(f"[RAG ENGINE] Error parsing formulation plain-text: {e}")

    # Final calculations sanity checks - if totals list is empty but LLM parsed something, double check
    return data
