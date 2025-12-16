import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from typing import List, Dict

load_dotenv()
# print("API Key:", os.getenv("OPENAI_API_KEY"))
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_response(messages: List[Dict[str, str]]) -> str:
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2
    )
    return response.choices[0].message.content
