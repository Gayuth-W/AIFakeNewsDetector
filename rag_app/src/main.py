from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
# from pydantic_models import QueryInput, QueryResponse
# from langchain_utils import get_rag_chain
# from db_utils import insert_application_logs, get_chat_history
import uuid
import logging

logging.basicConfig(filename="app.log", level=logging.INFO)

app=FastAPI(title="AI Fake News Detector")


class QueryInput(BaseModel):
  question: str
  session_id: Optional[str] = None
  model: str = "gpt-4o-mini"

@app.get("/health")
async def health_check():
  return{
    "status":"ok",
    "message": "Backedn is running"
  }
  
@app.post("/chat")
async def chat(query_input: dict):
    question = query_input.get("question")
    return {"answer": f"You asked: {question}"}
