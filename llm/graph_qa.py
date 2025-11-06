# llm/graph_qa.py
import os
from dotenv import load_dotenv

from langchain_ollama import OllamaLLM
from langchain_community.graphs import Neo4jGraph
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain

# En LangChain 0.2.x, PromptTemplate está en langchain_core.prompts
from langchain_core.prompts import PromptTemplate

load_dotenv()

# ---------------------------
# LLM
# ---------------------------
llm = OllamaLLM(
    model=os.getenv("LLM_MODEL", "gpt-oss:120b-cloud"),
    base_url=os.getenv("CLOUD_OLLAMA_URL", "http://localhost:11434"),
    temperature=float(os.getenv("TEMPERATURE", "0.2")),
)

# ---------------------------
# Grafo (AuraDB)
# ---------------------------
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USER", "neo4j"),
    password=os.getenv("NEO4J_PASSWORD"),
    refresh_schema=True,  # fuerza a leer el schema actual
)

# ---------------------------
# Prompts (DEBEN ser PromptTemplate)
# ---------------------------

# 1) Prompt para GENERAR CYPHER.
#   - Debe recibir EXACTAMENTE: schema y question
cypher_prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template=(
        "Eres un experto en café de especialidad y Cypher para Neo4j.\n"
        "Usa EXCLUSIVAMENTE las etiquetas y relaciones que aparezcan en el esquema provisto.\n\n"
        "ESQUEMA DEL GRAFO:\n{schema}\n\n"
        "INSTRUCCIONES:\n"
        "- Genera SOLO la consulta Cypher, sin explicación adicional.\n"
        "- Evita inventar etiquetas/relaciones/propiedades que no estén en el esquema.\n"
        "- Si la pregunta no aplica al grafo, produce una consulta vacía (MATCH LIMIT 0) y luego lo reportará el QA.\n\n"
        "PREGUNTA:\n{question}\n\n"
        "Cypher:"
    ),
)

# 2) Prompt para RESPUESTA en lenguaje natural.
#   - Debe recibir EXACTAMENTE: context y question
qa_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "Eres un asistente de café de especialidad.\n"
        "Usa el CONTEXTO recuperado del grafo para responder en español de forma breve, clara y útil.\n\n"
        "PREGUNTA:\n{question}\n\n"
        "CONTEXTO (resultados del grafo):\n{context}\n\n"
        "RESPUESTA:"
    ),
)

# ---------------------------
# Chain LLM ↔ Neo4j
# ---------------------------
chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    cypher_prompt=cypher_prompt,  # <-- TEMPLATE, no string plano
    qa_prompt=qa_prompt,          # <-- TEMPLATE, no string plano
    top_k=5,
    verbose=False,
    return_direct=False,
    allow_dangerous_requests=False,
)

def ask_cafe(question: str) -> str:
    """
    Recibe una pregunta en español sobre el dominio de café,
    genera Cypher, ejecuta en Neo4j y devuelve respuesta natural.
    """
    try:
        resp = chain.invoke({"query": question})
        # resp suele traer {'result': 'texto ...'}
        return resp.get("result", str(resp))
    except Exception as e:
        # Fallback amable si algo falla
        return f"Ocurrió un error procesando la consulta: {e}"
