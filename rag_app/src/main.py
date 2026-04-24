import asyncio
import logging
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

from rag_app.src.api.routes import router
from rag_app.src.core.llm import OLLAMA_MODEL, generate_response
from rag_app.src.db.cleanup import cleanup_expired_sessions
from rag_app.src.db.db import init_db
from rag_app.src.rag.rag_pipeline import retrieve_context
from rag_app.src.utils.session_utils import (
    add_message,
    get_or_create_session,
    get_session_history,
)

logging.basicConfig(filename="app.log", level=logging.INFO)

app = FastAPI(title="AI Fake News Detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryInput(BaseModel):
    question: str
    session_id: Optional[str] = None
    model: str = OLLAMA_MODEL


CLEANUP_INTERVAL = 60 * 60


async def periodic_cleanup():
    while True:
        cleanup_expired_sessions()
        await asyncio.sleep(CLEANUP_INTERVAL)


@app.on_event("startup")
async def startup_event():
    init_db()
    asyncio.create_task(periodic_cleanup())


@app.post("/chat")
async def chat(query_input: QueryInput):
    session_id, _ = get_or_create_session(query_input.session_id)

    add_message(session_id, "user", query_input.question)

    history = get_session_history(session_id)
    context, sources = retrieve_context(query_input.question)

    context_block = context if context else "No matching verified facts found."

    system_prompt = (
        "You are a factual assistant.\n\n"
        "Use the following verified information to answer if relevant.\n"
        "If the information is not relevant, answer normally.\n\n"
        f"Context:\n{context_block}"
    )

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)

    ai_response = await generate_response(messages, model=query_input.model)

    add_message(session_id, "assistant", ai_response)

    final_history = get_session_history(session_id)

    return {
        "session_id": session_id,
        "answer": ai_response,
        "sources": sources,
        "history_length": len(final_history),
    }


@app.get("/session/{session_id}")
async def get_session(session_id: str):
    history = get_session_history(session_id)

    if not history:
        raise HTTPException(
            status_code=404,
            detail="The relevant session was not found or has no messages",
        )

    return {
        "session_id": session_id,
        "messages": history,
        "message_count": len(history),
    }


@app.get("/")
def root():
    return {"status": "ok"}


app.include_router(router)
