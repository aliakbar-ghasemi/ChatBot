import sqlite3
from typing import List, Dict, Optional, Tuple
import json
import numpy as np

DB_PATH = "chatbot.db"


class DatabaseHelper:
    def __init__(self):
        self.db_path = DB_PATH
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    summary TEXT
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT,
                    message TEXT,
                    role TEXT, -- 'user' or 'bot'
                    timestamp TEXT,
                    vector BLOB,  -- Stores embedding as bytes
                    shape TEXT,   -- Stores shape as JSON
                    model TEXT,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id)
                )
            """
            )
            conn.commit()

    def add_message(
        self,
        conversation_id: str,
        message: str,
        role: str,
        timestamp: str,
        vector,
        model: str,
    ):
        """Insert a message into the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            vector_bytes = vector.tobytes()
            shape_json = json.dumps(vector.shape)

            cursor.execute(
                """
                INSERT INTO messages (conversation_id, message, role, timestamp, vector, shape, model)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    conversation_id,
                    message,
                    role,
                    timestamp,
                    vector_bytes,
                    shape_json,
                    model,
                ),
            )

            message_id = cursor.lastrowid  # Get inserted message ID
            conn.commit()
            return message_id  # Return message ID for FAISS indexing

    def get_message_text(self, message_id: int) -> Optional[str]:
        """Retrieve a message from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT message FROM messages WHERE id = ?", (message_id,))
            row = cursor.fetchone()
            if row:
                return row[0]
            return None

    def get_message_vector(self, message_id):
        """Retrieve stored embedding from SQLite."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT vector, shape FROM messages WHERE id = ?", (message_id,)
            )
            row = cursor.fetchone()
            if row:
                vector_bytes, shape_json = row
                shape = tuple(json.loads(shape_json))
                return np.frombuffer(vector_bytes, dtype=np.float32).reshape(shape)
            return None

    def get_conversation_messages(self, conversation_id: str) -> Optional[Dict]:
        """Retrieve a conversation's messages."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT title FROM conversations WHERE id = ?", (conversation_id,)
            )
            conversation = cursor.fetchone()
            if not conversation:
                return None

            cursor.execute(
                """
                SELECT message, role, timestamp, model FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC
            """,
                (conversation_id,),
            )
            rows = cursor.fetchall()
            messages = []
            # for message, role, timestamp, vector_bytes, shape_json in rows:
            for message, role, timestamp, model in rows:
                # shape = tuple(json.loads(shape_json))
                # vector = np.frombuffer(vector_bytes, dtype=np.float32).reshape(shape)
                message = {
                    "message": message,
                    "role": role,
                    "timestamp": timestamp,
                    "model": model,
                    # "vector": vector.tolist(),
                    # "shape": shape,
                }
                messages.append(message)

        return {"id": conversation_id, "title": conversation[0], "messages": messages}

    def get_all_conversations(self) -> List[Tuple[str, Optional[str]]]:
        """Retrieve all conversation IDs with their titles."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, title, created_at, summary FROM conversations ORDER BY modified_at DESC"
            )
            return cursor.fetchall()

    def add_conversation(self, conversation_id: str, title: str):
        """Insert a new conversation if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                    INSERT INTO conversations (id, title, modified_at) 
                    VALUES (?, ?, CURRENT_TIMESTAMP) 
                    ON CONFLICT(id) DO UPDATE SET modified_at = CURRENT_TIMESTAMP
                """,
                (conversation_id, title),
            )
            conn.commit()

    def set_conversation_title(self, conversation_id: str, title: str):
        """Update a conversation's title."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE conversations SET title = ? WHERE id = ?",
                (title, conversation_id),
            )
            conn.commit()

    def delete_conversation(self, conversation_id: str):
        """Delete a conversation and its associated messages."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM messages WHERE conversation_id = ?", (conversation_id,)
            )
            cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
            conn.commit()

    def get_conversation_summary(self, conversation_id: str):
        """Retrieve a conversation's summary."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT summary FROM conversations WHERE id = ?", (conversation_id,)
            )
            row = cursor.fetchone()
            if row:
                return row[0]
            return ""

    def set_conversation_summary(self, conversation_id: str, summary: str):
        """Update a conversation's summary."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE conversations SET summary = ? WHERE id = ?",
                (summary, conversation_id),
            )
            conn.commit()
