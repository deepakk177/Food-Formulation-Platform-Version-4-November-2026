"""
Authoritative Canonical Formulation Data Model.
Establishes a single source of truth for formulation states across retrieval, candidate selection,
mathematical optimization (SLSQP), nutrition calculations, scoring, compliance validation, and frontend delivery.
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import uuid
import datetime

class IngredientPropertySnapshot(BaseModel):
    """Immutable property snapshot of an ingredient at the moment of selection."""
    ingredient_id: str
    name: str
    category: str
    functional_role: str
    protein_pct: float = 0.0
    fat_pct: float = 0.0
    carb_pct: float = 0.0
    sugar_pct: float = 0.0
    fibre_pct: float = 0.0
    calories_per_100g: float = 0.0
    cost_per_kg: Optional[float] = None
    cost_status: str = "KNOWN"  # "KNOWN" or "COST_UNKNOWN"
    ins_number: Optional[str] = None
    cas_number: Optional[str] = None
    regulatory_status: str = "UNKNOWN"
    allergens: List[str] = Field(default_factory=list)
    source_evidence: str = "Grounded Repository DB"

class CanonicalComponent(BaseModel):
    """Authoritative formulation component record."""
    ingredient_id: str
    name: str
    percentage: float  # Exact mass balance fraction (sum == 100.0000%)
    quantity_g: float  # Grams in target batch size
    role: str
    formulation_role: str  # e.g., "Base Raw Material", "Functional Texturizer"
    cost_per_kg: Optional[float] = None
    cost_contribution: Optional[float] = None
    addition_order: int = 1
    addition_stage: str = "Phase 1: Blending"
    purpose: str = ""
    why_present: str = ""
    properties: IngredientPropertySnapshot

class NutritionYield(BaseModel):
    """Deterministic nutritional yield calculated strictly from grounded component mass."""
    basis: str = "100g formulation basis"
    unit: str = "g per 100g (kcal for calories)"
    protein: float = 0.0
    fat: float = 0.0
    carbohydrates: float = 0.0
    sugar: float = 0.0
    fibre: float = 0.0
    calories: float = 0.0
    per_serving: Dict[str, float] = Field(default_factory=dict)
    itemized_breakdown: List[Dict[str, Any]] = Field(default_factory=list)

class CostYield(BaseModel):
    """Deterministic cost yield calculated strictly from grounded component mass."""
    currency: str = "USD"
    cost_per_kg: Optional[float] = None
    cost_per_serving: Optional[float] = None
    cost_status: str = "KNOWN"  # "CALCULATED" or "COST_UNKNOWN"
    has_unknown_cost_components: bool = False
    itemized_breakdown: List[Dict[str, Any]] = Field(default_factory=list)

class OptimizationDiagnostic(BaseModel):
    """Complete diagnostic record from the SLSQP mathematical optimizer."""
    solver: str = "scipy.optimize.minimize (SLSQP)"
    is_feasible: bool = False
    status: str = "PENDING"  # "OPTIMIZED", "FEASIBILITY_WARNING", "INFEASIBLE"
    solver_message: str = ""
    iterations: int = 0
    active_constraints: List[str] = Field(default_factory=list)
    violated_constraints: List[str] = Field(default_factory=list)
    bounds: List[Dict[str, Any]] = Field(default_factory=list)
    mass_balance_deviation: float = 0.0

class ConstraintValidationResult(BaseModel):
    """Result of independent verification of hard and soft constraints."""
    passed_hard_constraints: bool = True
    hard_violations: List[str] = Field(default_factory=list)
    soft_satisfactions: Dict[str, float] = Field(default_factory=dict)
    soft_score: float = 100.0

class CanonicalFormulationState(BaseModel):
    """
    Authoritative Canonical Formulation State shared across all downstream modules.
    Guarantees that candidates, optimized recipes, compliance, scoring, and UI reports
    all refer to the exact same version-controlled state without mutation or divergence.
    """
    formulation_id: str = Field(default_factory=lambda: f"FORM-{uuid.uuid4().hex[:8].upper()}")
    candidate_set_id: str = "FC-001"
    version: str = "V1.0"
    created_at: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    
    # Context & Brief
    category: str = "General"
    title: str = "Formulation Dossier"
    strategy_key: str = "balanced"
    strategy_title: str = "Balanced Strategy"
    batch_size_kg: float = 1.0
    serving_size_g: float = 40.0

    # Traceability Lists
    retrieved_candidate_ids: List[str] = Field(default_factory=list)
    eligible_candidate_ids: List[str] = Field(default_factory=list)
    selected_candidate_ids: List[str] = Field(default_factory=list)
    missing_required_roles: List[str] = Field(default_factory=list)

    # Ingredients & Formulation
    components: List[CanonicalComponent] = Field(default_factory=list)
    total_percentage: float = 100.0000

    # Authoritative Numerical Calculations
    nutrition: NutritionYield = Field(default_factory=NutritionYield)
    cost: CostYield = Field(default_factory=CostYield)
    water_activity: float = 0.58
    water_activity_status: str = "EMPIRICAL_ESTIMATE"  # "MEASURED", "MODEL_PREDICTION", "EMPIRICAL_ESTIMATE"
    shelf_life_months: Optional[float] = None
    shelf_life_status: str = "INSUFFICIENT_LABELED_DATA"
    sensory_status: str = "INSUFFICIENT_LABELED_DATA"

    # Solver & Validation Diagnostics
    optimization_diagnostic: OptimizationDiagnostic = Field(default_factory=OptimizationDiagnostic)
    constraint_validation: ConstraintValidationResult = Field(default_factory=ConstraintValidationResult)

    # Multi-Objective Scoring & Strategy
    overall_score: float = 0.0
    scoring_breakdown: Dict[str, Any] = Field(default_factory=dict)
    strategy_rationale: Dict[str, Any] = Field(default_factory=dict)

    # Regulatory & Evidence
    compliance: Dict[str, Any] = Field(default_factory=dict)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    process_steps: List[str] = Field(default_factory=list)
    status: str = "VALIDATED"  # "VALIDATED", "FEASIBILITY_WARNING", "INFEASIBLE"

