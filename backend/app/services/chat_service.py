from app.utils.ollama_helper import OllamaHelper
from app.utils.memory.memory_helper import MemoryHelper
from typing import Dict, AsyncGenerator
from app.core.logger import logger
from app.utils.model_helper import select_model
from app.core.dependencies import validate_model


class ChatService:
    def __init__(self):
        """
        Initialize chat service with FAISS and Ollama helpers.
        """
        self.ollama_helper = OllamaHelper()
        self.memory = MemoryHelper()  # Adjust as per the model

    def generate_ollama_prompt(
        self, conversation_id: str, current_user_input: str
    ) -> str:
        """
        Generate prompt for Ollama based on conversation history and similar messages.
        """
        # Retrieve conversation history
        conversation_history = self.memory.get_conversation_messages(conversation_id)

        # Combine history with the current user message
        past_context = ""
        if conversation_history:
            past_context = "\n".join(
                [
                    "Pervious message:" + msg["message"]
                    for msg in conversation_history["messages"]
                ]
            )

        # Perform search to find similar messages
        similar_messages = self.memory.search_similar_messages(current_user_input)
        logger.debug(f"Similar messages: {similar_messages}")

        # Combine search results with conversation history for more context
        similar_context = ""
        if similar_messages is not None and len(similar_messages) > 0:
            similar_context = "\n".join(
                [f"Similar message: {msg}" for msg in similar_messages]
            )

        # Prepare the final input for Ollama chat
        final_input = f"{past_context}\n{similar_context}\nCurrent User Query: {current_user_input}"

        return final_input

    def get_model(self, conversation_id: str, current_user_input: str, model: str):
        """
        Get the model based on the provided model name.
        """
        if model:
            # Return model user selected
            return model
        else:
            # If no model is provided, use the model from the conversation history
            conversation_history = self.memory.get_conversation_messages(
                conversation_id
            )

            # Retrieve conversation history messages
            history_messages = ""
            if conversation_history:
                history_messages = " ".join(conversation_history["messages"])

            # Prepare context for model selection
            context = " ".join([f"Previous message: {msg}" for msg in history_messages])

            # Select the model based on the context
            return select_model(
                f"Context: {context}\nCurrent User Query: {current_user_input}"
            )

    async def process_chat(
        self, conversation_id: str, _model: str, message: str
    ) -> AsyncGenerator[str, None]:
        """
        Process user message, retrieve past context, and stream response.
        """
        # Retrive model
        model = self.get_model(conversation_id, message, _model)
        logger.debug(f"process_chat: Model: {model}")

        # Validate the model
        if not validate_model(model):
            raise HTTPException(status_code=400, detail=f"Invalid model: {model}")

        # Collect full assistant response
        assistant_message = ""

        # Call Ollama and stream response
        async for chunk in self.ollama_helper.generate_response(
            model, self.generate_ollama_prompt(conversation_id, message)
        ):
            assistant_message += chunk
            yield chunk

        # Store user message and assistant response
        self.memory.store_and_index_message(conversation_id, "user", message)
        self.memory.store_and_index_message(
            conversation_id, "assistant", assistant_message
        )

    def get_all_conversations(self):
        """Returns all stored conversations grouped by conversation_id."""
        return self.memory.get_all_conversations()

    def get_conversation_messages(self, conversation_id: str):
        """Returns the conversation with the given ID."""
        return self.memory.get_conversation_messages(conversation_id)

    def set_conversation_title(self, conversation_id: str, title: str):
        """Set or update the conversation title."""
        self.memory.set_conversation_title(conversation_id, title)
