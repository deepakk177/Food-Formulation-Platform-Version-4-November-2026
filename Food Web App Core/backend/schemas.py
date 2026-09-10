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
class BulkIngredientConc(BaseModel):
    name: str
    category: str
    percentage: float

class FunctionalIngredientConc(BaseModel):
    name: str
    functional_role: str
    percentage: float

class FormulationComposition(BaseModel):
    bulk_ingredients: List[BulkIngredientConc]
    functional_ingredients: List[FunctionalIngredientConc]

class FunctionalCoverageSchema(BaseModel):
    roles: Dict[str, str]
    completeness_score: float
    assessment: str

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

class FormulateRequest(BaseModel):
    project_id: Optional[str] = None
    query: str
    constraints: Dict[str, Any] = {}

class FormulateResponse(BaseModel):
    formulation: FormulationDetail
    compliance: Dict[str, ComplianceLogSchema]
    project_id: str
    formulation_id: str
