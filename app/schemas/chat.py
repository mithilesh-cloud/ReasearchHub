from pydantic import BaseModel


class ChatRequest(BaseModel):
    workspace_id: int
    message: str


class ChatResponse(BaseModel):
    answer: str
    references: list[str]
