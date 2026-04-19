from app.api.auth.models import User
from app.api.room.model import Room
from app.api.room.schema import RoomPreviewResponse
from sqlalchemy.orm import Session, joinedload
from app.api.auth.schema import GetMemeberInfoResponse, UserResponse
from sqlalchemy import select

def get_room_members_(room_id: str, session: Session, current_user: UserResponse):
    stmt = (
        select(Room)
        .where(Room.id == room_id)
        .options(joinedload(Room.members))
    )
    room = session.execute(stmt).unique().scalar_one_or_none()

    if not room:
        return []

    # تحويل الـ ORM users إلى Pydantic schema
    return [
        GetMemeberInfoResponse(
            id=user.id,
            username=user.username,
            full_name=user.full_name,
            department=user.department,
            role=user.role,
            email=user.email,
            gender=user.gender,
            is_online=user.is_online
        )
        for user in room.members
    ]
