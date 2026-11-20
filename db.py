import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "Food@123")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def get_driver():
    """Create and return a Neo4j driver instance."""
    return GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


def test_connection():
    """Verify connectivity and print summary stats."""
    with get_driver() as driver:
        driver.verify_connectivity()
        with driver.session(database=DATABASE) as session:
            node_count = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
            rel_count = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
            print(f"Connected to Neo4j successfully!")
            print(f"Database: {DATABASE}")
            print(f"Total Nodes: {node_count:,}")
            print(f"Total Relationships: {rel_count:,}")


if __name__ == "__main__":
    test_connection()
