from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.models.link_tables import PaperTag

if TYPE_CHECKING:
    from app.models.paper import Paper
    
class TagBase(SQLModel):
    name: str = Field(max_length=50, unique=True, index=True)

class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    papers: List["Paper"] = Relationship(back_populates="tags", link_model=PaperTag)
    
class TagRead(TagBase):
    pass

TagRead.model_rebuild()