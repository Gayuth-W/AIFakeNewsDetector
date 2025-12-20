from dotenv import load_dotenv
load_dotenv()
from rag_app.src.rag.rag_pipeline import retrieve_context
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from rag_app.src.db.cleanup import cleanup_expired_sessions
import asyncio
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


CLEANUP_INTERVAL = 60 * 60  # seconds, e.g., 1 hour

async def periodic_cleanup():
    while True:
        cleanup_expired_sessions(ttl_hours=24)
        await asyncio.sleep(CLEANUP_INTERVAL)

@app.on_event("startup")
async def startup_event():
    # Start the cleanup loop
    asyncio.create_task(periodic_cleanup())


@app.post("/chat")
async def chat(query_input: QueryInput):
    session_id, _ = get_or_create_session(query_input.session_id)

    # Store user message in DB
    add_message(session_id, "user", query_input.question)

    # Fetch full session history from DB
    history = get_session_history(session_id)

    context = retrieve_context(query_input.question)

    system_prompt = (
        "You are a factual assistant.\n\n"
        "Use the following verified information to answer if relevant.\n"
        "If the information is not relevant, answer normally.\n\n"
        f"Context:\n{context}"
    )

    messages = [{"role": "system", "content": system_prompt}]
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
