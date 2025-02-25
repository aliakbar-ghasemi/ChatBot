import ollama
import asyncio
from typing import AsyncGenerator
from app.core.logger import logger
from app.utils.memory.memory_helper import MemoryHelper
from app.utils.model_helper import select_model

prompt = """
    You are a highly skilled assistant specializing in understanding user queries and providing insightful responses. 
    Here is the conversation history that will help you understand the context of the current query:
    {history}

    Based on this context and the following similar questions/answers from previous conversations, 
    please help provide the most accurate and relevant answer:
    {similar_msgs}

    Current User Question: {current_question}

    Please provide a detailed and professional response.
    """


class OllamaHelper:
    def __init__(self):
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
                [msg["message"] for msg in conversation_history["messages"]]
            )

        # Perform search to find similar messages
        similar_messages = self.memory.search_similar_messages(current_user_input)
        logger.debug(f"Similar messages: {similar_messages}")

        # Combine search results with conversation history for more context
        similar_context = ""
        if similar_messages:
            similar_context = "\n".join(similar_messages)

        # Prepare the final input for Ollama chat
        final_input = prompt.format(
            history=past_context,
            similar_msgs=similar_context,
            current_question=current_user_input,
        )

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
            conversation_summary = self.memory.get_conversation_summary(
                conversation_id
            )

            # Retrieve conversation history messages
            #history_messages = ""
            #if conversation_history and isinstance(conversation_history, dict) and "messages" in conversation_history:
                # Ensure 'messages' is a list of strings
            #    if isinstance(conversation_history["messages"], list):
            #        history_messages = "\n".join([msg["message"] for msg in conversation_history["messages"]])
            
            # Select the model based on the context
            return select_model(
                f"Conversation Summary: {conversation_summary}\nCurrent User Query: {current_user_input}"
            )

    async def generate_response(
        self, model: str, prompt: str
    ) -> AsyncGenerator[str, None]:
        """
        Asynchronously processes chat input using the specified Ollama model.
        Streams responses as they are generated.
        """
        try:
            logger.warning(f"Processing chat with model: {model}")

            response = ollama.chat(
                model=model, messages=[{"role": "user", "content": prompt}], stream=True
            )

            for chunk in response:
                if "message" in chunk and "content" in chunk["message"]:
                    yield chunk["message"]["content"]
                    await asyncio.sleep(0.01)  # Allow event loop to handle other tasks
        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}")
            yield ""
