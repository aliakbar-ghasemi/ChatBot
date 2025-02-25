from app.utils.memory.faiss_helper import FaissMemoryHelper
from app.database.database import DatabaseHelper
from typing import List, Dict, Tuple, Optional
import ollama
import numpy as np
import datetime
from app.core.logger import logger
from app.utils.text_helper_transformers_summary import summarize_text

class MemoryHelper:
    def __init__(self):
        # Initialize helpers
        self.db_helper = DatabaseHelper()
        self.faiss_helper = FaissMemoryHelper()

    def generate_embedding(self, text):
        """Generate embedding using Ollama"""
        response = ollama.embeddings(model="nomic-embed-text", prompt=text)
        return np.array(response["embedding"], dtype=np.float32)

    # Store a message and add to FAISS
    async def store_and_index_message(self, conversation_id, sender, text, model = ""):
        print(f"Storing message: {sender}")
        timestamp = datetime.datetime.now().isoformat()
        embedding = self.generate_embedding(text)
        self.db_helper.add_conversation(conversation_id, text[:30]) 
        message_id = self.db_helper.add_message(conversation_id, text, sender, timestamp, embedding, model)
        self.faiss_helper.add_message_to_index(message_id, embedding)

    # Search for similar messages
    def search_similar_messages(self, query_text):
        query_vector = self.generate_embedding(query_text)
        message_ids, distances = self.faiss_helper.search_similar_messages(query_vector)

        if not message_ids:
            logger.warning("No similar messages found.")
            return []
    
        # Retrieve message texts from database
        similar_messages = []
        for i, message_id in enumerate(message_ids):
            if message_id != -1:  # Ignore invalid FAISS results
                logger.debug(f"Similar Message {i+1}: ID {message_id}, Distance: {distances[i]}")
                message = self.db_helper.get_message_text(message_id)
                if message:
                    similar_messages.append(message)
        
        # Return the list of similar messages
        return similar_messages 


    def get_conversation_messages(self, conversation_id: str):
            """Retrieve conversation messages."""
            return self.db_helper.get_conversation_messages(conversation_id)
        
    def get_all_conversations(self) -> List[Tuple[str, Optional[str]]]:
        """"Returns all conversation IDs with their titles."""
        return self.db_helper.get_all_conversations()
    
    def set_conversation_title(self, conversation_id, title):
        """Set the title of a conversation."""
        self.db_helper.set_conversation_title(conversation_id, title)
        
    async def generate_summary(self, conversation_id, prompt):
        """Generate a summary for a conversation."""
        print(f"Generating summary for conversation: {conversation_id}")
        old_summary = self.db_helper.get_conversation_summary(conversation_id)
        if not old_summary:
            old_summary = ""
        text = old_summary + "\n" + prompt
        new_summary = summarize_text(text.strip())
        self.db_helper.set_conversation_summary(conversation_id, new_summary)
        
    def get_conversation_summary(self, conversation_id):
        """Retrieve a conversation's summary."""
        return self.db_helper.get_conversation_summary(conversation_id)
