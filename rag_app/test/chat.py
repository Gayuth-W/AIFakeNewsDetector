import requests

url="http://localhost:8000/chat"

data={
  "question":"When was the green grow foundation was founded?",
  "session_id":None,
  "model":"gpt-4o-mini"
}

response =requests.post(url, json=data)

print("Response: ", response.json())