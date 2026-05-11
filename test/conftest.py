import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
from app.main import app
from app.database.db import get_session
from app.models.paper import Paper

sqlite_url = "sqlite:///:memory:"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

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
    paper = Paper(title="Initial Paper", authors="Author", year=2023, venue="Conf", abstract="...", pdf_path="...")
    session.add(paper)
    session.commit()
    session.refresh(paper)
    return paper