

from app.api.room.model import Room, Sprint, UserStory
from sqlalchemy.orm import Session
from app.api.auth.schema import UserResponse
from sqlalchemy import select


def get_user_story_(room_id: str, sprint_id: str, current_user: UserResponse, session:Session):
    
    stmt = select(Room).where(Room.id == room_id, Room.product_owner_id == current_user.id)  # TODO JOINLOAD TO CHECK IF SPRINT IT IS SAME OR NOT .
    room = session.execute(stmt).scalar_one_or_none()
    if room is None:
        raise Exception('room not found')
    
    user_story = select(UserStory).where(UserStory.sprint_id == sprint_id)
    story = session.execute(user_story).scalars().all()
    
    return story
    