from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database.db import get_session
from app.models.tag import Tag, TagCreate, TagReadWithPapers

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get("/", response_model=List[TagReadWithPapers], status_code=200)
def get_tags(session: Session = Depends(get_session)):
    '''
    Get all tags
    API: GET /tags/
    '''
    statement = select(Tag)
    return session.exec(statement).all()

@router.get("/{id}/", response_model=TagReadWithPapers, status_code=200)
def get_tag_by_id(id: int, session: Session = Depends(get_session)):
    '''
    Get tag by id
    API: GET /tags/{id}/
    '''
    db_tag = session.get(Tag, id)

    # invalid id : no paper found
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    return db_tag

@router.put("/{id}/", response_model=None, status_code=204)
def update_tag(id: int, tag_in: TagCreate, session: Session = Depends(get_session)):
    '''
    Update tag by id
    API: PUT /tags/{id}/
    '''
    db_tag = session.get(Tag, id)

    # invalid id : no paper found
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    # invalid : uniqueness
    conflict_tag = session.exec(select(Tag).where(Tag.name == tag_in.name)).first()
    if conflict_tag and conflict_tag.id != id:
        raise HTTPException(status_code=400, detail="Tag name exists")

    # update 
    update_data = tag_in.model_dump(exclude_unset=True)
    db_tag.sqlmodel_update(update_data)

    # save
    session.add(db_tag)
    session.commit()
    return

@router.delete("/{id}/", response_model=None, status_code=204)
def delete_tag(id: int, session: Session = Depends(get_session)):
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