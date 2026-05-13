from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field


class PaperTag(SQLModel, table=True):
    paper_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("paper.id", ondelete="CASCADE"),
            primary_key=True
        )
    )

    tag_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("tag.id", ondelete="CASCADE"),
            primary_key=True
        )
    )