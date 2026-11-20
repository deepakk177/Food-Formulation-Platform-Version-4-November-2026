"""
Grounded LLM Reasoning & Synthesis Engine for TCS Food Formulator.
Synthesizes scientific justifications, process recommendations, and evidence summaries
from validated candidates without inventing raw factual data, fake shelf lives, or altered numbers.
Strictly acts as an explanation and narrative-generation layer over deterministic backend calculations.
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

from groq_client import generate_chat_completion

logger = logging.getLogger("SynthesisEngine")

SYSTEM_SYNTHESIS_PROMPT = """\
You are an expert Principal Food Scientist at TCS Research.
Generate a grounded food formulation explanation based ONLY on the supplied validated candidate set and evidence.

Strict Rules:
1. Do NOT introduce any ingredient that is not present in the supplied validated candidate set.
2. Do NOT invent or alter ingredient percentages, quantities, nutritional values, regulatory status, or costs.
3. If any property, process recommendation, or shelf-life prediction is not verified, explicitly state 'INSUFFICIENT_LABELED_DATA' or 'REQUIRES_LABORATORY_VALIDATION'.
4. Explain the functional purpose of each selected ingredient and cite its evidence provenance.
5. Provide actionable, sequential process recommendations for manufacturing.
6. Output your response as a valid JSON object matching this structure:

