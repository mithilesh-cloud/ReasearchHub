from datetime import datetime

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.database.session import get_db
from app.models.user import User
from app.models.workspace import Workspace

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


class WorkspaceCreate(BaseModel):
    name: str
    description: str | None = None


class WorkspaceRead(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


def get_current_user_id(authorization: str = Header(default="")) -> int:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.replace("Bearer ", "", 1)
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload["sub"])


@router.post("", response_model=WorkspaceRead, status_code=status.HTTP_201_CREATED)
def create_workspace(
    payload: WorkspaceCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> Workspace:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    workspace = Workspace(name=payload.name, description=payload.description, owner_id=user_id)
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace


@router.get("", response_model=list[WorkspaceRead])
def list_workspaces(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> list[Workspace]:
    return db.query(Workspace).filter(Workspace.owner_id == user_id).all()
