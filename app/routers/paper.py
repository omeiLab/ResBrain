from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database.db import get_session
from app.models.paper import Paper, PaperCreate, PaperRead
from app.models.note import Note, NoteCreate, NoteRead
from app.services.tag_service import get_or_create_tags

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

@router.get("/", response_model=List[PaperRead], status_code=200)
def get_paper(session: Session = Depends(get_session)):
    '''
    Get all papers
    API: GET /papers/
    '''
    statement = select(Paper)
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