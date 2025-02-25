from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from app.services.chat_service import ChatService
from app.models.chat_model import ChatRequest
from app.core.logger import logger
from app.services.task_manager import task_manager
import datetime
import asyncio

router = APIRouter()
chat_service = ChatService()


async def start_chat(request: ChatRequest, queue: asyncio.Queue, background_tasks: BackgroundTasks):
    try:
        async for response_chunk in chat_service.process_chat(
            request.conversation_id, request.model, request.prompt.strip(), background_tasks
        ):
            if not task_manager.has_task(request.conversation_id):
                break  # Stop task if canceled
            print(f"Sending chunk: {response_chunk}")
            await queue.put(response_chunk)
    except asyncio.CancelledError:
        print(f"Task {task_id} was cancelled")
        await queue.put("Chat stopped by user.\n")
    except Exception as e:
        await queue.put(f"chat_task:Error: {str(e)}\n")
        # raise HTTPException(
        #    status_code=500, detail=f"Error processing chat: {str(e)}"
        # )
    finally:
        task_manager.cancel_task(request.conversation_id)
        await queue.put(None)  # Signal end of stream


async def response_generator(queue: asyncio.Queue):
    """
    Reads responses from the queue and streams them to the client.
    """
    while True:
        chunk = await queue.get()
        if chunk is None:  # End of stream signal
            break
        yield chunk


@router.post("/")
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    """
    Handles chat requests by streaming responses from the chatbot model.
    """
    # Check if conversation_id is provided and is not empty
    if not request.conversation_id or request.conversation_id.strip() == "":
        request.conversation_id = str(int(datetime.datetime.now().timestamp()))

    # Check if prompt is empty
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    queue = asyncio.Queue()
    task = asyncio.create_task(start_chat(request=request, queue=queue, background_tasks=background_tasks))

    task_manager.add_task(request.conversation_id, task, queue)

    # Stream responses from the queue
    return StreamingResponse(response_generator(queue), media_type="text/plain")


@router.post("/cancel")
async def cancel_chat(conversation_id: str):
    """
    Cancels an ongoing chat by stopping its task.
    """
    if task_manager.cancel_task(conversation_id):
        return {"message": f"Chat {conversation_id} canceled"}
    else:
        raise HTTPException(
            status_code=404, detail="Chat not found or already finished"
        )
