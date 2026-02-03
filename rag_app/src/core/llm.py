import os
from dotenv import load_dotenv, find_dotenv
from typing import List, Dict
from pathlib import Path
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

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
        if not isinstance(content, str):
            content = str(content)  # ensure it's a string

        if role == "user":
            lc_messages.append(HumanMessage(content=content))
        elif role == "assistant":
            lc_messages.append(AIMessage(content=content))
        elif role == "system":
            lc_messages.append(SystemMessage(content=content))
        else:
            # fallback for unknown roles
            lc_messages.append(HumanMessage(content=content))
    return lc_messages

async def generate_response(messages: List[Dict[str, str]]) -> str:
    lc_messages=convert_messages(messages)
    response = await llm.agenerate([lc_messages])
    return response.generations[0][0].text