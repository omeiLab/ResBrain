from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.models.link_tables import PaperTag
from app.models.tag import TagRead

if TYPE_CHECKING:
    from app.models.note import Note
    from app.models.tag import Tag

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
    
class PaperCreate(PaperBase):
    tags: List[str] = []

class PaperRead(PaperBase):
    tags: List["TagRead"] = []
    
PaperRead.model_rebuild()