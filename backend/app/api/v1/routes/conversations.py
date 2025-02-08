from fastapi import APIRouter, HTTPException, Depends
from app.services.chat_service import ChatService
from app.core.logger import logger

router = APIRouter()

@router.get("/")
async def get_all_conversations():
    return ChatService().get_all_conversations()

@router.get("/{conversation_id}")
async def get_chat_history(conversation_id: str):
    return ChatService().get_conversation(conversation_id)

@router.post("/{conversation_id}/update_title/")
async def update_title(conversation_id: str, title: str):
    ChatService().set_conversation_title(conversation_id, title)
    return {"status": "Title updated"}