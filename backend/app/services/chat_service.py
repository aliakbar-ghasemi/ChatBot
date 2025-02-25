from app.utils.ollama_helper import OllamaHelper
from app.utils.memory.memory_helper import MemoryHelper
from typing import Dict, AsyncGenerator
from app.core.logger import logger
from app.core.dependencies import validate_model
import asyncio
from fastapi import BackgroundTasks


class ChatService:
    def __init__(self):
        """
        Initialize chat service with FAISS and Ollama helpers.
        """
        self.ollama_helper = OllamaHelper()
        self.memory = MemoryHelper()  # Adjust as per the model

    async def process_chat(
        self,
        conversation_id: str,
        _model: str,
        message: str,
        background_tasks: BackgroundTasks,
    ) -> AsyncGenerator[str, None]:
        """
        Process user message, retrieve past context, and stream response.
        """
        # Retrive model
        model = self.ollama_helper.get_model(conversation_id, message, _model)
        logger.debug(f"process_chat: Model: {model}")

        # Validate the model
        if not validate_model(model):
            raise HTTPException(status_code=400, detail=f"Invalid model: {model}")

        background_tasks.add_task(
            self.memory.store_and_index_message, conversation_id, "user", message
        )

        # Collect full assistant response
        assistant_message = ""

        # Call Ollama and stream response
        try:
            async for chunk in self.ollama_helper.generate_response(
                model,
                self.ollama_helper.generate_ollama_prompt(conversation_id, message),
            ):
                assistant_message += chunk
                yield chunk

        except asyncio.CancelledError:
            logger.debug("process_chat: Cancelled")
            yield ""  # Send final message before stopping
        except Exception as e:
            logger.error(f"process_chat: Error: {str(e)}")
            yield ""
        finally:
            if(assistant_message and message):
                #print(f"process_chat: Assistant message: {assistant_message}")
                background_tasks.add_task(
                    self.memory.store_and_index_message,
                    conversation_id,
                    "assistant",
                    assistant_message.strip(),
                    model
                )
                background_tasks.add_task(
                    self.memory.generate_summary,
                    conversation_id,
                    f"{message}\n{assistant_message}",
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
