from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

# --- Link table ---
class PaperTag(SQLModel, table=True):
    paper_id: int = Field(foreign_key="paper.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)

# --- Tag ---
class TagBase(SQLModel):
    name: str = Field(max_length=50, unique=True, index=True)

class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    papers: List["Paper"] = Relationship(back_populates="tags", link_model=PaperTag)

# --- Note ---
class NoteBase(SQLModel):
    content: str
    paper_id: int = Field(foreign_key="paper.id", index=True)
    created_at: datetime = Field(default_factory=datetime.now)

class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    paper: "Paper" = Relationship(back_populates="notes")

# --- Paper ---
class PaperBase(SQLModel):
    title: str
    authors: str
    abstract: str
    year: int = Field(index=True)
    venue: str = Field(index=True)
    pdf_path: str
    created_at: datetime = Field(default_factory=datetime.now)

class Paper(PaperBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    notes: List["Note"] = Relationship(back_populates="paper")
    tags: List["Tag"] = Relationship(back_populates="papers", link_model=PaperTag)