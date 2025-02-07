from app.utils.ollama_helper import OllamaHelper
from app.utils.faiss_memory_helper import FaissMemoryHelper as Memory
from typing import Dict, AsyncGenerator
from app.core.logger import logger
import datetime

class ChatService:
    def __init__(self):
        """
        Initialize chat service with FAISS and Ollama helpers.
        """
        self.ollama_helper = OllamaHelper()
        self.memory = Memory() # Adjust as per the model
        
        
    async def process_chat(
        self, conversation_id: str, model: str, message: str
    ) -> AsyncGenerator[str, None]:
        """
        Process user message, retrieve past context, and stream response.
        """
        # Retrieve conversation history
        conversation = self.memory.get_conversation(conversation_id)
        logger.warning(f"process_chat: Conversation: {conversation}")
        # Extract previous messages for context
        past_context = ""
        if conversation:
            past_context = "\n".join([msg["message"] for msg in conversation["messages"]])
    
          
        # Collect full assistant response
        assistant_message = ""
        # Call Ollama and stream response
        async for chunk in self.ollama_helper.generate_response(model, (past_context + "\n" + message)):
            assistant_message += chunk
            yield chunk

        # Store user message and assistant response
        timestamp = datetime.datetime.now().isoformat()
        self.memory.add_message(conversation_id, message, "user", timestamp)
        self.memory.add_message(conversation_id, assistant_message, "assistant", timestamp)
    
    def get_all_conversations(self):
        """Returns all stored conversations grouped by conversation_id."""
        return self.memory.get_all_conversations()
    
    def get_conversation(self, conversation_id: str):
        """Returns the conversation with the given ID."""
        return self.memory.get_conversation(conversation_id)
        
        
        

