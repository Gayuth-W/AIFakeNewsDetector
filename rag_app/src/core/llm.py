import os
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from typing import List, Dict
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_response(messages: List[Dict[str, str]]) -> str:
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2
    )
    return response.choices[0].message.content
