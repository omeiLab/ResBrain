from sqlmodel import SQLModel, Field
    
class PaperTag(SQLModel, table=True):
    paper_id: int = Field(foreign_key="paper.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)