import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

def test_llm():
  api_key=os.getenv("OPENAI_API_KEY")
  if not api_key:
    print("There is no API key in the .env file")
    return
  
  llm=ChatOpenAI(model="gpt-4o-mini")
  response=llm.invoke("How are you doing?")
  print(response.content)
  
if __name__=="__main__":
  test_llm()