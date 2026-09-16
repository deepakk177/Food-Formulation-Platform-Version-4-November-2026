from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any, Optional
from uuid import UUID
import datetime

# --- Auth Schemas ---
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "Guided User"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    email: str
    role: str

# --- Ingredient Schemas ---
class IngredientSchema(BaseModel):
    name: str
    category: str
    protein: float
    fat: float
    carbs: float
    calories: float
    functional_role: str
    allergen: str

# --- Project Schemas ---
class ProjectCreate(BaseModel):
    name: str
    category: str
    query: Optional[str] = None

class ProjectResponse(BaseModel):
    id: UUID
    name: str
    category: str
    query: Optional[str]
    status: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

# --- Compliance Schemas ---
class ComplianceLogSchema(BaseModel):
    region: str
    status: str
    alerts: List[str]

    class Config:
        from_attributes = True

# --- Formulation Schemas ---
class IngredientComponentSchema(BaseModel):
    id: Optional[str] = None
    name: str
    category: str
    subcategory: Optional[str] = "General"
    functional_role: str
    formulation_role: Optional[str] = "Base Ingredient"
    percentage: float
    quantity_g: Optional[float] = 0.0
    ins_number: Optional[str] = None
    cas_number: Optional[str] = None
    pubchem_id: Optional[str] = None
    regulatory_status: Optional[str] = "Permitted"
    component_status: Optional[str] = "Required"  # Required, Recommended, Optional, Not Required
    purpose: Optional[str] = ""
    why_present: Optional[str] = ""
    addition_stage: Optional[str] = "Main Mixing"
    addition_order: Optional[int] = 1
    confidence: Optional[float] = 95.0
    source_evidence: Optional[str] = "USDA FDC / Codex GSFA"
    cost_per_kg: Optional[float] = 10.0
    protein: Optional[float] = 0.0
    fat: Optional[float] = 0.0
    carbs: Optional[float] = 0.0
    calories: Optional[float] = 0.0

class BulkIngredientConc(BaseModel):
    name: str
    category: str
    percentage: float

class FunctionalIngredientConc(BaseModel):
    name: str
    functional_role: str
    percentage: float

class FormulationComposition(BaseModel):
    bulk_ingredients: List[Dict[str, Any]] = []
    functional_ingredients: List[Dict[str, Any]] = []
    
    # Complete Industrial Component Groups
    base_ingredients: Optional[List[IngredientComponentSchema]] = []
    functional_additives: Optional[List[IngredientComponentSchema]] = []
    sensory_flavor_color: Optional[List[IngredientComponentSchema]] = []
    preservation_system: Optional[List[IngredientComponentSchema]] = []
    leavening_system: Optional[List[IngredientComponentSchema]] = []
    fortification_system: Optional[List[IngredientComponentSchema]] = []
    processing_aids: Optional[List[IngredientComponentSchema]] = []
    all_components: Optional[List[IngredientComponentSchema]] = []

class CompletenessCheckResult(BaseModel):
    completeness_score: float
    status: str
    checklist: Dict[str, bool] = {}
    evaluated_aspects: List[str] = []
    recommendations: List[str] = []

class FunctionalCoverageSchema(BaseModel):
    roles: Dict[str, str]
    completeness_score: float
    assessment: str
    completeness_audit: Optional[CompletenessCheckResult] = None

class PerformancePredictionSchema(BaseModel):
    protein: float
    fat: float
    carbohydrates: float
    calories: float
    texture: str
    mouthfeel: str
    viscosity: str
    shelf_life: int

class FormulationDetail(BaseModel):
    recipe_id: str
    recipe_name: str
    category: str
    composition: FormulationComposition
    functional_coverage: FunctionalCoverageSchema
    performance_prediction: PerformancePredictionSchema
    process_recommendations: List[str]
    status: str
    candidate_sets: Optional[List[Dict[str, Any]]] = []

class FormulateRequest(BaseModel):
    project_id: Optional[str] = None
    query: str
    constraints: Dict[str, Any] = {}

class FormulateResponse(BaseModel):
    formulation: FormulationDetail
    compliance: Dict[str, ComplianceLogSchema]
    project_id: str
    formulation_id: str

