from pydantic import BaseModel
from datetime import datetime

# Define your request model
class ChatRequest(BaseModel):
    prompt: str
    model: str = ""  # Allow empty model
    conversation_id: str = str(int(datetime.now().timestamp()))  # Default to current timestamp