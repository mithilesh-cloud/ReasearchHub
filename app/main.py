from fastapi import FastAPI

from app.core.config import settings
from app.database.session import Base, engine
from app.routers import auth, chat, search, workspace

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version=settings.app_version)


@app.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(workspace.router, prefix=settings.api_prefix)
app.include_router(search.router, prefix=settings.api_prefix)
app.include_router(chat.router, prefix=settings.api_prefix)
