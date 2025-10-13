

from app.api.room.model import UserStory
from sqlalchemy.orm import Session
from app.api.auth.schema import UserResponse
from sqlalchemy import select

def get_backlog_list_(room_id: str, current_user: UserResponse, session: Session):
    stmt = select(UserStory).where(UserStory.room_id  == room_id, UserStory.created_by == current_user.id)
    backlogs = session.execute(stmt).scalars().all()
    return backlogs