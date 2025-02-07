import sqlite3
from typing import List, Dict, Optional, Tuple

DB_PATH = "chatbot.db"

def setup_database():
    """Initialize the SQLite database and create tables if they don't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT,
                message TEXT,
                role TEXT,
                timestamp TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        """)
        conn.commit()

def add_conversation(conversation_id: str, title: str):
    """Insert a new conversation if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO conversations (id, title) VALUES (?, ?)", (conversation_id, title))
        conn.commit()

def add_message(conversation_id: str, message: str, role: str, timestamp: str):
    """Insert a message into the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages (conversation_id, message, role, timestamp)
            VALUES (?, ?, ?, ?)
        """, (conversation_id, message, role, timestamp))
        conn.commit()

def get_conversation(conversation_id: str) -> Optional[Dict]:
    """Retrieve a conversation's messages."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM conversations WHERE id = ?", (conversation_id,))
        conversation = cursor.fetchone()
        if not conversation:
            return None
        
        cursor.execute("""
            SELECT message, role, timestamp FROM messages WHERE conversation_id = ?
        """, (conversation_id,))
        messages = [{"message": row[0], "role": row[1], "timestamp": row[2]} for row in cursor.fetchall()]
    
    return {"id": conversation_id, "title": conversation[0], "messages": messages}

def get_all_conversations() -> List[Tuple[str, Optional[str]]]:
    """Retrieve all conversation IDs with their titles."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM conversations")
        return cursor.fetchall()

def set_conversation_title(conversation_id: str, title: str):
    """Update a conversation's title."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE conversations SET title = ? WHERE id = ?", (title, conversation_id))
        conn.commit()
        

# Call setup_database() to initialize the database