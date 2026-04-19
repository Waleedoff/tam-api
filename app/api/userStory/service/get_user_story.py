

from app.api.room.model import Room, Sprint, UserStory
from sqlalchemy.orm import Session
from app.api.auth.schema import UserResponse
from sqlalchemy import select


def get_user_story_(session:Session):
    

    
    user_story = select(UserStory)
    story = session.execute(user_story).scalars().all()
    
    return story
    