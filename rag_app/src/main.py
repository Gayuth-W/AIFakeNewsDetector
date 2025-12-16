from typing import Optional, Dict, List
from fastapi import FastAPI
from pydantic import BaseModel
import logging
from rag_app.src.utils.session_utils import (
    get_or_create_session,
    add_message,
    get_session_history
)

logging.basicConfig(filename="app.log", level=logging.INFO)

app = FastAPI(title="AI Fake News Detector")

# this is an in memory store for chat sessions
chat_sessions: Dict[str, List[Dict[str, str]]] = {}

class QueryInput(BaseModel):
    question: str
    session_id: Optional[str] = None
    model: str = "gpt-4o-mini"

@app.post("/chat")
async def chat(query_input: QueryInput):
    session_id, history = get_or_create_session(query_input.session_id)

    # user message
    add_message(session_id, "human", query_input.question)

    # fake AI response for now
    ai_response = f"You asked: {query_input.question}"

    # AI message
    add_message(session_id, "ai", ai_response)
    
    # this will get the full sesion history
    history = get_session_history(session_id)    

    return {
        "session_id": session_id,
        "answer": ai_response,
        "history_length": len(history)
    }