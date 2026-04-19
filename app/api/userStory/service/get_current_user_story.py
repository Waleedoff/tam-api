from app.api.auth.schema import UserResponse
from app.api.room.enums import SprintStatus
from app.api.room.model import Sprint, UserStory
from sqlalchemy.orm import Session
from sqlalchemy import select


def get_current_user_story_(session: Session):
    sprint_stmt = select(Sprint.id).where(Sprint.status == SprintStatus.ACTIVE)
    sprint_id = session.execute(sprint_stmt).scalar_one_or_none()
    
    if sprint_id is None:
        raise Exception("not found ")
    

    user_story_stmt = select(UserStory).where(UserStory.sprint_id == sprint_id)
    get_user_story_result = session.execute(user_story_stmt).scalars().all()

    return get_user_story_result