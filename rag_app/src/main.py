from typing import Optional, Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from rag_app.src.utils.session_utils import (
    get_or_create_session,
    add_message,
    get_session_history
)

logging.basicConfig(filename="app.log", level=logging.INFO)

app = FastAPI(title="AI Fake News Detector")

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
    
@app.get("/session/{session_id}")   
async def get_session(session_id: str):
    history=get_session_history(session_id)
    
    if not history:
        raise HTTPException(
            status_code=400,
            detai="The relavant session is not found or has no message"
        )
    
    return{
        "session_id":session_id,
        "messages":history,
        "message_count":len(history)
    }