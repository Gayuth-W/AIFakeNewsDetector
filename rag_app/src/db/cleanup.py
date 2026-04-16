import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "chat_app.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def cleanup_expired_sessions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM sessions WHERE expires_at <= ?", (datetime.utcnow(),))
    expired_sessions = [row["id"] for row in cursor.fetchall()]

    # Delete messages of expired sessions
    if expired_sessions:
        cursor.executemany(
            "DELETE FROM messages WHERE session_id = ?",
            [(sid,) for sid in expired_sessions]
        )
        cursor.executemany(
            "DELETE FROM sessions WHERE id = ?",
            [(sid,) for sid in expired_sessions]
        )

    conn.commit()
    conn.close()
    print(f"Cleaned up {len(expired_sessions)} expired sessions.")