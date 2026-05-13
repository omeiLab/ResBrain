from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database.db import get_session
from app.models.tag import Tag, TagReadWithPapers

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get("/", response_model=List[TagReadWithPapers], status_code=200)
def get_tags(session: Session = Depends(get_session)):
    '''
    Get all tags
    API: GET /tags/
    '''
    statement = select(Tag)
    return session.exec(statement).all()

@router.delete("/{id}/", response_model=None, status_code=204)
def delete_tag_by_id(id: int, session: Session = Depends(get_session)):
    '''
    Delete a tag by id
    API: DELETE /tags/{id}/
    '''
    db_tag = session.get(Tag, id)

    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    session.delete(db_tag)
    session.commit()
    return