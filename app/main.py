from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.database.session import Base, engine
from app.models import Conversation, Paper, User, Workspace  # noqa: F401
from app.routers import auth, chat, search, workspace

settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "ok", "service": settings.APP_NAME}


app.include_router(auth.router)
app.include_router(workspace.router)
app.include_router(search.router)
app.include_router(chat.router)
