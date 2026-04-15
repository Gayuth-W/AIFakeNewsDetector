import os
from typing import List, Dict
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")


def get_llm(model: str | None = None) -> ChatOllama:
    return ChatOllama(
        model=model or OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0,
    )


def convert_messages(messages: List[Dict[str, str]]):
    lc_messages = []
    for message in messages:
        role = message.get("role")
        content = message.get("content")
        if not isinstance(content, str):
            content = str(content)

        if role == "user":
            lc_messages.append(HumanMessage(content=content))
        elif role == "assistant":
            lc_messages.append(AIMessage(content=content))
        elif role == "system":
            lc_messages.append(SystemMessage(content=content))
        else:
            lc_messages.append(HumanMessage(content=content))
    return lc_messages


async def generate_response(
    messages: List[Dict[str, str]], model: str | None = None
) -> str:
    llm = get_llm(model)
    lc_messages = convert_messages(messages)
    response = await llm.agenerate([lc_messages])
    return response.generations[0][0].text
