
from typing import Sequence
from app.api.auth.models import User
from app.api.auth.schema import UserResponse
from app.api.room.model import Sprint
from sqlalchemy.orm import Session
from sqlalchemy import select

def get_sprints_(room_id: str, current_user: UserResponse,   session: Session):
    stmt = select(Sprint).where(Sprint.room_id == room_id, Sprint.created_by == current_user.id)
    sprints: Sequence[Sprint] = session.execute(stmt).scalars().all()
    return sprints