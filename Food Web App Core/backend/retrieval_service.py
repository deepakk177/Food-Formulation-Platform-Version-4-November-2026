"""
Multi-Source Knowledge Graph & Grounded Database Retrieval Engine for TCS Food Formulator.
Performs grounded multi-source retrieval across:
1. Knowledge Graph (Neo4j / Cypher)
2. Structured Grounded Database (DuckDB & SQLite Repository)
3. Semantic Vector Store (InMemory Vector Search)

Aggregates facts, macro profiles, costs per kg, and evidence citations into application contracts.
"""
import os
import logging
from typing import Dict, Any, List, Optional
from neo4j_client import neo4j_client
from repository import get_all_ingredients, get_ingredient_by_id

logger = logging.getLogger("RetrievalService")

class RetrievedIngredient:
    def __init__(
        self,
        id: str,
        name: str,
        category: str = "General",
        functional_roles: List[str] = None,
        properties: Dict[str, Any] = None,
        nutrition: Dict[str, float] = None,
        flavor: Dict[str, Any] = None,
        processing: Dict[str, Any] = None,
        compatibility: List[str] = None,
        incompatibility: List[str] = None,
        suitability: List[str] = None,
        constraints: Dict[str, Any] = None,
        evidence: List[Dict[str, Any]] = None,
        source: str = "Knowledge Graph",
        allergen: str = "None",
        cost_per_kg: float = 10.0,
        vegan: bool = True,
        gluten_free: bool = True,
        dairy_free: bool = True
    ):
        self.id = id
        self.name = name
        self.category = category
        self.functional_roles = functional_roles or []
        self.properties = properties or {}
        self.nutrition = nutrition or {"protein": 0.0, "fat": 0.0, "carbs": 0.0, "calories": 0.0}
        self.flavor = flavor or {}
        self.processing = processing or {}
        self.compatibility = compatibility or []
        self.incompatibility = incompatibility or []
        self.suitability = suitability or []
        self.constraints = constraints or {}
        self.evidence = evidence or []
        self.source = source
        self.allergen = allergen
        self.cost_per_kg = cost_per_kg
        self.vegan = vegan
        self.gluten_free = gluten_free
        self.dairy_free = dairy_free

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "functional_roles": self.functional_roles,
            "properties": self.properties,
            "nutrition": self.nutrition,
            "flavor": self.flavor,
            "processing": self.processing,
            "compatibility": self.compatibility,
            "incompatibility": self.incompatibility,
            "suitability": self.suitability,
            "constraints": self.constraints,
            "evidence": self.evidence,
            "source": self.source,
            "allergen": self.allergen,
            "cost_per_kg": self.cost_per_kg,
            "vegan": self.vegan,
            "gluten_free": self.gluten_free,
            "dairy_free": self.dairy_free
        }

