from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class User(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

class Conversation(BaseModel):
    id: UUID
    user_id: UUID
    title: Optional[str] = "chat"
    created_at: datetime

class Message(BaseModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    modality: str = "text"
    intent: Optional[str] = None
    created_at: datetime

class File(BaseModel):
    id: UUID
    user_id: UUID
    file_name: str
    mime_type: str
    status: str = "processing"
    chunks_count: int = 0
    collection_name: Optional[str] = None
    raw_text_path: Optional[str] = None
    created_at: datetime
