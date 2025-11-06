import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def run_cypher(query: str, params: dict | None = None):
    with driver.session() as session:
        result = session.run(query, params or {})
        return [r.data() for r in result]

def get_schema():
    """Retorna un resumen de nodos y rels para el prompt del LLM."""
    q = """
    CALL db.schema.visualization() YIELD nodes, relationships
    RETURN [n IN nodes | labels(n)[0]] AS node_labels,
           [r IN relationships | type(r)] AS rel_types
    """
    res = run_cypher(q)
    if not res:
        return {"nodes": [], "rels": []}
    return {"nodes": sorted(set(res[0]["node_labels"])),
            "rels":  sorted(set(res[0]["rel_types"]))}