{
  "title": "<Formulation Title>",
  "justification_summary": "<Explanation of why this formulation satisfies requirements>",
  "ingredient_explanations": [
    {
      "ingredientId": "<id>",
      "name": "<name>",
      "functionalRole": "<role>",
      "justification": "<why selected>",
      "evidenceSource": "<source>"
    }
  ],
  "process_recommendations": [
    "<Step 1>",
    "<Step 2>",
    "<Step 3>"
  ],
  "sensory_predictions": {
    "texture": "INSUFFICIENT_LABELED_DATA (Requires laboratory texture profile analysis)",
    "mouthfeel": "INSUFFICIENT_LABELED_DATA (Requires descriptive sensory panel)",
    "viscosity": "INSUFFICIENT_LABELED_DATA (Requires rotational rheometer testing)",
    "shelf_life": "INSUFFICIENT_LABELED_DATA (Requires accelerated stability kinetics testing)"
  },
  "warnings": []
}
"""

class SynthesisEngine:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "")

    def synthesize(
        self,
        query: str,
        requirements: Dict[str, Any],
        ranked_candidate: Dict[str, Any],
        evidence_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Synthesizes final formulation report narrative.
        All numerical values, composition tables, costs, and compliance results are locked
        to deterministic backend calculations and cannot be altered by the LLM.
        """
        composition = ranked_candidate.get("composition", {})
        all_components = composition.get("all_components", [])
        if not all_components:
            bulk = composition.get("bulk_ingredients", [])
            func = composition.get("functional_ingredients", [])
            all_components = bulk + func

        cat_str = requirements.get("category") or requirements.get("product_type") or "Food Matrix"
        prod_type = str(cat_str).replace("_", " ").title()
        
        default_process_steps = ranked_candidate.get("process_steps")
        if not default_process_steps or len(default_process_steps) < 3:
            default_process_steps = [
                f"1. Measure and pre-blend dry formulation ingredients uniformly according to ratio specifications.",
                f"2. Incorporate liquid/fat matrix and functional ingredients under controlled shear to achieve homogeneous dispersion.",
                f"3. Form, package, and hermetically seal under controlled ambient conditions to preserve {prod_type} stability."
            ]

        # Valid ingredient IDs and names from the deterministic candidate
        valid_comp_map = {
            (c.get("id") or f"ing_{c.get('name','').lower().replace(' ','_')}"): c.get("name")
            for c in all_components
        }
        valid_comp_names = {c.get("name", "").lower(): c for c in all_components}

        # Attempt Groq LLM synthesis for narrative explanation
        context_str = json.dumps({
            "user_query": query,
            "requirements": requirements,
            "validated_candidate_set": [
                {
                    "id": c.get("id"),
                    "name": c.get("name"),
                    "percentage": c.get("percentage"),
                    "role": c.get("functional_role"),
                    "cost_per_kg": c.get("cost_per_kg"),
                    "protein": c.get("protein")
                }
                for c in all_components
            ],
            "evidence": evidence_list[:5]
        }, indent=2)

        messages = [
            {"role": "system", "content": SYSTEM_SYNTHESIS_PROMPT},
            {"role": "user", "content": f"Validated Candidate Set & Evidence:\n{context_str}"}
        ]

        llm_content = generate_chat_completion(messages=messages, temperature=0.1)
        if llm_content:
            try:
                content = llm_content.strip()
                if content.startswith("```json"):
                    content = content.split("```json")[1].split("```")[0].strip()
                elif content.startswith("```"):
                    content = content.split("```")[1].split("```")[0].strip()

                parsed = json.loads(content)
                
                # Strict Sanitization: filter ingredient_explanations to ONLY valid ingredients
                sanitized_explanations = []
                for exp in parsed.get("ingredient_explanations", []):
                    exp_id = exp.get("ingredientId")
                    exp_name = str(exp.get("name", "")).lower()
                    if exp_id in valid_comp_map or exp_name in valid_comp_names:
                        matched = valid_comp_names.get(exp_name) or {}
                        sanitized_explanations.append({
                            "ingredientId": exp_id or matched.get("id"),
                            "name": exp.get("name") or matched.get("name"),
                            "functionalRole": exp.get("functionalRole") or matched.get("functional_role", "Raw Material"),
                            "justification": exp.get("justification", ""),
                            "evidenceSource": exp.get("evidenceSource") or matched.get("source_evidence", "Grounded DB")
                        })

                # If LLM missed any components, fill them deterministically
                explained_names = {e["name"].lower() for e in sanitized_explanations}
                for c in all_components:
                    if c.get("name", "").lower() not in explained_names:
                        role = c.get("functional_role") or c.get("category") or "Bulking Agent"
                        sanitized_explanations.append({
                            "ingredientId": c.get("id", f"ing_{c.get('name', '001').lower().replace(' ', '_')}"),
                            "name": c.get("name"),
                            "functionalRole": role,
                            "justification": f"Fulfills '{role}' in {prod_type} matrix at {c.get('percentage', 0.0)}% inclusion.",
                            "evidenceSource": c.get("source_evidence") or "Grounded Repository DB"
                        })

                # Lock down numerical and physical structures from backend
                parsed["composition"] = composition
                parsed["ingredient_explanations"] = sanitized_explanations
                parsed["performance"] = ranked_candidate.get("score", {}).get("performance", {})
                parsed["functional_coverage"] = ranked_candidate.get("functional_coverage", {})
                if not parsed.get("process_recommendations") or len(parsed.get("process_recommendations")) < 3:
                    parsed["process_recommendations"] = default_process_steps

                # Enforce honest status for sensory & shelf life
                parsed["sensory_predictions"] = {
                    "texture": "INSUFFICIENT_LABELED_DATA (Requires laboratory texture profile analysis)",
                    "mouthfeel": "INSUFFICIENT_LABELED_DATA (Requires trained descriptive panel)",
                    "viscosity": "INSUFFICIENT_LABELED_DATA (Requires rotational rheometer testing)",
                    "shelf_life": "INSUFFICIENT_LABELED_DATA (Requires accelerated stability kinetics testing)"
                }
                return parsed
            except Exception as e:
                logger.warning(f"Groq LLM synthesis parsing fallback: {e}")

        # Deterministic Grounded Synthesis Fallback
        ing_explanations = []
        for ing in all_components:
            role = ing.get("functional_role") or ing.get("category") or "Bulking Agent"
            prov = ing.get("source_evidence") or ing.get("source") or "Grounded Repository DB"
            ing_explanations.append({
                "ingredientId": ing.get("id", f"ing_{ing.get('name', '001').lower().replace(' ', '_')}"),
                "name": ing.get("name"),
                "functionalRole": role,
                "justification": f"Selected to fulfill '{role}' functionality. Inclusion = {ing.get('percentage', 0.0)}%.",
                "evidenceSource": prov
            })

        return {
            "title": f"Grounded AI {prod_type} Formulation",
            "justification_summary": f"Formulation generated from grounded Knowledge Graph retrieval for brief '{query}'. Satisfies dietary constraints and mathematical mass balance.",
            "composition": composition,
            "ingredient_explanations": ing_explanations,
            "performance": ranked_candidate.get("score", {}).get("performance", {}),
            "functional_coverage": ranked_candidate.get("functional_coverage", {}),
            "process_recommendations": default_process_steps,
            "sensory_predictions": {
                "texture": "INSUFFICIENT_LABELED_DATA (Requires laboratory texture profile analysis)",
                "mouthfeel": "INSUFFICIENT_LABELED_DATA (Requires trained descriptive panel)",
                "viscosity": "INSUFFICIENT_LABELED_DATA (Requires rotational rheometer testing)",
                "shelf_life": "INSUFFICIENT_LABELED_DATA (Requires accelerated stability kinetics testing)"
            },
            "warnings": []
        }

# Global singleton instance
synthesis_engine = SynthesisEngine()
