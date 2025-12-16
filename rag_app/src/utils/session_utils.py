import uuid

_sessions={}

def get_or_create_session(session_id: str | None):
  if session_id and session_id in _sessions:
    return session_id, _sessions[session_id]
  
  new_session_id=str(uuid.uuid4())
  _sessions[new_session_id]=[]
  return new_session_id, _sessions[new_session_id]

def add_message(session_id: str, role: str, content: str):
  _sessions[session_id].append({
    "role":role,
    "content": content
  })
  
def get_session_history(session_id: id):
  return _sessions.get(session_id, [])