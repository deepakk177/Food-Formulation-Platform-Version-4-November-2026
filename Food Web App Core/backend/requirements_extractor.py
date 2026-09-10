"""
ProductBriefParser Engine for TCS Food Formulator
Parses natural language product briefs into normalized ProductBrief data objects,
extracting Hard Constraints, Soft Objectives, and Dynamic Experiment Strategies.
"""
import re
import os
import json
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

try:
    from langchain_groq import ChatGroq
    from langchain_core.messages import SystemMessage, HumanMessage
except ImportError:
    ChatGroq = None

logger = logging.getLogger("ProductBriefParser")

class TargetValue:
    def __init__(self, value: float, operator: str = ">="):
        self.value = value
        self.operator = operator

class NutritionTargets(BaseModel):
    protein_min: Optional[float] = None
    protein_max: Optional[float] = None
    fat_min: Optional[float] = None
    fat_max: Optional[float] = None
    carbohydrate_max: Optional[float] = None
    sugar_max: Optional[float] = None
    fibre_min: Optional[float] = None
    sodium_max: Optional[float] = None
    calories_max: Optional[float] = None

    def __contains__(self, item: str) -> bool:
        if "protein" in item:
            return self.protein_min is not None
        return getattr(self, item, None) is not None

    def __getitem__(self, item: str) -> TargetValue:
        val = getattr(self, item, None)
        if val is None and "protein" in item:
            val = self.protein_min
        return TargetValue(float(val) if val is not None else 0.0)

    def get(self, item: str, default: Any = None) -> Any:
        if "protein" in item:
            return self.protein_min if self.protein_min is not None else default
        return getattr(self, item, default)

class ProductBrief(BaseModel):
    category: Optional[str] = None
    product_type: Optional[str] = None
    description: Optional[str] = None

    texture_requirements: List[str] = Field(default_factory=list)
    mouthfeel_requirements: List[str] = Field(default_factory=list)

    dietary_requirements: List[str] = Field(default_factory=list)
    allergen_constraints: List[str] = Field(default_factory=list)

    nutrition_targets: NutritionTargets = Field(default_factory=NutritionTargets)

    functional_goals: List[str] = Field(default_factory=list)

    flavor_profile: List[str] = Field(default_factory=list)
    aroma_profile: List[str] = Field(default_factory=list)

    processing_constraints: List[str] = Field(default_factory=list)
    shelf_life_requirements: Optional[str] = None

    water_activity_target: Optional[str] = None  # E.g. "LOW" or "0.55" if explicit
    pH_target: Optional[str] = None

    regulatory_market: List[str] = Field(default_factory=list)
    cost_target: Optional[float] = None

    excluded_ingredients: List[str] = Field(default_factory=list)
    preferred_ingredients: List[str] = Field(default_factory=list)

    required_claims: List[str] = Field(default_factory=list)
    prohibited_claims: List[str] = Field(default_factory=list)

    # Added: Hard Constraints, Soft Objectives & Dynamic Experiment Strategies
    hard_constraints: List[str] = Field(default_factory=list)
    soft_objectives: List[str] = Field(default_factory=list)
    experiment_strategies: List[str] = Field(default_factory=list)

    @property
    def dietary_constraints(self) -> List[str]:
        return [d.lower() for d in self.dietary_requirements]

    @property
    def exclusions(self) -> List[str]:
        return self.excluded_ingredients

