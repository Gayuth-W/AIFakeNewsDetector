import os
from dotenv import load_dotenv, find_dotenv
from typing import List, Dict
from pathlib import Path
from langchain_community.chat_models import ChatOllama

env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

llm = ChatOllama(
    model="gemma3:1b",
    base_url="http://localhost:11434",
    temperature=0
)

def convert_messages(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    lc_messages = []
    for message in messages:
        role = message.get("role")
        content = message.get("content")
        if role == "user":
            lc_messages.append({"type": "human", "text": content})
        elif role == "assistant":
            lc_messages.append({"type": "ai", "text": content})
        elif role == "system":
            lc_messages.append({"type": "system", "text": content})
    return lc_messages

async def generate_response(messages: List[Dict[str, str]]) -> str:
    lc_messages=convert_messages(messages)
    response = await llm.agenerate([lc_messages])
    return response.content
