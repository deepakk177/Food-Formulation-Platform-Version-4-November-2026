# Auto-reload trigger: Full API & Deterministic Formulation Engine Enabled
import os
import json
import uuid
import datetime
import hashlib
import base64
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, User, Project, Formulation, ComplianceLog
from schemas import (
    UserRegister, UserLogin, TokenResponse,
    ProjectCreate, ProjectResponse, FormulateRequest, FormulateResponse
)
from compliance import evaluate_compliance

# Grounded KG & Repository Data Layer
from repository import get_all_ingredients, get_ingredient_by_id, init_db
from requirements_extractor import product_brief_parser
from candidate_engine import candidate_engine
from scoring_engine import scoring_engine
from synthesis_engine import synthesis_engine
from neo4j_client import neo4j_client
from retrieval_service import retrieval_orchestrator

app = FastAPI(
    title="TCS Food Formulator API",
    description="Data-Driven Knowledge-Graph Food Formulation Engine"
)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "TCS Food Formulator API",
        "version": "1.0.0",
        "documentation": "http://localhost:8000/docs",
        "frontend_app": "http://localhost:3000",
        "message": "Welcome to TCS Food Formulator Backend API. Access the Web Frontend at http://localhost:3000"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JWT_SECRET = os.getenv("JWT_SECRET", "tcs_secret_key_67890")
security = HTTPBearer()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def create_token(payload: dict) -> str:
    payload["exp"] = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat()
    payload_str = json.dumps(payload)
    payload_b64 = base64.urlsafe_b64encode(payload_str.encode("utf-8")).decode("utf-8")
    sig = hashlib.sha256(f"{payload_b64}.{JWT_SECRET}".encode("utf-8")).hexdigest()
    return f"{payload_b64}.{sig}"

def decode_token(token: str) -> dict:
    try:
        parts = token.split(".")
        if len(parts) != 2:
            raise HTTPException(status_code=401, detail="Invalid token structure")
        payload_b64, sig = parts
        expected_sig = hashlib.sha256(f"{payload_b64}.{JWT_SECRET}".encode("utf-8")).hexdigest()
        if sig != expected_sig:
            raise HTTPException(status_code=401, detail="Token signature validation failed")
        
        payload_str = base64.urlsafe_b64decode(payload_b64.encode("utf-8")).decode("utf-8")
        payload = json.loads(payload_str)
        
        if datetime.datetime.fromisoformat(payload["exp"]) < datetime.datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token has expired")
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return decode_token(token)

# Build DB tables on startup
Base.metadata.create_all(bind=engine)
init_db()

