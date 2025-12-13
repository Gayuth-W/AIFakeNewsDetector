from typing import Optional, Dict, List
from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import logging

logging.basicConfig(filename="app.log", level=logging.INFO)

app = FastAPI(title="AI Fake News Detector")

# In-memory store for chat sessions
chat_sessions: Dict[str, List[Dict[str, str]]] = {}


class QueryInput(BaseModel):
    question: str
    session_id: Optional[str] = None
    model: str = "gpt-4o-mini"


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "Backend is running"
    }


@app.post("/chat")
async def chat(query_input: QueryInput):
    #this will generate a new session id if it is not present
    session_id = query_input.session_id or str(uuid.uuid4())

    # initialize the session id if not present
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    # append the user query to the chat history
    chat_sessions[session_id].append({"role": "user", "content": query_input.question})

    # sample ai response
    ai_response = f"You asked: {query_input.question}"

    # append the response to the chat history
    chat_sessions[session_id].append({"role": "assistant", "content": ai_response})

    # logging to app.log
    logging.info(f"Session ID: {session_id}, User Query: {query_input.question}, AI Response: {ai_response}")

    return {
        "answer": ai_response,
        "session_id": session_id,
        "model": query_input.model
    }
