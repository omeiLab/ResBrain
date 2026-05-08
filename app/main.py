from contextlib import asynccontextmanager
from fastapi import FastAPI
from database.db import create_db_and_tables
from models.models import Note, Paper, Tag

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)