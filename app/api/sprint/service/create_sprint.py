

from app.api.room.model import Room, Sprint
from sqlalchemy.orm import Session
from app.api.auth.schema import UserResponse
from app.api.sprint.schema import CreateSprintRequest
from sqlalchemy import select


def create_sprint_(room_id: str, body: CreateSprintRequest, current_user: UserResponse, session:Session):
    
    stmt = select(Room).where(Room.id == room_id)
    room = session.execute(stmt).scalar_one_or_none()
    if room is None:
        raise Exception('room not found')
    
    sprint = Sprint(**body.model_dump(), room_id=room_id, created_by=current_user.id)
    
    session.add(sprint)
    
    return 