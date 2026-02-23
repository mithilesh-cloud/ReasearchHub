from datetime import datetime

from pydantic import BaseModel


class ChatRequest(BaseModel):
    workspace_id: int
    question: str


class ChatResponse(BaseModel):
    answer: str


class ConversationRead(BaseModel):
    id: int
    workspace_id: int
    user_message: str
    assistant_message: str
    created_at: datetime

    class Config:
        from_attributes = True
