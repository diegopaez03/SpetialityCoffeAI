import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

from llm.graph_qa import ask_cafe

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN", "token1")

app = FastAPI()
templates = Jinja2Templates(directory="api/templates")

class ChatIn(BaseModel):
    message: str
    token: str

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
def chat(payload: ChatIn):
    if payload.token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido.")
    answer = ask_cafe(payload.message)
    return {"answer": answer}
