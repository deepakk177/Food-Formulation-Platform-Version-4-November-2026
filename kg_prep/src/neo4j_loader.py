"""
Neo4j Ingestion Loader for FoodKG Pipeline
Loads CSV nodes and relationships from data/output into Neo4j using parameterized Cypher.
"""
import os
import sys
import glob
import logging
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List

try:
    from neo4j import GraphDatabase, Driver
except ImportError:
    print("[WARNING] neo4j package not installed. Run 'pip install neo4j'.")
    GraphDatabase = None
    Driver = None

logger = logging.getLogger("Neo4jLoader")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

NODE_LABEL_MAP = {
    "Allergens.csv": "Allergen",
    "Compounds.csv": "Compound",
    "Constraints.csv": "Constraint",
    "Equipment.csv": "Equipment",
    "Evidence.csv": "Evidence",
    "FlavorMolecules.csv": "FlavorMolecule",
    "Flavors.csv": "Flavor",
    "FoodAdditives.csv": "FoodAdditive",
    "FoodCategories.csv": "FoodCategory",
    "FunctionalRoles.csv": "FunctionalRole",
    "INS.csv": "INS",
    "Ingredients.csv": "Ingredient",
    "Nutrients.csv": "Nutrient",
    "Packaging.csv": "Packaging",
    "ProcessConditions.csv": "ProcessCondition",
    "Processes.csv": "Process",
    "Products.csv": "Product",
    "Properties.csv": "Property",
    "Regulations.csv": "Regulation",
    "Sources.csv": "Source"
}

RELATIONSHIP_TYPE_MAP = {
    "evidence_supports_entity.csv": "EVIDENCE_SUPPORTS_ENTITY",
    "foodadditive_allowed_in_foodcategory.csv": "FOODADDITIVE_ALLOWED_IN_FOODCATEGORY",
    "foodadditive_has_ins.csv": "FOODADDITIVE_HAS_INS",
    "ingredient_contains_compound.csv": "INGREDIENT_CONTAINS_COMPOUND",
    "ingredient_has_constraint.csv": "INGREDIENT_HAS_CONSTRAINT",
    "ingredient_has_flavor.csv": "INGREDIENT_HAS_FLAVOR",
    "ingredient_has_nutrient.csv": "INGREDIENT_HAS_NUTRIENT",
    "ingredient_has_property.csv": "INGREDIENT_HAS_PROPERTY",
    "ingredient_performs_role.csv": "INGREDIENT_PERFORMS_ROLE",
    "ingredient_used_in_product.csv": "INGREDIENT_USED_IN_PRODUCT",
    "process_has_condition.csv": "PROCESS_HAS_CONDITION",
    "product_complies_with.csv": "PRODUCT_COMPLIES_WITH",
    "product_has_constraint.csv": "PRODUCT_HAS_CONSTRAINT",
    "product_in_category.csv": "PRODUCT_IN_CATEGORY",
    "product_requires_process.csv": "PRODUCT_REQUIRES_PROCESS",
    "regulation_has_constraint.csv": "REGULATION_HAS_CONSTRAINT"
}

