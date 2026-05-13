from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.db import create_db_and_tables
from app.models.note import Note
from app.models.paper import Paper
from app.models.tag import Tag
from app.routers import paper, tag, note

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(paper.router)
app.include_router(tag.router)
app.include_router(note.router)