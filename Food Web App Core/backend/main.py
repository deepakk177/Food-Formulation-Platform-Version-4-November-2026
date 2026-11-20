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
from db_models import Base, User, Project, Formulation, ComplianceLog
from schemas import (
    UserRegister, UserLogin, TokenResponse,
    ProjectCreate, ProjectResponse, FormulateRequest, FormulateResponse
)
from compliance import evaluate_compliance

# Grounded KG & Repository Data Layer
from repository import get_all_ingredients, get_ingredient_by_id, init_db
from requirements_extractor import product_brief_parser
from candidate_engine import candidate_engine, STRATEGY_REGISTRY
from scoring_engine import scoring_engine
from models.ranking.model import ranking_model
from synthesis_engine import synthesis_engine
from neo4j_client import neo4j_client
from retrieval_service import retrieval_orchestrator
from validation_gate import validation_gate
from calculation_service import calculation_service
from strategy_classifier import dynamic_strategy_classifier

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
    custom_comp = payload.get("composition")
    if custom_comp and (custom_comp.get("bulk_ingredients") or custom_comp.get("functional_ingredients")):
        # User defined a custom formulation in Expert Formulator!
        bulk_items = custom_comp.get("bulk_ingredients", [])
        func_items = custom_comp.get("functional_ingredients", [])
        all_user_items = bulk_items + func_items

        from repository import get_all_ingredients
        all_db_map = {i["name"].lower(): i for i in get_all_ingredients()}

        all_formatted = []
        tot_prot = 0.0
        tot_fat = 0.0
        tot_carb = 0.0
        tot_cal = 0.0
        tot_cost = 0.0
        has_cost = True

        for item in all_user_items:
            nm = item.get("name", "")
            pct = float(item.get("percentage", 0.0))
            db_match = all_db_map.get(nm.lower(), {})

            p_val = float(db_match.get("protein", 0.0) or 0.0)
            f_val = float(db_match.get("fat", 0.0) or 0.0)
            c_val = float(db_match.get("carbs", 0.0) or 0.0)
            cal_val = float(db_match.get("energy", db_match.get("calories", 0.0)) or 0.0)
            cost_val = float(db_match.get("cost_per_kg")) if db_match.get("cost_per_kg") is not None else None

            tot_prot += (pct / 100.0) * p_val
            tot_fat += (pct / 100.0) * f_val
            tot_carb += (pct / 100.0) * c_val
            tot_cal += (pct / 100.0) * cal_val
            if cost_val is not None:
                tot_cost += (pct / 100.0) * cost_val
            else:
                has_cost = False

            f_role = item.get("functional_role") or db_match.get("functional_role") or item.get("category", "Raw Material")
            all_formatted.append({
                "name": nm,
                "percentage": pct,
                "functional_role": f_role,
                "category": item.get("category") or db_match.get("category", "General"),
                "allergen": str(db_match.get("allergens", "None")),
                "regulatory_status": "Permitted" if db_match.get("evidence_claim") else "UNKNOWN",
                "ins_number": db_match.get("ins_number"),
                "source": "Expert Custom Recipe",
                "source_evidence": db_match.get("evidence_source", "Custom Recipe Specification"),
                "protein": p_val,
                "fat": f_val,
                "carbs": c_val,
                "calories": cal_val,
                "cost_per_kg": cost_val
            })

        custom_candidate = {
            "candidate_id": "FC-EXPERT",
            "set_name": "Expert Custom Formulation",
            "title": f"Expert Formulation: {brief_dict.get('category', 'Custom Product')}",
            "strategy": "expert_custom",
            "composition": {
                "bulk_ingredients": bulk_items,
                "functional_ingredients": func_items,
                "all_components": all_formatted
            },
            "total_percentage": round(sum(i["percentage"] for i in all_formatted), 4),
            "is_mathematically_valid": abs(sum(i["percentage"] for i in all_formatted) - 100.0) <= 0.05,
            "completeness_audit": {"completeness_score": 100.0, "status": "Expert Validated", "passed_checks": 14},
            "nutrition": {
                "protein": round(tot_prot, 1),
                "fat": round(tot_fat, 1),
                "carbohydrates": round(tot_carb, 1),
                "calories": round(tot_cal, 1),
                "cost_per_kg": round(tot_cost, 2) if has_cost else None,
                "cost_status": "KNOWN" if has_cost else "COST_UNKNOWN"
            },
            "cost_per_kg": round(tot_cost, 2) if has_cost else None,
            "cost_status": "KNOWN" if has_cost else "COST_UNKNOWN",
            "process_steps": [
                "1. Dispense dry and bulk ingredients as specified in expert formulation.",
                "2. Blend functional components uniformly into the matrix.",
                "3. Thermal processing and packaging under standard GMP hygiene conditions."
            ]
        }
        candidates = [custom_candidate]
    else:
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

    # 3. Score and Validate All Candidate Sets Independently
    eligible_ids = [getattr(i, "id", "") for i in retrieved_ingredients]
    brief_obj_for_val = brief_obj if 'brief_obj' in locals() else product_brief_parser.parse(brief_dict.get("description", ""))

    for cand in candidates:
        strat = cand.get("strategy_id") or cand.get("strategy", "balanced")
        strat_entry = STRATEGY_REGISTRY.get(strat)
        if not strat_entry:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported strategy '{strat}'. Supported strategies: {list(STRATEGY_REGISTRY.keys())}"
            )

        prof = strat_entry["scoring_profile"]
        cand["strategy_id"] = strat
        cand["strategy_name"] = strat_entry["label"]
        cand["scoring_profile"] = prof

        # Independent score calculation using Universal Evaluation Benchmark (UEB)
        scoring_res = scoring_engine.calculate_scores(cand, brief_dict, profile_name=prof)
        cand["scoring"] = scoring_res

        # Independent validation gate execution
        val_res = validation_gate.validate_candidate_set(
            cand,
            brief_obj_for_val,
            eligible_candidate_ids=eligible_ids
        )
        cand["validation_report"] = val_res
        cand["feasibility_status"] = val_res["status"]
        cand["is_feasible"] = bool(val_res["is_feasible"])
        cand["hard_constraint_violations"] = val_res.get("hard_constraint_violations", [])
        cand["violations"] = cand["hard_constraint_violations"]

        # Canonical Serialized Evaluation Fields (Requirement 6)
        cand["optimization_objective_score"] = scoring_res.get("optimization_objective_score", scoring_res["overall_score"])
        cand["nutrition_fit_score"] = scoring_res.get("nutrition_fit_score", scoring_res.get("radar", {}).get("Nutrition", 0.0))
        cand["cost_efficiency_score"] = scoring_res.get("cost_efficiency_score", scoring_res.get("radar", {}).get("Cost", 0.0))
        cand["functional_role_coverage_score"] = scoring_res.get("functional_role_coverage_score", scoring_res.get("radar", {}).get("FRC", 0.0))
        cand["compatibility_score"] = scoring_res.get("compatibility_score", scoring_res.get("radar", {}).get("Compatibility", 0.0))
        cand["soft_constraint_score"] = scoring_res.get("soft_constraint_score", scoring_res.get("radar", {}).get("Constraint_Satisfaction", 0.0))
        cand["universal_evaluation_score"] = scoring_res["overall_score"]
        cand["evaluation_coverage"] = scoring_res.get("evaluation_coverage", 100.0)

    # Dynamic Candidate Set Strategy Classification (Master Implementation Parts 3 & 4)
    # Assigns: Cost Optimized, Nutrition Maximized, Balanced Set, Functionality & Flavor
    candidates = dynamic_strategy_classifier.classify_candidates(candidates, brief_obj_for_val)

    # 4. Separate Feasibility from Quality Ranking (Requirement 5)
    # Infeasible candidates are strictly disqualified from winning, but kept visible for diagnostic audit
    feasible_candidates = [c for c in candidates if c.get("is_feasible", False)]
    infeasible_candidates = [c for c in candidates if not c.get("is_feasible", False)]

    # Documented Multi-Tier Tie-Breaking Comparator:
    # 1. Primary: Universal Evaluation Score (higher is better)
    # 2. Secondary: Soft Constraint Satisfaction Score (higher is better)
    # 3. Tertiary: Ingredient Cost per kg (lower is better, represented as negative cost)
    # 4. Quaternary: Functional Role Coverage FRC (higher is better)
    def candidate_ranking_key(c):
        overall = float(c["universal_evaluation_score"])
        soft_sat = float(c["soft_constraint_score"])
        cost = float(c.get("cost_per_kg") or 999.0)
        frc = float(c["functional_role_coverage_score"])
        return (overall, soft_sat, -cost, frc)

    feasible_candidates.sort(key=candidate_ranking_key, reverse=True)
    infeasible_candidates.sort(key=candidate_ranking_key, reverse=True)

    # Assign unambiguous rank numbers, positions, and selection state
    for rank_idx, c in enumerate(feasible_candidates, start=1):
        c["rank"] = rank_idx
        c["ranking_position"] = rank_idx
        c["ranking_status"] = "FEASIBLE"
        c["is_selected"] = False

    for rank_idx, c in enumerate(infeasible_candidates, start=len(feasible_candidates) + 1):
        c["rank"] = None
        c["ranking_position"] = None
        c["ranking_status"] = "DISQUALIFIED_INFEASIBLE"
        c["is_selected"] = False

    # Preserved full list: feasible winners first, followed by infeasible candidates
    candidates = feasible_candidates + infeasible_candidates

    # Check if a specific candidate was requested by ID or index
    selected_idx = payload.get("selected_candidate_index")
    selected_cid = payload.get("selected_candidate_id")

    if selected_cid:
        chosen_candidate = next((c for c in candidates if c.get("candidate_id") == selected_cid or c.get("formulation_id") == selected_cid), None)
    elif selected_idx is not None and 0 <= int(selected_idx) < len(candidates):
        chosen_candidate = candidates[int(selected_idx)]
    else:
        # Default winner is the top-ranked FEASIBLE candidate (NOT blindly Balanced)
        chosen_candidate = feasible_candidates[0] if feasible_candidates else (candidates[0] if candidates else None)

    if not chosen_candidate:
        raise HTTPException(
            status_code=422,
            detail="Zero formulation candidates could be synthesized from the eligible ingredients."
        )

    chosen_candidate["is_selected"] = True

    has_feasible_winner = len(feasible_candidates) > 0
    formulation_pipeline_status = "APPROVED" if (chosen_candidate.get("is_feasible") and has_feasible_winner) else (
        "NO_FEASIBLE_WINNER" if not has_feasible_winner else "SELECTED_CANDIDATE_INFEASIBLE"
    )

    scoring = chosen_candidate["scoring"]
    validation_res = chosen_candidate.get("validation_report") or validation_gate.validate_candidate_set(
        chosen_candidate,
        brief_obj_for_val,
        eligible_candidate_ids=eligible_ids
    )
    val_status = formulation_pipeline_status

    # Grounded Synthesis Report Generation for chosen candidate
    audit_data = chosen_candidate.get("completeness_audit", {})
    comp_score = audit_data.get("completeness_score", 0.0)
    assessment = audit_data.get("status", "Evaluated")

    synthesized = synthesis_engine.synthesize(
        query=brief_dict.get("description", "Food Formulation"),
        requirements=brief_dict,
        ranked_candidate={"composition": chosen_candidate["composition"], "functional_coverage": {"completeness_score": comp_score}},
        evidence_list=retrieved.get("evidence", [])
    )

    # Regional Compliance Audit for chosen candidate
    compliance_results = evaluate_compliance(chosen_candidate["composition"], {
        "vegan": "Vegan" in brief_dict.get("dietary_requirements", []),
        "gluten_free": "Gluten-Free" in brief_dict.get("dietary_requirements", [])
    }, product_category=brief_dict.get("category", "General"))

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
            "recipe_id": chosen_candidate["candidate_id"],
            "candidate_id": chosen_candidate["candidate_id"],
            "formulation_id": chosen_candidate.get("formulation_id", f"FORM-{chosen_candidate['candidate_id']}"),
            "canonical_nutrition": chosen_candidate.get("canonical_nutrition") or chosen_candidate["nutrition"].get("canonical_nutrition"),
            "recipe_name": chosen_candidate.get("title", title),
            "category": brief_dict.get("category", "General"),
            "strategy": chosen_candidate.get("strategy_id", chosen_candidate.get("strategy", "balanced")),
            "strategy_id": chosen_candidate.get("strategy_id", chosen_candidate.get("strategy")),
            "strategy_label": chosen_candidate.get("strategy_label", chosen_candidate.get("strategy_name", "Balanced Set")),
            "strategy_name": chosen_candidate.get("strategy_label", chosen_candidate.get("strategy_name", "Balanced Set")),
            "strategy_short_label": chosen_candidate.get("strategy_short_label", chosen_candidate.get("strategy_label", "Balanced Set")),
            "strategy_rationale": chosen_candidate.get("strategy_rationale"),
            "scoring_profile": chosen_candidate.get("scoring_profile", "BALANCED"),
            "composition": chosen_candidate["composition"],
            "functional_coverage": {
                "roles": {"Protein Source": chosen_candidate["composition"]["functional_ingredients"][0]["name"] if chosen_candidate["composition"].get("functional_ingredients") else "Protein Isolate"},
                "completeness_score": comp_score,
                "assessment": assessment
            },
            "performance_prediction": chosen_candidate["nutrition"],
            "radar_scores": scoring["radar_scores"],
            "overall_score": scoring["overall_score"],
            "universal_evaluation_score": scoring.get("universal_evaluation_score", scoring["overall_score"]),
            "optimization_objective_score": scoring.get("optimization_objective_score", scoring["overall_score"]),
            "evaluation_coverage": scoring.get("evaluation_coverage", 100.0),
            "cost_per_kg_inr": scoring["cost_per_kg_inr"],
            "cost_per_kg": chosen_candidate.get("cost_per_kg"),
            "cost_snapshot": chosen_candidate.get("cost_snapshot"),
            "currency": "USD",
            "cost_status": chosen_candidate.get("cost_status", chosen_candidate["nutrition"].get("cost_status", "KNOWN")),
            "process_recommendations": chosen_candidate.get("process_steps", synthesized.get("process_recommendations", [])),
            "status": val_status,
            "feasibility_status": chosen_candidate.get("feasibility_status", "FEASIBLE"),
            "is_feasible": chosen_candidate.get("is_feasible", False),
            "is_selected": True,
            "validation_report": validation_res,
            "compliance": compliance_results,
            "regulatory_compliance": compliance_results,
            "estimated_cost_per_kg": chosen_candidate.get("cost_per_kg")
        },
        "has_feasible_winner": has_feasible_winner,
        "pipeline_status": formulation_pipeline_status,
        "sensitivity_analysis": ranking_model.evaluate_weight_sensitivity(feasible_candidates if feasible_candidates else candidates, brief_dict),
        "compliance": compliance_results,
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
    composition = req.get("composition")

    brief = product_brief_parser.parse(query)
    brief_dict = brief.dict()
    if constraints:
        if constraints.get("vegan") and "Vegan" not in brief_dict["dietary_requirements"]:
            brief_dict["dietary_requirements"].append("Vegan")
        if constraints.get("gluten_free") and "Gluten-Free" not in brief_dict["dietary_requirements"]:
            brief_dict["dietary_requirements"].append("Gluten-Free")

    payload = {"product_brief": brief_dict, "query": query}
    if composition:
        payload["composition"] = composition

    res = generate_formulation_pipeline(payload)
    
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
        "candidate_sets": res.get("candidate_sets", []),
        "parsed_brief": res.get("parsed_brief", brief_dict),
        "formulation": res["formulation"],
        "compliance": res["compliance"],
        "evidence": res.get("evidence", []),
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

