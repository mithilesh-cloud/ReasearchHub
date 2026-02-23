from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.paper import Paper
from app.schemas.paper import PaperCreate, PaperRead
from app.services.search_service import search_papers

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/papers", response_model=PaperRead, status_code=201)
def add_paper(workspace_id: int, payload: PaperCreate, db: Session = Depends(get_db)) -> Paper:
    paper = Paper(workspace_id=workspace_id, **payload.model_dump())
    db.add(paper)
    db.commit()
    db.refresh(paper)
    return paper


@router.get("/papers", response_model=list[PaperRead])
def query_papers(
    workspace_id: int,
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
) -> list[Paper]:
    results = search_papers(db, q, workspace_id)
    if not results:
        raise HTTPException(status_code=404, detail="No papers found")
    return results
