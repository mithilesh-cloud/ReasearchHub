from pydantic import BaseModel


class WorkspaceCreate(BaseModel):
    name: str
    description: str | None = None


class WorkspaceOut(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True
