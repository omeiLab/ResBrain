from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database.db import get_session
from app.models.note import Note, NoteCreate, NoteRead

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("/{id}/", response_model=NoteRead, status_code=200)
def get_note(id: int, session: Session = Depends(get_session)):
    '''
    Get all notes
    API: GET /notes/{id}/
    '''
    db_note = session.get(Note, id)

    # invalid id : no paper found
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return db_note

@router.patch("/{id}/", response_model=None, status_code=204)
def update_note(id: int, note_in: NoteCreate, session: Session = Depends(get_session)):
    '''
    Update note by id
    API: PATCH /notes/{id}/
    '''
    db_note = session.get(Note, id)

    # invalid id : no paper found
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    # update other columns
    update_data = note_in.model_dump(exclude_unset=True)
    update_data['updated_at'] = datetime.now()
    db_note.sqlmodel_update(update_data)

    # save
    session.add(db_note)
    session.commit()
    return

@router.delete("/{id}/", response_model=None, status_code=204)
def delete_tag(id: int, session: Session = Depends(get_session)):
    '''
    Delete a note by id
    API: DELETE /notes/{id}/
    '''
    db_note = session.get(Note, id)

    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    session.delete(db_note)
    session.commit()
    return