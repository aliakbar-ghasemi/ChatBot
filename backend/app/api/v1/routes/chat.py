from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.services.chat_service import ChatService
from app.models.chat_model import ChatRequest
from app.core.logger import logger
import datetime

router = APIRouter()


@router.post("/")
async def chat(request: ChatRequest):
    """
    Handles chat requests by streaming responses from the chatbot model.
    """
    if not request.conversation_id or request.conversation_id.strip() == "":
        request.conversation_id = str(int(datetime.datetime.now().timestamp()))

    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        return StreamingResponse(
            ChatService().process_chat(request.conversation_id, request.model, request.prompt),
            media_type="text/plain",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")
