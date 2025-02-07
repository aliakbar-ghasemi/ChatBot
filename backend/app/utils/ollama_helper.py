import ollama
import asyncio
from typing import AsyncGenerator
from app.core.logger import logger

class OllamaHelper:
    async def generate_response(self, model: str, prompt: str) -> AsyncGenerator[str, None]:
        """
            Asynchronously processes chat input using the specified Ollama model.
            Streams responses as they are generated.
        """
        try:
            logger.warning(f"Processing chat with model: {model}")
            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
        
            for chunk in response:
                if "message" in chunk and "content" in chunk["message"]:
                    yield chunk["message"]["content"]
                    await asyncio.sleep(0)  # Allow event loop to handle other tasks
        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}")
            yield f"Error processing chat: {str(e)}"
