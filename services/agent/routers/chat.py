from fastapi import APIRouter, Header, Request
from pydantic import BaseModel
from controllers.chat_controller import chat_controller
from typing import Optional

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    file_id: Optional[str] = None

@router.post("/chat")
async def chat(request: Request, body: ChatRequest, user_id: str = Header(...)):
    return chat_controller.handle(
        user_message=body.message,
        user_id=user_id,
        conversation_id=body.conversation_id,
        file_id=body.file_id
    )