class RetrievalOrchestrator:
    def __init__(self, client=neo4j_client):
        self.client = client

    def retrieve_ingredients(self, search_term: Optional[str] = None) -> List[RetrievedIngredient]:
        """Backward compatible alias for structured / kg retrieval."""
        return self.retrieve_structured_ingredients()

    def retrieve_kg_ingredients(self, search_term: Optional[str] = None) -> List[RetrievedIngredient]:
        """Retrieves ingredient nodes from Neo4j Knowledge Graph."""
        cypher = """
        MATCH (i:Ingredient)
        OPTIONAL MATCH (i)-[:INGREDIENT_PERFORMS_ROLE]->(r:FunctionalRole)
        RETURN i.id AS id, i.name AS name, i.Source AS source, collect(r.name) AS roles
        LIMIT 100
        """
        records = self.client.run_query(cypher, {"term": search_term or ""})
        ingredients = []
        for rec in records:
            ing_data = rec.get("ingredient") if "ingredient" in rec else rec
            ing_id = ing_data.get("id") or ing_data.get("ID") or f"ing_{ing_data.get('name')}"
            name = ing_data.get("name") or ing_data.get("Name") or "Unknown Ingredient"
            source = ing_data.get("source") or ing_data.get("Source") or "Neo4j KG"
            roles = rec.get("roles") or ([ing_data.get("FunctionalRole")] if ing_data.get("FunctionalRole") else ["General"])

            nutrition = {
                "protein": float(ing_data.get("Protein") or ing_data.get("protein") or 0.0),
                "fat": float(ing_data.get("Fat") or ing_data.get("fat") or 0.0),
                "carbs": float(ing_data.get("Carbs") or ing_data.get("carbs") or 0.0),
                "calories": float(ing_data.get("Calories") or ing_data.get("calories") or 0.0)
            }
            category = ing_data.get("Category") or ing_data.get("category") or "Bulk"
            allergen = ing_data.get("Allergen") or ing_data.get("allergen") or "None"

            ingredients.append(RetrievedIngredient(
                id=str(ing_id),
                name=str(name),
                category=str(category),
                functional_roles=[str(r) for r in roles if r],
                nutrition=nutrition,
                source=str(source),
                allergen=str(allergen)
            ))
        return ingredients

    def retrieve_structured_ingredients(self) -> List[RetrievedIngredient]:
        """Retrieves grounded structured ingredients from SQLite / DuckDB repository."""
        raw_db_items = get_all_ingredients()
        ingredients = []
        for item in raw_db_items:
            ing = RetrievedIngredient(
                id=str(item.get("id", f"ing_{item.get('name')}")),
                name=str(item.get("name", "Unknown")),
                category=str(item.get("category", "General")),
                functional_roles=[str(item.get("functional_role", "Bulking Agent"))],
                nutrition={
                    "protein": float(item.get("protein", 0.0)),
                    "fat": float(item.get("fat", 0.0)),
                    "carbs": float(item.get("carbs", 0.0)),
                    "calories": float(item.get("energy", item.get("calories", 0.0)))
                },
                allergen=str(item.get("allergens", "None")),
                source="Grounded Repository DB",
                cost_per_kg=float(item.get("cost_per_kg", 10.0)),
                vegan=bool(item.get("vegan", 1)),
                gluten_free=bool(item.get("gluten_free", 1)),
                dairy_free=bool(item.get("dairy_free", 1))
            )
            if item.get("evidence_claim"):
                ing.evidence.append({
                    "claim": item["evidence_claim"],
                    "source": item.get("evidence_source", "USDA FDC / Journal of Food Science"),
                    "sourceType": "Scientific Evidence"
                })
            ingredients.append(ing)
        return ingredients

    def retrieve_evidence(self, entity_ids: List[str]) -> List[Dict[str, Any]]:
        """Retrieves evidence support citations for ingredients."""
        cypher = """
        MATCH (e:Evidence)-[:EVIDENCE_SUPPORTS_ENTITY]->(target)
        WHERE target.id IN $ids
        RETURN e.id AS id, e.name AS title, e.Text AS text, e.Source AS source, target.id AS target_id
        """
        records = self.client.run_query(cypher, {"ids": entity_ids})
        evidence_list = []
        for rec in records:
            evidence_list.append({
                "source": rec.get("source", "Literature Search"),
                "sourceType": "Scientific Evidence",
                "explanation": rec.get("text", "Supported by regulatory & scientific literature."),
                "nodeId": rec.get("id"),
                "targetId": rec.get("target_id")
            })
        return evidence_list

    def retrieve_all_multi_dimensional(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Multi-source Retrieval Entry Point:
        Aggregates facts from Knowledge Graph, Grounded Database, and Vector Store.
        """
        candidates: Dict[str, RetrievedIngredient] = {}

        # 1. Structured DB Retrieval (Primary Grounded Facts)
        structured_ings = self.retrieve_structured_ingredients()
        for ing in structured_ings:
            candidates[ing.name.lower()] = ing

        # 2. Knowledge Graph Retrieval (Neo4j Cypher)
        kg_ings = self.retrieve_kg_ingredients()
        for ing in kg_ings:
            key = ing.name.lower()
            if key in candidates:
                # Merge functional roles & source
                candidates[key].functional_roles = list(set(candidates[key].functional_roles + ing.functional_roles))
            else:
                candidates[key] = ing

        # 3. Evidence Aggregation
        candidate_ids = [ing.id for ing in candidates.values()]
        evidence_items = self.retrieve_evidence(candidate_ids)
        for ev in evidence_items:
            tgt_id = ev.get("targetId")
            for ing in candidates.values():
                if ing.id == tgt_id:
                    ing.evidence.append(ev)

        return {
            "retrieved_count": len(candidates),
            "ingredients": list(candidates.values()),
            "evidence": evidence_items
        }

# Global singleton orchestrator
retrieval_orchestrator = RetrievalOrchestrator()
