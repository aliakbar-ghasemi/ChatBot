from pydantic import BaseModel

# Define your request model
class ChatRequest(BaseModel):
    prompt: str
    model: str = ""  # Allow empty model