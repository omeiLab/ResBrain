from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.database.db import get_session
from app.models.paper import Paper, PaperCreate, PaperRead
from app.services.tag_service import get_or_create_tags

router = APIRouter(prefix="/papers", tags=["papers"])

@router.post("/", response_model=PaperRead, status_code=201)
def create_paper(paper_in: PaperCreate, session: Session = Depends(get_session)):
    '''
    Create a new paper.
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