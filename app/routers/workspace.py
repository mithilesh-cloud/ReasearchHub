from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.paper import Paper
from app.models.user import User
from app.models.workspace import Workspace
from app.routers.auth import get_current_user
from app.schemas.paper import PaperOut
from app.schemas.workspace import WorkspaceCreate, WorkspaceOut

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.post("", response_model=WorkspaceOut)
def create_workspace(
    payload: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ws = Workspace(name=payload.name, description=payload.description, owner_id=current_user.id)
    db.add(ws)
    db.commit()
    db.refresh(ws)
    return ws


@router.get("", response_model=list[WorkspaceOut])
def list_workspaces(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Workspace).filter(Workspace.owner_id == current_user.id).all()


@router.get("/{workspace_id}/papers", response_model=list[PaperOut])
def get_workspace_papers(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ws = db.query(Workspace).filter(Workspace.id == workspace_id, Workspace.owner_id == current_user.id).first()
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return db.query(Paper).filter(Paper.workspace_id == workspace_id).all()
