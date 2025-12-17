from dotenv import load_dotenv
load_dotenv()

from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

from rag_app.src.core.llm import generate_response
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
    session_id, _ = get_or_create_session(query_input.session_id)

    # Store user message in DB
    add_message(session_id, "user", query_input.question)

    # Fetch full session history from DB
    history = get_session_history(session_id)

    messages = [{"role": "system", "content": "You are a factual assistant."}]
    messages.extend(history)
    messages.append({"role": "user", "content": query_input.question})

    # Get AI response
    ai_response = await generate_response(messages)

    # Store AI response in DB
    add_message(session_id, "assistant", ai_response)

    final_history = get_session_history(session_id)

    return {
        "session_id": session_id,
        "answer": ai_response,
        "history_length": len(final_history)
    }

@app.get("/session/{session_id}")
async def get_session(session_id: str):
    history = get_session_history(session_id)

    if not history:
        raise HTTPException(
            status_code=404,
            detail="The relevant session was not found or has no messages"
        )

    return {
        "session_id": session_id,
        "messages": history,
        "message_count": len(history)
    }