class Neo4jDataLoader:
    def __init__(self, uri: str = None, username: str = None, password: str = None, database: str = None):
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.username = username or os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "password")
        self.database = database or os.getenv("NEO4J_DATABASE", "neo4j")
        self.driver = None

    def connect(self) -> bool:
        if not GraphDatabase:
            logger.error("neo4j library is missing.")
            return False
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
            self.driver.verify_connectivity()
            logger.info(f"Successfully connected to Neo4j at {self.uri}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j at {self.uri}: {e}")
            return False

    def close(self):
        if self.driver:
            self.driver.close()
            logger.info("Closed Neo4j connection.")

    def create_constraints_and_indexes(self):
        """Creates unique constraints and indexes on node IDs for performance."""
        logger.info("Creating Neo4j constraints and indexes...")
        with self.driver.session(database=self.database) as session:
            for node_file, label in NODE_LABEL_MAP.items():
                query = f"CREATE CONSTRAINT constraint_{label.lower()}_id IF NOT EXISTS FOR (n:{label}) REQUIRE n.id IS UNIQUE"
                try:
                    session.run(query)
                except Exception as e:
                    fallback_query = f"CREATE INDEX index_{label.lower()}_id IF NOT EXISTS FOR (n:{label}) ON (n.id)"
                    try:
                        session.run(fallback_query)
                    except Exception as ex:
                        logger.warning(f"Index creation for {label} warning: {ex}")

    def load_nodes(self, nodes_dir: Path, batch_size: int = 500) -> int:
        """Imports node CSV files into Neo4j."""
        total_nodes = 0
        with self.driver.session(database=self.database) as session:
            for csv_file in nodes_dir.glob("*.csv"):
                filename = csv_file.name
                label = NODE_LABEL_MAP.get(filename)
                if not label:
                    logger.warning(f"Skipping unmapped node file: {filename}")
                    continue

                df = pd.read_csv(csv_file).fillna("")
                records = df.to_dict(orient="records")
                if not records:
                    continue

                formatted_records = []
                for rec in records:
                    item = {}
                    for k, v in rec.items():
                        clean_key = "id" if k.upper() == "ID" else ("name" if k.upper() == "NAME" else k)
                        item[clean_key] = v
                    formatted_records.append(item)

                query = f"""
                UNWIND $batch AS row
                MERGE (n:{label} {{id: row.id}})
                SET n += row
                """
                
                for i in range(0, len(formatted_records), batch_size):
                    batch = formatted_records[i:i + batch_size]
                    session.run(query, batch=batch)

                total_nodes += len(formatted_records)
                logger.info(f"Loaded {len(formatted_records)} nodes into label :{label}")

        return total_nodes

    def load_relationships(self, rels_dir: Path, batch_size: int = 500) -> int:
        """Imports relationship CSV files into Neo4j."""
        total_rels = 0
        with self.driver.session(database=self.database) as session:
            for csv_file in rels_dir.glob("*.csv"):
                filename = csv_file.name
                rel_type = RELATIONSHIP_TYPE_MAP.get(filename)
                if not rel_type:
                    logger.warning(f"Skipping unmapped relationship file: {filename}")
                    continue

                df = pd.read_csv(csv_file).fillna("")
                records = df.to_dict(orient="records")
                if not records:
                    continue

                query = f"""
                UNWIND $batch AS row
                MATCH (source {{id: row.SourceID}})
                MATCH (target {{id: row.TargetID}})
                MERGE (source)-[r:{rel_type}]->(target)
                SET r.source_dataset = row.SourceDataset
                """

                for i in range(0, len(records), batch_size):
                    batch = records[i:i + batch_size]
                    session.run(query, batch=batch)

                total_rels += len(records)
                logger.info(f"Loaded {len(records)} relationships of type :{rel_type}")

        return total_rels

    def load_all(self, output_dir: Path) -> Dict[str, Any]:
        nodes_dir = output_dir / "Nodes"
        rels_dir = output_dir / "Relationships"
        
        if not (nodes_dir.exists() and rels_dir.exists()):
            raise FileNotFoundError(f"Missing Nodes or Relationships directory in {output_dir}")

        self.create_constraints_and_indexes()
        node_count = self.load_nodes(nodes_dir)
        rel_count = self.load_relationships(rels_dir)
        
        return {
            "success": True,
            "nodes_loaded": node_count,
            "relationships_loaded": rel_count
        }

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    output_dir = project_root / "data" / "output"
    
    loader = Neo4jDataLoader()
    if loader.connect():
        try:
            res = loader.load_all(output_dir)
            print(f"[SUCCESS] Loaded {res['nodes_loaded']} nodes and {res['relationships_loaded']} relationships into Neo4j.")
        finally:
            loader.close()
    else:
        print("[ERROR] Could not connect to Neo4j. Check your connection settings.")
