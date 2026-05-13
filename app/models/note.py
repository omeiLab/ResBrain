from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, ForeignKey

if TYPE_CHECKING:
    from app.models.paper import Paper

class NoteBase(SQLModel):
    content: str

class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    paper_id: int = Field(
        sa_column=Column(
            ForeignKey("paper.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    paper: "Paper" = Relationship(back_populates="notes")

class NoteCreate(SQLModel):
    content: str

class NoteRead(NoteBase):
    id: int
    paper_id: int
    created_at: datetime
    updated_at: datetime