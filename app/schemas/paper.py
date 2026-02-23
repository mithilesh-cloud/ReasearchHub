from pydantic import BaseModel


class SearchQuery(BaseModel):
    query: str
    max_results: int = 10


class PaperResult(BaseModel):
    external_id: str | None = None
    title: str
    authors: list[str] = []
    published_date: str | None = None
    abstract: str | None = None
    source: str = "arxiv"


class PaperImportRequest(BaseModel):
    workspace_id: int
    paper: PaperResult


class PaperOut(BaseModel):
    id: int
    workspace_id: int
    external_id: str | None = None
    title: str
    authors: str | None = None
    published_date: str | None = None
    abstract: str | None = None
    source: str

    class Config:
        from_attributes = True
