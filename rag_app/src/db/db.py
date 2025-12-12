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

    #chat session logs table
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

    #metadata for uploaded documents
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_store (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    conn.commit()
    conn.close()
    
def insert_application_logs(session_id, user_query, gpt_response, model):
  conn=get_db_connection()
  conn.execute(
      '''
      INSERT INTO application_logs (session_id, user_query, gpt_response, model)
      VALUES (?, ?, ?, ?)
      ''',
      (session_id, user_query, gpt_response, model)
  )
  conn.commit()
  conn.close()
  
def get_chat_history(session_id):
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute(
      '''
      SELECT user_query, gpt_response
      FROM application_logs
      WHERE session_id = ?
      ORDER BY created_at ASC
      ''',
      (session_id,)
  )
  rows = cursor.fetchall()
  conn.close()
  
  messages = []
  for row in rows:
      messages.append({"role": "human", "content": row["user_query"]})
      messages.append({"role": "ai", "content": row["gpt_response"]})

  return messages

def insert_document_record(filename):
  conn = get_db_connection()
  cursor = conn.cursor()

  cursor.execute(
      '''
      INSERT INTO document_store (filename)
      VALUES (?)
      ''',
      (filename,)
  )
  file_id = cursor.lastrowid

  conn.commit()
  conn.close()

  return file_id

def delete_document_record(file_id):
  conn = get_db_connection()
  conn.execute(
      '''
      DELETE FROM document_store
      WHERE id = ?
      ''',
      (file_id,)
  )
  conn.commit()
  conn.close()
  
def get_all_documents():
  conn = get_db_connection()
  cursor = conn.cursor()

  cursor.execute('''
      SELECT id, filename, upload_timestamp
      FROM document_store
      ORDER BY upload_timestamp DESC
  ''')

  documents = cursor.fetchall()
  conn.close()

  return [dict(doc) for doc in documents]