class ProductBriefParser:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.llm = None
        if self.api_key and ChatGroq:
            try:
                self.llm = ChatGroq(
                    model_name="llama-3.3-70b-versatile",
                    temperature=0.0,
                    groq_api_key=self.api_key
                )
            except Exception as e:
                logger.warning(f"Groq LLM init warning: {e}")

    def parse(self, user_prompt: str) -> ProductBrief:
        """Parses natural language prompt into normalized ProductBrief."""
        return self.extract(user_prompt)

    def extract(self, user_prompt: str) -> ProductBrief:
        """Extracts requirements from natural language prompt."""
        if not user_prompt or not user_prompt.strip():
            return ProductBrief()

        p_lower = user_prompt.lower()
        dietary = []
        excluded = []
        textures = []
        flavors = []
        claims = []
        nutrition = NutritionTargets()
        category = "General"
        product_type = "general_food"

        # Categorization
        if "chocolate" in p_lower or "bar" in p_lower:
            category = "Confectionery & Chocolate"
            product_type = "chocolate_bar"
        elif "bread" in p_lower or "bakery" in p_lower:
            category = "Bakery & Bread"
            product_type = "bakery_bread"
        elif "snack" in p_lower:
            category = "Snacks & Savory"
            product_type = "snack"
        elif "beverage" in p_lower or "drink" in p_lower:
            category = "Beverage"
            product_type = "beverage"

        # Dietary Requirements
        if "vegan" in p_lower:
            dietary.append("Vegan")
            excluded.extend(["dairy", "milk", "egg", "whey", "butter", "gelatin"])
        if "gluten-free" in p_lower or "gluten free" in p_lower:
            dietary.append("Gluten-Free")
            excluded.extend(["wheat", "rye", "barley", "gluten"])
        if "dairy-free" in p_lower or "dairy free" in p_lower or "no dairy" in p_lower:
            dietary.append("Dairy-Free")
            excluded.extend(["dairy", "milk", "whey", "butter"])
        if "allergen-free" in p_lower or "allergen free" in p_lower:
            dietary.append("Allergen-Free")
            excluded.extend(["peanuts", "tree nuts", "soy", "dairy", "eggs", "wheat"])

        # Explicit Protein
        prot_match = re.search(r"(\d+(?:\.\d+)?)\s*%\s*protein", p_lower)
        if prot_match:
            nutrition.protein_min = float(prot_match.group(1))
        elif "high protein" in p_lower or "protein" in p_lower:
            nutrition.protein_min = 15.0

        # Cost Target
        cost_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:dollar|\$|usd|inr)\s*/?\s*kg", p_lower)
        cost_target = float(cost_match.group(1)) if cost_match else None

        # Explicit / Qualitative Water Activity
        water_act = None
        aw_num = re.search(r"aw\s*=?\s*(\d+(?:\.\d+)?)", p_lower)
        if aw_num:
            water_act = aw_num.group(1)
        elif "low water activity" in p_lower or "aw" in p_lower:
            water_act = "0.60"

        # Textures
        if "smooth" in p_lower: textures.append("Smooth")
        if "creamy" in p_lower: textures.append("Creamy")
        if "soft" in p_lower: textures.append("Soft")
        if "crunchy" in p_lower: textures.append("Crunchy")
        if "chewy" in p_lower: textures.append("Chewy")

        # Flavors
        if "cocoa" in p_lower: flavors.append("clean cocoa")
        if "vanilla" in p_lower: flavors.append("vanilla")
        if "berry" in p_lower: flavors.append("wild berry")

        # Claims
        if "efsa" in p_lower or "digestive" in p_lower:
            claims.append("Digestive Health EFSA Claim")

        # Shelf life
        shelf_match = re.search(r"(\d+)\s*-?\s*(?:day|month)", p_lower)
        shelf_life = f"{shelf_match.group(0)}" if shelf_match else "9 months"

        # Build Hard Constraints list
        hard_constraints = []
        for d in dietary:
            hard_constraints.append(f"DIETARY_EXCLUSIVE_{d.upper().replace('-', '_')}")
        if excluded:
            hard_constraints.append("EXCLUDED_INGREDIENTS_PROHIBITION")

        # Build Soft Objectives
        soft_objectives = []
        if nutrition.protein_min:
            soft_objectives.append("MAXIMIZE_PROTEIN_DENSITY")
        if "low cost" in p_lower or "cost" in p_lower or cost_target is not None:
            soft_objectives.append("MINIMIZE_RAW_MATERIAL_COST")
        if textures:
            soft_objectives.append("OPTIMIZE_TEXTURE_AND_MOUTHFEEL")
        if "clean label" in p_lower or "prebiotic" in p_lower or "fiber" in p_lower:
            soft_objectives.append("MAXIMIZE_CLEAN_LABEL_FIBER")

        # Determine Dynamic Experiment Strategies
        experiment_strategies = ["nutrition_maximized", "cost_optimized", "balanced", "functionality_texture"]
        if "clean label" in p_lower or "fiber" in p_lower:
            experiment_strategies.append("clean_label_fiber")

        return ProductBrief(
            category=category,
            product_type=product_type,
            description=user_prompt,
            texture_requirements=textures,
            dietary_requirements=dietary,
            allergen_constraints=list(set(excluded)),
            nutrition_targets=nutrition,
            flavor_profile=flavors,
            water_activity_target=water_act,
            shelf_life_requirements=shelf_life,
            excluded_ingredients=list(set(excluded)),
            required_claims=claims,
            cost_target=cost_target,
            hard_constraints=hard_constraints,
            soft_objectives=soft_objectives,
            experiment_strategies=experiment_strategies
        )

# Global singleton instance
product_brief_parser = ProductBriefParser()

# Backward compatibility aliases
requirements_extractor = product_brief_parser
FormulationRequirements = ProductBrief
