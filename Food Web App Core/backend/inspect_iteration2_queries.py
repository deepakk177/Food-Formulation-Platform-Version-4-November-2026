"""
Inspection Script: Exact Queries and Results for Iteration 2 (Multi-Source Retrieval)
Shows exact Cypher, SQL, and Vector search queries and their exact output payloads.
"""
import sys
import json
import numpy as np

from requirements_extractor import ProductBriefParser
from retrieval_service import retrieval_orchestrator
from neo4j_client import neo4j_client
import sqlite3
from repository import DB_PATH
from rag_engine import get_vector_store

def run_inspection():
    prompt = "Formulate a high protein vegan snack bar gluten-free with low cost"
    print("=" * 80)
    print(f"EXACT QUERIES & RESULTS FOR ITERATION 2: MULTI-SOURCE HYBRID RETRIEVAL")
    print(f"PROMPT: '{prompt}'")
    print("=" * 80)

    # 1. Parse Brief
    parser = ProductBriefParser()
    brief = parser.extract(prompt)

    # -------------------------------------------------------------------------
    # QUERY 1: NEO4J KNOWLEDGE GRAPH (CYPHER QUERY)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("1. NEO4J KNOWLEDGE GRAPH QUERY (CYPHER)")
    print("-" * 80)
    
    exact_cypher = """MATCH (i:Ingredient)
OPTIONAL MATCH (i)-[:INGREDIENT_PERFORMS_ROLE]->(r:FunctionalRole)
RETURN i.id AS id, i.name AS name, i.Source AS source, collect(r.name) AS roles
LIMIT 100"""
    
    print("\n[EXACT CYPHER QUERY STRING EXECUTED]:")
    print(exact_cypher)

    kg_records = neo4j_client.run_query(exact_cypher, {"term": ""})
    print(f"\n[NEO4J QUERY RESULT COUNT]: {len(kg_records)} records returned")
    print("\n[SAMPLE RAW NEO4J RECORDS RETURNED (First 3)]:")
    for rec in kg_records[:3]:
        print(json.dumps(rec, indent=2))

    # -------------------------------------------------------------------------
    # QUERY 2: GROUNDED SQLITE / DUCKDB DATABASE (SQL QUERY)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("2. GROUNDED SQLITE / DUCKDB DATABASE QUERY (SQL)")
    print("-" * 80)
    
    exact_sql = "SELECT * FROM ingredients LIMIT 500;"
    print("\n[EXACT SQL QUERY STRING EXECUTED]:")
    print(exact_sql)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(exact_sql)
    sql_rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    print(f"\n[SQL QUERY RESULT COUNT]: {len(sql_rows)} database rows fetched")
    print("\n[SAMPLE RAW SQL ROW RECORD RETURNED (First 2)]:")
    for row in sql_rows[:2]:
        # Filter down keys for readable presentation
        sample_row = {
            "id": row.get("id"),
            "name": row.get("name"),
            "category": row.get("category"),
            "functional_role": row.get("functional_role"),
            "cost_per_kg": row.get("cost_per_kg"),
            "protein": row.get("protein"),
            "fat": row.get("fat"),
            "carbs": row.get("carbs"),
            "vegan": row.get("vegan"),
            "gluten_free": row.get("gluten_free"),
            "allergens": row.get("allergens"),
            "evidence_claim": row.get("evidence_claim"),
            "evidence_source": row.get("evidence_source")
        }
        print(json.dumps(sample_row, indent=2))

    # -------------------------------------------------------------------------
    # QUERY 3: SEMANTIC VECTOR STORE (MINILM-L6 EMBEDDINGS & COSINE SEARCH)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("3. SEMANTIC VECTOR STORE QUERY (COSINE SIMILARITY over sentence-transformers/all-MiniLM-L6-v2)")
    print("-" * 80)
    
    query_text = f"high protein vegan gluten-free snack bar {brief.category or ''}"
    print(f"\n[EXACT VECTOR QUERY EMBEDDING INPUT TEXT]: '{query_text}'")
    
    exact_vector_formula = """
q_emb = HuggingFaceEmbeddings("sentence-transformers/all-MiniLM-L6-v2").embed_query(query_text)
sims = (doc_embeddings @ q_emb) / (||doc_embeddings|| * ||q_emb||)
top_k_documents = argsort(sims)[::-1][:k]
"""
    print("\n[EXACT COSINE SEARCH MATHEMATICAL EXECUTABLE FORMULA]:")
    print(exact_vector_formula.strip())

    try:
        vector_store = get_vector_store()
        vec_docs = vector_store._cosine_search(query_text, k=5)
        print(f"\n[VECTOR STORE RESULT COUNT]: {len(vec_docs)} semantically matching documents retrieved")
        print("\n[SAMPLE RAW RETRIEVED VECTOR DOCUMENTS WITH METADATA (First 3)]:")
        for idx, doc in enumerate(vec_docs[:3], 1):
            print(f"\n  Vector Result #{idx}:")
            print(f"    - Content Snippet: {json.dumps(doc.page_content)}")
            print(f"    - Metadata JSON  : {json.dumps(doc.metadata)}")
    except Exception as e:
        print(f"Vector search execution: {e}")

    print("\n" + "=" * 80)
    print("ITERATION 2 QUERY INSPECTION COMPLETE")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    run_inspection()
