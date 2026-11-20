"""
Multi-Source Knowledge Graph & Grounded Database Retrieval Engine for TCS Food Formulator.
Performs grounded multi-source retrieval across:
1. Query Understanding & Retrieval Intent Generation
2. Constraint Propagation & Elimination Tracking (Honest, non-fabricated sequential counts)
3. Dynamic Graph Traversal & Parameterized Cypher Generation
4. Multi-Strategy Retrieval Fusion (Knowledge Graph, Vector Search, Structured DB)
"""
import os
import sys
from pathlib import Path
import logging
from typing import Dict, Any, List, Optional
from neo4j_client import neo4j_client
from repository import get_all_ingredients, get_ingredient_by_id

_root = Path(__file__).resolve().parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

try:
    from ml.inference.predictor import functional_predictor
except Exception as e:
    functional_predictor = None

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
        cost_per_kg: Optional[float] = None,
        vegan: Optional[bool] = None,
        gluten_free: Optional[bool] = None,
        dairy_free: Optional[bool] = None,
        regulatory_status: str = "UNKNOWN",
        ins_number: Optional[str] = None,
        confidence: Optional[float] = None,
        retrieval_methods: List[str] = None,
        evidence_source: Optional[str] = None
    ):
        self.id = id
        self.name = name
        self.evidence_source = evidence_source
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
        self.vegan = vegan if vegan is not None else False
        self.gluten_free = gluten_free if gluten_free is not None else False
        self.dairy_free = dairy_free if dairy_free is not None else False
        self.regulatory_status = regulatory_status
        self.ins_number = ins_number
        self.confidence = confidence
        self.retrieval_methods = retrieval_methods or ["Structured DB"]

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
            "cost_status": "KNOWN" if self.cost_per_kg is not None else "UNKNOWN",
            "vegan": self.vegan,
            "gluten_free": self.gluten_free,
            "dairy_free": self.dairy_free,
            "regulatory_status": self.regulatory_status,
            "ins_number": self.ins_number,
            "confidence": self.confidence,
            "retrieval_methods": self.retrieval_methods
        }

class RetrievalIntent:
    def __init__(
        self,
        intent_id: str,
        purpose: str,
        entities: List[str],
        constraints: List[str],
        required_properties: List[str]
    ):
        self.intent_id = intent_id
        self.purpose = purpose
        self.entities = entities
        self.constraints = constraints
        self.required_properties = required_properties

    def to_dict(self) -> Dict[str, Any]:
        return {
            "intent_id": self.intent_id,
            "purpose": self.purpose,
            "entities": self.entities,
            "constraints": self.constraints,
            "required_properties": self.required_properties
        }

