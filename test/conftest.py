import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.database.db import get_session
from app.models.paper import Paper
from app.models.tag import Tag
from app.models.note import Note

sqlite_url = "sqlite:///:memory:"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, poolclass=StaticPool)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):

    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()
    
@pytest.fixture
def sample_paper(session):
    paper = Paper(title="ReAct", authors="Yao", year=2023, venue="ICLR", abstract="...", pdf_path="...")
    session.add(paper)
    session.commit()
    session.refresh(paper)
    return paper

@pytest.fixture
def sample_tag(session):
    tag1 = Tag(name="Attention")
    tag2 = Tag(name="DL")
    tag = [tag1, tag2]
    session.add_all(tag)
    session.commit()
    # session.refresh(tag)
    return tag

@pytest.fixture
def sample_note(session, sample_paper):
    note = Note(
        content="ReAct = Reasoning + Acting",
        paper_id=sample_paper.id
    )
    session.add(note)
    session.commit()
    session.refresh(note)
    return note