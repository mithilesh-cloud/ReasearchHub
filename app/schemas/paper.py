from datetime import datetime

from pydantic import BaseModel


class PaperCreate(BaseModel):
    title: str
    abstract: str | None = None
    source_url: str | None = None


class PaperRead(PaperCreate):
    id: int
    workspace_id: int
    created_at: datetime

    class Config:
        from_attributes = True
