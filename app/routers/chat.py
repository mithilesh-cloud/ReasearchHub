from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.conversation import Conversation
from app.models.paper import Paper
from app.models.user import User
from app.models.workspace import Workspace
from app.routers.auth import get_current_user
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.embedding_service import embed_text
from app.services.llm_service import ask_llm
from app.services.vector_service import top_k_similar
from app.utils.prompt_builder import build_research_prompt

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workspace = (
        db.query(Workspace)
        .filter(Workspace.id == payload.workspace_id, Workspace.owner_id == current_user.id)
        .first()
    )
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    papers = db.query(Paper).filter(Paper.workspace_id == workspace.id).all()
    if not papers:
        raise HTTPException(status_code=400, detail="No papers in workspace. Import papers first.")

    query_embedding = embed_text(payload.message)
    paper_vectors = [(paper.id, paper.embedding or []) for paper in papers]
    selected_ids = set(top_k_similar(query_embedding, paper_vectors, k=4))

    selected_papers = [paper for paper in papers if paper.id in selected_ids] or papers[:3]
    contexts = [f"Title: {p.title}\nAuthors: {p.authors}\nAbstract: {p.abstract}" for p in selected_papers]
    prompt = build_research_prompt(payload.message, contexts)
    answer = ask_llm(prompt)

    convo = Conversation(workspace_id=workspace.id, user_message=payload.message, assistant_message=answer)
    db.add(convo)
    db.commit()

    return ChatResponse(answer=answer, references=[p.title for p in selected_papers])
