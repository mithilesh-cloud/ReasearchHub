from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.conversation import Conversation
from app.models.paper import Paper
from app.schemas.chat import ChatRequest, ChatResponse, ConversationRead
from app.services.llm_service import generate_answer
from app.utils.prompt_builder import build_research_prompt

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    papers = db.query(Paper).filter(Paper.workspace_id == payload.workspace_id).limit(5).all()
    if not papers:
        raise HTTPException(status_code=404, detail="No papers found for workspace")

    summaries = [f"{paper.title}: {paper.abstract or 'No abstract'}" for paper in papers]
    prompt = build_research_prompt(payload.question, summaries)
    answer = generate_answer(payload.question, context=prompt)

    conversation = Conversation(
        workspace_id=payload.workspace_id,
        user_message=payload.question,
        assistant_message=answer,
    )
    db.add(conversation)
    db.commit()

    return ChatResponse(answer=answer)


@router.get("/{workspace_id}", response_model=list[ConversationRead])
def conversation_history(workspace_id: int, db: Session = Depends(get_db)) -> list[Conversation]:
    return (
        db.query(Conversation)
        .filter(Conversation.workspace_id == workspace_id)
        .order_by(Conversation.created_at.desc())
        .all()
    )