# Seed default user and demo project on startup
@app.on_event("startup")
def startup_populate():
    db = next(get_db())
    try:
        admin = db.query(User).filter_by(email="admin@tcs.com").first()
        if not admin:
            hashed = hash_password("admin123")
            admin = User(
                username="administrator",
                email="admin@tcs.com",
                password_hash=hashed,
                role="Expert User"
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("[DB] Default admin account seeded: admin@tcs.com / admin123")
    except Exception as e:
        print(f"[DB] Startup seeding failed: {e}")
    finally:
        db.close()

# --- Taxonomy API Endpoints ---
@app.get("/api/taxonomy/textures")
def get_texture_taxonomy():
    tax_path = os.path.join(script_dir, "data", "taxonomy", "texture_taxonomy.json")
    map_path = os.path.join(script_dir, "data", "taxonomy", "category_texture_map.json")
    textures = []
    category_map = {}
    if os.path.exists(tax_path):
        with open(tax_path, "r", encoding="utf-8") as f:
            textures = json.load(f).get("textures", [])
    if os.path.exists(map_path):
        with open(map_path, "r", encoding="utf-8") as f:
            category_map = json.load(f)
    return {"textures": textures, "category_texture_map": category_map}

@app.get("/api/taxonomy/dietary")
def get_dietary_taxonomy():
    diet_path = os.path.join(script_dir, "data", "taxonomy", "dietary_requirements.json")
    if os.path.exists(diet_path):
        with open(diet_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"dietary_requirements": []}

# --- Ingredients API Endpoints ---
@app.get("/api/ingredients")
def get_ingredients_api():
    return get_all_ingredients()

@app.get("/api/ingredients/{ing_id}")
def get_ingredient_detail_api(ing_id: str):
    ing = get_ingredient_by_id(ing_id)
    if not ing:
        raise HTTPException(status_code=404, detail="Ingredient not found in repository.")
    return ing

@app.get("/api/evidence/{ingredient_id}")
def get_ingredient_evidence_api(ingredient_id: str):
    ing = get_ingredient_by_id(ingredient_id)
    if not ing or not ing.get("evidence_claim"):
        return {"ingredient_id": ingredient_id, "has_evidence": False, "evidence": []}
    return {
        "ingredient_id": ingredient_id,
        "has_evidence": True,
        "evidence": [{
            "claim": ing["evidence_claim"],
            "source_title": ing["evidence_source"],
            "evidence_type": "Scientific Literature"
        }]
    }

# --- Product Brief Parsing Endpoint ---
@app.post("/api/formulation/parse-brief")
def parse_brief_api(payload: Dict[str, Any]):
    query = payload.get("query", "")
    brief = product_brief_parser.parse(query)
    return brief.dict()

# --- Retrieval Endpoint ---
@app.post("/api/formulation/retrieve")
def retrieve_formulation_api(payload: Dict[str, Any]):
    brief_dict = payload.get("product_brief", {})
    retrieved = retrieval_orchestrator.retrieve_all_multi_dimensional(brief_dict)
    ing_dicts = [ing.to_dict() for ing in retrieved.get("ingredients", [])]
    return {
        "candidate_count": len(ing_dicts),
        "candidates": ing_dicts,
        "evidence": retrieved.get("evidence", [])
    }

# --- Primary Formulation Pipeline Generation API Endpoint ---
@app.post("/api/formulation/generate")
def generate_formulation_pipeline(payload: Dict[str, Any]):
    brief_dict = payload.get("product_brief", {})
    if not brief_dict or not brief_dict.get("description"):
        query = payload.get("query", "")
        brief = product_brief_parser.parse(query)
        brief_dict = brief.dict()

    # 1. Multi-Source Retrieval
    retrieved = retrieval_orchestrator.retrieve_all_multi_dimensional(brief_dict)
    retrieved_ingredients = retrieved.get("ingredients", [])

    # 2. Dynamic Constraint-Aware Experiment Generation
    brief_obj = product_brief_parser.parse(brief_dict.get("description", ""))
    if isinstance(brief_dict.get("nutrition_targets"), dict):
        for k, v in brief_dict["nutrition_targets"].items():
            if hasattr(brief_obj.nutrition_targets, k):
                setattr(brief_obj.nutrition_targets, k, v)
    if brief_dict.get("category"):
        brief_obj.category = brief_dict["category"]
    if brief_dict.get("dietary_requirements"):
        brief_obj.dietary_requirements = brief_dict["dietary_requirements"]

    candidates = candidate_engine.generate_experiments(brief_obj, retrieved_ingredients)
    if not candidates:
        raise HTTPException(
            status_code=422,
            detail="Formulation infeasible under the selected constraints. Zero ingredients in repository satisfy all requirements."
        )

    # 3. Score and Rank Experiments
    for cand in candidates:
        cand["scoring"] = scoring_engine.calculate_scores(cand, brief_dict)
    
    # Sort candidates by overall score descending
    candidates.sort(key=lambda x: x["scoring"]["overall_score"], reverse=True)
    top_candidate = candidates[0]
    scoring = top_candidate["scoring"]

    # 4. Grounded Synthesis Report Generation
    synthesized = synthesis_engine.synthesize(
        query=brief_dict.get("description", "Food Formulation"),
        requirements=brief_dict,
        ranked_candidate={"composition": top_candidate["composition"], "functional_coverage": {"completeness_score": 90.0}},
        evidence_list=retrieved.get("evidence", [])
    )

    # 5. Regional Compliance Audit
    compliance_results = evaluate_compliance(top_candidate["composition"], {
        "vegan": "Vegan" in brief_dict.get("dietary_requirements", []),
        "gluten_free": "Gluten-Free" in brief_dict.get("dietary_requirements", [])
    })

    # Dynamic Title
    prod_type = brief_dict.get("category", "Food")
    title = f"{prod_type} Formulation"
    if brief_dict.get("dietary_requirements"):
        title = f"{', '.join(brief_dict['dietary_requirements'])} {title}"

    response_payload = {
        "request_id": f"REQ_{uuid.uuid4().hex[:8].upper()}",
        "parsed_brief": brief_dict,
        "candidate_sets": candidates,
        "formulation": {
            "recipe_id": top_candidate["candidate_id"],
            "recipe_name": title,
            "category": brief_dict.get("category", "General"),
            "composition": top_candidate["composition"],
            "functional_coverage": {
                "roles": {"Protein Source": top_candidate["composition"]["functional_ingredients"][0]["name"] if top_candidate["composition"].get("functional_ingredients") else "Protein Isolate"},
                "completeness_score": 90.0,
                "assessment": "FUNCTIONALLY COMPLETE"
            },
            "performance_prediction": top_candidate["nutrition"],
            "radar_scores": scoring["radar_scores"],
            "overall_score": scoring["overall_score"],
            "cost_per_kg_inr": scoring["cost_per_kg_inr"],
            "process_recommendations": top_candidate.get("process_steps", synthesized.get("process_recommendations", [])),
            "status": "READY FOR VIRTUAL VALIDATION"
        },
        "compliance": compliance_results,
        "evidence": retrieved.get("evidence", [])
    }
    return response_payload

# Formulation Generation Endpoints
@app.post("/api/formulate")
@app.post("/api/formulation/generate")
def formulate_api(req: Dict[str, Any], db: Session = Depends(get_db)):
    query = req.get("query") or req.get("prompt") or "Formulate a food product brief"
    constraints = req.get("constraints", {})

    brief = product_brief_parser.parse(query)
    brief_dict = brief.dict()
    if constraints:
        if constraints.get("vegan") and "Vegan" not in brief_dict["dietary_requirements"]:
            brief_dict["dietary_requirements"].append("Vegan")
        if constraints.get("gluten_free") and "Gluten-Free" not in brief_dict["dietary_requirements"]:
            brief_dict["dietary_requirements"].append("Gluten-Free")

    res = generate_formulation_pipeline({"product_brief": brief_dict, "query": query})
    
    # Save project to SQLite
    project_id = req.get("project_id")
    if not project_id:
        proj = Project(
            name=res["formulation"]["recipe_name"],
            category=res["formulation"]["category"],
            query=query,
            status="Formulated"
        )
        db.add(proj)
        db.commit()
        db.refresh(proj)
        project_id = str(proj.id)

    form = Formulation(
        project_id=uuid.UUID(project_id),
        version="V1.0",
        composition=res["formulation"]["composition"],
        functional_coverage=res["formulation"]["functional_coverage"],
        performance_prediction=res["formulation"]["performance_prediction"],
        process_recommendations=res["formulation"]["process_recommendations"],
        status=res["formulation"]["status"]
    )
    db.add(form)
    db.commit()
    db.refresh(form)

    return {
        "formulation": res["formulation"],
        "compliance": res["compliance"],
        "project_id": project_id,
        "formulation_id": str(form.id)
    }

# --- Health & Diagnostic Endpoints ---
@app.get("/api/kg/health")
def get_kg_health():
    return neo4j_client.get_health()

@app.get("/api/retrieval/health")
def get_retrieval_health():
    return {"status": "ok", "ingredients_count": len(get_all_ingredients())}

# --- Auth Routes ---
@app.post("/api/auth/register", response_model=TokenResponse)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter((User.email == user_in.email) | (User.username == user_in.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    hashed = hash_password(user_in.password)
    user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed,
        role=user_in.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token({"sub": str(user.id), "username": user.username, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "email": user.email,
        "role": user.role
    }

@app.post("/api/auth/login", response_model=TokenResponse)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=user_in.email).first()
    if not user or user.password_hash != hash_password(user_in.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    token = create_token({"sub": str(user.id), "username": user.username, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "email": user.email,
        "role": user.role
    }

# --- Project Routes ---
@app.get("/api/projects")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    results = []
    for proj in projects:
        latest_form = db.query(Formulation).filter_by(project_id=proj.id).order_by(Formulation.created_at.desc()).first()
        results.append({
            "id": str(proj.id),
            "name": proj.name,
            "category": proj.category,
            "query": proj.query,
            "status": proj.status,
            "created_at": proj.created_at.isoformat(),
            "updated_at": proj.updated_at.isoformat(),
            "version": latest_form.version if latest_form else "None",
            "formulation_id": str(latest_form.id) if latest_form else None
        })
    return results

@app.post("/api/projects", response_model=ProjectResponse)
def create_project(proj_in: ProjectCreate, db: Session = Depends(get_db)):
    proj = Project(
        name=proj_in.name,
        category=proj_in.category,
        query=proj_in.query,
        status="Pending"
    )
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj

@app.get("/api/projects/{project_id}")
def get_project_detail(project_id: str, db: Session = Depends(get_db)):
    try:
        p_uuid = uuid.UUID(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID UUID")
    
    proj = db.query(Project).filter_by(id=p_uuid).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
        
    formulations = db.query(Formulation).filter_by(project_id=p_uuid).order_by(Formulation.created_at.desc()).all()
    
    formulations_list = []
    for form in formulations:
        comp_logs = db.query(ComplianceLog).filter_by(formulation_id=form.id).all()
        compliance_dict = {
            log.region: {"status": log.status, "alerts": log.alerts}
            for log in comp_logs
        }
        formulations_list.append({
            "id": str(form.id),
            "version": form.version,
            "composition": form.composition,
            "functional_coverage": form.functional_coverage,
            "performance_prediction": form.performance_prediction,
            "process_recommendations": form.process_recommendations,
            "status": form.status,
            "created_at": form.created_at.isoformat(),
            "compliance": compliance_dict
        })

    return {
        "id": str(proj.id),
        "name": proj.name,
        "category": proj.category,
        "query": proj.query,
        "status": proj.status,
        "created_at": proj.created_at.isoformat(),
        "formulations": formulations_list
    }

@app.put("/api/projects/{project_id}")
def update_project(project_id: str, payload: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        p_uuid = uuid.UUID(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID UUID")
    
    proj = db.query(Project).filter_by(id=p_uuid).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")

    if "name" in payload:
        proj.name = payload["name"]
    if "category" in payload:
        proj.category = payload["category"]
    if "status" in payload:
        proj.status = payload["status"]
    
    proj.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(proj)
    return {"status": "success", "project": {"id": str(proj.id), "name": proj.name, "category": proj.category, "status": proj.status}}

@app.post("/api/projects/{project_id}/duplicate")
def duplicate_project(project_id: str, db: Session = Depends(get_db)):
    try:
        p_uuid = uuid.UUID(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID UUID")
    
    proj = db.query(Project).filter_by(id=p_uuid).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")

    new_proj = Project(
        name=f"{proj.name} (Copy)",
        category=proj.category,
        query=proj.query,
        status=proj.status
    )
    db.add(new_proj)
    db.commit()
    db.refresh(new_proj)

    # Duplicate latest formulation if any
    latest_form = db.query(Formulation).filter_by(project_id=p_uuid).order_by(Formulation.created_at.desc()).first()
    if latest_form:
        new_form = Formulation(
            project_id=new_proj.id,
            version=f"{latest_form.version} (Copy)",
            composition=latest_form.composition,
            functional_coverage=latest_form.functional_coverage,
            performance_prediction=latest_form.performance_prediction,
            process_recommendations=latest_form.process_recommendations,
            status=latest_form.status
        )
        db.add(new_form)
        db.commit()

    return {"status": "success", "duplicated_id": str(new_proj.id), "name": new_proj.name}

@app.delete("/api/projects/{project_id}")
def delete_project(project_id: str, db: Session = Depends(get_db)):
    try:
        p_uuid = uuid.UUID(project_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid project ID UUID")
    
    proj = db.query(Project).filter_by(id=p_uuid).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")

    db.query(Formulation).filter_by(project_id=p_uuid).delete()
    db.delete(proj)
    db.commit()
    return {"status": "success", "message": f"Project {project_id} deleted successfully."}

@app.get("/api/user/profile")
def get_user_profile():
    return {
        "name": "Dr. Jane Smith",
        "avatar_initials": "DJS",
        "role": "Senior R&D Scientist",
        "department": "Plant-Based Food Formulations & Innovation",
        "organization": "TCS Food Formulations R&D Center",
        "email": "jane.smith@tcs.com",
        "joined_date": "2024-01-15",
        "preferences": {
            "default_units": "Metric (kg, g, °C)",
            "compliance_alerts": True,
            "auto_save": True,
            "ai_mode": "Deep KG Embedding"
        }
    }

# --- Export Report Route ---
@app.post("/api/reports/export")
def export_report(req: Dict[str, Any]):
    recipe_name = req.get("recipe_name", "Formulation_Report")
    file_name = f"{recipe_name.replace(' ', '_')}.csv"
    
    csv_lines = ["Ingredient,Category,Role,Percentage"]
    composition = req.get("composition", {})
    
    for ing in composition.get("bulk_ingredients", []):
        csv_lines.append(f"{ing.get('name')},{ing.get('category')},Bulk,{ing.get('percentage')}%")
    for ing in composition.get("functional_ingredients", []):
        csv_lines.append(f"{ing.get('name')},Functional,{ing.get('functional_role')},{ing.get('percentage')}%")
        
    return {
        "file_name": file_name,
        "content_type": "text/csv",
        "data": "\n".join(csv_lines)
    }

# =======================================================
# KNOWLEDGE GRAPH API ROUTES (Neo4j + Grounded KG Index)
# =======================================================

@app.get("/api/knowledge-graph/health")
def get_kg_health():
    """Diagnostic health check for Neo4j database & Knowledge Graph layer."""
    return neo4j_client.get_health()

@app.get("/api/knowledge-graph")
def get_full_knowledge_graph(limit: int = 80):
    """Returns overview Knowledge Graph data for interactive Cytoscape dashboard."""
    return neo4j_client.get_full_graph(limit=limit)

@app.get("/api/knowledge-graph/search")
def search_knowledge_graph(q: str = ""):
    """Searches graph nodes matching query across ingredients, properties, functions, constraints, processes, nutrients, allergens, claims."""
    if not q or not q.strip():
        return {"query": "", "results": []}
    results = neo4j_client.search_nodes(query=q)
    return {"query": q, "results": results}

@app.get("/api/knowledge-graph/ingredient/{ingredient_id}")
def get_ingredient_graph_details(ingredient_id: str):
    """Returns specific node details and 1-hop connections."""
    return neo4j_client.get_node_details(ingredient_id=ingredient_id)

@app.get("/api/knowledge-graph/ingredient/{ingredient_id}/subgraph")
def get_ingredient_subgraph(ingredient_id: str, depth: int = 2):
    """Retrieves selected ingredient and its connected neighborhood (depth 1..3)."""
    clamped_depth = max(1, min(depth, 3))
    return neo4j_client.get_ingredient_subgraph(ingredient_id=ingredient_id, depth=clamped_depth)

@app.get("/api/knowledge-graph/node/{node_id}")
def get_node_by_id(node_id: str):
    """Returns details for any individual node in the graph."""
    return neo4j_client.get_node_details(node_id=node_id)

@app.get("/api/knowledge-graph/neighbors/{node_id}")
def get_node_neighbors(node_id: str):
    """Retrieves 1-step neighbors for progressive node expansion."""
    return neo4j_client.get_node_neighbors(node_id=node_id)

