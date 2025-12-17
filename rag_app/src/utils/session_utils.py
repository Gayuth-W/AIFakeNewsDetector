# src/utils/session_utils.py
import uuid
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "chat_app.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

SESSION_TTL_HOURS = 24

def get_or_create_session(session_id: str | None):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow()

    # If session_id provided, check if it exists and not expired
    if session_id:
        cursor.execute("SELECT * FROM sessions WHERE id = ? AND expires_at > ?", (session_id, now))
        row = cursor.fetchone()
        if row:
            # Session exists and valid
            cursor.close()
            conn.close()
            # Fetch messages
            messages = get_session_history(session_id)
            return session_id, messages

    # Create new session
    new_session_id = str(uuid.uuid4())
    created_at = now
    expires_at = now + timedelta(hours=SESSION_TTL_HOURS)

    cursor.execute(
        "INSERT INTO sessions (id, created_at, expires_at) VALUES (?, ?, ?)",
        (new_session_id, created_at, expires_at)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return new_session_id, []

def add_message(session_id: str, role: str, content: str):
    conn = get_connection()
    cursor = conn.cursor()
    created_at = datetime.utcnow()

    cursor.execute(
        "INSERT INTO messages (session_id, role, content, created_at) VALUES (?, ?, ?, ?)",
        (session_id, role, content, created_at)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_session_history(session_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    # Only return messages for sessions that exist and not expired
    now = datetime.utcnow()
    cursor.execute(
        """
        SELECT * FROM messages
        WHERE session_id IN (
            SELECT id FROM sessions WHERE id = ? AND expires_at > ?
        )
        ORDER BY created_at ASC
        """,
        (session_id, now)
    )
    rows = cursor.fetchall()
    messages = [{"role": row["role"], "content": row["content"]} for row in rows]

    cursor.close()
    conn.close()
    return messages