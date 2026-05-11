from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.paper import Paper

class NoteBase(SQLModel):
    content: str
    paper_id: int = Field(foreign_key="paper.id", index=True)
    created_at: datetime = Field(default_factory=datetime.now)

class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    paper: "Paper" = Relationship(back_populates="notes")
