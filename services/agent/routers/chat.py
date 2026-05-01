from fastapi import APIRouter, Request
from pydantic import BaseModel
from controllers.chat_controller import chat_controller
from typing import Optional

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

@router.post("/chat")
async def chat(request: Request, body: ChatRequest):
    return chat_controller.handle(
        user_message=body.message,
        user_id=request.state.user_id,
        conversation_id=body.conversation_id,
    )
