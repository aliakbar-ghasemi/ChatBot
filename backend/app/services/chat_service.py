import asyncio
import ollama
from typing import AsyncGenerator
from app.core.logger import logger

async def process_chat(prompt: str, model: str) -> AsyncGenerator[str, None]:
    """
    Asynchronously processes chat input using the specified Ollama model.
    Streams responses as they are generated.
    """
    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}], stream=True)
        
        for chunk in response:
            if "message" in chunk and "content" in chunk["message"]:
                yield chunk["message"]["content"]
                await asyncio.sleep(0)  # Allow event loop to handle other tasks
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        yield f"Error processing chat: {str(e)}"
