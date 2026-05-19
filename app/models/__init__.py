from .paper import Paper, PaperRead
from .tag import Tag, TagRead, TagReadWithPapers
from .note import Note
from .link_tables import PaperTag

PaperRead.model_rebuild()
TagReadWithPapers.model_rebuild()