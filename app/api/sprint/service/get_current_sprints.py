from app.api.room.enums import SprintStatus
from app.api.room.model import Sprint, UserStory
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select


# TODO WHERE IS THE BEST CHOIC TO GET USERSTORY FIRST AND THEN CHCK IF THEIR SPRINT ACTIVE OR NOT
# OR DIRECT TO GET ACTIVE SPRINT AND THEN GET THEIR STORY IF ANY.

def get_current_sprints_and_their_user_stories_(session: Session):
    
    stmt = select(Sprint).where(Sprint.status == SprintStatus.ACTIVE).options(
        joinedload(Sprint.user_stories))
    sprints = session.execute(stmt).scalars().unique().all()

    return sprints