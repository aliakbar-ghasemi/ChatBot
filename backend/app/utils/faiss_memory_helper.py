import faiss
import numpy as np
import json
import ollama
from typing import List, Dict, Tuple, Optional
from app.database.database import (
    setup_database,
    add_conversation,
    add_message,
    get_conversation,
    get_all_conversations,
    set_conversation_title
)

class FaissMemoryHelper:
    def __init__(self, embedding_dim: int = 4096):
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatL2(embedding_dim)  # FAISS index
        setup_database()  # Ensure database is set up
        
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate an embedding using Ollama."""
        response = ollama.embeddings(model="mistral", prompt=text)
        embedding = np.array(response["embedding"], dtype=np.float32)
    
        # Ensure embedding matches FAISS expected dimension
        if embedding.shape[0] != self.embedding_dim:
            raise ValueError(f"Embedding dimension mismatch: Expected {self.embedding_dim}, got {embedding.shape[0]}")

        return embedding.reshape(1, -1)  # Ensure correct shape

    def add_message(self, conversation_id: str, message: str, role: str, timestamp: str):
        """Adds a message to FAISS and stores metadata, generating embedding automatically."""
        embedding = self.generate_embedding(message)
        
        # Add vector to FAISS
        self.index.add(embedding)
        
        # Add conversation if it's new
        add_conversation(conversation_id, message[:30])  # Auto-title from first message
        
        # Store message in SQLite
        add_message(conversation_id, message, role, timestamp)
        

    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """Retrieve conversation messages."""
        return get_conversation(conversation_id)

    def get_all_conversations(self) -> List[Tuple[str, Optional[str]]]:
        """"Returns all conversation IDs with their titles."""
        return get_all_conversations()

    def set_title(self, conversation_id: str, title: str):
        """Set or update the conversation title."""
        set_conversation_title(conversation_id, title)
