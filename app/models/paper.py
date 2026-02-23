from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database.session import Base


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False, index=True)
    external_id = Column(String(255), nullable=True, index=True)
    title = Column(String(500), nullable=False)
    authors = Column(String(1000), nullable=True)
    published_date = Column(String(50), nullable=True)
    abstract = Column(Text, nullable=True)
    source = Column(String(50), default="arxiv")
    embedding = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    workspace = relationship("Workspace", back_populates="papers")
