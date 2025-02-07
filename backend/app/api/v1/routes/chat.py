from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.services.chat_service import ChatService
from app.core.dependencies import validate_model
from app.models.chat_model import ChatRequest
from app.utils.model_helper import select_model
from app.core.logger import logger

router = APIRouter()


@router.post("/")
async def chat(request: ChatRequest):
    """
    Handles chat requests by streaming responses from the chatbot model.
    """
    model = ""
    if request.model:
        model = request.model
    else:
        model = select_model(request.prompt)  # Select the correct model

    # Validate the model
    if not validate_model(model):
        raise HTTPException(status_code=400, detail=f"Invalid model: {model}")

    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        return StreamingResponse(
            ChatService().process_chat(request.conversation_id, model, request.prompt),
            media_type="text/plain",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")