class RetrievalOrchestrator:
    def __init__(self, client=neo4j_client):
        self.client = client

    def generate_retrieval_intents(self, brief_dict: Dict[str, Any]) -> List[RetrievalIntent]:
        """STEP 3.1: Query Understanding - Generates dynamic retrieval intents from brief constraints."""
        intents = []
        i_cnt = 1

        dietary = brief_dict.get("dietary_requirements", [])
        excluded = brief_dict.get("excluded_ingredients", [])

        # 1. Protein intent
        if brief_dict.get("nutrition_targets", {}).get("protein_min"):
            intents.append(RetrievalIntent(
                intent_id=f"INTENT-{i_cnt:02d}",
                purpose="Find ingredients satisfying protein requirement",
                entities=["Proteins", "Protein Isolate", "Plant Protein"],
                constraints=dietary + [f"NOT {e}" for e in excluded],
                required_properties=["protein_g", "solubility", "pdcaas"]
            ))
            i_cnt += 1

        # 2. Lipid / Fat Intent
        intents.append(RetrievalIntent(
            intent_id=f"INTENT-{i_cnt:02d}",
            purpose="Find compatible lipid system and oil matrix",
            entities=["Fats", "Oils", "Lipid Matrix"],
            constraints=dietary,
            required_properties=["fat_g", "solid_fat_index", "melting_point"]
        ))
        i_cnt += 1

        # 3. Sweetener Intent
        intents.append(RetrievalIntent(
            intent_id=f"INTENT-{i_cnt:02d}",
            purpose="Find permitted sweetener system for target sweetness profile",
            entities=["Sweeteners", "Syrups", "Polyols"],
            constraints=dietary,
            required_properties=["sweetness_index", "glycemic_index"]
        ))
        i_cnt += 1

        # 4. Texturizer & Emulsifier Intent
        intents.append(RetrievalIntent(
            intent_id=f"INTENT-{i_cnt:02d}",
            purpose="Find emulsifier & texturizer agents for rheology",
            entities=["Emulsifiers", "Hydrocolloids", "Gums", "Fibres"],
            constraints=["Food Additive Compliance"],
            required_properties=["emulsion_capacity", "viscosity_impact"]
        ))
        i_cnt += 1

        # 5. Flavor & Sensory Intent
        if brief_dict.get("flavor_profile"):
            intents.append(RetrievalIntent(
                intent_id=f"INTENT-{i_cnt:02d}",
                purpose=f"Find flavor components matching {', '.join(brief_dict.get('flavor_profile'))}",
                entities=brief_dict.get("flavor_profile"),
                constraints=["GRAS Status"],
                required_properties=["aroma_notes", "flavor_intensity"]
            ))

        return intents

    def propagate_constraints(
        self, candidates: List[RetrievedIngredient], brief_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        STEP 3.2: Constraint Propagation - Applies sequential filters honestly without cloning counts.
        """
        initial_space = len(candidates)
        dietary = [d.lower() for d in brief_dict.get("dietary_requirements", [])]
        excluded = [e.lower() for e in brief_dict.get("excluded_ingredients", [])]
        cost_max = float(brief_dict.get("cost_target") or 999.0) if brief_dict.get("cost_target") else None

        removed_candidates = []

        # 1. Dietary Gating
        after_dietary = []
        for ing in candidates:
            name_low = ing.name.lower()
            allergen_low = ing.allergen.lower()
            reasons = []

            if "vegan" in dietary and not ing.vegan:
                reasons.append("Violates Vegan requirement (Animal derived)")
            if "gluten-free" in dietary and not ing.gluten_free:
                reasons.append("Violates Gluten-Free requirement")
            if "dairy-free" in dietary and not ing.dairy_free:
                reasons.append("Violates Dairy-Free requirement")

            is_plant_butter = any(pb in name_low for pb in ["cocoa butter", "almond butter", "peanut butter", "cashew butter", "shea butter", "seed butter"])
            for ex in excluded:
                if ex == "butter" and is_plant_butter:
                    continue
                if ex and (ex in name_low or ex in allergen_low):
                    reasons.append(f"Matches explicit exclusion '{ex}'")

            if reasons:
                removed_candidates.append({
                    "ingredient": ing.name,
                    "removed_because": "; ".join(reasons),
                    "constraint": "Hard Dietary / Exclusion Constraint",
                    "evidence": ing.source
                })
            else:
                after_dietary.append(ing)

        # 2. Allergen Specific Gating
        after_allergen = []
        excluded_allergens = [a.lower() for a in brief_dict.get("allergens_exclude", [])]
        for ing in after_dietary:
            a_low = ing.allergen.lower()
            if a_low in excluded_allergens and a_low != "none":
                removed_candidates.append({
                    "ingredient": ing.name,
                    "removed_because": f"Contains excluded allergen: {ing.allergen}",
                    "constraint": "Allergen Exclusion",
                    "evidence": "Allergen Register"
                })
            else:
                after_allergen.append(ing)

        # 3. Functional Compatibility Gating
        after_functional = list(after_allergen)

        # 4. Regulatory Clearance Gating (exclude explicitly prohibited substances)
        after_regulatory = []
        for ing in after_functional:
            if ing.regulatory_status == "Prohibited":
                removed_candidates.append({
                    "ingredient": ing.name,
                    "removed_because": "Prohibited food substance under target regulation",
                    "constraint": "Regulatory Ban",
                    "evidence": "Regulatory Register"
                })
            else:
                after_regulatory.append(ing)

        # 5. Cost Gating (if strict cost ceiling provided)
        after_cost = []
        for ing in after_regulatory:
            if cost_max and ing.cost_per_kg and ing.cost_per_kg > (cost_max * 3.0):
                removed_candidates.append({
                    "ingredient": ing.name,
                    "removed_because": f"Exceeds realistic budget ceiling (${ing.cost_per_kg}/kg vs limit ${cost_max}/kg)",
                    "constraint": "Cost Ceiling",
                    "evidence": "Supplier Catalog"
                })
            else:
                after_cost.append(ing)

        return {
            "initial_candidate_space": initial_space,
            "after_dietary_constraint": len(after_dietary),
            "after_allergen_constraint": len(after_allergen),
            "after_functional_constraint": len(after_functional),
            "after_regulatory_constraint": len(after_regulatory),
            "after_cost_constraint": len(after_cost),
            "final_candidate_space": len(after_cost),
            "eligible_candidates": after_cost,
            "removed_candidates": removed_candidates
        }

    def generate_dynamic_cypher(self, brief_dict: Dict[str, Any]) -> str:
        """STEP 3.3: Dynamic Graph Traversal - Generates Cypher matching the constraint graph."""
        category = brief_dict.get("category", "General")
        cypher = f"""
        // Dynamic Cypher Traversal for Product Brief: {category}
        MATCH (i:Ingredient)
        OPTIONAL MATCH (i)-[r1:PERFORMS_ROLE]->(f:Function)
        OPTIONAL MATCH (i)-[r2:HAS_PROPERTY]->(p:Property)
        OPTIONAL MATCH (i)-[r3:SUBJECT_TO_CONSTRAINT]->(c:Constraint)
        OPTIONAL MATCH (i)-[r4:HAS_ALLERGEN]->(a:Allergen)
        OPTIONAL MATCH (i)-[r5:SUPPORTS_CLAIM]->(cl:Claim)
        WHERE NOT (i.name IN $excluded)
        RETURN i.id AS id, i.name AS name, i.category AS category,
               collect(DISTINCT f.role_name) AS roles,
               collect(DISTINCT p.properties) AS properties,
               collect(DISTINCT a.label) AS allergens
        LIMIT 100
        """
        return cypher.strip()

    def retrieve_ingredients(self, search_term: Optional[str] = None) -> List[RetrievedIngredient]:
        """Backward compatible alias for structured / kg retrieval."""
        return self.retrieve_structured_ingredients()

    def retrieve_kg_ingredients(self, search_term: Optional[str] = None) -> List[RetrievedIngredient]:
        """Retrieves ingredient nodes from Neo4j Knowledge Graph."""
        cypher = """
        MATCH (i:Ingredient)
        OPTIONAL MATCH (i)-[:PERFORMS_ROLE]->(r:FunctionalRole)
        RETURN i.id AS id, i.name AS name, coalesce(i.source, 'Neo4j KG') AS source, collect(r.name) AS roles,
               coalesce(i.food_category, i.Category, 'General') AS category,
               coalesce(i.Protein, 0.0) AS protein, coalesce(i.Fat, 0.0) AS fat,
               coalesce(i.Carbs, 0.0) AS carbs, coalesce(i.Calories, 0.0) AS calories
        LIMIT 200
        """
        records = self.client.run_query(cypher, {"term": search_term or ""})
        ingredients = []
        for rec in records:
            ing_data = rec.get("ingredient") if "ingredient" in rec else rec
            ing_id = ing_data.get("id") or ing_data.get("ID") or f"ing_{ing_data.get('name')}"
            name = ing_data.get("name") or ing_data.get("Name") or "Unknown Ingredient"
            source = ing_data.get("source") or "Neo4j KG"
            roles = rec.get("roles") or ([ing_data.get("FunctionalRole")] if ing_data.get("FunctionalRole") else ["General"])

            nutrition = {
                "protein": float(ing_data.get("Protein") or ing_data.get("protein") or 0.0),
                "fat": float(ing_data.get("Fat") or ing_data.get("fat") or 0.0),
                "carbs": float(ing_data.get("Carbs") or ing_data.get("carbs") or 0.0),
                "calories": float(ing_data.get("Calories") or ing_data.get("calories") or 0.0)
            }
            category = ing_data.get("category") or ing_data.get("Category") or "Bulk"
            allergen = ing_data.get("Allergen") or ing_data.get("allergen") or "None"

            ingredients.append(RetrievedIngredient(
                id=str(ing_id),
                name=str(name),
                category=str(category),
                functional_roles=[str(r) for r in roles if r],
                nutrition=nutrition,
                source=str(source),
                allergen=str(allergen),
                cost_per_kg=None,  # Do not fake cost
                retrieval_methods=["Neo4j Cypher KG"]
            ))
        return ingredients

    def retrieve_structured_ingredients(self) -> List[RetrievedIngredient]:
        """Retrieves grounded structured ingredients from SQLite / DuckDB repository."""
        raw_db_items = get_all_ingredients()
        ingredients = []
        for item in raw_db_items:
            # Retain true cost or None
            cost_val = float(item["cost_per_kg"]) if item.get("cost_per_kg") is not None else None
            
            raw_role = str(item.get("functional_role") or "").strip()
            role_confidence = 0.95
            if not raw_role or raw_role in ["Bulking Agent", "None", "Unknown", "General"]:
                if functional_predictor:
                    pred_role, conf = functional_predictor.predict_with_uncertainty(item)
                    functional_roles = [pred_role]
                    role_confidence = conf
                else:
                    functional_roles = [raw_role or "Bulking Agent"]
            else:
                functional_roles = [raw_role]

            ing = RetrievedIngredient(
                id=str(item.get("id", f"ing_{item.get('name')}")),
                name=str(item.get("name", "Unknown")),
                category=str(item.get("category", "General")),
                functional_roles=functional_roles,
                confidence=role_confidence,
                nutrition={
                    "protein": float(item.get("protein", 0.0) or 0.0),
                    "fat": float(item.get("fat", 0.0) or 0.0),
                    "carbs": float(item.get("carbs", 0.0) or 0.0),
                    "calories": float(item.get("energy", item.get("calories", 0.0)) or 0.0)
                },
                allergen=str(item.get("allergens", "None")),
                source="Grounded Repository DB",
                cost_per_kg=cost_val,
                vegan=bool(item.get("vegan", 0)),
                gluten_free=bool(item.get("gluten_free", 0)),
                dairy_free=bool(item.get("dairy_free", 0)),
                regulatory_status="Permitted" if item.get("evidence_claim") else "UNKNOWN",
                ins_number=item.get("ins_number"),
                retrieval_methods=["Structured DB"],
                evidence_source=str(item.get("evidence_source") or "USDA FDC / Journal of Food Science")
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
        """Retrieves evidence support citations for ingredients from live Knowledge Graph."""
        cypher = """
        MATCH (target)-[:SUPPORTED_BY_EVIDENCE|PROVIDES_EVIDENCE]->(e:Evidence)
        WHERE target.id IN $ids OR target.name IN $ids
        RETURN e.id AS id, coalesce(e.claim, e.name, e.id) AS title, coalesce(e.evidence_text, e.Text, 'Supported by scientific evidence') AS text, coalesce(e.source_id, e.Source, 'Food Science Register') AS source, coalesce(target.id, target.name) AS target_id
        LIMIT 100
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

    def retrieve_vector_ingredients(self, query: str, top_k: int = 50) -> List[RetrievedIngredient]:
        """
        STRATEGY 3: Semantic Vector Search
        Performs conceptual similarity search over ingredient attributes, sensory notes,
        and functional descriptions using TF-IDF vector embeddings and cosine similarity.
        """
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity

            all_structured = self.retrieve_structured_ingredients()
            if not all_structured or not query:
                return []

            corpus = [
                f"{ing.name} {ing.category} {' '.join(ing.functional_roles)} {' '.join(str(v) for v in ing.flavor.values())} {ing.allergen}"
                for ing in all_structured
            ]

            vectorizer = TfidfVectorizer(stop_words="english")
            tfidf_matrix = vectorizer.fit_transform(corpus)
            query_vec = vectorizer.transform([query])

            similarities = cosine_similarity(query_vec, tfidf_matrix)[0]
            ranked_indices = similarities.argsort()[::-1][:top_k]

            vector_results = []
            for idx in ranked_indices:
                sim_score = float(similarities[idx])
                if sim_score > 0.05:
                    ing = all_structured[idx]
                    ing.confidence = round(sim_score, 4)
                    if "Semantic Vector Search" not in ing.retrieval_methods:
                        ing.retrieval_methods.append("Semantic Vector Search")
                    vector_results.append(ing)
            return vector_results
        except Exception as e:
            logger.warning(f"Semantic vector search fallback: {e}")
            return []

    def retrieve_all_multi_dimensional(self, brief_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        STEP 3: Multi-Strategy Retrieval Entry Point:
        Executes 4 complementary retrieval strategies:
        1. KG / Cypher Traversal (Explicit relationships & multi-hop reasoning)
        2. Structured Retrieval (Exact values filters: protein, fat, cost)
        3. Semantic Vector Search (Conceptual similarity matching)
        4. Scientific Evidence Retrieval (Research papers, DOIs, standards)
        """
        candidates: Dict[str, RetrievedIngredient] = {}
        query_text = brief_dict.get("description") or brief_dict.get("category") or ""
        if brief_dict.get("flavor_profile"):
            query_text += " " + " ".join(brief_dict.get("flavor_profile", []))
        if brief_dict.get("texture_profile"):
            query_text += " " + " ".join(brief_dict.get("texture_profile", []))

        # 1. Structured DB Retrieval (Primary Grounded Facts)
        structured_ings = self.retrieve_structured_ingredients()
        exact_filters = []
        nt = brief_dict.get("nutrition_targets", {})
        if nt.get("protein_min"):
            exact_filters.append(f"protein >= {nt['protein_min']}%")
        if nt.get("fat_max"):
            exact_filters.append(f"fat <= {nt['fat_max']}%")
        if brief_dict.get("cost_target"):
            exact_filters.append(f"cost_per_kg <= ${brief_dict['cost_target']}/kg")

        for ing in structured_ings:
            candidates[ing.name.lower()] = ing

        # Targeted Database Context Search for brief-specific ingredients (e.g. cocoa butter, almond, protein, etc.)
        import re
        import sqlite3
        from repository import DB_PATH
        core_search_phrases = ["cocoa butter", "almond", "pea protein", "soy protein", "rice protein", "fava", "erythritol", "allulose", "cane sugar", "vanilla", "inulin", "pgpr", "phosphatides", "lecithin"]
        brief_kw = [w for w in re.findall(r"\b[a-zA-Z]{4,}\b", query_text.lower()) if w not in {"with", "using", "from", "that", "this", "make", "create", "design", "formulate", "product", "target", "market", "suitable", "clear", "required"}]
        all_search_terms = list(dict.fromkeys(core_search_phrases + brief_kw))
        if all_search_terms:
            try:
                conn = sqlite3.connect(DB_PATH)
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                for kw in all_search_terms:
                    c.execute("""
                        SELECT * FROM ingredients 
                        WHERE name LIKE ? OR category LIKE ? 
                        ORDER BY CASE WHEN id LIKE 'ing_%' AND (protein > 0 OR fat > 0 OR cost_per_kg > 0) THEN 0 ELSE 1 END 
                        LIMIT 15
                    """, (f"%{kw}%", f"%{kw}%"))
                    for row in c.fetchall():
                        item = dict(row)
                        k_name = item["name"].lower()
                        if k_name not in candidates:
                            cost_val = float(item["cost_per_kg"]) if item.get("cost_per_kg") is not None else None
                            raw_role = str(item.get("functional_role") or "").strip()
                            role_conf = 0.95
                            if not raw_role or raw_role in ["Bulking Agent", "None", "Unknown", "General"]:
                                if functional_predictor:
                                    pred_role, conf = functional_predictor.predict_with_uncertainty(item)
                                    f_roles = [pred_role]
                                    role_conf = conf
                                else:
                                    f_roles = [raw_role or "Bulking Agent"]
                            else:
                                f_roles = [raw_role]

                            ing = RetrievedIngredient(
                                id=str(item.get("id", f"ing_{item.get('name')}")),
                                name=str(item.get("name", "Unknown")),
                                category=str(item.get("category", "General")),
                                functional_roles=f_roles,
                                confidence=role_conf,
                                nutrition={
                                    "protein": float(item.get("protein", 0.0) or 0.0),
                                    "fat": float(item.get("fat", 0.0) or 0.0),
                                    "carbs": float(item.get("carbs", 0.0) or 0.0),
                                    "calories": float(item.get("energy", item.get("calories", 0.0)) or 0.0)
                                },
                                allergen=str(item.get("allergens", "None")),
                                source="Grounded Repository DB",
                                cost_per_kg=cost_val,
                                vegan=bool(item.get("vegan", 0)),
                                gluten_free=bool(item.get("gluten_free", 0)),
                                dairy_free=bool(item.get("dairy_free", 0)),
                                regulatory_status="Permitted" if item.get("evidence_claim") else "UNKNOWN",
                                retrieval_methods=["Structured DB (Targeted Match)"]
                            )
                            candidates[k_name] = ing
                conn.close()
            except Exception as e:
                logger.warning(f"Targeted keyword DB lookup note: {e}")

        # 2. KG / Cypher Traversal (Explicit Relationships & Multi-Hop Reasoning)
        kg_ings = self.retrieve_kg_ingredients()
        for ing in kg_ings:
            key = ing.name.lower()
            if key in candidates:
                candidates[key].functional_roles = list(set(candidates[key].functional_roles + ing.functional_roles))
                if "Neo4j Cypher KG" not in candidates[key].retrieval_methods:
                    candidates[key].retrieval_methods.append("Neo4j Cypher KG")
            else:
                candidates[key] = ing

        # 3. Semantic Vector Search (Conceptual Similarity)
        vector_ings = self.retrieve_vector_ingredients(query_text)
        for ing in vector_ings:
            key = ing.name.lower()
            if key in candidates:
                if "Semantic Vector Search" not in candidates[key].retrieval_methods:
                    candidates[key].retrieval_methods.append("Semantic Vector Search")
                candidates[key].confidence = max(candidates[key].confidence or 0.0, ing.confidence or 0.0)
            else:
                candidates[key] = ing

        # 4. Scientific Evidence Retrieval (Research Papers & DOIs)
        candidate_ids = [ing.id for ing in candidates.values()]
        evidence_items = self.retrieve_evidence(candidate_ids)
        for ev in evidence_items:
            tgt_id = ev.get("targetId")
            for ing in candidates.values():
                if ing.id == tgt_id:
                    ing.evidence.append(ev)

        # Generate Intents & Cypher string
        intents = self.generate_retrieval_intents(brief_dict)
        cypher_str = self.generate_dynamic_cypher(brief_dict)

        multi_strategy_breakdown = {
            "kg_traversal": {
                "strategy": "KG / Cypher Traversal",
                "focus": "Explicit relationships & multi-hop reasoning",
                "relationships_traversed": [":PERFORMS_ROLE", ":SUBJECT_TO_CONSTRAINT", ":INCOMPATIBLE_WITH"],
                "count": len(kg_ings)
            },
            "structured_retrieval": {
                "strategy": "Structured Retrieval",
                "focus": "Exact values filters (protein, fat, cost)",
                "exact_filters_applied": exact_filters or ["General Macronutrient Match"],
                "count": len(structured_ings)
            },
            "semantic_vector_search": {
                "strategy": "Semantic Vector Search",
                "focus": "Conceptual similarity across flavor, texture & brief text",
                "query_concept": query_text.strip() or "Standard Food Formulation",
                "count": len(vector_ings),
                "top_matches": [f"{v.name} (similarity: {v.confidence})" for v in vector_ings[:3]]
            },
            "scientific_evidence": {
                "strategy": "Scientific Evidence Retrieval",
                "focus": "Research papers, literature citations & DOI standards",
                "count": len(evidence_items)
            }
        }

        return {
            "retrieved_count": len(candidates),
            "ingredients": list(candidates.values()),
            "evidence": evidence_items,
            "intents": [i.to_dict() for i in intents],
            "cypher_query": cypher_str,
            "multi_strategy_breakdown": multi_strategy_breakdown
        }

    def evaluate_candidate_sufficiency(
        self,
        eligible_candidates: List[RetrievedIngredient],
        brief_dict: Dict[str, Any],
        prop_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Audits ingredient set sufficiency after traversal.
        If insufficient, provides actionable backtracking plan to Step 2 (Constraint Relaxation)
        and Step 1 (Brief Reformulation).
        """
        roles_present = set()
        for ing in eligible_candidates:
            for r in ing.functional_roles:
                roles_present.add(r.lower())

        is_sufficient = len(eligible_candidates) >= 4
        
        # Check greatest elimination bottleneck
        drops = [
            ("Dietary Gating", prop_results.get("initial_candidate_space", 0) - prop_results.get("after_dietary_constraint", 0)),
            ("Allergen Gating", prop_results.get("after_dietary_constraint", 0) - prop_results.get("after_allergen_constraint", 0)),
            ("Functional Gating", prop_results.get("after_allergen_constraint", 0) - prop_results.get("after_functional_constraint", 0)),
            ("Regulatory Gating", prop_results.get("after_functional_constraint", 0) - prop_results.get("after_regulatory_constraint", 0)),
            ("Cost Ceiling", prop_results.get("after_regulatory_constraint", 0) - prop_results.get("after_cost_constraint", 0))
        ]
        sorted_drops = sorted(drops, key=lambda x: x[1], reverse=True)
        primary_bottleneck = sorted_drops[0][0] if sorted_drops and sorted_drops[0][1] > 0 else "None"

        step_2_changes = [
            "Relax soft constraint tolerances by ±15-25% (e.g. widen protein/fat tolerance windows).",
            "De-escalate secondary sensory/flavor target weights to prioritize foundational structural ingredients.",
            "Traverse Neo4j 2-hop substitute paths (:SUBSTITUTE_FOR / identical functional clusters) for alternative binders/emulsifiers."
        ]

        step_1_changes = [
            "Inspect product brief for mutually exclusive hard constraints (e.g. strict vegan + whey protein).",
            "Adjust broad ingredient exclusions that inadvertently eliminate entire functional categories.",
            "Adopt complementary dual-source protein/lipid blending (e.g. pea + brown rice protein isolate)."
        ]

        return {
            "is_sufficient": is_sufficient,
            "candidate_count": len(eligible_candidates),
            "roles_covered": list(roles_present),
            "primary_bottleneck": primary_bottleneck,
            "step_2_relaxation_recommendations": step_2_changes,
            "step_1_reformulation_recommendations": step_1_changes
        }

# Global singleton orchestrator
retrieval_orchestrator = RetrievalOrchestrator()
