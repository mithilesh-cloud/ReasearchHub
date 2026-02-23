from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.paper import Paper
from app.models.user import User
from app.models.workspace import Workspace
from app.routers.auth import get_current_user
from app.schemas.paper import PaperImportRequest, PaperOut, PaperResult, SearchQuery
from app.services.embedding_service import embed_text
from app.services.search_service import search_papers

router = APIRouter(prefix="/papers", tags=["papers"])


@router.post("/search", response_model=list[PaperResult])
async def search_endpoint(payload: SearchQuery, _current_user: User = Depends(get_current_user)):
    return await search_papers(payload.query, payload.max_results)


@router.post("/import", response_model=PaperOut)
def import_paper(
    payload: PaperImportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ws = db.query(Workspace).filter(Workspace.id == payload.workspace_id, Workspace.owner_id == current_user.id).first()
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")

    embedding = embed_text(payload.paper.abstract or payload.paper.title)
    paper = Paper(
        workspace_id=payload.workspace_id,
        external_id=payload.paper.external_id,
        title=payload.paper.title,
        authors=", ".join(payload.paper.authors),
        published_date=payload.paper.published_date,
        abstract=payload.paper.abstract,
        source=payload.paper.source,
        embedding=embedding,
    )
    db.add(paper)
    db.commit()
    db.refresh(paper)
    return paper
