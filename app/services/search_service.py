from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.services.embedding_service import embed_text
from app.services.vector_service import cosine_similarity


def search_papers(db: Session, query: str, workspace_id: int, limit: int = 10) -> list[Paper]:
    query_embedding = embed_text(query)
    papers = db.query(Paper).filter(Paper.workspace_id == workspace_id).all()

    ranked = sorted(
        papers,
        key=lambda paper: cosine_similarity(
            query_embedding,
            embed_text(f"{paper.title} {paper.abstract or ''}"),
        ),
        reverse=True,
    )
    return ranked[:limit]
