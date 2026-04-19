

from app.api.room.model import Sprint, UserStory
from sqlalchemy.orm import Session
from app.api.auth.schema import UserResponse
from app.api.sprint.schema import CreateSprintRequest
from sqlalchemy import select


def create_sprint_(body: CreateSprintRequest, current_user: UserResponse, session:Session):
    

    sprint = Sprint(**body.model_dump(exclude={"user_stories"}),status="PLANNED", created_by=current_user.id)

    session.add(sprint)
    session.flush()
    
    user_stories_ids = [story.id for story in body.user_stories]
    
    user_stories = select(UserStory).where(UserStory.id.in_(user_stories_ids))
    usrstory = session.execute(user_stories).scalars().all()

    # TODO USE EXTEND MORE MUCH IDIOMATIC THAN EXPLICIT LOOP
    # usrstory.extend(sprint.id)

    for ut in usrstory:
        ut.sprint_id = sprint.id

    session.commit()
    