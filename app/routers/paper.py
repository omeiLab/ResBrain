import shutil
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlmodel import Session, select, or_
from typing import List, Optional
from app.database.db import get_session
from app.models.paper import Paper, PaperCreate, PaperRead
from app.models.tag import Tag
from app.models.note import Note, NoteCreate, NoteRead
from app.services.tag_service import get_or_create_tags

UPLOAD_DIR = Path("storage/pdfs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/papers", tags=["papers"])

@router.post("/", response_model=PaperRead, status_code=201)
def create_paper(paper_in: PaperCreate, session: Session = Depends(get_session)):
    '''
    Create a new paper
    API: POST /papers/
    '''
    # receive a list of tags' names, return the list of Tag objects
    tag_objects = get_or_create_tags(session, paper_in.tags)
    paper_data = paper_in.model_dump(exclude={"tags"})
    db_paper = Paper(**paper_data)
    db_paper.tags = tag_objects
    
    # save to db
    session.add(db_paper)
    session.commit()
    session.refresh(db_paper)
    
    return db_paper

@router.post("/{id}/notes/", response_model=NoteRead, status_code=201)
def create_note(note_in: NoteCreate, id: int, session: Session = Depends(get_session)):
    '''
    Create a new note
    API: POST /papers/{id}/notes/
    '''
    db_paper = session.get(Paper, id)

    # invalid id : no paper found
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    note_data = note_in.model_dump()
    db_note = Note(**note_data)
    db_note.paper_id = id

    # save to db
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    
    return db_note

@router.post("/{id}/upload", response_model=PaperRead, status_code=200)
def upload_pdf(id: int, file: UploadFile = File(...), session: Session = Depends(get_session)):
    '''
    Upload pdf for specified paper
    API: POST /papers/{id}/upload/
    '''
    db_paper = session.get(Paper, id)

    # invalid id : no paper found
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # invalid file : only pdf allows
    if not file.filename.endswith(".pdf"):   # type: ignore
        raise HTTPException(status_code=400, detail="Only PDF allows")
    
    # save to storage
    file_path = UPLOAD_DIR / f'{id}_{file.filename}'
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_paper.pdf_path = str(file_path)
    session.add(db_paper)
    session.commit()
    session.refresh(db_paper)
    
    return db_paper

@router.get("/", response_model=List[PaperRead], status_code=200)
def get_paper(
    year: Optional[int] = None,
    venue: Optional[str] = None,
    tag: Optional[str] = None,
    q: Optional[str] = None,
    session: Session = Depends(get_session)
):
    '''
    Get all papers with filters
    API: GET /papers/
    '''
    statement = select(Paper)

    # apply filters
    if year is not None:
        statement = statement.where(Paper.year == year)
    if venue is not None:
        statement = statement.where(Paper.venue == venue)
    if tag is not None:
        statement = statement.where(Paper.tags.any(name=tag))   # type: ignore
    if q is not None:
        statement = statement.where(
            or_(
                Paper.title.contains(q),    # type: ignore
                Paper.abstract.contains(q)  # type: ignore
            )
        )

    return session.exec(statement).all()

@router.get("/{id}/", response_model=PaperRead, status_code=200)
def get_paper_by_id(id: int, session: Session = Depends(get_session)):
    '''
    Get papers by id
    API: GET /papers/{id}/
    '''
    db_paper = session.get(Paper, id)

    # invalid id : no paper found
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    return db_paper

@router.get("/{id}/notes/", response_model=List[NoteRead], status_code=200)
def get_note(id: int, session: Session = Depends(get_session)):
    '''
    Get all notes
    API: GET /papers/{id}/notes/
    '''
    db_paper = session.get(Paper, id)

    # invalid id : no paper found
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    return db_paper.notes

@router.put("/{id}/", response_model=None, status_code=204)
def update_paper(id: int, paper_in: PaperCreate, session: Session = Depends(get_session)):
    '''
    Update paper by id
    API: PUT /papers/{id}/
    '''
    db_paper = session.get(Paper, id)

    # invalid id : no paper found
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # handle tags
    if paper_in.tags is not None:
        tag_objects = get_or_create_tags(session, paper_in.tags)
        db_paper.tags = tag_objects # replace all

    # update other columns
    update_data = paper_in.model_dump(exclude={"tags"}, exclude_unset=True)
    db_paper.sqlmodel_update(update_data)

    # save
    session.add(db_paper)
    session.commit()
    return

@router.delete("/{id}/", response_model=None, status_code=204)
def delete_paper(id: int, session: Session = Depends(get_session)):
    '''
    Delete paper by id
    API: DELETE /papers/{id}/
    '''
    db_paper = session.get(Paper, id)

    # invalid id : no paper found
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    session.delete(db_paper)
    session.commit()
    return