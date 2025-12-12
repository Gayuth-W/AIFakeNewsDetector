import sqlite3
from datetime import datetime
import os

DB_PATH=os.path.join(os.path.dirname(__file__), "..", "..", "data", "rag_app.db")
DB_PATH=os.path.abspath(DB_PATH)

def get_db_connection():
  conn=sqlite3.connect(DB_PATH)
  conn.row_factory=sqlite3.Row
  return conn

def initialize_database():
    """Create required tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Chat session logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS application_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_query TEXT,
            gpt_response TEXT,
            model TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # Metadata for uploaded documents
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_store (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    conn.commit()
    conn.close()