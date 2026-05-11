from sqlmodel import Session, select, col
from typing import List
from app.models.tag import Tag

def get_or_create_tags(session: Session, tag_names: List[str]) -> List[Tag]:
    """
    Given a list of tags' names. 
    Return the corresponding list of Tag objects, create the tag if one not exists.
    """
    if not tag_names:
        return []

    # fetch all the names of existed tags
    unique_names = list(set(name.strip() for name in tag_names if name.strip()))

    # get the rows where Tag.name exists
    statement = select(Tag).where(col(Tag.name).in_(unique_names))
    existing_tags = session.exec(statement).all()
    existing_names = {t.name for t in existing_tags}
    
    # for one not exists, create a new Tag
    new_tags = [Tag(name=name) for name in unique_names if name not in existing_names]
    
    # add new tags to session
    for tag in new_tags:
        session.add(tag)
        
    return list(existing_tags) + new_tags