import os
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM

load_dotenv()

OLLAMA_BASE   = os.getenv("CLOUD_OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL  = os.getenv("LLM_MODEL", "gpt-oss:120b-cloud")
API_TOKEN     = os.getenv("API_TOKEN", "")
TEMPERATURE   = float(os.getenv("TEMPERATURE", "0.2"))

llm = OllamaLLM(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE,
    temperature=TEMPERATURE
)

if __name__ == "__main__":
    print(llm.invoke("Contesta en 10 palabras: ¿qué es un pour-over?"))
