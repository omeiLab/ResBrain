from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, ForeignKey, Column, Integer

if TYPE_CHECKING:
    from app.models.paper import Paper

class NoteBase(SQLModel):
    content: str
    paper_id: int = Field(
        sa_column=Column(
            ForeignKey("paper.id", ondelete="CASCADE"),
            nullable=False
        )
    )

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    paper: "Paper" = Relationship(back_populates="notes")

class NoteCreate(NoteBase):
    pass

class NoteRead(NoteBase):
    id: int
